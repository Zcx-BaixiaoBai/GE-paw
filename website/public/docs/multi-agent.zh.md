# 

gepaw ****?gepaw  AI ?

>  **v0.1.0** ?

**?*

1. **?* - 
2. **** - ?

---

## 

### ?

****?gepaw ?"

- **?*
- **?*
- **?*
- **?*?Discord?

?

---

## 

### ?



- ?*** - 
- ?*** - ?
- ?*** - ?

?

### ?

 gepaw?

- **** - 
- **Discord** - 
- **?* - 

?

### ?



- **?* - ?
- **?* - ?

---

## ?

### 

> ?*?*?

#### 1. 

 gepaw **?*****?

```
?
? ? [?] (1)    ?
?
```



- 
- 
-  ID

?

#### 2. 

** ??*?

1. "?
2. ?
   - ****?"?
   - ********?
   - **ID**"coder"?
3. ""

?

> ****?***"?Python/JavaScript ??

#### 3. 



- **** - ? ?"?
- **?* - ??????
- **** - ???"?
- **** - ???"?AGENTS.md ?SOUL.md

****?

#### 4. 

?* ??*?

- ""?PROFILE.md?
- ""

---

## 

### 

****?

****?

1. 

   - `work` - 
   - `personal` - 

2. ?`work` 

   - 
   - ?
   - AGENTS.md?

3. ?`personal` 
   -  Discord 
   - ?
   - ?

****?`work` ?Discord ?`personal` ?

### 

****?

****?

1. 

   - `coder` - 
   - `writer` - 
   - `planner` - 

2. ?

****?

### 

****?

****?

1. 

   - `zh-assistant` - language: "zh"?
   - `en-assistant` - language: "en"?

2. ?AGENTS.md ?SOUL.md ?

****?`zh-assistant`?`en-assistant`?

---

## 

### Q: 

**?*?

?

- ??
- ?
- ?

### Q: 

?

### Q: 

 LLM?

### Q: ?

 Discord ?

### Q: 

? ???

**** `~/.gepaw/workspaces/{agent_id}` ?

### Q: ?

`default` ?

### Q: 

****?

- API Key?
- TAVILY_API_KEY 

****?

- 
- ?
- 
- 
- 

---

## ?

?gepaw **v0.0.x** **v0.1.0** ****?

1. **?*

   - ?`default` 
   - 

2. ****

   -  gepaw ?
   - ??
   - ?

3. ****
   
   ```bash
   cp -r ~/.gepaw ~/.gepaw.backup
   ```

---

## ?

?

### 

**Multi-Agent Collaboration?* 

- ****
- **?*?
- ****?
- ?***?

### ?

#### 

1. ?
2. **???*
3.  **Multi-Agent Collaboration** ?
4. ?
5. ""

####  CLI 

```bash
# 
gepaw skills config

# 
gepaw skills config --agent-id abc123

# ?
# -  ???"multi_agent_collaboration"
# - ?
# - 
```

### ?

?

#### ?



**?*

```
?
```

?

1. ?"
2. ?
3. ?"?
4. ""
5. 

#### ?



**?*

```


?
1. []
2. []
3. []
4. []
5. []
```

### 

#### 

```
?

?
1. ?
2. 
3. ?
4. ?
```

#### 

```


?
1. 
2. ""
3. ""
4. ?
```

#### 

```
?

?
1. ???
2. 
3. 
4. 
```

### ?

- ****?
- **?*
- ****?
- **?*

### ?

?

#### 

 A ?B 

- ****name? 
- **ID**agent_id? ?
- ****description? ?
- **PROFILE.md**- ?

#### ?

**?*?

?****?

```
?Python/JavaScript 
```

```
?
```

```

```

?**?*?

```

```

```
?
```

```

```

**?*?

1. ?***""?"?
2. ?*?*"Python/JavaScript"???
3. ?***""?"?

#### PROFILE.md 

?*** `PROFILE.md` 

```
~/.gepaw/workspaces/{agent_id}/PROFILE.md
```

**??**?PROFILE.md?

#### ?

 CLI 

```bash
gepaw agents list

# ?
# Agent ID: code_reviewer
# Name: 
# Description: ?Python/JavaScript 
# Workspace: ~/.gepaw/workspaces/code_reviewer
# Profile: []
```

?**Description** ?**PROFILE.md** ?

### 

- ** skill**?"?
- **?*
- ** Profile**PROFILE.md 
- **?*
- **** API 
- ****?3-5 

---

## CLI ?API

>  API?

### ?CLI

?CLI ?

#### ?

```bash
gepaw agents list
```



- **Agent ID**
- **Name**
- **Description**?
- **Workspace**
- **Profile** `PROFILE.md` 

****?

```
Agent ID: code_reviewer
Name: 
Description: ?Python/JavaScript 
Workspace: ~/.gepaw/workspaces/code_reviewer
Profile: []

Agent ID: writer_bot
Name: 
Description: ?
Workspace: ~/.gepaw/workspaces/writer_bot
Profile: []
```

?**Description** ?**Profile** ?

#### 

```bash
# 
gepaw agents chat \
  --from-agent <current_agent> \
  --to-agent <target_agent> \
  --text ""

# ?
gepaw agents chat \
  --from-agent <current_agent> \
  --to-agent <target_agent> \
  --session-id "<session_id>" \
  --text ""

# ?
gepaw agents chat --background \
  --from-agent <current_agent> \
  --to-agent <target_agent> \
  --text ""
#  [TASK_ID: xxx] [SESSION: xxx]

# ?--to-agent 
gepaw agents chat --background \
  --task-id <task_id>
# submitted ?pending ?running ?finished
# finished completed failed?
```

****?

 `--background` ?`task_id`?

**?*?

- `submitted`?
- `pending`?
- `running`?
- `finished` `completed` ?`failed`?

**?*?

- ?
- 
- 
- API
- 

> ****?[CLI - ](./cli#??

### ?CLI

 CLI ?`--agent-id`  `default`

```bash
# 
gepaw channels list --agent-id abc123
gepaw cron list --agent-id abc123
gepaw skills list --agent-id abc123

# 
gepaw cron create \
  --agent-id abc123 \
  --type agent \
  --name "? \
  --cron "0 9 * * *" \
  --channel console \
  --target-user "user1" \
  --target-session "session1" \
  --text ""
```

** `--agent-id` ?*?

- `gepaw channels` - 
- `gepaw cron` - 
- `gepaw daemon` - ?
- `gepaw chats` - 
- `gepaw skills` - ?

**?`--agent-id` ?*

- `gepaw init` - ?
- `gepaw providers` - ?
- `gepaw models` - 
- `gepaw env` - 

### REST API

#### ?API

|                             |    |            |
| ------------------------------- | ------ | -------------- |
| `/api/agents`                   | GET    |  |
| `/api/agents`                   | POST   |    |
| `/api/agents/{agent_id}`        | GET    | ?|
| `/api/agents/{agent_id}`        | PUT    | ?|
| `/api/agents/{agent_id}`        | DELETE | ?    |
| `/api/agents/{agent_id}/active` | POST   |      |

#### ?API

?API ?`X-Agent-Id` HTTP 

```bash
# 
curl -H "X-Agent-Id: abc123" http://localhost:7860/api/chats

# 
curl -X POST http://localhost:7860/api/cron/jobs \
  -H "X-Agent-Id: abc123" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

 `X-Agent-Id` ?API ?

- `/api/chats/*` - 
- `/api/cron/*` - 
- `/api/config/*` - ?
- `/api/skills/*` - ?
- `/api/tools/*` - 
- `/api/mcp/*` - MCP ?
- `/api/agent/*` - 

### 



#### v0.0.x?

```
~/.gepaw/
 config.json          # ?
 chats.json
 jobs.json
 AGENTS.md
 ...
```

#### v0.1.0+?

```
~/.gepaw/
 config.json          # providers, agents.profiles?
 workspaces/
     default/         # 
    ?   agent.json   # ?
    ?   chats.json
    ?   jobs.json
    ?   AGENTS.md
    ?   ...
     abc123/          # ?
         ...
```

---

## ?

### ?

?****?-5 ?

?**?*?

?

### ?

?****?

- `default` - ?
- `work-assistant` - 
- `code-reviewer` - 

?**?*?

- `abc123` - 
- `test1`, `test2` - ?

### 



```bash
# ?
cp -r ~/.gepaw/workspaces/abc123 ~/backups/agent-abc123-$(date +%Y%m%d)

# 
cp -r ~/.gepaw/workspaces ~/backups/workspaces-$(date +%Y%m%d)
```

---

##  Agent spawn_subagent?

>  **v1.1.10** ?

?* workspace ?Agent** `chat_with_agent`gepaw **?*?

### 

|                          | ?                   | ?        |                          |
| ---------------------------- | ------------------------- | ------------------ | -------------------------------- |
| `chat_with_agent`            |  Agent  workspace |  text?   |  AgentQA?|
| `spawn_subagent(fork=False)` | ?Agent ?  |  session?| ?                  |
| `spawn_subagent(fork=True)`  |       |    |    |

### ?

- **Ephemeral?* Agent  session?
- ** Agent** Agent ?Agent personatools?session ?
- ****`fork=True` ?Coding Mode?

### fork=True ?

|                                        |                                                                                                 |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| ?Coding Mode + project_dir ?git  | ?`<project_dir>/.gepaw/worktrees/` ?**git worktree** Agent  worktree ?  |
| ?Coding Mode + workspace ?git  | ?`<workspace_dir>/.gepaw/worktrees/` ?**git worktree** Agent  worktree ?|
| ?git                         | ** fork**?parent                              |

`fork=True` **?*Git worktree  git ?

###  spawn_subagent?

** `spawn_subagent(fork=False)`?*?

- ?*?*
- ****

```
" src/core ?API ?
"?
""
```

** `spawn_subagent(fork=True)`**?

- ?*?*
- ?*?*?git ?
- **?*?

```
""
"?
"?
```

** `chat_with_agent` Agent?*?

- ?AgentQA Agent?Agent 

### 

#### 

```
?src/core 

Agent ?
spawn_subagent(task=" src/core ?)
?: [SESSION: sub-ab12]
         ...
```

#### ?

```
spawn_subagent(
    task="?,
    background=True,
)
?: [TASK_ID: task-cd34]
         [SESSION: sub-ef56]
         ?check_agent_task(task_id="task-cd34") 
```

#### fork=True + git  ??worktree

```
spawn_subagent(
    task="?parser ?,
    fork=True,
)
?[SESSION: sub-gh78]
   ?..
   [FORK_BRANCH: fork/ab12ef34]
   ?

#  ?worktree 
```

#### fork=True + ?git  ??

```
spawn_subagent(
    task=" API ",
    fork=True,
)
?[SESSION: sub-ij90]
   API ?..

# ?worktree  ??Agent 
```

### .worktreeinclude ?

?git worktree  `.gitignore` ?`.env`?

 `.worktreeinclude`  worktree 

```
# .worktreeinclude
.env
.env.local
config/local.json
```

gepaw ?worktree ?

> `.worktreeinclude`  git worktree ?

### 

**Qspawn_subagent ?chat_with_agent ?*



- `spawn_subagent`  Agent?session?
- `chat_with_agent`  Agent

**Qfork=True ?Coding Mode **

`fork=True` ?

- ?git ?Coding Mode ?project_dir  workspace worktree  + ?
-  git 

**Qworktree ?*

- **?* `[FORK_BRANCH]` ?`git worktree remove` 
- **?*?
- **?git ** worktree

**Qbackground=True  worktree ?*



```bash
git worktree list
git worktree remove .gepaw/worktrees/<id>
```

**Q Agent ?session **

 Agent  `chat_with_agent` ?`session_id`?

---

## 

- [CLI ](./cli) - ?
- [](./config) - 
- [](./console) - Web 
- [](./skills) - ?
