import { GoogleGenAI, type FunctionDeclaration } from "@google/genai";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

// Initialize Gemini API Client (reads GEMINI_API_KEY from environment)
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY || "" });

async function main() {
  // 1. Initialize and connect to your local MCP Server
  const transport = new StdioClientTransport({
    command: "node",
    args: ["/path/to/your/server/build/index.js"],
  });

  const mcpClient = new Client(
    { name: "ai-bridge-client", version: "1.0.0" },
    { capabilities: { tools: {} } },
  );

  console.log("Connecting to MCP Server...");
  await mcpClient.connect(transport);

  try {
    // 2. Fetch all tools exposed by the MCP server
    const { tools: mcpTools } = await mcpClient.listTools();
    console.log(`Discovered ${mcpTools.length} tools from MCP server.`);

    // 3. Convert MCP tools to Gemini Function Declaration format
    const geminiTools: FunctionDeclaration[] = mcpTools.map((tool) => ({
      name: tool.name,
      description: tool.description || `Execute ${tool.name}`,
      parameters: tool.inputSchema as FunctionDeclaration["parameters"],
    }));

    // 4. Send the user prompt to Gemini along with the discovered tools
    const userPrompt = "Can you calculate the sum of 142 and 583?";
    console.log(`\nUser Prompt: "${userPrompt}"`);
    console.log("Sending request to Gemini...");

    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash",
      contents: userPrompt,
      config: {
        // Register the translated MCP tools with the model
        tools: [{ functionDeclarations: geminiTools }],
      },
    });

    // 5. Check if the AI decided to call an MCP tool
    const functionCalls = response.functionCalls;

    if (functionCalls && functionCalls.length > 0) {
      const call = functionCalls[0];
      console.log(`\n🤖 AI requested tool call: "${call.name}"`);
      console.log(`Arguments:`, JSON.stringify(call.args));

      // 6. Execute the tool on the MCP server using the arguments provided by the AI
      console.log("Executing tool via MCP client...");
      const toolResult = await mcpClient.callTool({
        name: call.name,
        arguments: call.args as Record<string, unknown>,
      });

      console.log(
        "\nMCP Server Output:",
        JSON.stringify(toolResult.content, null, 2),
      );

      // 7. (Optional) Feed the result back to Gemini to get a final conversational response
      const finalResponse = await ai.models.generateContent({
        model: "gemini-2.5-flash",
        contents: [
          { role: "user", parts: [{ text: userPrompt }] },
          { role: "model", parts: [{ functionCall: call }] },
          {
            role: "user",
            parts: [
              {
                functionResponse: {
                  name: call.name,
                  // Reformat the text content for the model's history
                  response: { result: toolResult.content },
                },
              },
            ],
          },
        ],
      });

      console.log(`\n🤖 Final AI Response: ${finalResponse.text}`);
    } else {
      // If the model didn't need any tools, just print its direct text response
      console.log(`\n🤖 AI Response (No tool needed): ${response.text}`);
    }
  } catch (error) {
    console.error("Error in AI-MCP pipeline:", error);
  } finally {
    // 8. Clean up process connections
    await mcpClient.close();
    console.log("\nMCP connection safely closed.");
  }
}

main();
