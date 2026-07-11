from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b:int) -> int:
    """_summery__
    Add to two number
    """
    return a + b


@mcp.tool()
def multiply(a: int, b:int) -> int:
    """_summery__
    multiply to two number
    """
    return a * b


if __name__ == "__main__":
    mcp.run(transport='stdio')