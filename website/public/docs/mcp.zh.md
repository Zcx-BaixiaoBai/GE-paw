# MCP ?

gepaw  **MCP?* ?****?

---

## 

gepaw ?

1. ****?gepaw 

   - ???"
   - /

2. **MCP ** MCP ?
   - ???MCP"?
   - MCP 

?

---

## MCP

**MCPModel Context Protocol?*  gepaw ?MCP API ?

### 

 MCP 

- **Node.js** 18+ [](https://nodejs.org/)?

```bash
node --version  # ?
```

>  MCP ?

---

###  MCP ?

1.  **??MCP**
2.  **+ ** 
3.  MCP  JSON 
4.  **** 

![MCP](https://img.alicdn.com/imgextra/i1/O1CN01HrYuzS24mpUDOgB6m_!!6000000007434-2-tps-3822-2070.png)

---

### 

gepaw  JSON ?

####  1?mcpServers ?***?

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/folder"
      ],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

####  2

 `mcpServers` ?

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/folder"]
  }
}
```

####  3

```json
{
  "key": "filesystem",
  "name": "",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/folder"]
}
```

> ?

---

### 

#### 

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Documents"
      ]
    }
  }
}
```

#### Tavily?

Tavily ?AI ?

```json
{
  "mcpServers": {
    "tavily": {
      "command": "npx",
      "args": ["-y", "tavily-mcp@latest"],
      "env": {
        "TAVILY_API_KEY": "tvly-xxxxxxxxxxxxx"
      }
    }
  }
}
```

> ****?`tavily_search` ?`TAVILY_API_KEY`tavily mcp?

####  MCP 

```json
{
  "mcpServers": {
    "remote-api": {
      "transport": "streamable_http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer your-token"
      }
    }
  }
}
```

---

### 

#### 

MCP ?

- **stdio** ??`command` 
- **streamable_http** ? HTTP ?`url` 
- **sse** ?Server-Sent Events?`url` ?`transport: "sse"`

#### ?

- `command` ?stdio ?
- `args` ?
- `env` ? API ?
- `cwd` ?
- `url` ?HTTP/SSE ?
- `headers` ??
- `transport` ?

#### 

- **stdio **`command` ?
- **streamable_http / sse **`url` ?
- ?

---

### 

?MCP ?

|           |      | ?   |                                                                |
| ------------- | -------- | --------- | ------------------------------------------------------------------ |
| `name`        | string   | -         | ?                                                |
| `description` | string   | `""`      | ?                                                        |
| `enabled`     | bool     | `true`    |                                                    |
| `transport`   | string   | `"stdio"` | `"stdio"`/ `"streamable_http"` / `"sse"` |
| `url`         | string   | `""`      |  MCP ?HTTP/SSE ?                         |
| `headers`     | object   | `{}`      | HTTP  HTTP/SSE ?                                 |
| `command`     | string   | `""`      | ?stdio  `"npx"``"python"`?               |
| `args`        | string[] | `[]`      | ?stdio ?                                       |
| `env`         | object   | `{}`      |                                                |
| `cwd`         | string   | `""`      | ?stdio ?                                       |

> **?* `transport` ?`command` ?stdio `url` ?http/sse?

---

## 

gepaw ?

---

### 

![tool](https://img.alicdn.com/imgextra/i1/O1CN018oZy751gxmArrsFbC_!!6000000004209-2-tps-3822-2070.png)

#### ?

1.  **??**
2. 
3. 
4. ?***?***

****

- **?*
- **?*?

> ?

> ****[](./multi-agent)?

---

### 

|          |                   |                                             |
| ------------ | ------------------------- | --------------------------------------------------- |
|      | `read_file`               | ?                     |
|      | `write_file`              | ?                                     |
|      | `edit_file`               | ?         |
|      | `append_file`             | ?                                 |
|      | `grep_search`             | ?             |
|      | `glob_search`             |                                 |
|      | `execute_shell_command`   |  Shell ?                      |
| ?  | `delegate_external_agent` |  ACP ?runner              |
|  | `browser_use`             | ?30+ ?|
|          | `desktop_screenshot`      | ?                                 |
|      | `view_image`              | ?                         |
|      | `send_file_to_user`       | ?                   |
|      | `memory_search`           | ?MEMORY.md                      |
|          | `get_current_time`        | ?                                 |
|          | `set_user_timezone`       |                                     |
|          | `get_token_usage`         |  LLM Token ?                          |

### 

****

- `read_file`?
  -  `start_line` ?`end_line` ?
  - ?50KB?`start_line` 
  - 
- `edit_file`
- `append_file`
  - 
  - ?
  - 

****

- `grep_search`
  - `pattern`
  - `path`
  - `is_regex` pattern  False?
  - `case_sensitive`?True?
  - `context_lines`?0?5?
  - `include_pattern`?"\*.py"
- `glob_search`?`**/*.json`

****

- `execute_shell_command`?Shell 
  - Windows  cmd.exeLinux/macOS  bash?
  - `command`?
  - `timeout`?60 ?
  - `cwd`
  - ?

**ACP?*

**?*

- ?runner?`claude_code``codex``qwen_code``opencode`
-  runner  API Key 
- ?**??** ?`delegate_external_agent` 
- ?
  - ?claude code ?
  -  claude code ?md ?
- gepaw ?`delegate_external_agent`?
-  `delegate_external_agent` ?
-  runner ?

- `delegate_external_agent` ACPAgent Client Protocol?runner ?
  - ?coding agent
  - ?runner`qwen_code``claude_code``codex``opencode`
  -  **** **??** 
  - `action`?`start``message``respond``close`
    - `start` `message` ?`hi`
    - `message`?
    - `respond``message` ?* option id**
    - `close`?
  - `runner`runner ?`qwen_code``claude_code``codex``opencode`
  - `message` `respond`  id
  - `cwd`
  - ?

****

- 
- ?*** id
- ?
- ?

**?*

`execute_shell_command` ?

- ****?
  - lscat
- ****
  - ?

?

- `list_background_tasks` - ?
- `get_task_output` - 
- `cancel_task` - ?

?`execute_shell_command` ?

****

- `browser_use`?30+ ?
  - ****start, stop, open, navigate, navigate_back, close
  - ****click, type, hover, drag, select_option
  - ****snapshot, screenshot, console_messages, network_requests
  - ****fill_form, file_upload, press_key
  - **JavaScript **eval, evaluate, run_code
  - ****cookies_get, cookies_set, cookies_clear, tabs, wait_for, pdf, resize, handle_dialog, install, connect_cdp, list_cdp_targets, clear_browser_cache
-  `action` 
- headless `headed=True` ?
-  `page_id`?
- `click` `ref`/`selector``page_x``page_y` viewport ?`ref > selector > page_x/page_y` `ref/selector` ?
  -  `page.mouse.click(...)`?`button` ?`double_click`?`modifiers_json`
  - **?*  Canvas/WebGL  DOM  `action=evaluate` evaluate ?1) `action=evaluate`  canvas ?bounding rect?2) (3) `action=click`  `page_x`/`page_y`

```json
{
  "action": "click",
  "page_x": 420,
  "page_y": 260
}
```

**CDP ?*
 Chrome DevTools Protocol (CDP) ?Chrome 

- **?CDP **?`action="start"` ?`cdp_port` 9222Chrome  `--remote-debugging-port` 
- ****?`action="connect_cdp"` ?`cdp_url` `http://localhost:9222` Chrome
- ** CDP **?`action="list_cdp_targets"` ?9000-10000?CDP 

**CDP ?*

- ?Chrome ?
- ?
- 

**?*

- `desktop_screenshot`
  - `path`
  - `capture_window` macOS  True 
- `view_image`
  - ****?

****

- `memory_search`?
  - ****?
    - ?*??**?"
    - ?
  - `query`?
  - `max_results`?5?
  - `min_score` 0.1?
  -  MEMORY.md ?memory/\*.md 

****

- `get_current_time`?`YYYY-MM-DD HH:MM:SS  ()`
- `set_user_timezone`?
  - `timezone_name`IANA  "Asia/Shanghai"?America/New_York"?UTC"

****

- `get_token_usage`?LLM Token ?
  - `days`?N  30?
  - `model_name`
  - `provider_id`

---

### ?

 `agent.json` ?`tools.builtins` ?

**?*

```json
{
  "tools": {
    "builtin_tools": {
      "execute_shell_command": {
        "name": "execute_shell_command",
        "enabled": true,
        "display_to_user": true,
        "async_execution": false
      },
      "read_file": {
        "name": "read_file",
        "enabled": true,
        "display_to_user": true,
        "async_execution": false
      }
    }
  }
}
```

****

|               |    | ? |                                                                                                                               |
| ----------------- | ------ | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | string | -       | ?                                                                                                                       |
| `enabled`         | bool   | `true`  | ?                                                                                                                   |
| `display_to_user` | bool   | `true`  | ?`false` ?`view_image` ?`false`?|
| `async_execution` | bool   | `false` | ?`execute_shell_command` ?                                                                        |

> **?* ?? `agent.json`?
