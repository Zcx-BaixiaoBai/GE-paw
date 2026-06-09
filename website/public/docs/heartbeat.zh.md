# 

 gepaw ?*?gepaw?gepaw ?*gepaw ?

**?*?**HEARTBEAT.md** ?**heartbeat** ?workspace  [](./console) ** ?**?

?[](./intro)?

---

## 

1. ?workspace ?***?**HEARTBEAT.md**?`gepaw_HEARTBEAT_FILE` ** gepaw ?*gepaw ?
2.  **`enabled` ?true** ?**every**?Cron???gepaw ?gepaw ?
3. **** ?**target** ?
   - **main**?gepaw?
   - **last** gepaw **?gepaw ?**?

?**active hours**?08:00?2:00?

---

## ?HEARTBEAT.md

**?*`<gepaw_WORKING_DIR>/workspaces/<agent_id>/HEARTBEAT.md`?
`<gepaw_WORKING_DIR>` ?`~/.gepaw` `gepaw_WORKING_DIR` `<agent_id>`  `default`?

?`HEARTBEAT.md` **`gepaw_HEARTBEAT_FILE`** ?workspace ?+ ?

?gepaw  Markdown QwenPaw ?



```markdown
# Heartbeat checklist

- ?
-  2h ?
- ?
- ?8h?check-in
```

?`gepaw init`?`--defaults` HEARTBEAT.md?

---

## 

![heartbeat](https://img.alicdn.com/imgextra/i2/O1CN0197MAPx2002prwqU5N_!!6000000006786-2-tps-3822-2070.png)

?console ?****agent.json?

**?*  **`workspaces/<agent_id>/agent.json`**  **`heartbeat`** ?
?**`config.json`** ?`agents.defaults.heartbeat`  `agent.json` **`agent.json` **?

|             |                                                                                                                                                                                                                   |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **enabled**     | ?* false** **true** ?                                                                                                                                                     |
| **every**       | ?`"30m"``"1h"``"2h30m"``"90s"`**?* ?** Cron** ??? 9:00`"0 9 * * *"`?Cron ?|
| **target**      | **main** ?*last**  `last_dispatch` **inbox** ?                                                                                                                  |
| **activeHours** | `{ "start": "08:00", "end": "22:00" }`?                                                                                                                                                 |

`every`  **6 **?

 gepaw 30 ?**`agent.json`** 

```json
{
  "heartbeat": {
    "enabled": true,
    "every": "30m",
    "target": "main"
  }
}
```

 1  08:00?2:00 ?

```json
{
  "heartbeat": {
    "enabled": true,
    "every": "1h",
    "target": "last",
    "activeHours": { "start": "08:00", "end": "22:00" }
  }
}
```

 config.json?

---

## 

|          |                        |  (cron)              |
| -------- | -------------------------- | ---------------------------- |
| **** | HEARTBEAT.md?  |                  |
| **** |                |              |
| **?* |  | ?      |
| **** | /        |  |

> ?9  2 ?[](./cron) [CLI](./cli) ?`gepaw cron create`?

---

## 

- [](./intro) ??
- [](./console) ?Web 
- [](./channels) ?target=last ?
- [](./cron) ?
- [CLI](./cli) ?init cron 
- [](./config) ?config.jsonagent.json ?
