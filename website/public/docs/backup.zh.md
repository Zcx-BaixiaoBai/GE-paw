# ?

**?* ?gepaw ****?

> ** ?**

---

## ?

?= ?zip  `~/.gepaw.backups/<backup_id>.zip`

|              |                             |                                                                                                                   |
| ---------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **** | `~/.gepaw/workspaces/<agent_id>/` | ?`bot_token``app_secret` ?|
| ****     | `~/.gepaw/config.json`            | ?                                                                                           |
| ****       | `~/.gepaw/skill_pool/`            | ?                                                                                                     |
| ****     | `~/.gepaw.secret/`                | **LLM ?API Key?*?                                               |

> ****?

?zip ?

```
<backup_id>.zip
 meta.json                        # id /  /  /  / Agent 
 data/
    config.json                   # 
    workspaces/<agent_id>/...     #  Agent 
    skill_pool/...                # 
    secrets/...                   # 
```

 ID  `gepaw-<version>-<timestamp>-<short8>`?

> ****?API Key ?***?API Key?

---

## 

??** ?**?************?

|          |                                                                                                                                    |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| **** | **?*?+  +  + ****?               |
| **** | ??Agent  ? ??*?*?|

> ?

### 

![](https://img.alicdn.com/imgextra/i3/O1CN01lMb2N81Wh9e3WnYPG_!!6000000002819-2-tps-882-928.png)



1. ?****?
2. ****?
3. ?
4. ?***?
5.  ****?

### 



1. ?**** ****?
2. 
   - ****?
   - ****?`config.json`?
   - ****?`skill_pool/` ?
   - **** `~/.gepaw.secret/` ?
3.  ****?

---

## 

>  **?*?

### ?

![](https://img.alicdn.com/imgextra/i4/O1CN01xIWPgV1bBcS9THtY8_!!6000000003427-2-tps-866-273.png)

 ****  **?* 

- ?
- ?

### 

|            |                                  |                                                                            |
| -------------- | ---------------------------------------- | ------------------------------------------------------------------------------ |
| ****   |          | ?***?    |
| **?* | ?| ****?***?|

### 

****

- ?
- ?

?

1.  ****?
2. ?
3.  **?*?

### ?

**?*

- **** `~/.gepaw/workspaces/<agent_id>/`?
- ** /  / **?

?

1. ?**?*?
2. ?
3. ?
4.  /  / ?
5.  **?*?

![](https://img.alicdn.com/imgextra/i2/O1CN01rObfhL23GTtnvidfq_!!6000000007228-2-tps-1131-1396.png)

---

##  /  / 

|      |                                                                                                                                         |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **** |  ****?`.zip` ?                                                              |
| **** |  **** `.zip` ?ID ?***?|
| **** |  zip ?                                                                                    |

---

## 

- ****?API Key`bot_token``app_secret` ?*?*
- ?*?*?
- ****?

---

## 

|              |                                                        |
| ---------------- | -------------------------------------------------------------- |
|      |                  |
|      | ?**** ?            |
|  | ?**?*  |

---

## 

|      |  / ?               |
| -------- | ---------------------------- |
|  | `~/.gepaw.backups/`        |
|  | `<>/<backup_id>.zip` |

---

## Docker 

Docker  `/app/working.backups` Docker ?

?`docker run` ?`-v gepaw-backups:/app/working.backups`?

```bash
docker run -p 127.0.0.1:8088:8088 \
  -v gepaw-data:/app/working \
  -v gepaw-secrets:/app/working.secret \
  -v gepaw-backups:/app/working.backups \
  agentscope/gepaw:latest
```

---

## 

**Q?*
A?

**Q**
AQwenPaw ?

**Q**
A???

---

## 

- [](./console) ??
- [](./config) ?`config.json`?
- [](./multi-agent) ?Agent ?
- [Skills](./skills) ? Agent 
