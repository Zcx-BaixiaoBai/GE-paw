from pathlib import Path
p = Path('src/agentscope_runtime/engine/schemas/agent_schemas.py')
t = p.read_text(encoding='utf-8')
old = '    FUNCTION_CALL_OUTPUT = "function_call_output"'
new = old + chr(10) + '    PLUGIN_CALL = "plugin_call"' + chr(10) + '    PLUGIN_CALL_OUTPUT = "plugin_call_output"' + chr(10) + '    MCP_TOOL_CALL = "mcp_tool_call"' + chr(10) + '    MCP_TOOL_CALL_OUTPUT = "mcp_tool_call_output"'
t2 = t.replace(old, new, 1)
p.write_text(t2, encoding='utf-8')
print('replaced' if t != t2 else 'NOT replaced')
