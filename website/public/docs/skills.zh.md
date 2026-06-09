# Skills

**Skills** Skills Hub 
?

 Skill 

- **** ?[](./console) ?**???* ?
- **?* ?`$gepaw_WORKING_DIR`?`~/.gepaw`
   `$gepaw_WORKING_DIR/skill_pool/` ?
  `$gepaw_WORKING_DIR/workspaces/{agent_id}/skills/`?

>  [](./intro)?

?

---

## ?

gepaw ?skills ?

- **?*  `$gepaw_WORKING_DIR/skill_pool/`
  ?`~/.gepaw/skill_pool/`?
- **** ?
  `$gepaw_WORKING_DIR/workspaces/{agent_id}/skills/`
  ?`~/.gepaw/workspaces/{agent_id}/skills/`?

```
$gepaw_WORKING_DIR/                      #  ~/.gepaw
  skill_pool/                # ?
    skill.json               # ?
    pdf/
      SKILL.md
    cron/
      SKILL.md
    my_shared_skill/
      SKILL.md
  workspaces/
    default/
      skill.json             # ?
      skills/                # 
        pdf/
          SKILL.md
        my_skill/
          SKILL.md
```

![](https://img.alicdn.com/imgextra/i3/O1CN01BY2oPh1KqykMev8jC_!!6000000001216-2-tps-1919-1080.png)

### 

 **** ?
?



- **?* ?
- ****  URL ?ZIP?
  ?
- ** / ?* ?skill 
  
   builtin?builtin ?
- **?* 
  gepaw ?/ API 
  ?

?

1. **?*?
    Skill ?ID ?

   | Skill ID                      |                                                                                                |                                                            |
   | ----------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
   | **browser_cdp**               | ?Chrome ?CDP / ?CDP ?      |                                                            |
   | **browser_visible**           | headed?                    |                                                            |
   | **channel_message**           |  session / channel ?                                 |                                                            |
   | **QA_source_index**           | gepaw ?                      |                                                            |
   | **cron**                      |  `gepaw cron` ?          |                                                            |
   | **dingtalk_channel**          | ?                              |                                                            |
   | **docx**                      | Word ?docx?                | https://github.com/anthropics/skills/tree/main/skills/docx     |
   | **file_reader**               |  .txt?md?json?csv?log?py PDF ?Office ?Skill ?|                                                            |
   | **guidance**                  |  gepaw ?                                                     |                                                            |
   | **himalaya**                  |  CLI IMAP/SMTP?`himalaya` ?                      | https://github.com/openclaw/openclaw/tree/main/skills/himalaya |
   | **multi_agent_collaboration** | ?agent ?agent ?            |                                                            |
   | **news**                      | ?        |                                                            |
   | **pdf**                       | PDF ???OCR ?         | https://github.com/anthropics/skills/tree/main/skills/pdf      |
   | **pptx**                      | PPT?pptx?                                      | https://github.com/anthropics/skills/tree/main/skills/pptx     |
   | **xlsx**                      | ?xlsx?xlsm?csv?tsv?                | https://github.com/anthropics/skills/tree/main/skills/xlsx     |

   ?**?* / **?* ?
   ?**?* 
   ?

   ?**Cron**  [CLI](./cli) ?
   `gepaw cron`  ** ?** ?

   - `gepaw cron create --type agent --name "xxx" --cron "0 9 * * *" ...`
   - `gepaw cron list`
   - `gepaw cron state <job_id>`

2. **?*?
   ?skill?

3. **?URL ?*?
   ?Hub / GitHub URL ?

4. ** ZIP ?*?
    skill ?

5. **?*?
   ?**???*  ****?

6. **?*?
    `$gepaw_WORKING_DIR/skill_pool/` **?*
   ?

### ?

?`skills/` ?Agent
?skill?

---

## Workspace 



### 1. 

?

1.  **** ?
2. ?skill  ****?
3. ?
4. skill ?***?

 skill?

### 2. 

?[](./console) ?**???* ?
 `skills/` ?`skill.json`?***?

 skill  **AI **?
**Beta**?skill **?*?
?skill ?

### 3.  ZIP 

 ZIP ?
 skill ****?

### 4.  URL 

?URL ?

- `https://skills.sh/...`
- `https://clawhub.ai/...`
- `https://skillsmp.com/...`
- `https://lobehub.com/...`
- `https://market.lobehub.com/...`LobeHub ?
- `https://github.com/...`
- `https://modelscope.cn/skills/...`

CLI ?URL 

**** ?`--agent-id``install` / `uninstall` ?

```bash
gepaw skills install <skill_url>
gepaw skills install <skill_url> --agent-id <agent_id>
```

CLI 

```bash
gepaw skills uninstall <skill_name>
gepaw skills uninstall <skill_name> --agent-id <agent_id>
```

#### 

1.  [](./console) ?**???*?**?Skills Hub ?*?

   ![import](https://img.alicdn.com/imgextra/i2/O1CN01iaEhjy1hOnXfVjZaK_!!6000000004268-2-tps-3822-2070.png)

2.  Skill URL **URL **?

   ![url](https://img.alicdn.com/imgextra/i2/O1CN01l47mhN1aKwu48KLry_!!6000000003312-2-tps-3822-2070.png)

3. **?Skills Hub ?*?

   ![click](https://img.alicdn.com/imgextra/i4/O1CN01amjZHZ1lwT7eVqWx9_!!6000000004883-2-tps-3822-2070.png)

4. skill ?***?

   ![new](https://img.alicdn.com/imgextra/i4/O1CN01TOYn2U1RFbk5BQOR1_!!6000000002082-2-tps-3822-2070.png)

#### URL 

1. ?`skills.sh` `clawhub.ai``skillsmp.com`?
   `lobehub.com``modelscope.cn` ?
2.  Skill `find-skills` ?

   ![find](https://img.alicdn.com/imgextra/i4/O1CN015bgbAR1ph8JbtTsIY_!!6000000005391-2-tps-3410-2064.png)

3. ?URL?Skill  Skill URL?

   ![url](https://img.alicdn.com/imgextra/i2/O1CN01d1l5kO1wgrODXukNV_!!6000000006338-2-tps-3410-2064.png)

   LobeHub ?`https://market.lobehub.com/...` ?
   ?

4. ?GitHub  Skills?`SKILL.md` ?anthropics
   skills  `skill-creator` ?URL ?

   ![github](https://img.alicdn.com/imgextra/i2/O1CN0117GbZa1lLN24GNpqI_!!6000000004802-2-tps-3410-2064.png)

#### 

- ?Skill ?
- URL ?
  ?GitHub ?? ??`GITHUB_TOKEN`?
  ?GitHub ?
  [PAT](https://docs.github.com/zh/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)?

### 5. 

 `$gepaw_WORKING_DIR/workspaces/{agent_id}/skills/` ?skill 
gepaw ?

 skill 
?skill ?

?`$gepaw_WORKING_DIR/workspaces/{agent_id}/skills/` ?`SKILL.md`?
`SKILL.md` ?`name` ?`description` ?YAML front matter Skill
?`metadata.requires` gepaw ?
`require_bins` ?`require_envs` ?Skill?

#### SKILL.md 

```markdown
---
name: my_skill
description: ?
metadata:
  requires:
    bins: [ffmpeg]
    env: [MY_SKILL_API_KEY]
---

# 

?Skill ?
```

`name` ?`description` ?***`metadata` ?

?Skill ?***?`skill.json`?
?CLI ?

### 6.  /make-skill ?(Beta)

, ?
 skill?

```
/make-skill 
```

 skill ?
Agent  skill 
workspace?***?

`<focus>` ?skill ?`-`?
`view image debug` ?`view-image-debug`?
?

`/make-skill` ?skill?`/skills` ?
?

---



- ** / ?*  skill ?
- **?* ?skill?skill ?
- **?*  skill ?
- ** / config?*  skill 
  ?

---

## ?

 skill ??** ??*?
"?URL "?



- **ClawHub** ??
- **ModelScope** ??
- **Aliyun** ??** ?** ?tooltip ?

?

- ?banner ?
  ?
- ?***?**?*?Agent?
- ?

 skill `installed_from` ?**** ?`clawhub``modelscope`?
`aliyun``skills-sh``lobehub``skillsmp``github``url``zip` skilllegacy ?

skills.shlobehub.comgithub.com ?
??URL "?

---

## 

 Skill Skill ?*?*
`channels: ["all"]`?

?Skill 

1. ?**???* ?
2.  `discord``telegram``console`?

Agent ?`channels` ?`"all"`?
?
Discord ?

---

## Skill Config ?

 Skill ?manifest ?`config` ?config ?
 Skill ?workspace gepaw  Agent
Skill ?

 **???*  config
API ?

### 

config  SKILL.md `metadata.requires.env` ?key ?
 `requires.env`  key  JSON ?
 config  key?

 config ?`gepaw_SKILL_CONFIG_<SKILL_NAME>`JSON ?
 `requires.env` ?

?

### 

?`SKILL.md` 

```markdown
---
name: my_skill
description: demo
metadata:
  requires:
    env: [MY_API_KEY, BASE_URL]
---
```

config 

```json
{
  "MY_API_KEY": "sk-demo",
  "BASE_URL": "https://api.example.com",
  "timeout": 30
}
```



- `MY_API_KEY`  config `requires.env`?
- `BASE_URL`  config `requires.env`?
- `timeout`  `requires.env`  JSON ?
- `gepaw_SKILL_CONFIG_MY_SKILL`  JSON ?

Python ?

```python
import json
import os

api_key = os.environ.get("MY_API_KEY", "")
base_url = os.environ.get("BASE_URL", "")
cfg = json.loads(os.environ.get("gepaw_SKILL_CONFIG_MY_SKILL", "{}"))
timeout = cfg.get("timeout", 30)
```

Config ?config ?
?config ?

### ?

Skill ?

1. **?* ?
2. **** ?manifest `skill.json`?`config` ?
   ?Agent ?
3. **** ?`config` ?
   ?

 `requires` `metadata.openclaw.requires` ?`metadata.gepaw.requires` ?`metadata.requires`?

---

## 

?`active_skills/` ?`customized_skills/` 
`skills/` ?

**** `active_skills/` ?
`customized_skills/`  skill 
 skill?
?* `active_skills/` ?`customized_skills/`  skill ?*

| ?              | ?                                                          |
| -------------------- | ---------------------------------------------------------------- |
| `active_skills/`     | ?`skills/`?                                      |
| `customized_skills/` | ?`skills/` active  |

****
`-active` / `-customize` ?
?

---

## 

- [](./intro) ??
- [](./console) ? Skills ?
- [](./channels) ?iMessageDiscordQQ
- [](./heartbeat) ?/
- [CLI](./cli) ?
- [](./config) ??config
