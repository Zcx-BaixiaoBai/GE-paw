# ?

gepaw ****

- **** ??
- **** ??
- **** ?`config.json` ?`agent.json` ?

?**v0.1.0** gepaw ****

1. ****`config.json`?
2. **?*`agent.json`??

---

## 

?`~/.gepaw`?`gepaw init` ?

```
$gepaw_WORKING_DIR/                      #  ~/.gepaw
 config.json                          # 
 workspaces/
?   default/                         # 
?  ?   agent.json                   # ?
?  ?   chats.json                   # 
?  ?   jobs.json                    # 
?  ?   token_usage.json             # Token ?
?  ?   AGENTS.md                    # 
?  ?   SOUL.md                      # 
?  ?   PROFILE.md                   # 
?  ?   BOOTSTRAP.md                 # ?
?  ?   MEMORY.md                    # 
?  ?   skills/                      # ?
?  ?   skill.json                   # 
?  ?   memory/                      # 
?  ?   browser/                     # cookies?
?   abc123/                          # 
?       ...
 skill_pool/                          # 
     skill.json                       # 
     ...

$gepaw_SECRET_DIR/                       #  ~/.gepaw.secret
 providers.json                       #  API Key
 envs.json                            # 
```

> **?* `$gepaw_WORKING_DIR` ?`$gepaw_SECRET_DIR`  `~/.gepaw` ?`~/.gepaw.secret`""?

---

## 

?

**?*

|                        | ?             |                                                                                         |
| -------------------------- | ------------------- | ------------------------------------------------------------------------------------------- |
| `gepaw_WORKING_DIR`      | `~/.gepaw`        | ?                                                                             |
| `gepaw_SECRET_DIR`       | `~/.gepaw.secret` | ?`providers.json` ?`envs.json`Docker  `/app/working.secret` |
| `gepaw_CONFIG_FILE`      | `config.json`       | ?`gepaw_WORKING_DIR`?                                                 |
| `gepaw_HEARTBEAT_FILE`   | `HEARTBEAT.md`      |                                                             |
| `gepaw_JOBS_FILE`        | `jobs.json`         |                                                         |
| `gepaw_CHATS_FILE`       | `chats.json`        |                                                         |
| `gepaw_TOKEN_USAGE_FILE` | `token_usage.json`  | Token ?                                                 |

**?*

|                                  | ?        |                                                             |
| ------------------------------------ | -------------- | --------------------------------------------------------------- |
| `gepaw_LOG_LEVEL`                  | `info`         | `debug` / `info` / `warning` / `error` / `critical`?|
| `gepaw_MEMORY_COMPACT_THRESHOLD`   | `100000`       | ?                                         |
| `gepaw_MEMORY_COMPACT_KEEP_RECENT` | `3`            |                                           |
| `gepaw_MEMORY_COMPACT_RATIO`       | `0.7`          | ?                     |
| `gepaw_CONSOLE_STATIC_DIR`         | __ | ?                                         |

****

|                          | ? |                                      |
| ---------------------------- | ------- | ---------------------------------------- |
| `gepaw_AUTH_ENABLED`       | `false` |  Web ?             |
| `gepaw_AUTH_USERNAME`      | -       |          |
| `gepaw_AUTH_PASSWORD`      | -       |            |
| `gepaw_TOOL_GUARD_ENABLED` | `true`  |                          |
| `gepaw_SKILL_SCAN_MODE`    | `warn`  | `block` / `warn` / `off`?|

****

|                    | ?|                                                    |
| ---------------------- | ------ | ------------------------------------------------------ |
| `FTS_ENABLED`          | `true` |  BM25 ?                                |
| `MEMORY_STORE_BACKEND` | `auto` | `auto` / `local` / `chroma` / `sqlite`?|

---

## 

?**v0.1.0** ?

1. **** - `~/.gepaw/config.json`?
2. **?* - `~/.gepaw/workspaces/{agent_id}/agent.json`

###  config.json



```json
{
  "agents": {
    "active_agent": "default",
    "profiles": {
      "default": {
        "id": "default",
        "name": "?,
        "description": "",
        "enabled": true,
        "workspace_dir": "~/.gepaw/workspaces/default"
      }
    }
  },
  "last_api": {
    "host": "127.0.0.1",
    "port": 8088
  },
  "show_tool_details": true,
  "user_timezone": "Asia/Shanghai",
  "last_dispatch": {
    "channel": "console",
    "user_id": "user1",
    "session_id": "session123"
  }
}
```

** config.json ?*

|                   |            | ?        |                                              |
| --------------------- | -------------- | -------------- | ------------------------------------------------ |
| `agents.active_agent` | string         | `"default"`    | ?ID                              |
| `agents.profiles`     | object         | `{}`           | key ?agent_id?           |
| `last_api.host`       | string \| null | `null`         |  `gepaw app`                 |
| `last_api.port`       | int \| null    | `null`         |  `gepaw app` ?                   |
| `show_tool_details`   | bool           | `true`         | /            |
| `user_timezone`       | string         | __ | IANA  `"Asia/Shanghai"`?           |
| `last_dispatch`       | object \| null | `null`         |  `target="last"`?|

**`agents.profiles[agent_id]`** ?

|             |    |  |                                                               |
| --------------- | ------ | ---- | ----------------------------------------------------------------- |
| `id`            | string | ?  |                                                     |
| `name`          | string | ?  | ?                                                   |
| `description`   | string | ?  | ?                       |
| `enabled`       | bool   | ?  |                                                   |
| `workspace_dir` | string | ?  | ?`$gepaw_WORKING_DIR/workspaces/{id}`?|

> **?*  config.json ?`channels``mcp``tools``security`  `agent.json` ?
>
> ****  `agent.json`  `config.json`?`agent.json` ?`agent.json` ?

> **?* ?`$gepaw_SECRET_DIR/providers.json`?`~/.gepaw.secret/providers.json`?
> **** ?`$gepaw_SECRET_DIR/envs.json`?`~/.gepaw.secret/envs.json`?

### ?agent.json

`$gepaw_WORKING_DIR/workspaces/{agent_id}/` `agent.json`MCP?

```json
{
  "id": "default",
  "name": "?,
  "description": "",
  "workspace_dir": "",
  "channels": {
    "console": {
      "enabled": true,
      "bot_prefix": ""
    },
    "dingtalk": {
      "enabled": false,
      "bot_prefix": "",
      "client_id": "",
      "client_secret": ""
    }
  },
  "mcp": {
    "clients": {
      "filesystem": {
        "name": "",
        "enabled": true,
        "command": "npx",
        "args": [
          "-y",
          "@modelcontextprotocol/server-filesystem",
          "/path/to/folder"
        ]
      }
    }
  },
  "heartbeat": {
    "enabled": false,
    "every": "30m",
    "target": "main",
    "activeHours": null
  },
  "running": {
    "max_iters": 50,
    "llm_retry_enabled": true,
    "llm_max_retries": 3,
    "llm_backoff_base": 1.0,
    "llm_backoff_cap": 10.0,
    "max_input_length": 131072
  },
  "active_model": null,
  "language": "zh",
  "system_prompt_files": ["AGENTS.md", "SOUL.md", "PROFILE.md"],
  "tools": {
    "builtin_tools": {}
  },
  "security": {
    "tool_guard": {
      "enabled": true,
      "shell_evasion_checks": {
        "command_substitution": false,
        "obfuscated_flags": false,
        "backslash_escaped_whitespace": false,
        "backslash_escaped_operators": false,
        "newlines": false,
        "comment_quote_desync": false,
        "quoted_newline": false
      }
    },
    "file_guard": {
      "enabled": true
    },
    "skill_scanner": {
      "mode": "warn"
    },
    "allow_no_auth_hosts": ["127.0.0.1", "::1"]
  },
  "last_dispatch": null
}
```

> **?* ?`agent.json` ?

---

### agent.json 

#### `channels` ?

 `enabled``bot_prefix`?`client_id``client_secret`?

****

- **console** ??
- **dingtalk** ?
- **feishu** ?/Lark
- **discord** ?Discord
- **telegram** ?Telegram
- **qq** ?QQ ?
- **imessage** ?iMessage macOS?
- **mattermost** ?Mattermost
- **matrix** ?Matrix
- **wecom** ?
- **wechat** ?iLink?
- **xiaoyi** ?
- **mqtt** ?MQTT
- **voice** ?Voice

> **?*  `client_id` `app_id`?[](./channels)?

 ? `agent.json`?

> **** ?2 ?`agent.json` ?

---

#### `mcp` ?MCP ?

MCP FilesystemGitSQLite ?MCP ?

 MCP stdio/HTTP/SSE URL ?

> **?* MCP ?[MCP](./mcp)?

 ?MCP `agent.json`?

---

#### `heartbeat` ?

 `HEARTBEAT.md` ?

|           |            | ?  |                                                                          |
| ------------- | -------------- | -------- | ---------------------------------------------------------------------------- |
| `enabled`     | bool           | `false`  |                                                              |
| `every`       | string         | `"30m"`  | ?`Nh``Nm``Ns`  `"1h"``"30m"``"2h30m"``"90s"` |
| `target`      | string         | `"main"` | `"main"` = `"last"` = ?    |
| `activeHours` | object \| null | `null`   | `start``end` ?4                                |

 [](./heartbeat)?

---

#### `running` ??

?

**?*

|                          |   | ? |                                                                                                                                                                                                                      |
| ---------------------------- | ----- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `max_iters`                  | int   | `100`   | ReAct Agent - ?1?                                                                                                                                                                         |
| `shell_command_timeout`      | float | `60.0`  | `execute_shell_command` LLM  timeout ?                                                                                                                               |
| `shell_command_executable`   | str   | `""`    | `execute_shell_command` ?Linux/macOS  shell  `/bin/bash``/bin/zsh`Windows ?`powershell.exe` / `pwsh.exe`?`$SHELL` ?`/bin/sh`Windows  `cmd.exe`?|
| `auto_continue_on_text_only` | bool  | `false` | ?,Agent ?                                                                                                                                                        |

**LLM **

|                     |   | ? |                                                         |
| ----------------------- | ----- | ------- | ----------------------------------------------------------- |
| `llm_retry_enabled`     | bool  | `true`  |  LLM API        |
| `llm_max_retries`       | int   | `3`     |  LLM API  ?1?                |
| `llm_backoff_base`      | float | `1.0`   | ??0.1?                   |
| `llm_backoff_cap`       | float | `10.0`  |  ?0.5 ?`llm_backoff_base`?|
| `llm_max_concurrent`    | int   | `10`    | ?LLM ?                    |
| `llm_max_qpm`           | int   | `600`   | QPM? = ?                    |
| `llm_rate_limit_pause`  | float | `5.0`   |  429 ?                    |
| `llm_rate_limit_jitter` | float | `1.0`   | ?         |
| `llm_acquire_timeout`   | float | `300.0` |                           |

****

|                        |    | ?         |                                                   |
| -------------------------- | ------ | --------------- | ----------------------------------------------------- |
| `max_input_length`         | int    | `131072` (128K) | token  ?1000?|
| `history_max_length`       | int    | `10000`         | `/history`                |
| `context_manager_backend`  | string | `"light"`       |                                   |
| `memory_manager_backend`   | string | `"remelight"`   | ?                                   |
| `light_context_config`     | object | __    | Light                                 |
| `reme_light_memory_config` | object | __    | ReMeLight ?                             |

**Light `light_context_config` **

|                            |    | ?    |                                             |
| ------------------------------ | ------ | ---------- | ----------------------------------------------- |
| `dialog_path`                  | string | `"dialog"` |                 |
| `token_count_estimate_divisor` | float  | `4.0`      | ?token byte_len / divisor?|

**Light `light_context_config.context_compact_config` **

|                           |   | ?|                                             |
| ----------------------------- | ----- | ------ | ----------------------------------------------- |
| `enabled`                     | bool  | `true` | ?                         |
| `compact_threshold_ratio`     | float | `0.8`  | ?`max_input_length`?|
| `reserve_threshold_ratio`     | float | `0.1`  |                       |
| `compact_with_thinking_block` | bool  | `true` |                             |

**Light `light_context_config.tool_result_pruning_config` **

|                            |  | ? |                        |
| ------------------------------ | ---- | ------- | -------------------------- |
| `enabled`                      | bool | `true`  |        |
| `pruning_recent_n`             | int  | `2`     | ?N ? |
| `pruning_old_msg_max_bytes`    | int  | `3000`  | ?  |
| `pruning_recent_msg_max_bytes` | int  | `50000` | ?|
| `offload_retention_days`       | int  | `5`     |        |

**ReMeLight `reme_light_memory_config` **

|                             |         | ?        |                                                      |
| ------------------------------- | ----------- | -------------- | -------------------------------------------------------- |
| `summarize_when_compact`        | bool        | `true`         |                            |
| `auto_memory_interval`          | int \| null | `null`         |  N null  |
| `dream_cron`                    | string      | `"0 23 * * *"` | ?Cron ?          |
| `rebuild_memory_index_on_start` | bool        | `false`        | ?                              |
| `recursive_file_watcher`        | bool        | `false`        |                                      |
| `auto_memory_search_config`     | object      | __   |                                          |
| `embedding_model_config`        | object      | __   | Embedding                                        |

**`reme_light_memory_config.auto_memory_search_config` **

|           |   | ? |                                         |
| ------------- | ----- | ------- | ------------------------------------------- |
| `enabled`     | bool  | `false` |             |
| `max_results` | int   | `1`     | ?                 |
| `min_score`   | float | `0.1`   | 0.0 - 1.0?|
| `timeout`     | float | `10.0`  | ?                     |

**Embedding `reme_light_memory_config.embedding_model_config` **

|                |    | ?    |                                                 |
| ------------------ | ------ | ---------- | --------------------------------------------------- |
| `backend`          | string | `"openai"` | Embedding  `"openai"`?                |
| `api_key`          | string | `""`       | Embedding  API Key                          |
| `base_url`         | string | `""`       | ?API                              |
| `model_name`       | string | `""`       | Embedding  `"text-embedding-3-small"`?|
| `dimensions`       | int    | `1024`     | Embedding                                   |
| `enable_cache`     | bool   | `true`     |  Embedding                              |
| `use_dimensions`   | bool   | `false`    | ?                                 |
| `max_cache_size`   | int    | `3000`     | ?                                       |
| `max_input_length` | int    | `8192`     | Embedding ?                           |
| `max_batch_size`   | int    | `10`       | ?                               |

 **??**  LLM ?

---

#### `language` & `system_prompt_files` ?

|                   |           | ?                                  |                              |
| --------------------- | ------------- | ---------------------------------------- | -------------------------------- |
| `language`            | string        | `"zh"`                                   | `zh` / `en` / `ru`?|
| `system_prompt_files` | array[string] | `["AGENTS.md", "SOUL.md", "PROFILE.md"]` | ?  |

**** ?

- ?**???* ?
-  `system_prompt_files` ?
- ?**??** ?

**?*  [](./persona) ?

---

#### `active_model` ??

?

|           |    | ?|                                           |
| ------------- | ------ | ------ | --------------------------------------------- |
| `provider_id` | string | `""`   | ?ID `"dashscope"``"openai"`?|
| `model`       | string | `""`   |  `"qwen-max"``"gpt-4"`?       |

?`null`  ??

---

#### `plan` ?

|       |  | ? |              |
| --------- | ---- | ------- | ---------------- |
| `enabled` | bool | `false` |  |

??`/plan` ?[](./plan)?

---

#### `approval_level` ?

|              |    | ?  |                                                                           |
| ---------------- | ------ | -------- | ----------------------------------------------------------------------------- |
| `approval_level` | string | `"AUTO"` | : `STRICT``SMART``AUTO``OFF`?[](./security)?|

---

#### `tools` ?

??

> **?* ?[MCP ](./mcp)?

 ? `agent.json`?

---

#### `security` ?

?

- **`tool_guard`** ??
- **`file_guard`** ?
- **`skill_scanner`** ??

?

|                   |      | ?                |                                                   |
| --------------------- | -------- | ---------------------- | ----------------------------------------------------- |
| `allow_no_auth_hosts` | string[] | `["127.0.0.1", "::1"]` | IP  Web ?localhost  |

> **?*  [](./security)?

?? `agent.json`?

---

#### `last_dispatch` ??

 `target = "last"` ?

|          |    | ?|                                      |
| ------------ | ------ | ------ | ---------------------------------------- |
| `channel`    | string | `""`   |  `"discord"``"dingtalk"`?|
| `user_id`    | string | `""`   | ?ID                        |
| `session_id` | string | `""`   | / ID                             |

?

---

## ?

gepaw ?LLM  `$gepaw_SECRET_DIR/providers.json`?`~/.gepaw.secret/providers.json`?



- **`gepaw init`** ??
- **?UI** ???
- **API** ?`PUT /providers/{id}` ?`PUT /providers/active_llm`

****

| ?                                 | ID                       |                           |
| --------------------------------------- | ------------------------ | ----------------------------- |
| gepaw Local                           | `gepaw-local`          |  llama.cpp            |
| Ollama                                  | `ollama`                 |  Ollama               |
| LM Studio                               | `lmstudio`               |  LM Studio            |
| OpenRouter                              | `openrouter`             | OpenRouter        |
| ModelScope                      | `modelscope`             |               |
| DashScope                       | `dashscope`              | ?           |
| ?Coding PlanChina?        | `aliyun-codingplan`      | ?Coding Plan        |
| ?Coding PlanInternational?| `aliyun-codingplan-intl` | ?Coding Plan ?|
| OpenAI                                  | `openai`                 | OpenAI API                    |
| Azure OpenAI                            | `azure-openai`           | Azure OpenAI Service          |
| Anthropic                               | `anthropic`              | Anthropic Claude API          |
| Google Gemini                           | `gemini`                 | Google Gemini API             |
| DeepSeek                                | `deepseek`               | DeepSeek API                  |
| KimiChina?                          | `kimi-cn`                | Moonshot Kimi ?         |
| KimiInternational?                  | `kimi-intl`              | Moonshot Kimi ?         |
| MiniMaxChina?                       | `minimax-cn`             | MiniMax ?               |
| MiniMaxInternational?               | `minimax`                | MiniMax ?               |
| ZhipuBigModel?                      | `zhipu-cn`               | ?API            |
| Zhipu Coding PlanBigModel?          | `zhipu-cn-codingplan`    | ?Coding Plan        |
| ZhipuZ.AI?                          | `zhipu-intl`             | ?API            |
| Zhipu Coding PlanZ.AI?              | `zhipu-intl-codingplan`  | ?Coding Plan        |
| OpenCode                                | `opencode`               | OpenCode Zen          |
| SiliconFlowChina?                   | `siliconflow-cn`         | ?               |
| SiliconFlowInternational?           | `siliconflow-intl`       | ?               |
| ?                                 | `custom`                 | ?OpenAI         |

> **?* `providers.json` ?[](./models)?

> **?*  `gepaw init` ?

---

## 

?MCP  API Key `TAVILY_API_KEY`?

- **`gepaw init`** ? "Configure environment variables?"
- **?UI** ??
- **API** ?`GET/PUT/DELETE /envs`

 `os.environ` ?

> **?*  API KeyQwenPaw ?

---

## Skills?

?

- **`$gepaw_WORKING_DIR/skill_pool/`** ?
- **`$gepaw_WORKING_DIR/workspaces/{agent_id}/skills/`** ??

?`SKILL.md` ?`skill.json` ?`~/.gepaw/workspaces/default/skill.json`?

> **?* `skill.json` Config ?[](./skills)?

?

- **?* ???
- **`gepaw skills config`** ?CLI ?
- **** `skill.json` ??

---

## Memory?



- **`MEMORY.md`** ??
- **`memory/YYYY-MM-DD.md`** ??

?

> **?* Embedding ?[](./memory)?

---

## 

- ?**`$gepaw_WORKING_DIR`**?`~/.gepaw`?
- ?**v0.1.0** ?
  - ****`config.json`?
  - **?*`workspaces/{agent_id}/agent.json`?
-  **?* ?JSON ?
-  Markdown ?[](./persona)?
- ?*?* 2 ?

---

## 

- [](./intro) ??
- [](./persona) ?
- [](./channels) ?
- [](./heartbeat) ?
- [](./multi-agent) ?
- [](./memory) ?
- [](./skills) ??
- [MCP](./mcp) ?MCP ?
