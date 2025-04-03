# Documentation MCP Server

This was created following AO - Software & AI Youtube tutorial on how to create MCP Servers in Python.
<https://www.youtube.com/watch?v=Ek8JHgZtmcI>

## Initialization

To add the mcp server to claude run:
`claude mcp add`
Give a server a chosen name when prompted.

I chose for the server to be available in the **project** directory as recommended.

For the server command, i use the entire binary for my uv installation:
`/Users/baw/.local/bin/uv`

For command arguements, use:
`--directory /Users/baw/Desktop/dev/mcp/first_mcp_server run main.py`

Continue without environment variables since a .env file I already declared. Confirm and the server should be installed.

## Testing

To list the available mcp servers run:  
`clause mcp list`  
The new server first_mcp server should be listed.

We can run claude code using command:  
 `claude`

Then test with a query like:

> create a new function that implements a chroma db vector database with langchain. Make sure to use the latest integration

Run **MCP Inspector** to debug Server with:  
`npx @modelcontextprotocal/inspector uv run main.py`
