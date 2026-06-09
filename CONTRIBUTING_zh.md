# ?gepaw 

## ?

 gepaw gepaw ** AI **QQDiscordiMessage  **Skills** ?gepaw Skill bug?

**** [GitHub](https://github.com/agentscope-ai/gepaw)  [](https://gepaw.agentscope.io/)  [Apache 2.0](LICENSE)

---

## 

?

### 1. 



- **?[Open Issues](https://github.com/agentscope-ai/gepaw/issues)**  [Projects](https://github.com/agentscope-ai/gepaw/projects) ?
- ** issue** ?
- **?issue** issue ?

### 2. 

 [Conventional Commits](https://www.conventionalcommits.org/) ?

**?*
```
<type>(<scope>): <subject>
```

**?*
- `feat:` ?
- `fix:` Bug 
- `docs:` ?
- `style:` ?
- `refactor:`  bug ?
- `perf:` 
- `test:` ?
- `chore:` 

**?*
```bash
feat(channels): add Telegram channel stub
fix(skills): correct SKILL.md front matter parsing
docs(readme): update quick start for Docker
refactor(providers): simplify custom provider validation
test(agents): add tests for skill loading
```

### 3. Pull Request 

PR ?

**?* ` <type>(<scope>): <description> `

- `feat``fix``docs``test``refactor``chore``perf``style``build``revert`?
- **scope **?
- ?

**?*
```
feat(models): add custom provider for Azure OpenAI
fix(channels): handle empty content_parts in Discord
docs(skills): document Skills Hub import
```

### 4. ?

- **push/?PR **
  ```bash
  pip install -e ".[dev,full]"
  pre-commit install
  pre-commit run --all-files
  pytest
  ```
- ** pre-commit ** ?
  `pre-commit run --all-files`?
- **CI ?* pre-commit  PR not merge-ready?
- **** ?`console` ?`website` 
  ```bash
  cd console && npm run format
  cd website && npm run format
  ```
- **?* ?README?`website/public/docs/` ?

---

## 

gepaw ?***Skills ?

---

### ?/ ?

gepaw  DashScopeModelScope OllamaLM Studio?

?

1.  OpenAI `chat.completions` API ?Anthropic `messages` API?issue ?
2.  `/model/list` ?

?`src/gepaw/providers/provider_manager.py` ?Provider  `ProviderManager` ?gepaw ?

 PR 

1. ?PR ?
2. `website/public/docs/models.*.md`?
3. ?

---

### ?

?gepaw ?*QQDiscordiMessage**  gepaw ?IM ?

- **?* ?* payload ?`content_parts`** `TextContent``ImageContent``FileContent`agent ?`AgentRequest`?
- **?*  **`BaseChannel` ?* `src/gepaw/app/channels/base.py` ?
  - ?`channel`  `"telegram"`?
  - ?receive ?`content_parts` ?`process` ?send response?
  - ?manager ?
- **?* ?`src/gepaw/app/channels/registry.py` ?*?*?`custom_channels/telegram.py`  `custom_channels/telegram/`?`channel`  `BaseChannel` ?
- **CLI?* /?
  - `gepaw channels install <key>` ? `--path` / `--url` 
  - `gepaw channels add <key>` ?
  - `gepaw channels remove <key>` ??`custom_channels/` 
  - `gepaw channels config` ??

?***?Console ?CLI  `website/public/docs/channels.*.md` webhooks ?

---

###  Skills

**Skills** ?gepaw cronPDF/Office?*?* skills?

- **?*  skill ?***
  - **`SKILL.md`** ?agent ?Markdown ?YAML front matter  `name` ?`description` `metadata` Console?
  - **`references/`**?agent ?
  - **`scripts/`**?skill ?
- **?*  skills  `src/gepaw/agents/skills/<skill_name>/`  **customized_skills**?**active_skills** ?`SKILL.md` ?
- **?* ?***?skill ****?*** Skills ?

#### ?Skill Description

?model ?skill`description` **?*

**??*
```yaml
---
name: example_skill
description: "Use this skill whenever user wants to []. Trigger especially when user mentions: []. Also use when []."

# 
...
```

**?**
1. ****?"Use this skill whenever user wants to..." ?"Trigger when user asks for..."
2. **?* description 
   - "Trigger especially when user mentions: \"call\", \"dial\", \"phone\", \"microsip\""
   - "Also trigger for desktop automation tasks like opening apps, controlling windows"
3. ****
   - ??Make phone calls via MicroSIP or similar desktop apps"
   - ??Control desktop"
4. **** SKILL.md 

**??*
- ""?"?
-  model 
- 

** ?*

| ?|  | ?|
|------|---------------|-------------|
| Desktop Control | "" | "Use this skill whenever user wants to control desktop applications or make phone calls. Trigger especially when user mentions: \"call\" (), \"dial\" (), \"phone\" (), \"microsip\", or requests to use specific desktop apps." |
| File Reader | "" | "Use this skill when user asks to read or summarize local text-based files. PDFs, Office documents, and images are out of scope." |

- **Skills Hub?* gepaw ?hub ClawHub?skills skill  hub ?`SKILL.md` + `references/`/`scripts/` ?hub ?

 skills **cron**?*file_reader**?*news**?*pdf**?*docx**?*pptx**?*xlsx**?*browser_visible** skill  `agents/skills/` ?`website/public/docs/skills.*.md`  Skills ?

---

### WindowsLinuxmacOS 

gepaw ?**Windows**?*Linux** ?**macOS** ?

- **** shell / Windows  Linux ?macOS ?
- **** `install.sh``pip` ?`gepaw init` / `gepaw app` ?
- **?* ?
- **?*  README  Windows  WSLApple Silicon vs x86?

?PR ?issue?

---

### 

- **MCP** gepaw ?**MCP **?MCP  agent ?
- **?* ?[](https://gepaw.agentscope.io/)?`website/public/docs/` ?README ?
- **Bug **  issue?
- **** ??? + cron"??
- ****

---

## 

### ??

- ?
- ?issue ?
- ?
- ?
- ?PR ?
- ?

### ?

-  PR?
-  CI ?pre-commit ?
- ?PR ?
-  API?
-  issue ?

---

## 

- **?* [GitHub Discussions](https://github.com/agentscope-ai/gepaw/discussions)
- **Bug ** [GitHub Issues](https://github.com/agentscope-ai/gepaw/issues)
- **?* ?[README](README_zh.md) [Discord](https://discord.gg/eYMpfnkG8h)

 gepaw ?
