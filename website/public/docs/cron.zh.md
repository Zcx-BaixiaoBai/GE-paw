# 

?gepaw cron job?

- ?25 ?
- ?9:30 ?

?[](./heartbeat) ?***?

---

##  vs 



- ****?15  2 ?9:00?
- **** 2026 ?1 ?1 ?9:00?

 Cron ?

?

![todo](https://img.alicdn.com/imgextra/i1/O1CN01KOSlHG1EBP6mzmTpr_!!6000000000313-2-tps-1734-936.png)

?

![todo](https://img.alicdn.com/imgextra/i3/O1CN01AJU7UV1G0zKh4JqRO_!!6000000000561-2-tps-1728-1266.png)

 **?/**?

## 

****

> ?[FAQ](https://gepaw.agentscope.io/docs/faq) ?**** 

1.  **** ?

![todo](https://img.alicdn.com/imgextra/i2/O1CN01bJJo2e1LoydlqxGxu_!!6000000001347-2-tps-1190-1984.png)

2. ?
   - **** ??
   - **** ??
   - ****
     -  ****?**Cron ?* `0 9 * * *` =  9:00?
     -  ****?
       - ?**** ?
       -  ****  ****?
         -  ****?
         -  **?* ****?
         -  **** ****??
   - **?*
     -  **text**?***
     - **agent**?***QwenPawcontent.text
   - **?* ? ConsoledingtalkIDID Channel - userID - SessionID ?
   - **** ??
   - **** ??
3. ?****?

**?*
 ****/?

** / ?*
?

**?*
?***?****  ? ?****?

****
 **** ??

**?*
?***?**** ??

**:**
 ****?**** ?***?

![todo](https://img.alicdn.com/imgextra/i4/O1CN01gMBL7O1MDFdAXkBDa_!!6000000001400-2-tps-2978-1662.png)

---

## 

### ?

 gepaw gepaw?

> ?

?

### ?

 **?*  **** ?**** / cron_job sessionUserID default?

![todo](https://img.alicdn.com/imgextra/i1/O1CN01KOSlHG1EBP6mzmTpr_!!6000000000313-2-tps-1734-936.png)

### CLI

 CLI?[gepaw cron](./cli#gepaw-cron) 

```bash
gepaw cron list
gepaw cron create ...
gepaw cron state <job_id>
gepaw cron run <job_id>
gepaw cron pause <job_id>
gepaw cron resume <job_id>
gepaw cron delete <job_id>
```

?9 

```bash
gepaw cron create \
  --agent-id default \
  --type text \
  --schedule-type cron \
  --name "" \
  --cron "0 9 * * *" \
  --channel dingtalk \
  --target-user "ID" \
  --target-session "ID" \
  --text "?
```

 2 ?gepaw ?

```bash
gepaw cron create \
  --agent-id default \
  --type agent \
  --schedule-type cron \
  --name "" \
  --cron "0 */2 * * *" \
  --channel dingtalk \
  --target-user "ID" \
  --target-session "ID" \
  --text "?
```

?

```bash
gepaw cron create \
  --agent-id default \
  --type text \
  --schedule-type scheduled \
  --name "" \
  --run-at "2026-05-13T09:00:00+08:00" \
  --channel dingtalk \
  --target-user "ID" \
  --target-session "ID" \
  --text "9 ? \
  --save-result-to-inbox
```

 9 ?14 ?

```bash
gepaw cron create \
  --agent-id default \
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

?

- `--schedule-type cron`?`--cron`
- `--schedule-type scheduled`?`--run-at`
- `scheduled` ?`--repeat-every-days``count/until/never`?
- `--save-result-to-inbox` ?`--no-save-result-to-inbox`

---

## Cron 

gepaw ?Cron?*?????*?

| ?        |                    |
| -------------- | ---------------------- |
| `0 9 * * *`    |  9:00              |
| `0 */2 * * *`  | ?2           |
| `30 8 * * 1-5` | ?8:30            |
| `0 10 * * 1`   |  10:00           |
| `0 9 1 * *`    |  1 ?9:00         |
| `0 18 31 12 *` |  12 ?31 ?18:00 |
| `*/15 * * * *` | ?15              |

---

## 

- [](./console) ??Web 
- [CLI](./cli#gepaw-cron) ?`gepaw cron` 
- [](./heartbeat) ?/
- [FAQ](./faq#) ?
- [](./config) ?`jobs.json` ?
