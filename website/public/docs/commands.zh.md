# 

 `/` ?*?* AI ?

---

## 

?

|        | ?|       |     |              |
| ---------- | -------- | ------------- | ----------- | -------------------- |
| `/compact` | ??   |  ?| ? | ? + ?|
| `/new`     | ??   | ?       | ? | ??   |
| `/clear`   | ??   | ?       | ??  | ?      |

---

### /compact - 

**?*?

```
/compact
```



```
/compact 
```

**?*

```
**Compact Complete!**

- Messages compacted: 12
**Compressed Summary:**
?..
- Summary task started in background
```

>  `/compact` ?*?*?
>  ?`/compact`?

---

### /new - 

**?*?

```
/new
```

**?*

```
**New Conversation Started!**

- Summary task started in background
- Ready for new conversation
```

---

### /clear - 

**?*?***?

```
/clear
```

**?*

```
**History Cleared!**

- Compressed summary reset
- Memory is now empty
```

>  ****`/clear` ?*?*?`/new` ?

---

## 

?

|                 |                  |
| ------------------- | ------------------------ |
| `/history`          |   + Token  |
| `/message`          |            |
| `/compact_str`      |            |
| `/summarize_status` |  ?         |
| `/dump_history`     |        |
| `/load_history`     | ?          |

---

### /history - 

?*?*?

```
/history
```

**?*

```
**Conversation History**

- Total messages: 3
- Estimated tokens: 1256
- Max input length: 128000
- Context usage: 0.98%
- Compressed summary tokens: 128

[1] **user** (text_tokens=42)
    content: [text(tokens=42)]
    preview: ?Python ...

[2] **assistant** (text_tokens=256)
    content: [text(tokens=256)]
    preview: ?..

[3] **user** (text_tokens=28)
    content: [text(tokens=28)]
    preview: 

---

- Use /message <index> to view full message content
- Use /compact_str to view full compact summary
```

>  **** `/history` ?
>
> ?`Context usage`  75%  `compact`?
>
> ?`/history` ?`/compact` ?`/new` ?
>
> Token [ReMeInMemoryMemory ](https://github.com/agentscope-ai/ReMe/blob/v0.3.0.6b2/reme/memory/file_based/reme_in_memory_memory.py#L122)?

---

### /message - 

?

```
/message <index>
```

**?*

- `index` - ?1 

**?*

```
/message 1
```

**?*

```
**Message 1/3**

- **Timestamp:** 2024-01-15 10:30:00
- **Name:** user
- **Role:** user
- **Content:**
?Python ?
```

---

### /compact_str - 

?

```
/compact_str
```

**?*

```
**Compressed Summary**

?..
```

**?*

```
**No Compressed Summary**

- No summary has been generated yet
- Use /compact or wait for auto-compaction
```

---

### /summarize_status - ?

 ID?

```
/summarize_status
```

**?*

```
**Summary Task Status**

- **task-001**
  - Start: 2024-01-15 10:30:00
  - Status: completed
  - Result: ...
- **task-002**
  - Start: 2024-01-15 10:35:00
  - Status: failed
  - Error: Summary generation timeout
```

>   `/compact` ?`/new` ?

---

### /dump_history - 

 JSONL ?

```
/dump_history
```

**?*

```
**History Dumped!**

- Messages saved: 15
- Has summary: True
- File: `/path/to/workspace/debug_history.jsonl`
```

>  ****?`/load_history` ?

---

### /load_history - 

?JSONL ****?

```
/load_history
```

**?*

```
**History Loaded!**

- Messages loaded: 15
- Has summary: True
- File: `/path/to/workspace/debug_history.jsonl`
- Memory cleared before loading
```

**?*

-  `debug_history.jsonl` 
- 10000 ?
- ?
- ****?

>  ****`/load_history` 

---

## Skill 

?skill ?Agent 
skill?

- `/skills` ?skill?
- `/<skill_name>`  skill  description ?
  path?
- `/<skill_name> <input>`  Agent  `skill_name`?input
  ?
- `/[skill_name]` ?

?

- `skill_name` ?`/skills` ?
-  skill ?

---

## 

?AI  Agent ?

|                              |                    |  |
| -------------------------------- | ---------------------- | ---- |
| `/model`                         | ?    | ?  |
| `/model -h` ?`/model help`     |            | ?  |
| `/model list`                    | ?      | ?  |
| `/model <provider>:<model>`      | ?        | ?  |
| `/model reset`                   |      | ?  |
| `/model info <provider>:<model>` | ?| ?  |

---

### `/model` - 

 Agent ?

**?*

```
/model
```

**?*

```
**Current Model**

Provider: `openai`
Model: `gpt-4o` ?

Use `/model list` to see all available models.
```

---

### `/model -h` ?`/model help` - 

?`/model` ?

**?*

```
/model -h
/model --help
/model help
```

**?*

```
**Model Management Commands**

Manage and switch AI models for the current agent.

**Available Commands:**

`/model` - Show current active model
`/model list` - List all available models
`/model <provider>:<model>` - Switch to specified model
`/model reset` - Reset to global default model
`/model info <provider>:<model>` - Show model information
`/model help` or `/model -h` - Show this help message

**Examples:**

`/model` - Show current model
`/model list` - List all models
`/model openai:gpt-4o` - Switch to GPT-4o
`/model reset` - Reset to global default
`/model info openai:gpt-4o` - Show GPT-4o information

**Capability Indicators:**

?- Supports image input
 - Supports video input
```

---

### `/model list` - ?

?Provider  **[ACTIVE]**?

**?*

```
/model list
```

**?*

```
**Available Models**

**OpenAI** (`openai`)
  - `gpt-4o` ?**[ACTIVE]**
  - `gpt-4o-mini` ?
  - `gpt-3.5-turbo`
  - `my-custom-model` *(user-added)*

**Anthropic** (`anthropic`)
  - `claude-3-5-sonnet-20241022`
  - `claude-3-opus-20240229`

**Google** (`gemini`)
  - `gemini-2.0-flash-exp` ?

---
Total: 3 provider(s), 8 model(s)

Use `/model <provider>:<model>` to switch models.
Example: `/model openai:gpt-4o`
```

**?*

- ?- 
-  - 
- _(user-added)_ -  `gepaw models add-model` ?

---

### `/model <provider>:<model>` - 

?Agent ?

**?*

```
/model <provider>:<model>
```

**?*

```
/model openai:gpt-4o
/model anthropic:claude-3-5-sonnet-20241022
/model gemini:gemini-2.0-flash-exp
```

**?*

```
**Model Switched**

Provider: `anthropic`
Model: `claude-3-5-sonnet-20241022`

The new model will be used for subsequent messages.
```

>  **** Agent?Agent ?

---

### `/model reset` - 

?Agent ?Web UI ?

**?*

```
/model reset
```

**?*

```
**Model Reset**

Agent model has been reset to global default:

Provider: `openai`
Model: `gpt-4o`

The global default model will be used for subsequent messages.
```

>  **** Agent ?

---

### `/model info` - 

?

**?*

```
/model info <provider>:<model>
```

**?*

```
/model info openai:gpt-4o
/model info anthropic:claude-3-5-sonnet-20241022
```

**?*

```
**Model Information**

**Provider:** `openai` (OpenAI)
**Model ID:** `gpt-4o`
**Model Name:** GPT-4o
**Capabilities:** ?Image,  Multimodal
**Probe Source:** documentation

**Status:** ?Currently active

---
Use `/model openai:gpt-4o` to switch to this model.
```

---

## 

?gepaw  Agent ?

?`/daemon <?` ?`/status`?`gepaw daemon <?`?

|                                 |                                                                          |  |  |
| ----------------------------------- | ---------------------------------------------------------------------------- | ---- | ---- |
| `/stop`                             |                                                  | ?  | ?  |
| `/stop session=<session_id>`        | ?                                                          | ?  | ?  |
| `/daemon status` ?`/status`       |                                      | ?  | ?  |
| `/daemon restart` ?`/restart`     |                                          | ?  | ?  |
| `/daemon reload-config`             | ?                                                      | ?  | ?  |
| `/daemon version`                   |                                                    | ?  | ?  |
| `/daemon logs` ?`/daemon logs 50` | ?N  100 ?2000 ?`gepaw.log`?| ?  | ?  |
| `/approval approve [request_id]`    | ?ID                                        | ?  | ?  |
| `/approval deny [request_id]`       |                                                  | ?  | ?  |
| `/approval list`                    |                                                            | ?  | ?  |
| `/approval cancel <request_id>`     |                                                              | ?  | ?  |
| `/approve`                          | `/approval approve` ?                                              | ?  | ?  |
| `/deny`                             | `/approval deny` ?                                                 | ?  | ?  |

---

### `/stop` - 

?

**?*

```
/stop                       # ?
/stop session=<session_id>  # ?
```

>  ****`/stop` ?

---

### `/daemon status` ?`/status` - ?

?

**?*

```
/status                    # 
gepaw daemon status        # ?
```

---

### `/daemon restart` ?`/restart` - ?

 channelscronMCP MCP ?

**?*

```
/restart                   # 
gepaw daemon restart       # 
```

>  **** MCP  `/daemon reload-config`  `/daemon restart` ?

---

### `/daemon reload-config` - 

channelscronMCP?

**?*

```
/daemon reload-config           # 
gepaw daemon reload-config      # ?
```

---

### `/daemon version` - 

 gepaw ?

**?*

```
/daemon version            # 
gepaw daemon version       # ?
```

---

### `/daemon logs` - 

?`gepaw.log` ?N ?100 ?2000 ?

**?*

```
/daemon logs               #  100 ?
/daemon logs 50            #  50 ?
gepaw daemon logs -n 200   # ?200 ?
```

>  ****?512KB ?

---

### `/approval` - 

 `approval_level`  `STRICT` ?`SMART`  CRITICAL ?HIGH ?

**?*

```
/approval approve [request_id]           # ?
/approval deny [request_id] [reason]     # 
/approval list                           # ?
/approval list --all                     # 
/approval cancel <request_id>            # 
```

**?*

```
/approve                                 # ?/approval approve
/approve <request_id>                    # ?/approval approve <request_id>
/deny                                    # ?/approval deny
/deny <request_id> <reason>              # ?/approval deny <request_id> <reason>
```

> `/approval list` ?`--all` ?`-a` ?Agent ?

---

### 

?daemon ?`/stop` ?`/approval` ?

```bash
gepaw daemon status
gepaw daemon restart
gepaw daemon reload-config
gepaw daemon version
gepaw daemon logs -n 50
```

**?*  `--agent-id`  `default`?

```bash
gepaw daemon status --agent-id abc123
gepaw daemon version --agent-id abc123
```

---

## Mission Mode - 

Mission Mode ?*?* [Claude Code](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) ?[Ralph Loop](https://github.com/snarktank/ralph)user stories **master agent ?worker agents ?verifier agents** ?

### ?

-  **?*Phase 1  PRDPhase 2 
-  **?*Master agent ?worker
- ?****?story  verifier agent ?
-  ****?story ?story ?
-  ****?agent ?

### 

**? Mission Mode **

- ?
- 
- 
- 

**? Mission Mode **

- ?bug?
- ?
- ???

### 

####  Mission

```bash
/mission <>
```

**?*

```
/mission  TODO ?Python JSON 
```

****

- `--max-iterations N`:  Phase 2  1-100?20?
- `--verify <command>`: ?`pytest`?

```
/mission  Web API --max-iterations 30 --verify "pytest tests/"
```

#### Phase 1: PRD 

Agent 

1. 
2. 
3.  `prd.json` ?story ?

**PRD ?*

```json
{
  "project": "todo-cli-app",
  "description": "?TODO ",
  "userStories": [
    {
      "id": "US-001",
      "title": "",
      "description": "As a user, I want to add new tasks...",
      "acceptanceCriteria": [
        " 'todo add <task>' ?,
        "?todos.json "
      ],
      "priority": 1,
      "passes": false
    }
  ]
}
```

#### Phase 2: ?

** PRD?*

 PRD ?Phase 2?

```
?
```

****

```
 US-001 ?story?
```

Agent ?PRD?

**Phase 2 ?*

1. **Master **?worker agent  story
2. **Worker **??
3. **Verifier **?agent ?
4. ** PRD**?story  `passes: true`
5. ****?story ?

#### 

```bash
/mission status
```

**?*

```
**Mission Status** ?mission-20260415-123456
- Session: e2e-abc123
- Phase: execution
- Project: todo-cli-app
- Progress: 2/4 stories passed
- Loop dir: ~/.copaw/workspaces/default/missions/mission-20260415-123456

  ?US-001: 
  ?US-002: 
  ?US-003: 
  ?US-004: 
```

#### ?Mission

```bash
/mission list
```

### 

 mission ?`~/.copaw/workspaces/default/missions/mission-<timestamp>/` 

```
mission-20260415-123456/
 prd.json              # ?
 loop_config.json      # ?
 task.md               # 
 progress.txt          # Codebase Patterns?
 <?
```

### 

1. **Session **?session ?mission ?
2. **PRD **Phase 2  PRD ?schema
3. ****Phase 2 master agent **** `edit_file``browser_use`  worker 
4. ****?`--max-iterations` 
5. **Git ** Git agent ?commit 
6. ** **?
   - **Worker ?verifier agents ?* `--background` ?
   -  session  `/approve` 
   - Master agent 
   - ****?worker  `missions/<mission-xxx>/` ** Mission Mode**
   - ?shell 

### 

#### ?

```
/mission  --verify "npm test"
```

?`npm test` ?

#### 

```
/mission  --max-iterations 50
```

#### ?

Phase 2  master agent ?

```
US-003 
```

### 

**PRD ?*

```
 ** Phase 2**: prd.json :
  - Missing required field: userStories

?PRD ?
```

****?`prd.json`?`userStories` ?story ?

**?*

```
 **Mission reached max iterations** (20). 2/4 stories passed.
```

****?

1.  `/mission status`  story
2.  `--max-iterations` 
3. ?

### 

|              |            | Agent           |         |
| ---------------- | ------------------ | ------------------- | --------------- |
| **?*     | ?| ?agent    | ?   |
| **Mission Mode** | ?    | Master  workers | Master  |

---

## Plan Mode - 

 [](./plan)?

|                |                                         |  |
| ------------------ | ------------------------------------------- | ---- |
| `/plan`            | / | ?  |
| `/plan <>` | ?           | ?  |

---

## Proactive Mode - 

Proactive Mode AI ?

### ?

-  **?*
-  **?*?
-  ****?
-  ****

### 

****

- ****AgentAgent ?
- **?*Agent?
- 

### 

#### 

```bash
/proactive
/proactive on
/proactive <?
```

**?*

```bash
/proactive      # 30
/proactive on   # ?0
/proactive 60   # 60?
```

#### 

```bash
/proactive off
```

### 

1. ****
2. ****
3. ****?
4. ****
5. ****?

#### ?

- ?
- 
- 

### 

1. **?*?
2. ****?
3. ****AI

### 

- ?
- 

---
