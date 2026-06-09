# ACP 

gepaw ?**ACPAgent Client Protocol?* 

1. **gepaw ?ACP  Tool **QwenPaw  ACP runner
2. **gepaw  ACP Server** ACP ?gepaw

?

---

## gepaw ?ACP  Tool 

QwenPaw ?**ACP client / orchestrator**?*?ACP runner**?

 `delegate_external_agent` gepaw ?ACP ?agent runtime  `opencode``qwen_code``claude_code``codex`?agent ?ACP ?Agent <https://agentclientprotocol.com/get-started/agents>gepaw  agent  ACP ?runner?

### ?

QwenPaw ?`delegate_external_agent` 

- ?ACP runner 
-  runner ?
- ?runner ?
- 

 gepaw ?agent  gepaw ?

###  runner

?runner ?ACP ?agentAPI Key ?ACP ?agent ?https://agentclientprotocol.com/get-started/agents>?

![qwen](https://gw.alicdn.com/imgextra/i1/O1CN01XtTTNP1IuyyyKi5ZS_!!6000000000954-2-tps-1196-664.png)

 gepaw  runner runner ?

 runner ?**Workspace ?ACP**  `delegate_external_agent` ?

 ACP  runner ?

- `enabled`
- `command`
- `args`
- `env`
- `trusted`
- `tool_parse_mode`
- `stdio_buffer_limit_bytes`

?

- `command` ?`args`  runner ?
- `env` 
- `tool_parse_mode` ?`stdio_buffer_limit_bytes`  ACP ?stdio ?

 Linux/macOS`command` ?agent ?ACP ?`opencode``qwen`?ACP  `npx``args`  `--acp``-y` ?*?*?runner `opencode``qwen_code``claude_code``codex` ACP  runner?ACP ?

![config_mac](https://gw.alicdn.com/imgextra/i3/O1CN01pskmLt29VwyFGhO1r_!!6000000008074-2-tps-1224-472.png)

 Windows agent `command`  `cmd``args` ?`/c`?*?*

![config_win](https://gw.alicdn.com/imgextra/i3/O1CN01BDYXdk22Zt4726sHa_!!6000000007135-2-tps-1608-792.png)

?`delegate_external_agent` ?

![config](https://gw.alicdn.com/imgextra/i1/O1CN01xNZfYc1OM4UFIR79S_!!6000000001690-2-tps-1224-696.png)

?agent ?

![comm](https://gw.alicdn.com/imgextra/i4/O1CN01lk5XhU2988NFcFtR0_!!6000000008022-2-tps-2022-1166.png)

### ?

?ACP 

1. ?**Workspace ?ACP** ?runner?
2.  `delegate_external_agent(action="start", runner="...", message="...")`?runner ?
3.  `delegate_external_agent(action="message", runner="...", message="...")` runner ?
4.  runner  `delegate_external_agent(action="respond", runner="...", message="<exact option id>")`  `message` ?* option id**?
5.  `delegate_external_agent(action="close", runner="...")` ?runner ?

?`start` ?`message` ?Markdown  action`start``message``respond``close`?

### ?

?

|       | ?                                     |
| --------- | ----------------------------------------- |
| `start`   |  ACP                      |
| `message` | ?               |
| `respond` | ?option id  |
| `close`   |  ACP                          |

### 

?ACP runner gepaw ****?



- 
- 
- 

 ACP ?gepaw ?

### ?ACP as Tool

?

- ?gepaw ?agent runtime 
-  ACP-compatible  runner
-  gepaw  agent

### ACP Tool ?MCP ?

ACP as Tool ?MCP 

- **MCP** gepaw 
- **ACP as Tool** gepaw  **agent** runtime

?API?**MCP**?
?agent ?agent  **ACP as Tool**?

---

## gepaw as ACP Server

QwenPaw  stdio JSON-RPC ?[Agent Client Protocol (ACP)](https://github.com/agentclientprotocol/python-sdk)  [Zed](https://zed.dev)[OpenCode](https://github.com/nicholasgasior/opencode) ?ACP  `gepaw acp` ?gepaw?

### ?

```bash
#  gepaw  ACP ?
gepaw acp

# 
gepaw acp --agent mybot

# 
gepaw acp --workspace /path/to/workspace

#  stderr?
gepaw acp --debug
```

 stdin/stdout  ACP JSON-RPC stderr ?

### ?ACP 

|                 |                                              |
| ------------------- | ------------------------------------------------ |
| `initialize`        | ?                  |
| `new_session`       |                                      |
| `load_session`      | ?ID ?                        |
| `resume_session`    | ?                              |
| `list_sessions`     | ?`cwd`                     |
| `close_session`     | ?                                  |
| `prompt`            |                |
| `set_session_model` |  LLM  `provider_id:model_id` |
| `set_config_option` | ?Tool Guard ?          |
| `cancel`            | ?`prompt`                          |

### 

?`prompt`  `session_update` 

|               |                  |
| --------------------- | ------------------------ |
| `agent_message_chunk` | ?  |
| `agent_thought_chunk` |  |
| `tool_call`           | ?            |
| `tool_call_update`    | ?  |

### ?

?`initialize` ?

```json
{
  "load_session": true,
  "session_capabilities": {
    "close": {},
    "list": {},
    "resume": {}
  }
}
```

### 

 `set_config_option` ?

|  ID |    |    | ?   | ?                                                                     |
| ------- | ------ | ------ | --------- | --------------------------------------------------------------------------- |
| `mode`  | select | `mode` | `default` | `default` Tool Guard`bypassPermissions`?|

### 

ACP 

1. **CLI **`--agent` ?`--workspace` ?
2. **WORKING_DIR ** `WORKING_DIR`  `config.json` ?`agents.active_agent`?`~/.gepaw` `~/.copaw` `gepaw_WORKING_DIR` ?
3. **?* ID `"default"`  `WORKING_DIR/workspaces/default/`

---

## ACP Server vs ACP Tool

|            | gepaw as ACP Server            | gepaw using ACP as Tool           |
| -------------- | -------------------------------- | ----------------------------------- |
| gepaw ?| Server / ?         | Client / ?                    |
|        | ?gepaw           | gepaw  runner             |
|        |  gepaw | ?gepaw ?agent |
|        | `gepaw acp`                    | delegation tool + ACP runner    |
|        |            | ?runner       |

---

## 

ACP ?gepaw ?

- ** gepaw**?ACP server
- **?gepaw ** ACP agent 

 gepaw  **ACP Server**?
 gepaw ?agent runtime **ACP as Tool**?
