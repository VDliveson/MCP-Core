from fastmcp import FastMCP
from tools.web_scraper import (
    scrape_url,
    extract_links,
    extract_metadata,
    extract_structured_data,
)

# Initialize FastMCP server
mcp = FastMCP("mcp-core")

mcp.tool()(scrape_url)
mcp.tool()(extract_links)
mcp.tool()(extract_metadata)
mcp.tool()(extract_structured_data)

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
