from pathlib import Path
p = Path("src/agentscope_runtime/engine/schemas/agent_schemas.py")
data = p.read_bytes()
old = b'    MCP_TOOL_CALL = "mcp_tool_call"\n    MCP_TOOL_CALL_OUTPUT = "mcp_tool_call_output"\n'
new = b'    MCP_TOOL_CALL = "mcp_tool_call"\n    MCP_TOOL_CALL_OUTPUT = "mcp_tool_call_output"\n    REASONING = "reasoning"\n'
print("found:", old in data)
data = data.replace(old, new)
p.write_bytes(data)
print("done")
