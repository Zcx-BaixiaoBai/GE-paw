# CLI

`gepaw` ?gepaw ?? ??
?

>  [](./intro)?

---

## ?

 gepaw?

### gepaw init

?

```bash
gepaw init              # ?
gepaw init --defaults   # ?
gepaw init --force      # 
```

****

1. **** ??
2. **LLM ?* ??API Key?*?*?
3. **** ??
4. **HEARTBEAT.md** ??

### gepaw app

 gepaw ?

```bash
gepaw app                             #  127.0.0.1:8088
gepaw app --reload                    # ?
gepaw app --log-level debug           # 
```

|           | ?     |                                                           |
| ------------- | ----------- | ------------------------------------------------------------- |
| `--host`      | `127.0.0.1` |                                                       |
| `--port`      | `8088`      |                                                       |
| `--reload`    |         | ?                               |
| `--log-level` | `info`      | `critical` / `error` / `warning` / `info` / `debug` / `trace` |
| `--workers`   | ?          | **[]** QwenPaw  1 ?worker           |

> **?* `--workers` QwenPaw ?worker  worker  WebSocket ?

### ?

`gepaw app`  `http://127.0.0.1:8088/`  **?* ?
?Web ?[](./console)?

?`{"message": "gepaw Web Console is not available."}` API ?

**?* ?`console/` ?`npm ci && npm run build`?

`mkdir -p src/gepaw/console && cp -R console/dist/. src/gepaw/console/`?
Docker ?pip ?

### gepaw daemon

?`/daemon status` CLI ?

|                            |                                                                            |
| ------------------------------ | ------------------------------------------------------------------------------ |
| `gepaw daemon status`        |                                                |
| `gepaw daemon restart`       |  /daemon restart ?                           |
| `gepaw daemon reload-config` | /MCP  /daemon restart ?|
| `gepaw daemon version`       | ?                                                                    |
| `gepaw daemon logs [-n N]`   | ?N  100?`gepaw.log`?                         |

**?*  `--agent-id`  `default`?

```bash
gepaw daemon status                     # ?
gepaw daemon status --agent-id abc123   # ?
gepaw daemon version
gepaw daemon logs -n 50
```

### gepaw doctor

****?`config.json` `agent.json`?
MCPHTTP API ?Agent ?
?* `doctor` **?
**`gepaw doctor fix`**?`doctor-fix-backups/` ?

```bash
gepaw doctor                      # ?
gepaw doctor --deep               #  +  llama 
gepaw doctor --port 8088          #  API ?
gepaw doctor fix --dry-run        # ?
gepaw doctor fix -y --only ?     # ?--help?
```

|             |  |                                                |
| --------------- | -------- | -------------------------------------------------- |
| `--timeout`     | `doctor` | API / ?HTTP ?5             |
| `--llm-timeout` | `doctor` |  15                    |
| `--deep`        | `doctor` | `gepaw-local` ?|

**`doctor` ?host/port?* ?`gepaw --host` /
`--port`  `doctor`CLI 
**`config.json` ?`last_api`** `gepaw app` 
** `last_api` ?* `127.0.0.1:8088`
?`--port`?`last_api`?

**`doctor fix`** ?

#### ?

```bash
gepaw doctor fix --dry-run
# ?
gepaw doctor fix --dry-run --only ensure-working-dir,ensure-workspace-dirs

# 
gepaw doctor fix --only ensure-working-dir,ensure-workspace-dirs
```

- `--dry-run` ?
-  jobs.json FAIL  0 
  ?CI ?

#### fix ids?

 `--only` ?id?

- 
  - `ensure-working-dir`?
  - `ensure-workspace-dirs` agent workspace 
-  fix ids ?
  - `gepaw doctor fix --help`
- ?`gepaw doctor` ?
  ?`doctor fix --dry-run --only ...` ?

#### 

?

```bash
gepaw doctor fix --dry-run --only seed-missing-agent-json,reset-invalid-agent-json
gepaw doctor fix -y --only seed-missing-agent-json,reset-invalid-agent-json
```

- `-y` ?`--dry-run`?
- `--non-interactive` ?+  + ?

#### ?



- `doctor-fix-backups/<?/files/`

?`files/` ?

> ?`--no-backup`?

---

## ?

 gepaw ?LLM ?

### gepaw models

 LLM ?

|                                      |                                    |
| ---------------------------------------- | -------------------------------------- |
| `gepaw models list`                    | API Key  |
| `gepaw models config`                  | API Key ?     |
| `gepaw models config-key [provider]`   |  API Key           |
| `gepaw models set-llm`                 |  API Key?        |
| `gepaw models local`                   |                    |
| `gepaw models download <repo_id>`      | llama.cpp?         |
| `gepaw models remove-local <model_id>` |                    |

```bash
gepaw models list                    # ?
gepaw models config                  # ?
gepaw models config-key modelscope   #  ModelScope ?API Key
gepaw models config-key dashscope    #  DashScope ?API Key
gepaw models config-key custom       # Base URL + Key?
gepaw models set-llm                 # ?
```

#### 

gepaw  llama.cppOllama ?LM Studio  API Key?
 [Ollama](https://ollama.com/download) ?[LM Studio](https://lmstudio.ai/download)?

```bash
#  Q4_K_M GGUF?
gepaw models download Qwen/Qwen3-4B-GGUF

# ?ModelScope 
gepaw models download Qwen/Qwen2-0.5B-Instruct-GGUF --source modelscope

# ?
gepaw models local

# ?
gepaw models remove-local <model_id>
gepaw models remove-local <model_id> --yes   # 
```

|        | ?| ?       |                                            |
| ---------- | ---- | ------------- | ---------------------------------------------- |
| `--source` | `-s` | `huggingface` | `huggingface` ?`modelscope`?       |
| `--file`   | `-f` | __    | GGUF  Q4_K_M?|

#### Ollama 

gepaw  Ollama  Ollama  [ollama.com](https://ollama.com)  Ollama?

 Ollama SDK`pip install 'gepaw[ollama]'` `--extras ollama` ?

```bash
#  Ollama 
ollama pull mistral:7b
ollama pull qwen2.5:3b

#  Ollama 
ollama list

#  Ollama 
ollama rm mistral:7b

# ?Ollama ?
gepaw models config           #  Ollama ?
gepaw models set-llm          # ?Ollama 
```

**?*

-  Ollama ?gepaw ?
-  `ollama`  `gepaw models`?
-  Ollama CLI ?gepaw /

> **?* API Key gepaw ?
>  [ ?](./config#??

### gepaw env

?

|                         |                  |
| --------------------------- | -------------------- |
| `gepaw env list`          | ?|
| `gepaw env set KEY VALUE` | ?      |
| `gepaw env delete KEY`    |              |

```bash
gepaw env list
gepaw env set TAVILY_API_KEY "tvly-xxxxxxxx"
gepaw env set GITHUB_TOKEN "ghp_xxxxxxxx"
gepaw env delete TAVILY_API_KEY
```

> **?* gepaw ?
>  [ ?](./config#)?

---

## 

?gepaw ?

### gepaw channels

iMessage / Discord / DingTalk / Feishu / QQ / Console ?
****?`config` `configure` ?`remove` `uninstall`?

**?* ?`gepaw channel` `gepaw channels` ?

|                              |                                                                             |
| -------------------------------- | ------------------------------------------------------------------------------- |
| `gepaw channels list`          | ?                                                 |
| `gepaw channels send`          | ??5                                     |
| `gepaw channels install <key>` | ?`custom_channels/`  `--path` / `--url`           |
| `gepaw channels add <key>`     | ?config?config?`--path` / `--url`                 |
| `gepaw channels remove <key>`  | ?`custom_channels/` `--keep-config`  config |
| `gepaw channels config`        | ??                                                  |

**?*  `--agent-id`  `default`?

```bash
gepaw channels list                    # ?
gepaw channels list --agent-id abc123  # ?
gepaw channels install my_channel      # ?
gepaw channels install my_channel --path ./my_channel.py
gepaw channels add dingtalk            # ?config
gepaw channels remove my_channel       #  config ?
gepaw channels remove my_channel --keep-config   # ?config 
gepaw channels config                  # 
gepaw channels config --agent-id abc123 # 
```

?`config` ??

|          |                                                              |
| ------------ | -------------------------------------------------------------------------- |
| **iMessage** | Bot ?                                            |
| **Discord**  | Bot Bot TokenHTTP ?                                  |
| **DingTalk** | Bot Client IDClient SecretCard  ID/KeyRobot Code |
| **Feishu**   | Bot App IDApp Secret                                               |
| **QQ**       | Bot App IDClient Secret                                            |
| **Console**  | Bot                                                                    |

> ?[](./channels)?

#### ?

> **Channel Message**

 `gepaw channels send` ??*?* ??

 **channel_message** ?

**?*

- 
- ?
- ?
- "?

```bash
# 
gepaw chats list --agent-id my_bot --channel feishu

# ?
gepaw channels send \
  --agent-id my_bot \
  --channel feishu \
  --target-user ou_xxxx \
  --target-session session_id_xxxx \
  --text ""
```

**?5 ?*

- `--agent-id`?ID
- `--channel`console/dingtalk/feishu/discord/imessage/qq?
- `--target-user`?ID `gepaw chats list` ?
- `--target-session`?ID `gepaw chats list` ?
- `--text`?

**?*

-  `gepaw chats list`  ? `target-user` ?`target-session`
- 
-  `gepaw agents chat`"??

**?`gepaw agents chat` **

- `gepaw channels send`?
- `gepaw agents chat`?

---

## ?

?

### gepaw agents

> **Multi-Agent Collaboration**

 **multi_agent_collaboration**  `gepaw agents chat` ?

**?* ?`gepaw agent` `gepaw agents` ?

|                     |                                                        |
| ----------------------- | ---------------------------------------------------------- |
| `gepaw agents list`   | ID?          |
| `gepaw agents create` | ?      |
| `gepaw agents delete` | ?|
| `gepaw agents chat`   | ?                  |

```bash
# 
gepaw agents list
gepaw agent list  # 

# ?
gepaw agents create --name "?
gepaw agents create --name "" --template coder --skill web_search --skill pdf_reader
gepaw agents create --name "GPT Bot" --provider-id openai --model-id gpt-4

# 
gepaw agents delete my_agent
gepaw agents delete my_agent --remove-workspace  # ?
gepaw agents delete my_agent --yes                # 

# ?
gepaw agents chat \
  --agent-id my_bot \
  --to-agent helper_bot \
  --text "?

# session ?
gepaw agents chat \
  --agent-id my_bot \
  --to-agent helper_bot \
  --session-id collab_session_001 \
  --text "?

# 
gepaw agents chat --background \
  --agent-id my_bot \
  --to-agent data_analyst \
  --text " /data/logs/2026-03-26.log ?
#  [TASK_ID: xxx] [SESSION: xxx]

# ?--to-agent 
gepaw agents chat --background \
  --task-id <task_id>
# submitted ?pending ?running ?finished
# finished completed failed?

# ?
gepaw agents chat \
  --agent-id my_bot \
  --to-agent helper_bot \
  --text "" \
  --mode stream
```

**?*

- `--from-agent``--agent-id`?ID?
- `--to-agent` ID?
- `--text`?

**?*

- `--background`?
- `--task-id`?`--background` 

****

- `--session-id` ID?
- `--mode`??`final` `stream`?
  - ****`--background` ?`--mode stream` 
- `--base-url`?API 
- `--timeout` 300?
- `--json-output`?JSON ?

**?*

 `--background`  `task_id`?

****?

- ?
- 
- 
- ?API
- 

**?*?

- `submitted`?
- `pending`?
- `running`?
- `finished` `completed` ?`failed` ?

**?* `--from-agent` ?`--agent-id`  `--task-id``--to-agent` ?

**?`gepaw channels send` **

- `gepaw agents chat`?
- `gepaw channels send`??

---

## 

?gepaw ?9  2 ?
**?`gepaw app` ?*

### gepaw cron

|                            |                            |
| ------------------------------ | ------------------------------ |
| `gepaw cron list`            | ?                  |
| `gepaw cron get <job_id>`    |                    |
| `gepaw cron state <job_id>`  |  |
| `gepaw cron create ...`      |                        |
| `gepaw cron delete <job_id>` |                        |
| `gepaw cron pause <job_id>`  |                        |
| `gepaw cron resume <job_id>` | ?                |
| `gepaw cron run <job_id>`    | ?                  |

**?*  `--agent-id`  `default`?

### 

****



- **text** ??
- **agent** ??gepaw ?

```bash
# text?9 ?
gepaw cron create \
  --type text \
  --schedule-type cron \
  --name "" \
  --cron "0 9 * * *" \
  --channel dingtalk \
  --target-user "ID" \
  --target-session "ID" \
  --text ""

# agent?
gepaw cron create \
  --agent-id abc123 \
  --type agent \
  --schedule-type cron \
  --name "? \
  --cron "0 */2 * * *" \
  --channel dingtalk \
  --target-user "ID" \
  --target-session "ID" \
  --text ""

# 
gepaw cron create \
  --type text \
  --schedule-type scheduled \
  --name "? \
  --run-at "2026-05-13T09:00:00+08:00" \
  --channel dingtalk \
  --target-user "ID" \
  --target-session "ID" \
  --text "9 ? \
  --save-result-to-inbox

# ?14 ?
gepaw cron create \
  --type text \
  --schedule-type scheduled \
  --name "" \
  --run-at "2026-05-13T09:00:00+08:00" \
  --repeat-every-days 1 \
  --repeat-end-type count \
  --repeat-count 14 \
  --channel dingtalk \
  --target-user "ID" \
  --target-session "ID" \
  --text "9 ? \
  --save-result-to-inbox
```



- `--schedule-type cron``--type``--name``--cron``--channel``--target-user``--target-session``--text`
- `--schedule-type scheduled``--type``--name``--run-at``--channel``--target-user``--target-session``--text`

`scheduled`?

- `--repeat-every-days`
- `--repeat-end-type count --repeat-count N` ?`--repeat-end-type until --repeat-until <ISO8601>`
- ?`--repeat-end-type never`

**JSON **

```bash
gepaw cron create -f job_spec.json
```

JSON ?`gepaw cron get <job_id>` ?

### 

|                                                    | ?  |                                                               |
| ------------------------------------------------------ | -------- | ----------------------------------------------------------------- |
| `--timezone`                                           |  | ?config  `user_timezone`?                 |
| `--enabled` / `--no-enabled`                           |      |                                                   |
| `--mode`                                               | `final`  | `stream`?`final`                |
| `--save-result-to-inbox` / `--no-save-result-to-inbox` |  | ?           |
| `--repeat-every-days`                                  | ?  | ?`--schedule-type scheduled`  N ?                 |
| `--repeat-end-type`                                    | `never`  | `never` / `until` / `count`                       |
| `--repeat-until`                                       | ?       | ?`--repeat-end-type until` ISO 8601             |
| `--repeat-count`                                       | ?       | ?`--repeat-end-type count` ?|
| `--base-url`                                           |      |  API                                                      |

### Cron 

**?????*?

| ?        |           |
| -------------- | ------------- |
| `0 9 * * *`    |  9:00     |
| `0 */2 * * *`  | ?2  |
| `30 8 * * 1-5` | ?8:30   |
| `0 0 * * 0`    | ?0:00   |
| `*/15 * * * *` | ?15     |

---

## 

 API ?*?`gepaw app` ?*

### gepaw chats

|                                      |                                                |
| ---------------------------------------- | -------------------------------------------------- |
| `gepaw chats list`                     |  `--user-id``--channel`  |
| `gepaw chats get <id>`                 | ?                            |
| `gepaw chats create ...`               | ?                                        |
| `gepaw chats update <id> --name "..."` | ?                                        |
| `gepaw chats delete <id>`              |                                            |

**?*  `--agent-id`  `default`?

```bash
gepaw chats list                        # 
gepaw chats list --agent-id abc123      # 
gepaw chats list --user-id alice --channel dingtalk
gepaw chats get 823845fe-dd13-43c2-ab8b-d05870602fd8
gepaw chats create --session-id "discord:alice" --user-id alice --name "My Chat"
gepaw chats create --agent-id abc123 -f chat.json
gepaw chats update <chat_id> --name "?
gepaw chats delete <chat_id>
```

---

## ?

 gepaw PDF ?

### gepaw skills

|                        |                                |
| -------------------------- | ---------------------------------- |
| `gepaw skills install`   | ?URL ?       |
| `gepaw skills uninstall` | ?|
| `gepaw skills list`      | /?       |
| `gepaw skills config`    | ?? |
| `gepaw skills info`      |  workspace   |

**?*  `--agent-id`  `default`?

```bash
gepaw skills install https://skills.sh/owner/repo/skill  # 
gepaw skills install https://skills.sh/owner/repo/skill --agent-id abc123  # ?
gepaw skills uninstall skill-creator  # 
gepaw skills uninstall skill-creator --agent-id abc123  # ?
gepaw skills list                   # ?
gepaw skills list --agent-id abc123 # ?
gepaw skills config                 # 
gepaw skills config --agent-id abc123 # 
gepaw skills info [skill_name]               # ?
gepaw skills info [skill_name] --agent-id abc123 # ?
```

?????

>  [](./skills)?

---

## 

### gepaw clean

?`~/.gepaw`?

```bash
gepaw clean             # 
gepaw clean --yes       # ?
gepaw clean --dry-run   # 
```

---

## 

?

|             | ?     |                                         |
| --------------- | ----------- | ------------------------------------------- |
| `--host`        | `127.0.0.1` | API ?`gepaw app`  |
| `--port`        | `8088`      | API ?`gepaw app`  |
| `-h` / `--help` |             |                                     |

?

```bash
gepaw --host 0.0.0.0 --port 9090 cron list
```

## 

?`~/.gepaw`?

- ****: `config.json`?
- ****: `workspaces/{agent_id}/`?

```
~/.gepaw/
 config.json              # 
 workspaces/
     default/             # 
    ?   agent.json       # ?
    ?   chats.json       # 
    ?   jobs.json        # 
    ?   AGENTS.md        # 
    ?   memory/          # 
     abc123/              # 
         ...
```

|                   |              |
| --------------------- | ---------------- |
| `gepaw_WORKING_DIR` |  |
| `gepaw_CONFIG_FILE` |  |

 [](./config) ?[](./multi-agent)?

---

## 

|                 | ?                                                                              |     |
| ------------------- | ------------------------------------------------------------------------------------ | :---------------: |
| `gepaw init`      | ?                                                                                   |        ?        |
| `gepaw app`       | ?                                                                                   | ?|
| `gepaw desktop`   | ?                                                                                   | ?|
| `gepaw doctor`    | `fix`                                                                                |        ?        |
| `gepaw daemon`    | `status`  `restart`  `reload-config`  `version`  `logs`                          |        ?        |
| `gepaw models`    | `list`  `config`  `config-key`  `set-llm`  `download`  `local`  `remove-local` |        ?        |
| `gepaw env`       | `list`  `set`  `delete`                                                            |        ?        |
| `gepaw channels`  | `list`  `send`  `install`  `add`  `remove`  `config`                            |      **?*       |
| `gepaw agents`    | `list`  `create`  `delete`  `chat`                                                |    ?     |
| `gepaw cron`      | `list`  `get`  `state`  `create`  `delete`  `pause`  `resume`  `run`          |      **?*       |
| `gepaw chats`     | `list`  `get`  `create`  `update`  `delete`                                      |      **?*       |
| `gepaw skills`    | `install`  `uninstall`  `list`  `config`  `info`                                 |        ?        |
| `gepaw task`      | ?                                                                                   |        ?        |
| `gepaw auth`      | `reset-password`                                                                     |        ?        |
| `gepaw plugin`    | `install`  `list`  `info`  `uninstall`  `validate`                               |        ?        |
| `gepaw acp`       | ?                                                                                   |        ?        |
| `gepaw clean`     | ?                                                                                   |        ?        |
| `gepaw shutdown`  | ?                                                                                   |        ?        |
| `gepaw update`    | ?                                                                                   |        ?        |
| `gepaw uninstall` | ?                                                                                   |        ?        |

 `create` `list``delete``chat` ?

---

## 

- [](./intro) ?gepaw ?
- [](./console) ?Web 
- [](./channels) ?iMessageDiscordQQ 
- [](./heartbeat) ?/
- [](./skills) ??
- [](./config) ??config.json
- [](./multi-agent) ?
