# wildberries-fast-mcp

A Python wrapper around [FastMCP](https://gofastmcp.com/integrations/openapi) that exposes the full Wildberries API as an MCP server.

WB API consists of several OpenAPI specifications, each containing one or few domains. 
Because `FastMCP.from_openapi` doesn't support multiple domains out of the box, specs with few domains are split into few scopes for simplicity.  


---

## Features

- Full coverage of the Wildberries public API
- Built on [FastMCP](https://gofastmcp.com/integrations/openapi) — a fast Python framework for MCP servers

---

## Installation

```bash
pip install wildberries-fast-mcp
```

Or with `uv`:

```bash
uv add wildberries-fast-mcp
```

---

## Quick Start


### Connect to Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "wildberries-content": {
      "command": "python",
      "args": ["-m", "wbmcp", "--scope", "products:content", "--token", "YOU_WB_API_TOKEN"]
    },
    "wildberries-prices": {
      "command": "python",
      "args": ["-m", "wbmcp", "--scope", "products:discounts-prices", "--token", "YOU_WB_API_TOKEN"]
    }
  }
}
```


## License

MIT