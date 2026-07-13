import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { string, z } from "zod";

const server = new McpServer({
  name: "chai",
  version: "1.0.0",
});

async function getWeatherByCity(city: string) {
  city = city.toLowerCase();
  const response = await fetch(
    `https://wttr.in/${city}?format=j1`,
  );
  if (!response.ok) {
    throw new Error(
      `Weather API request failed with status ${response.status}`,
    );
  }
  const data = await response.json();
  return data;
}
server.registerTool(
  "get_weather",
  {
    description:
      "Fetch current weather conditions for any city worldwide.",
    inputSchema: {
      city: z.string(),
    },
  },
  async ({ city }) => {
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(await getWeatherByCity(city)),
        },
      ],
    };
  },
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((err) => {
  console.error("McpServer failed to initiate:", err);
  process.exit(1);
});
