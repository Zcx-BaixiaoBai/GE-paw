# Heartbeat

In gepaw, **heartbeat** means: on a fixed interval, ask gepaw the
questions?you wrote in a file, and optionally send the gepaws reply to
**the channel where you last chatted**. Good for regular check-ins, daily
digests, scheduled reminders??gepaw runs without you sending a
message.

With **multiple agents**, each agent has its own **HEARTBEAT.md** and
**heartbeat** settings under that agents workspace. You can also turn heartbeat
on or off and change the interval in the [Console](./console) (**Control ?
Heartbeat**).

If you havent read [Introduction](./intro), skim the short notes there on
heartbeat and channels.

---

## How heartbeat works

1. In the current agents workspace there is a **heartbeat query file** (default
   name **HEARTBEAT.md**; rename with env **`gepaw_HEARTBEAT_FILE`**). Its
   content is **what to ask gepaw on each run** (one or more paragraphs; gepaw
   treats it as one user message).
2. When **`enabled` is true** in config, the system runs on your **every**
   value (**interval string** or **five-field cron**): read that file ?send as
   the user message ?gepaw replies.
3. **Whether the reply goes to a channel** is set by **target**:
   - **main** ?Run gepaw only; dont send the reply to any channel (e.g. local
     self-check, logs).
   - **last** ?Send the reply to the **channel/session where you last talked
     to gepaw** (e.g. if you last used DingTalk, the heartbeat reply goes to
     DingTalk).

You can also set **active hours**: heartbeat only runs in that daily window
(e.g. 08:00?2:00).

---

## Step 1: Write HEARTBEAT.md

**Path (multi-agent, usual case):**
`<gepaw_WORKING_DIR>/workspaces/<agent_id>/HEARTBEAT.md`.
Default `gepaw_WORKING_DIR` is `~/.gepaw` (override with **`gepaw_WORKING_DIR`**);
`<agent_id>` is the current agent id (e.g. `default`).

The default filename is `HEARTBEAT.md`; use **`gepaw_HEARTBEAT_FILE`** to change
it. The full path is always **that agents workspace root + that filename**.

The file is simply what to ask each time.?Plain text or Markdown; the whole
thing is one user message.

Example (customize as you like):

```markdown
# Heartbeat checklist

- Scan inbox for urgent email
- Check calendar for next 2h
- Review stuck todos
- Light check-in if quiet for 8h
```

If you ran `gepaw init` without `--defaults`, you may be prompted to edit
HEARTBEAT.md; choosing yes opens it in your default editor. You can edit the
file anytime; after save, the **next** heartbeat uses the new content.

---

## Step 2: Configure heartbeat

![heartbeat](https://img.alicdn.com/imgextra/i2/O1CN01yJmAht1oFMh9j9osZ_!!6000000005195-2-tps-3822-2070.png)

Prefer configuring on the Console **Heartbeat** page. To edit **`agent.json`**
instead, use the following.

**Interval, on/off, target, and active hours** are read from **`heartbeat`** in
the current agents **`workspaces/<agent_id>/agent.json`** (same as what the
Console saves). After migration from older layouts, legacy
**`agents.defaults.heartbeat`** in root **`config.json`** may have been merged
into the default agents **`agent.json`** ?treat **`agent.json`** as the
source of truth for new changes.

| Field           | Meaning                                                                                                                                                                                                                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **enabled**     | Heartbeat on/off. **Default false**; the schedule runs only when **true**.                                                                                                                                                                                                |
| **every**       | How often: an interval string (`"30m"`, `"1h"`, `"2h30m"`, `"90s"`) **or** a space-separated **five-field cron** (minute hour day month weekday ?same shape as cron jobs, e.g. daily 09:00: `"0 9 * * *"`). Cron is interpreted in the **process schedulers timezone**. |
| **target**      | **main** ?dont send to a channel; **last** ?send using **`last_dispatch`** for that agent; **inbox** ?send to Inbox.                                                                                                                                                  |
| **activeHours** | Optional daily window: `{ "start": "08:00", "end": "22:00" }`.                                                                                                                                                                                                            |

If **every** is omitted, the built-in default applies (currently about **6
hours** ?confirm in your installed version).

Example (heartbeat on, gepaw only, no channel, every 30m) ?in that agents
**`agent.json`**:

```json
{
  "heartbeat": {
    "enabled": true,
    "every": "30m",
    "target": "main"
  }
}
```

Example (send to last conversation channel, every 1h, only 08:00?2:00):

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

After changes, save **config.json**; if the service is running, settings apply
as implemented (some setups may need a restart ?see what you actually run).

---

## Heartbeat vs cron jobs

|              | Heartbeat                     | Cron jobs                       |
| ------------ | ----------------------------- | ------------------------------- |
| **Count**    | One file (HEARTBEAT.md)       | Many jobs                       |
| **Schedule** | One global interval           | Each job has its own schedule   |
| **Delivery** | Optional last channel or none | Each job sets channel and user  |
| **Best for** | One fixed checklist / digest  | Many tasks, times, and contents |

> Want good morning at 9?or every 2h ask todos and send to DingTalk?style
> multi-task automation? Use [Scheduled Tasks](./cron) (or
> [CLI](./cli) `gepaw cron create`) instead of heartbeat.

---

## Related pages

- [Introduction](./intro) ?What the project can do
- [Console](./console) ?Turn heartbeat on/off and change interval in the web UI
- [Channels](./channels) ?Connect channels first so target=last has somewhere to send
- [Scheduled Tasks](./cron) ?Manage multiple independent scheduled jobs
- [CLI](./cli) ?Heartbeat at init, cron jobs
- [Config & working dir](./config) ?config.json, agent.json, working directory
