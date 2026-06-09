# 

**** =  gepaw ?QQ  QQ ?[](./intro)?



- **?*??[](./console) ?**Control ?Channels** ?
- ** `agent.json`** ? `agent.json` ?`~/.gepaw/workspaces/default/agent.json`?`enabled: true` ?

?

---

## 

### 

?

![](https://cloud.video.taobao.com/vod/Fs7JecGIcHdL-np4AS7cXaLoywTDNj7BpiO7_Hb2_cA.mp4)

?

1.  [](https://open-dev.dingtalk.com/)

2. " ****"

   ![](https://img.alicdn.com/imgextra/i1/O1CN01KLtwvu1rt9weVn8in_!!6000000005688-2-tps-2809-1585.png)

3. ???**?*

   ![](https://img.alicdn.com/imgextra/i2/O1CN01AboPsn1XGQ84utCG8_!!6000000002896-2-tps-2814-1581.png)

4.  **Stream **?

   ![](https://img.alicdn.com/imgextra/i3/O1CN01KwmNZ61GwhDhKxgSv_!!6000000000687-2-tps-2814-1581.png)

   ![Stream+](https://img.alicdn.com/imgextra/i2/O1CN01tk8QW11NqvXYqcoPH_!!6000000001622-2-tps-2809-1590.png)

5. ?"?

   ![](https://img.alicdn.com/imgextra/i3/O1CN01lRCPuf1PQwIeFL4AL_!!6000000001836-2-tps-2818-1590.png)

   ![](https://img.alicdn.com/imgextra/i1/O1CN01vrzbIA1Qey2x8Jbua_!!6000000002002-2-tps-2809-1585.png)

6. ?"

   - **Client ID** AppKey?
   - **Client Secret** AppSecret?

   ![client](https://img.alicdn.com/imgextra/i3/O1CN01JsRrwx1hJImLfM7O1_!!6000000004256-2-tps-2809-1585.png)

7.  ** IP ?* ??API?**" IP"**?gepaw  IP?`curl ifconfig.me`  IP `Forbidden.AccessDenied.IpNotInWhiteList` ?

### 

console `agent.json` `~/.gepaw/workspaces/default/agent.json`?

**1**: console

?*DingTalk**?*Client ID**?*Client Secret**

![console](https://img.alicdn.com/imgextra/i4/O1CN01YVQdZe1WsbXoxJOnJ_!!6000000002844-2-tps-3822-2070.png)

**2**:  `agent.json`

 `agent.json` `~/.gepaw/workspaces/default/agent.json` `channels.dingtalk`

```json
"dingtalk": {
  "enabled": true,
  "bot_prefix": "[BOT]",
  "client_id": " Client ID",
  "client_secret": " Client Secret",
  "filter_tool_messages": false
}
```

**?*

|                 |    | ?      |                                                            |
| ------------------- | ------ | ------------ | -------------------------------------------------------------- |
| `client_id`         | string | `""` |  Client ID AppKey?                               |
| `client_secret`     | string | `""` |  Client Secret AppSecret?                        |
| `message_type`      | string | `"markdown"` | `"markdown"` ?`"card"`AI ?                 |
| `card_template_id`  | string | `""`         | AI  ID `message_type` ?`"card"`          |
| `card_template_key` | string | `"content"`  | AI           |
| `robot_code`        | string | `""`         |  `client_id`?|
| `media_dir`         | string | `null`       |                                |

> **?*
>
> - ?`filter_tool_messages: true`?
> - AI Card  `message_type`  `card` `card_template_id``card_template_key` ?
> -  `robot_code` gepaw  `client_id`?

?`gepaw app` ?

### ?

?

![](https://cloud.video.taobao.com/vod/e0icQREdiZ1LI0b1mWdBDQI94KdJSaJxO09X5BPaWvk.mp4)

?

1. ?

![](https://img.alicdn.com/imgextra/i4/O1CN019tRcAi1IIy630Kttu_!!6000000000871-2-tps-2809-2241.png)

2. ??

![](https://img.alicdn.com/imgextra/i3/O1CN01Ha69lm23sx9kLX8eD_!!6000000007312-2-tps-2809-2236.png)

3. 

![](https://img.alicdn.com/imgextra/i1/O1CN01zjnc7J23hxeOJGYiO_!!6000000007288-2-tps-2046-1630.png)

> **?*?

---

## 

 **WebSocket ?*  IP ?webhook?Open API?`chat_id``message_id` ?metadata?

### ?

1.  [](https://open.feishu.cn/app)?

![](https://img.alicdn.com/imgextra/i1/O1CN01awX3Nc1WjRc43kDSk_!!6000000002824-2-tps-4082-2126.png)

![build](https://img.alicdn.com/imgextra/i3/O1CN01OXSFsM1EDh4Xa2aOz_!!6000000000318-2-tps-4082-2126.png)

2.  **App ID**?*App Secret**

![id & secret](https://img.alicdn.com/imgextra/i2/O1CN01tWGGEE1PAuR7APQcs_!!6000000001801-2-tps-4082-2126.png)

3. ?`agent.json` ?**App ID** ?**App Secret**?agent.json?

4.  **`gepaw app`**  gepaw 

5.  **?*

![bot](https://img.alicdn.com/imgextra/i1/O1CN01eFPe0d1wU2IY4Fyvt_!!6000000006310-2-tps-4082-2126.png)

6. ?JSON

```json
{
  "scopes": {
    "tenant": [
      "aily:file:read",
      "aily:file:write",
      "aily:message:read",
      "aily:message:write",
      "corehr:file:download",
      "im:chat",
      "im:message",
      "im:message.group_msg",
      "im:message.p2p_msg:readonly",
      "im:message.reactions:read",
      "im:resource",
      "contact:user.base:readonly"
    ],
    "user": []
  }
}
```

![in/out](https://img.alicdn.com/imgextra/i4/O1CN01CpUMJn1ey7E6FIpOU_!!6000000003939-2-tps-4082-2126.png)

![json](https://img.alicdn.com/imgextra/i3/O1CN01idxezh1G04WY9SYZR_!!6000000000559-2-tps-4082-2126.png)

![confirm](https://img.alicdn.com/imgextra/i3/O1CN017nCNTC1Lj1TVH1OIt_!!6000000001334-2-tps-4082-2126.png)

![confirm](https://img.alicdn.com/imgextra/i3/O1CN01hwOxur1EV67a7clee_!!6000000000356-2-tps-4082-2126.png)

7. ?*WebSocket?*  IP?

> **** App ID/Secret ? `gepaw app` ? gepaw ?`gepaw app`?

![websocket](https://img.alicdn.com/imgextra/i2/O1CN01LQwKON1x7QMNP41kC_!!6000000006396-2-tps-4082-2126.png)

8. ****?* v2.0**

![reveive](https://img.alicdn.com/imgextra/i3/O1CN01svBdl41HTDLCtKFed_!!6000000000758-2-tps-4082-2126.png)

![click](https://img.alicdn.com/imgextra/i4/O1CN01Rat93U1sLYV9f5dhe_!!6000000005750-2-tps-4082-2126.png)

![result](https://img.alicdn.com/imgextra/i2/O1CN015GPfGr1BsxuoOXbYC_!!6000000000002-2-tps-4082-2126.png)

<div id="feishu-callback-config"></div>

9. ?*WebSocket?*  IP?

![websocket](https://img.alicdn.com/imgextra/i4/O1CN015r6kS71DLBxFDJQWe_!!6000000000199-2-tps-1671-848.png)

10. ****?***

![reveive](https://img.alicdn.com/imgextra/i3/O1CN017s7lz724GJMzKKKnC_!!6000000007363-2-tps-1685-855.png)

![click](https://img.alicdn.com/imgextra/i4/O1CN01CcGGmW1K0JCp7cQQV_!!6000000001101-2-tps-1679-847.png)

![result](https://img.alicdn.com/imgextra/i3/O1CN01V9kzMj1CbqkBnSI0x_!!6000000000100-2-tps-1682-847.png)

11. ?***?***?***

![create](https://img.alicdn.com/imgextra/i1/O1CN01zOqMGk1lhoREn9Lip_!!6000000004851-2-tps-4082-2126.png)

![info](https://img.alicdn.com/imgextra/i1/O1CN01SQg28h1nAUrLKTH1J_!!6000000005049-2-tps-4082-2126.png)

![save](https://img.alicdn.com/imgextra/i1/O1CN01ebVPlq1lzDUM1Mwej_!!6000000004889-2-tps-4082-2126.png)

###  agent.json

 `agent.json` `~/.gepaw/workspaces/default/agent.json``channels.feishu`?**App ID** ?**App Secret**

```json
"feishu": {
  "enabled": true,
  "bot_prefix": "[BOT]",
  "app_id": "cli_xxxxx",
  "app_secret": " App Secret",
  "domain": "feishu"
}
```

**?*

|                  |    | ?      |                                        |
| -------------------- | ------ | ------------ | ------------------------------------------ |
| `app_id`             | string | `""` |  App ID                            |
| `app_secret`         | string | `""` |  App Secret                        |
| `domain`             | string | `"feishu"`   | `"feishu"`?`"lark"`?   |
| `encrypt_key`        | string | `""`         | WebSocket  |
| `verification_token` | string | `""`         |  TokenWebSocket    |
| `media_dir`          | string | `null`       |            |

> **?* encrypt_keyverification_tokenmedia_dirWebSocket ?

**?* `pip install lark-oapi`

?SOCKS  `python-socks`?`pip install python-socks``python-socks is required to use a SOCKS proxy`?

> ? **App ID** ?**App Secret** Console gepaw ?
> ![console](https://img.alicdn.com/imgextra/i3/O1CN01KCQj1b1z8utMnRr6y_!!6000000006670-2-tps-3822-2070.png)

### ?

?json

|                        |                        |      |            |
| ------------------------------ | ------------------------------ | ------------ | -------------- |
|                        | aily:file:read                 |      | -              |
|                        | aily:file:write                |      | -              |
|                        | aily:message:read              |      | -              |
| ?                      | aily:message:write             |      | -              |
|                        | corehr:file:download           |      | -              |
| ?            | im:chat                        |      | -              |
| ?      | im:message                     |      | -              |
| ?| im:message.group_msg           |      | -              |
|    | im:message.p2p_msg:readonly    |      | -              |
|                | im:message.reactions:read      |      | -              |
|        | im:resource                    |      | -              |
| **?*       | **contact:user.base:readonly** | **** | **?* |

> ********?1d1aunknown#1d1a?**?*`contact:user.base:readonly` open_id gepaw /?

### ?

1. ?*?*****

![](https://img.alicdn.com/imgextra/i2/O1CN01bSKw0t1tCgReoZNRr_!!6000000005866-2-tps-2614-1488.png)

2. ?***

![](https://img.alicdn.com/imgextra/i1/O1CN01aNNTI51IZSM4TYqis_!!6000000000907-2-tps-3785-2158.png)

3. 

![](https://img.alicdn.com/imgextra/i1/O1CN01Kulh7i1Hfa2Dnfpa4_!!6000000000785-2-tps-2614-1488.png)

![](https://img.alicdn.com/imgextra/i4/O1CN01vsnwn71UMQTaEa0XX_!!6000000002503-2-tps-2614-1488.png)

---

## iMessage macOS?

>  iMessage ?**macOS** iMessage ?Linux / Windows ?

 iMessage ?

1.  **?Messages)** ?Apple ID?

2.  **imsg**?iMessage ?

   ```bash
   brew install steipete/tap/imsg
   ```

   >  Intel  Mac ?
   >
   > ```bash
   > git clone https://github.com/steipete/imsg.git
   > cd imsg
   > make build
   > sudo cp build/Release/imsg /usr/local/bin/
   > cp ./bin/imsg /usr/local/bin/
   > ```

3. ?iMessage ?**** ?gepaw ?app??**** ?****?????

   ![](https://img.alicdn.com/imgextra/i2/O1CN01gCbMWX1S2c77mcoPo_!!6000000002189-2-tps-958-440.png)

4.  iMessage  `~/Library/Messages/chat.db`?

   -  **??**?**iMessage**  **Enable**  **DB Path**?****?

     ![](https://img.alicdn.com/imgextra/i4/O1CN01yxsvJ51yOetCYur9f_!!6000000006569-2-tps-3822-2070.png)

   - ?`agent.json` `~/.gepaw/workspaces/default/agent.json`

     ```json
     "imessage": {
       "enabled": true,
       "bot_prefix": "[BOT]",
       "db_path": "~/Library/Messages/chat.db",
       "poll_sec": 1.0
     }
     ```

**iMessage ?*

|        |    | ?                      |                 |
| ---------- | ------ | ---------------------------- | ------------------- |
| `db_path`  | string | `~/Library/Messages/chat.db` | iMessage ?|
| `poll_sec` | float  | `1.0`                        | ?     |

5. ?iMessage Apple ID?

   ![](https://img.alicdn.com/imgextra/i4/O1CN01beScxi1rBBvSFeIbz_!!6000000005592-2-tps-1206-2622.png)

---

## Discord

###  Bot Token

1.  [Discord ](https://discord.com/developers/applications)

![Discord](https://img.alicdn.com/imgextra/i2/O1CN01oV68yZ1sb7y3nGoQN_!!6000000005784-2-tps-4066-2118.png)

2. 

![](https://img.alicdn.com/imgextra/i2/O1CN01eA9lA71kMukVCWR4y_!!6000000004670-2-tps-3726-1943.png)

3.  **Bot**?Bot?**Token**

![token](https://img.alicdn.com/imgextra/i1/O1CN01iuPiUe1lJzqEiIu23_!!6000000004799-2-tps-2814-1462.png)

4. ?Bot Message Content Intent??Send Messages??

![](https://img.alicdn.com/imgextra/i4/O1CN01EXH4w51FSdbxYKLG9_!!6000000000486-2-tps-4066-2118.png)

5. ?**OAuth2 ?URL ?* ?`bot` ?Bot Send Messages??

![bot](https://img.alicdn.com/imgextra/i2/O1CN01B2oXx71KVS7kjKSEm_!!6000000001169-2-tps-4066-2118.png)

![send messages](https://img.alicdn.com/imgextra/i3/O1CN01DlU9oi1QYYVBPoUIA_!!6000000001988-2-tps-4066-2118.png)

![link](https://img.alicdn.com/imgextra/i2/O1CN01ljhh1j1OZLxb2mAkO_!!6000000001719-2-tps-4066-2118.png)

6. discord Bot ?

![](https://img.alicdn.com/imgextra/i1/O1CN01ivgmOA1JuM2i9WNqm_!!6000000001088-2-tps-2806-1824.png)

![](https://img.alicdn.com/imgextra/i2/O1CN01ecRCVa1UeHvFUP0XQ_!!6000000002542-2-tps-2806-1824.png)

7. ?Bot

![](https://img.alicdn.com/imgextra/i2/O1CN014HOCCJ1fsuL2RQiB5_!!6000000004063-2-tps-2806-1824.png)

###  Bot

console `agent.json` `~/.gepaw/workspaces/default/agent.json`?

**1**: console

?*Discord**?*Bot Token**

![console](https://img.alicdn.com/imgextra/i1/O1CN01kRdzN61HBLu9LghUV_!!6000000000719-2-tps-3822-2070.png)

**2**:  `agent.json`

 `agent.json` `~/.gepaw/workspaces/default/agent.json` `channels.discord`

```json
"discord": {
  "enabled": true,
  "bot_prefix": "[BOT]",
  "bot_token": " Bot Token",
  "http_proxy": "",
  "http_proxy_auth": ""
}
```

**Discord ?*

|               |    | ?      |                                         |
| ----------------- | ------ | ------------ | ------------------------------------------- |
| `bot_token`       | string | `""` | Discord Bot Token                           |
| `http_proxy`      | string | `""`         |  `http://127.0.0.1:7890`?     |
| `http_proxy_auth` | string | `""`         | `?` |

> **?*  Discord API ?

---

## QQ

###  QQ ?

1.  [QQ ](https://q.qq.com/)

![](https://img.alicdn.com/imgextra/i4/O1CN01OjCvUf1oT6ZDWpEk5_!!6000000005225-2-tps-4082-2126.png)

2.  **?*?

![bot](https://img.alicdn.com/imgextra/i3/O1CN01xBbXWa1pSTdioYFdg_!!6000000005359-2-tps-4082-2126.png)

![confirm](https://img.alicdn.com/imgextra/i3/O1CN01zt7w0V1Ij4fjcm5MS_!!6000000000928-2-tps-4082-2126.png)

3. ********?*C2C**?*?*?*AT**?

![c2c](https://img.alicdn.com/imgextra/i4/O1CN01HDSoX91iOAbTVULZf_!!6000000004402-2-tps-4082-2126.png)

![at](https://img.alicdn.com/imgextra/i4/O1CN01UJn1AK1UKatKkjMv4_!!6000000002499-2-tps-4082-2126.png)

4. ******?*?*******

![1](https://img.alicdn.com/imgextra/i4/O1CN01BSdkXl1ckG0dC7vH9_!!6000000003638-2-tps-4082-2126.png)

![1](https://img.alicdn.com/imgextra/i4/O1CN01LGYUMe1la1hmtcuyY_!!6000000004834-2-tps-4082-2126.png)

5. ?*?*?*AppID**?*AppSecret** ClientSecret `agent.json` agent.json**IP?*IP?

   > **?* QwenPawQQIP`47.92.200.108`

![1](https://img.alicdn.com/imgextra/i4/O1CN012UQWI21cnvBAUcz54_!!6000000003646-2-tps-4082-2126.png)

6. QQ

![1](https://img.alicdn.com/imgextra/i3/O1CN01r1OvPy1kcwc30w32K_!!6000000004705-2-tps-4082-2126.png)

###  agent.json

 `agent.json` `~/.gepaw/workspaces/default/agent.json` `channels.qq`?`app_id` ?`client_secret`?

```json
"qq": {
  "enabled": true,
  "bot_prefix": "[BOT]",
  "app_id": " AppID",
  "client_secret": " AppSecret",
  "markdown_enabled": false,
  "max_reconnect_attempts": -1
}
```

**QQ ?*

|                      |    | ?      |                                       |
| ------------------------ | ------ | ------------ | ----------------------------------------- |
| `app_id`                 | string | `""` | QQ ?App ID                          |
| `client_secret`          | string | `""` | QQ ?Client Secret AppSecret?  |
| `markdown_enabled`       | bool   | `false`      |  Markdown  QQ ? |
| `max_reconnect_attempts` | int    | `-1`         | WebSocket `-1` = ?|

> **?* ?**AppID** ?**AppSecret** ?Token?

console?

![console](https://img.alicdn.com/imgextra/i3/O1CN01FJrXGd1dNBgbrPZMf_!!6000000003723-2-tps-3822-2070.png)

---

## OneBot v11NapCat / QQ ?

**OneBot** ** WebSocket** ?gepaw ?[NapCat](https://github.com/NapNeko/NapCatQQ)[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)[Lagrange](https://github.com/LagrangeDev/Lagrange.Core) ?[OneBot v11](https://github.com/botuniverse/onebot-11) ?

?QQ ?QQ Bot APIOneBot v11 ** QQ ** @?

### 

gepaw ?WebSocket OneBot  NapCat?

```
NapCat   WS? gepaw (:6199/ws)
```

###  NapCat

1.  Docker  NapCat?

   ```bash
   docker run -d \
     --name napcat \
     -e ACCOUNT=<QQ? \
     -p 6099:6099 \
     mlikiowa/napcat-docker:latest
   ```

2.  NapCat WebUI `http://localhost:6099` QQ ?

3.  **** ?**** ?**WebSocket ?*?WS
   - URL`ws://<gepaw>:6199/ws`
   - Access Token gepaw  `access_token` 

###  agent.json

```json
"onebot": {
  "enabled": true,
  "ws_host": "0.0.0.0",
  "ws_port": 6199,
  "access_token": "",
  "share_session_in_group": false
}
```

**OneBot ?*

|                      |    | ?   |                                                           |
| ------------------------ | ------ | --------- | ------------------------------------------------------------- |
| `ws_host`                | string | `0.0.0.0` | WebSocket                                       |
| `ws_port`                | int    | `6199`    | WebSocket ?                                     |
| `access_token`           | string | `""`      |  Token?NapCat                       |
| `share_session_in_group` | bool   | `false`   | ?`true` ?`false` ?|

> **Docker Compose ?* gepaw ?NapCat  Docker Compose NapCat ?WS ?`ws://gepaw:6199/ws`?

****

|  |  | ?|
| ---- | ---- | ---- |
|  | ?   | ?   |
|  | ?   | ?   |
|  |    | ?   |
|  |    | ?   |
|  | ?   | ?   |

> **?* ?gepaw `transcription_provider_type` LLM ?

---

## 

### ?

[](https://work.weixin.qq.com)?

![](https://img.alicdn.com/imgextra/i2/O1CN01Xg8B3i1EQWAKt5xj0_!!6000000000346-2-tps-2938-1588.png)



![](https://img.alicdn.com/imgextra/i4/O1CN01uRF1Mv1TX87bOQ045_!!6000000002391-2-tps-1538-905.png)

?

API?

### ?

-API-?

![?](https://img.alicdn.com/imgextra/i3/O1CN01lcA2rX1fm2P19SLcB_!!6000000004048-2-tps-1440-814.png)

![?](https://img.alicdn.com/imgextra/i1/O1CN014R3a0f1mnb3qbycMV_!!6000000004999-2-tps-1440-814.png)

![?](https://img.alicdn.com/imgextra/i4/O1CN01kZDNVk1ugHf73ybs2_!!6000000006066-2-tps-2938-1594.png)

`Bot ID``Secret`

![?](https://img.alicdn.com/imgextra/i1/O1CN01Znm7aQ1Tfpe5Ha9WL_!!6000000002410-2-tps-1482-992.png)

### bot

Console?`agent.json` Bot IDSecretbot

****console

![console](https://img.alicdn.com/imgextra/i1/O1CN01pyx6Ma1YMCl1kMnje_!!6000000003044-2-tps-3822-2070.png)

**?*?`agent.json`  `~/.gepaw/workspaces/default/agent.json`?

`wecom`

```json
"wecom": {
  "enabled": true,
  "bot_prefix": "[BOT]",
  "dm_policy": "open",
  "group_policy": "open",
  "bot_id": "your bot_id",
  "secret": "your secret",
  "media_dir": "~/.gepaw/media",
  "max_reconnect_attempts": -1
}
```

**?*

|                      |    | ?            |                                       |
| ------------------------ | ------ | ------------------ | ----------------------------------------- |
| `bot_id`                 | string | `""`       | ?Bot ID                     |
| `secret`                 | string | `""`       | ?Secret                     |
| `media_dir`              | string | `~/.gepaw/media` | ?         |
| `max_reconnect_attempts` | int    | `-1`               | WebSocket `-1` = ?|

### ?

![](https://img.alicdn.com/imgextra/i3/O1CN01ZsmpYr1tq4ViIbO80_!!6000000005952-2-tps-1308-1130.png)

---

## iLink?

 iLink Bot **** AI ?[iLink Bot HTTP API](https://weixin.qq.com/cgi-bin/readtemplate?t=ilink/chatbot) ?

> ****?BotiLink ?

### 

- ****Token ?`~/.gepaw/wechat_bot_token`?
- **** HTTP `getupdates`ASR ?
- **?* `sendmessage` iLink API ?

###  Console?

1. ?gepaw Web Console ?** ? ?iLink?*?
2.  **?*?
3. ?
4. Bot Token  **** ?

### 

 `agent.json` `~/.gepaw/workspaces/default/agent.json`?

```json
"wechat": {
  "enabled": true,
  "bot_prefix": "[BOT]",
  "bot_token": "your_bot_token",
  "bot_token_file": "~/.gepaw/wechat_bot_token",
  "base_url": "",
  "media_dir": "~/.gepaw/media",
  "dm_policy": "open",
  "group_policy": "open"
}
```

**?*

|              |    | ?                       |                                                 |
| ---------------- | ------ | ----------------------------- | --------------------------------------------------- |
| `bot_token`      | string | `""`                          |  Bearer Token?|
| `bot_token_file` | string | `~/.gepaw/wechat_bot_token` | Token                   |
| `base_url`       | string |                   | iLink API ?                 |
| `media_dir`      | string | `~/.gepaw/media`            | ?                         |

### 

?

```bash
WECHAT_CHANNEL_ENABLED=1
WECHAT_BOT_TOKEN=your_bot_token
WECHAT_BOT_TOKEN_FILE=~/.gepaw/wechat_bot_token
WECHAT_MEDIA_DIR=~/.gepaw/media
WECHAT_DM_POLICY=open
WECHAT_GROUP_POLICY=open
```

---

## Telegram

###  Telegram ?

1.  Telegram ?`@BotFather`  Bot @BotFather?
2. ?@BotFather 

   ![](https://img.alicdn.com/imgextra/i1/O1CN01wVVmbY1qkcxBn8Oc0_!!6000000005534-0-tps-817-1279.jpg)

3. ?bot_name?bot_token

   ![token](https://img.alicdn.com/imgextra/i3/O1CN01KUMvBW1UnuF599tNX_!!6000000002563-0-tps-1209-1237.jpg)

###  Bot

console?`agent.json`?

**1**: console

??**Telegram**?*Bot Token**

![console](https://img.alicdn.com/imgextra/i3/O1CN01wrQfVo1QmIOUaWqoW_!!6000000002018-2-tps-3822-2070.png)

**2**:  `agent.json`

 `agent.json` `~/.gepaw/workspaces/default/agent.json` `channels.telegram`

```json
"telegram": {
  "enabled": true,
  "bot_prefix": "[BOT]",
  "bot_token": " Bot Token",
  "http_proxy": "",
  "http_proxy_auth": ""
}
```

**Telegram ?*

|               |    | ?      |                                         |
| ----------------- | ------ | ------------ | ------------------------------------------- |
| `bot_token`       | string | `""` | Telegram Bot Token                          |
| `http_proxy`      | string | `""`         |  `http://127.0.0.1:7890`?     |
| `http_proxy_auth` | string | `""`         | `?` |

> **?*  Telegram API ?

### 

`dm_policy``group_policy``allow_from``deny_message``require_mention`?bot username ?

?`@BotFather` ?

```
/setprivacy -> ENABLED # bot
/setjoingroups -> DISABLED # Group?
```

---

## Mattermost

Mattermost  WebSocket  REST API ?**Thread** ?

### ?

1. ?Mattermost ?**Bot ** (System Console ?Integrations ?Bot Accounts)?
2.  `Post all`?**Access Token**?
3.  `agent.json` `~/.gepaw/workspaces/default/agent.json` **URL** ?**Token**?

**?*

```json
"mattermost": {
  "enabled": true,
  "bot_prefix": "[BOT]",
  "url": "https://mattermost.example.com",
  "bot_token": "your_access_token",
  "show_typing": true,
  "thread_follow_without_mention": false,
  "dm_policy": "open",
  "group_policy": "open"
}
```

**Mattermost ?*

|                             |    | ?      |                                                       |
| ------------------------------- | ------ | ------------ | --------------------------------------------------------- |
| `url`                           | string | `""` | Mattermost                                  |
| `bot_token`                     | string | `""` |  Access Token                                     |
| `show_typing`                   | bool   | `true`       | ?..?                          |
| `thread_follow_without_mention` | bool   | `false`      | ?Thread  @  |

> ****Mattermost ?`session_id` ?`mattermost_dm:{mm_channel_id}` Thread ID ?Session ?

---

## MQTT

### 

JSON?

JSON

```
{
  "text": "...",
  "redirect_client_id": "..."
}
```

### 

|                     | ?           | ?|                     |
| ----------------------- | --------------- | ------ | ----------------------- |
|                 | host            | Y      | 127.0.0.1               |
|                 | port            | Y      | 1883                    |
|                     | transport       | Y      | tcp                     |
|                 | clean_session   | Y      | true                    |
|  / ?| qos             | Y      | 2                       |
| ?                 | username        | N      |                         |
|                     | password        | N      |                         |
|                 | subscribe_topic | Y      | server/+/up             |
| ?               | publish_topic   | Y      | client/{client_id}/down |
| ?               | tls_enabled     | N      | false                   |
| CA ?              | tls_ca_certs    | N      | /tsl/ca.pem             |
| ?         | tls_certfile    | N      | /tsl/client.pem         |
| ?         | tls_keyfile     | N      | /tsl/client.key         |

### 

1. ?

   | subscribe_topic | publish_topic |
   | --------------- | ------------- |
   | server          | client        |

2. ?

   server/+/upclient_id`/server/client_a/up`QwenPaw`/client/client_b/down`?

   | subscribe_topic | publish_topic           |
   | --------------- | ----------------------- |
   | server/+/up     | client/{client_id}/down |

3. ?

   JSON`server/client_a/up``client/client_a/down`

   ```json
   {
     "text": "?,
     "redirect_client_id": "client_b"
   }
   ```

   redirect_client_id `client/client_b/down`QwenPaw?

---

## Matrix

Matrix  [matrix-nio](https://github.com/poljar/matrix-nio)  gepaw  Matrix ?

###  Access Token

1. ?Matrix  [matrix.org](https://matrix.org)?[app.element.io](https://app.element.io/#/register) ?

2.  **Access Token** Element?

   -  [app.element.io](https://app.element.io)
   -  ** ??? ?Access Token**
   -  Token `syt_...` 

   ?Matrix Client-Server API?

   ```bash
   curl -X POST "https://matrix.org/_matrix/client/v3/login" \
     -H "Content-Type: application/json" \
     -d '{"type":"m.login.password","user":"@yourbot:matrix.org","password":"yourpassword"}'
   ```

    `access_token`  Token?

3.  **User ID**`@?`?`@mybot:matrix.org` **Homeserver URL**?`https://matrix.org`?

### 

**?* ?Console ?

 ** ?**?**Matrix**?

- **Homeserver URL** ? `https://matrix.org`
- **User ID** ? `@mybot:matrix.org`
- **Access Token** ??Token

**** ?`agent.json`

?`agent.json` `~/.gepaw/workspaces/default/agent.json` `channels.matrix`?

```json
"matrix": {
  "enabled": true,
  "bot_prefix": "[BOT]",
  "homeserver": "https://matrix.org",
  "user_id": "@mybot:matrix.org",
  "access_token": "syt_..."
}
```

**Matrix ?*

|            |    | ?      |                                          |
| -------------- | ------ | ------------ | -------------------------------------------- |
| `homeserver`   | string | `""` | Matrix  `https://matrix.org`?|
| `user_id`      | string | `""` | ?User ID `@mybot:matrix.org`?    |
| `access_token` | string | `""` |  Access Token `syt_`       |

?gepaw ?

### ?

?Matrix ?Element?

### 

- Matrix **?*/?
- ?
-  `homeserver` ?`https://matrix.example.com`?

---

## Yuanbao?

 protobuf WebSocket  AI ??

###  Bot ?

1. ?**Bot** ?**Bot**?

   ![Bot](https://img.alicdn.com/imgextra/i3/O1CN01ChYAcN1L0b4pj7ODV_!!6000000001237-2-tps-2112-1440.png)

2. ?Bot ?**2**?**AppID** ?**AppSecret**?gepaw ?****?

   ![AppID ?AppSecret](https://img.alicdn.com/imgextra/i2/O1CN01F4vbLs29ID63r4cGf_!!6000000008044-2-tps-2112-1440.png)

**?*

```json
"yuanbao": {
  "enabled": true,
  "app_id": " AppID",
  "app_secret": " AppSecret"
}
```

**?*

|          |    | ?                   |                  |
| ------------ | ------ | ------------------------- | -------------------- |
| `app_id`     | string | `""`              | ?AppID     |
| `app_secret` | string | `""`              | ?AppSecret |
| `api_domain` | string | `bot.yuanbao.tencent.com` | REST API         |

---

## XiaoYi?

 **A2A (Agent-to-Agent) **  WebSocket ?

### ?

1. Agent?
2.  **AK** (Access Key)?*SK** (Secret Key) ?**Agent ID**?
3.  `agent.json` ?

**?*

```json
"xiaoyi": {
  "enabled": true,
  "bot_prefix": "[BOT]",
  "ak": "your_access_key",
  "sk": "your_secret_key",
  "agent_id": "your_agent_id",
  "ws_url": "wss://hag.cloud.huawei.com/openclaw/v1/ws/link"
}
```

**?*

|        |    | ?                                          |                 |
| ---------- | ------ | ------------------------------------------------ | ------------------- |
| `ak`       | string | `""`                                     |  Access Key |
| `sk`       | string | `""`                                     |  Secret Key     |
| `agent_id` | string | `""`                                     |         |
| `ws_url`   | string | `wss://hag.cloud.huawei.com/openclaw/v1/ws/link` | WebSocket       |

### ?

****JPEG, JPG, PNG, BMP, WEBP

****PDF, DOC, DOCX, PPT, PPTX, XLS, XLSX, TXT

> ?

---

## Voice

Voice  Twilio ConversationRelay STTTTS gepaw ?

### 

1. **Twilio ** [Twilio ](https://www.twilio.com/) ?
2. **Cloudflare Tunnel** gepaw ?Twilio 

###  Twilio ?

1.  [Twilio Console](https://console.twilio.com/)?
2. ?Dashboard 
   - **Account SID**
   - **Auth Token**
3. ?
   -  **Phone Numbers ?Buy a Number**
   - ?
   -  **Phone Number** `+1234567890` **Phone Number SID**

###  Cloudflare Tunnel

Twilio  gepaw ?Webhook ?

1.  Cloudflare Tunnel 

```bash
# macOS
brew install cloudflare/cloudflare/cloudflared

# Linux
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
sudo chmod +x /usr/local/bin/cloudflared
```

2.  8088 

```bash
cloudflared tunnel --url http://localhost:8088
```

3. ?URL`https://abc-def-ghi.trycloudflare.com`

###  Voice 

**?* ?Console ?

 ** ?**?**Voice**?

- **Twilio Account SID** Twilio Dashboard 
- **Twilio Auth Token** Twilio Dashboard 
- **Phone Number** `+1234567890`?
- **Phone Number SID** SID

?

- **TTS Provider** `google`?
- **TTS Voice** `en-US-Journey-D`?
- **STT Provider** `deepgram`?
- **Language**?`en-US`?
- **Welcome Greeting**?

****  `agent.json`

```json
{
  "channels": {
    "voice": {
      "enabled": true,
      "twilio_account_sid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "twilio_auth_token": "your_auth_token",
      "phone_number": "+1234567890",
      "phone_number_sid": "PNxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "tts_provider": "google",
      "tts_voice": "en-US-Journey-D",
      "stt_provider": "deepgram",
      "language": "en-US",
      "welcome_greeting": "Hi! This is gepaw. How can I help you?"
    }
  }
}
```

###  Twilio Webhook

?Twilio Console  Webhook?

1.  **Phone Numbers ?Manage ?Active Numbers**
2. 
3. ?**Voice Configuration** ?
   - **A Call Comes In** **Webhook**
   - **URL**?`https://your-cloudflare-url.trycloudflare.com/api/voice/callback`
   - **HTTP Method** **POST**
4. 

### 

 Twilio  gepaw ?

1. 
2. ?
3. gepaw ?Agent 
4. ?Agent 

**Voice ?*

|                  |    | ?                                      |                                |
| -------------------- | ------ | -------------------------------------------- | ---------------------------------- |
| `twilio_account_sid` | string | `""`                                 | Twilio Account SID                 |
| `twilio_auth_token`  | string | `""`                                 | Twilio Auth Token                  |
| `phone_number`       | string | `""`                                 | ?`+1234567890`?|
| `phone_number_sid`   | string | `""`                                 | ?SID                     |
| `tts_provider`       | string | `"google"`                                   |                    |
| `tts_voice`          | string | `"en-US-Journey-D"`                          | TTS                        |
| `stt_provider`       | string | `"deepgram"`                                 |                    |
| `language`           | string | `"en-US"`                                    |                            |
| `welcome_greeting`   | string | `"Hi! This is gepaw. How can I help you?"` | ?    |

> ****Voice ?Cloudflare Tunnelngrok ?

---

## SIP

SIP  SIP  LinphoneMicroSIPIP  gepaw  URL?

?

|         |             | ?                |
| ----------- | ------------------- | ---------------------------------- |
| **Dev**     | PoC?| ?? SIP ?      |
| **LiveKit** |     | LiveKit Server LiveKit Cloud?|

### Dev ? ?

QwenPaw ?SIP  AsteriskFreeSWITCH ?

1. ?

```bash
pip install "gepaw[sip]"
```

2.  gepaw ?

```bash
gepaw init --defaults
gepaw app
```

 **http://127.0.0.1:8088/** ?** ?**?API Key?** ? ?SIP** DashScope API Key?****??`sip_server` ?gepaw STT/TTS  `aliyun`?

gepaw ?SIP 

```
[SIP] Built-in SIP registrar started on 0.0.0.0:5060
[SIP] Quickstart: register your softphone to <IP>:5060
[SIP] Dial 'sip:agent@<IP>:5060' to talk with gepaw!
```

3.  [Linphone](https://www.linphone.org/linphone) SIP 

   -  **Preferences ?SIP Accounts ?Add**
   - Username?`caller`?
   - SIP Domain`127.0.0.1`?IP ?***?`localhost`?IPv6 ?
   - Transport?*UDP**
   -  ??
   - `sip:agent@127.0.0.1:5060`

    ?gepaw 

   ** pjsua/**

   ```bash
   pjsua --local-port=5062 \
     --bound-addr=127.0.0.1 \
     --no-tcp \
     --id='sip:caller@127.0.0.1:5062' \
     --registrar='sip:127.0.0.1:5060' \
     --realm='*' --username=caller --password=pass
   ```

    `m` ?`sip:agent@127.0.0.1:5060` `h` ?

> ****[](#)?

### LiveKit 3  SIP ?

 WebRTC ?LiveKit  SIP TrunkDocker ?Redis?

1.  [LiveKit Cloud](https://cloud.livekit.io/) **Settings ?Project** ?URL **Settings ?API keys** ?API Key ?API Secret?

2. ?gepaw ?

```bash
pip install "gepaw[sip,sip-livekit]"
gepaw init --defaults
gepaw app
```

 **http://127.0.0.1:8088/** ?** ?**?API Key?** ? ?SIP**SIP ?**Production (LiveKit)**?4 

- **LiveKit URL** `wss://<your-project>.livekit.cloud`?
- **LiveKit API Key**
- **LiveKit API Secret**
- **DashScope API Key**

?****?

`Connected to room: sip-inbound, waiting...`

3.  Token  [LiveKit Meet](https://meet.livekit.io/) ?

   ```bash
   #  LiveKit CLI
   brew install livekit-cli

   #  Token
   lk token create \
     --api-key <your-api-key> \
     --api-secret <your-api-secret> \
     --join --room sip-inbound \
     --identity test-user
   ```

   -  [meet.livekit.io](https://meet.livekit.io/) ? **"Custom"**
   -  LiveKit Cloud URL `wss://<your-project>.livekit.cloud`?
   - ?Token ?**Connect**
   -  ?gepaw 

> ****?SIP ?STT?4kHz TTS LiveKit ?

### 

?

**Dev  +  SIP **

 AsteriskFreeSWITCH ?SIP PBX  `sip_server`  PBX QwenPaw ?SIP  PBX ?

**LiveKit  + SIP Trunk?*

?PSTN  LiveKit Server + LiveKit SIP?SIP Trunk ?TwilioTelnyxVonage?[LiveKit SIP ](https://docs.livekit.io/sip/)?

|                           |  PSTN?   | ?| ?|
| --------------------------------- | -------------- | -------- | ------ |
| Dev + Asterisk/FreeSWITCH         |  trunk?|  | ?    |
| LiveKit + Twilio/Telnyx SIP Trunk | ?            | ?      | ?    |
| LiveKit +  SIP        | ?        | ?      | ?    |

### Dev 

Dev  `pyVoIP` ? Python SIP ?

**?* ?

 ** ?**?**SIP** **Dev (pyVoIP)** `sip_server` ?SIP ?****?

****  agent ?`agent.json`

```json
{
  "channels": {
    "sip": {
      "enabled": true,
      "sip_mode": "dev",
      "sip_server": "",
      "stt_provider": "aliyun",
      "tts_provider": "aliyun",
      "tts_voice": "longxiaochun",
      "language": "zh-CN",
      "welcome_greeting": "QwenPaw"
    }
  }
}
```

`sip_server` gepaw ?5060  SIP agent ?`sip_server` `"192.168.1.100:5060"`QwenPaw ?

### LiveKit 

?SIP/RTP ?LiveKit SIP Server?NAT QwenPaw  AI ?LiveKit ?

1. ?

```bash
pip install "gepaw[sip,sip-livekit]"
```

2. ?`agent.json` ?SIP ?

```json
{
  "channels": {
    "sip": {
      "enabled": true,
      "sip_mode": "livekit",
      "livekit_url": "wss://<your-project>.livekit.cloud",
      "livekit_api_key": "your-api-key",
      "livekit_api_secret": "your-api-secret",
      "stt_provider": "aliyun",
      "tts_provider": "aliyun",
      "tts_voice": "longxiaochun",
      "language": "zh-CN",
      "welcome_greeting": "QwenPaw"
    }
  }
}
```

> **`livekit_url`**LiveKit Cloud  `wss://<project>.livekit.cloud`?LiveKit Server  `ws://<host>:<port>`?

3.  gepaw SIP  LiveKit ?SIP Trunk ?Dispatch Rule?[LiveKit SIP ](https://docs.livekit.io/sip/)[](#livekit-?--sip-)?

### 

?SIP ?

1. ?
2. ??gepaw  STT ?
3. Agent ?
4.  TTS 
5. ??
6.  Agent ?

### SIP 

|                  |    | ?                                      |                                                    |
| -------------------- | ------ | -------------------------------------------- | ------------------------------------------------------ |
| `sip_mode`           | string | `"dev"`                                      | `"dev"`pyVoIP `"livekit"`              |
| `sip_server`         | string | `""`                                         | SIP dev ?|
| `sip_username`       | string | `""`                                         | SIP ?`agent`?          |
| `sip_password`       | string | `""`                                         | SIP                                            |
| `sip_host`           | string | `"0.0.0.0"`                                  |                                            |
| `sip_port`           | int    | `5061`                                       |  SIP agent                               |
| `sip_transport`      | string | `"UDP"`                                      | SIP `UDP``TCP` ?`TLS`                    |
| `rtp_port_low`       | int    | `10000`                                      | RTP  dev ?                       |
| `rtp_port_high`      | int    | `20000`                                      | RTP  dev ?                       |
| `livekit_url`        | string | `""`                                         | LiveKit Server WebSocket URL               |
| `livekit_api_key`    | string | `""`                                         | LiveKit API                            |
| `livekit_api_secret` | string | `""`                                         | LiveKit API                            |
| `tts_provider`       | string | `"aliyun"`                                   | TTS  `aliyun`?                       |
| `tts_voice`          | string | `"longxiaochun"`                             | TTS                                            |
| `stt_provider`       | string | `"aliyun"`                                   | STT  `aliyun`?                       |
| `language`           | string | `"zh-CN"`                                    |                                                |
| `welcome_greeting`   | string | `"Hi! This is gepaw. How can I help you?"` | ?                        |
| `call_timeout`       | float  | `30.0`                                       | ?                                    |

---

## 

### 

|        | ?    | /                                                                                          |
| ---------- | ---------- | ------------------------------------------------------------------------------------------------------ |
|        | dingtalk   | client_id, client_secret, message_type, card_template_id, card_template_key, robot_code                |
|        | feishu     | app_id, app_secret?encrypt_key, verification_token, media_dir                                    |
| iMessage   | imessage   | db_path, poll_sec macOS?                                                                         |
| Discord    | discord    | bot_token?http_proxy, http_proxy_auth                                                            |
| QQ         | qq         | app_id, client_secret                                                                                  |
| Telegram   | telegram   | bot_token?http_proxy, http_proxy_auth                                                            |
| Mattermost | mattermost | url, bot_token; ?show_typing, dm_policy, allow_from                                                |
| Matrix     | matrix     | homeserver, user_id, access_token                                                                      |
|    | wecom      | bot_id, secret?media_dir                                                                         |
|    | wechat     | bot_token?bot_token_file, base_url, media_dir                                      |
|        | xiaoyi     | ak, sk, agent_id?ws_url                                                                          |
|        | yuanbao    | app_id, app_secret?api_domain, media_dir                                                         |
| Voice      | voice      | twilio_account_sid, twilio_auth_token, phone_number, phone_number_sid?tts_provider, stt_provider |

`dm_policy``group_policy``allow_from``deny_message``require_mention`?

 [](./config)?

### 

?

|                    |      | ?  |                                                     |
| ---------------------- | -------- | -------- | ------------------------------------------------------- |
| `enabled`              | bool     | `false`  | ?                                         |
| `bot_prefix`           | string   | `""`     |  `[BOT]`?                           |
| `filter_tool_messages` | bool     | `false`  | /                               |
| `filter_thinking`      | bool     | `false`  | ?                                   |
| `dm_policy`            | string   | `"open"` | `"open"`/ `"allowlist"`?|
| `group_policy`         | string   | `"open"` | `"open"`/ `"allowlist"`?|
| `allow_from`           | string[] | `[]`     | ?policy ?`"allowlist"`          |
| `deny_message`         | string   | `""`     |                                     |
| `require_mention`      | bool     | `false`  | ?@??                                |

### ?

?/  /  /  / ******?*?
? ? ? ?

|        |  |  |  |  |  | ?| ?| ?| ?| ?|
| ---------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
|        | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       |
|        | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       |
| Discord    | ?       | ?       | ?       | ?       | ?       | ?       |        |        |        |        |
| iMessage   | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       |
| QQ         | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       |
|    | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       |
|    | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       |
| Telegram   | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       |
| Mattermost | ?       | ?       |        |        | ?       | ?       | ?       |        |        | ?       |
| Matrix     | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       |
|        | ?       | ?       | ?       | ?       | ?       | ?       |        |        |        |        |
|        | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       |
| Voice      | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       | ?       |

?

- ****downloadCode webhook  /  /  / ?
- ****WebSocket Open API  /  / ?metadata  `feishu_chat_id``feishu_message_id` ?
- **Discord** /  /  / ?Agent  ?
- **iMessage**?imsg + /?
- **QQ**  ?+ ?
- **Telegram**telegram?/  /  / ?
- ****WebSocket markdown/template_card ?
- **iLink?*HTTP AES-128-ECB ASR ?MP3 iLink API ?
- **Matrix**?/  /  /  `mxc://`  URL?Matrix `m.image``m.video``m.audio``m.file`?
- ****JPEG/PNG/BMP/WEBPPDF/DOC/DOCX/PPT/PPTX/XLS/XLSX/TXT?
- **** COS CDN  Bot?
- **Voice**Agent ?

###  HTTP 

 `agent.json` 

- `GET /config/channels` ?
- `PUT /config/channels` ?
- `GET /config/channels/{channel_name}` ? `dingtalk``imessage`?
- `PUT /config/channels/{channel_name}` ?

---

## 

Slack  **BaseChannel** ?

### 

- **ChannelManager**  channel ?channel  **`self._enqueue(payload)`** manager manager ?**`channel.consume_one(payload)`**?
- ?** `consume_one`** payload  `AgentRequest` `_process` `send_message_content` `_on_consume_error` `consume_one`?

### 

|                                                     |                                                                                                                                        |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `build_agent_request_from_native(self, native_payload)` | ?`AgentRequest`?runtime ?`Message`/`TextContent`/`ImageContent`  `request.channel_meta` ?|
| `from_env` / `from_config`                              | ?                                                                                                                |
| `async start()` / `async stop()`                        | ?                                                                                                          |
| `async send(self, to_handle, text, meta=None)`          | ?                                                                                                              |

### 

- ****`_payload_to_request`payloadAgentRequest`get_to_handle_from_request` `user_id``get_on_reply_sent_args``_before_consume_process` receive_id`_on_consume_error` `send_content_parts`?**`refresh_webhook_or_token`** token ?
- ****`resolve_session_id``build_agent_request_from_user_content``_message_to_content_parts``send_message_content``send_content_parts``to_handle_from_target`?

?**`consume_one`**?**`get_to_handle_from_request`** / **`get_on_reply_sent_args`**?

### ?

?manager  `consume_one`

```python
# my_channel.py
from agentscope_runtime.engine.schemas.agent_schemas import TextContent, ContentType
from gepaw.app.channels.base import BaseChannel
from gepaw.app.channels.schema import ChannelType

class MyChannel(BaseChannel):
    channel: ChannelType = "my_channel"

    def __init__(self, process, enabled=True, bot_prefix="", **kwargs):
        super().__init__(process, on_reply_sent=kwargs.get("on_reply_sent"))
        self.enabled = enabled
        self.bot_prefix = bot_prefix

    @classmethod
    def from_config(cls, process, config, on_reply_sent=None, show_tool_details=True):
        return cls(process=process, enabled=getattr(config, "enabled", True),
                   bot_prefix=getattr(config, "bot_prefix", ""), on_reply_sent=on_reply_sent)

    @classmethod
    def from_env(cls, process, on_reply_sent=None):
        return cls(process=process, on_reply_sent=on_reply_sent)

    def build_agent_request_from_native(self, native_payload):
        payload = native_payload if isinstance(native_payload, dict) else {}
        channel_id = payload.get("channel_id") or self.channel
        sender_id = payload.get("sender_id") or ""
        meta = payload.get("meta") or {}
        session_id = self.resolve_session_id(sender_id, meta)
        text = payload.get("text", "")
        content_parts = [TextContent(type=ContentType.TEXT, text=text)]
        request = self.build_agent_request_from_user_content(
            channel_id=channel_id, sender_id=sender_id, session_id=session_id,
            content_parts=content_parts, channel_meta=meta,
        )
        request.channel_meta = meta
        return request

    async def start(self):
        pass

    async def stop(self):
        pass

    async def send(self, to_handle, text, meta=None):
        #  HTTP API ?
        pass
```

?native `_enqueue` ?manager 

```python
native = {
    "channel_id": "my_channel",
    "sender_id": "user_123",
    "text": "",
    "meta": {},
}
self._enqueue(native)
```

###  + ///?

?`build_agent_request_from_native` ?runtime ?content `build_agent_request_from_user_content`?

```python
from agentscope_runtime.engine.schemas.agent_schemas import (
    TextContent, ImageContent, VideoContent, AudioContent, FileContent, ContentType,
)

def build_agent_request_from_native(self, native_payload):
    payload = native_payload if isinstance(native_payload, dict) else {}
    channel_id = payload.get("channel_id") or self.channel
    sender_id = payload.get("sender_id") or ""
    meta = payload.get("meta") or {}
    session_id = self.resolve_session_id(sender_id, meta)
    content_parts = []
    if payload.get("text"):
        content_parts.append(TextContent(type=ContentType.TEXT, text=payload["text"]))
    for att in payload.get("attachments") or []:
        t = (att.get("type") or "file").lower()
        url = att.get("url") or ""
        if not url:
            continue
        if t == "image":
            content_parts.append(ImageContent(type=ContentType.IMAGE, image_url=url))
        elif t == "video":
            content_parts.append(VideoContent(type=ContentType.VIDEO, video_url=url))
        elif t == "audio":
            content_parts.append(AudioContent(type=ContentType.AUDIO, data=url))
        else:
            content_parts.append(FileContent(type=ContentType.FILE, file_url=url))
    if not content_parts:
        content_parts = [TextContent(type=ContentType.TEXT, text="")]
    request = self.build_agent_request_from_user_content(
        channel_id=channel_id, sender_id=sender_id, session_id=session_id,
        content_parts=content_parts, channel_meta=meta,
    )
    request.channel_meta = meta
    return request
```

###  CLI

- ****?`custom_channels/`?`~/.gepaw/custom_channels/`Manager ?`.py`  `__init__.py` ?`BaseChannel` ?`channel` ?
- ****`gepaw channels install <key>`  `custom_channels/` ?`<key>.py` ?`--path <>` ?`--url <URL>` ?`gepaw channels add <key>` ?config ?`--path`/`--url`?
- ****`gepaw channels remove <key>`  `custom_channels/`  `--no-keep-config` `config.json` ?`channels` ?key?
- **Config**`ChannelConfig`  `extra="allow"``config.json` ?`channels` ?key?extra `gepaw channels config` ?config?

### HTTP 

?Webhook SlackLINE  `register_app_routes` ?HTTP  gepaw ?

gepaw  `custom_channels/` ?`register_app_routes`  FastAPI `app` ?

****?

|  |                      |
| -------- | ------------------------ |
| `/api/`  |                  |
|  |  |

** ?`register_app_routes(app)`**

- ****`app` ?FastAPI 
- ****None
- **?* startup/shutdown 
- ****

** ?Echo **?

```
<workspace>/
 custom_channels/
     my_echo/
         __init__.py
```

```python
# custom_channels/my_echo/__init__.py
from gepaw.app.channels.base import BaseChannel

class MyEchoChannel(BaseChannel):
    """?""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def _listen(self):
        pass  #  HTTP 

    async def _send(self, target, content, **kwargs):
        self.logger.info(f"Would send to {target}: {content}")


def register_app_routes(app):
    """ HTTP ?""

    @app.post("/api/my-echo/callback")
    async def echo_callback(request):
        """Webhook ?""
        body = await request.json()

        from gepaw.app.channels.base import TextContent
        channel = MyEchoChannel()
        channel.enqueue_user_message(
            user_id=body.get("user_id", "anonymous"),
            session_id=body.get("session_id", "default"),
            content=[TextContent(type="text", text=body.get("text", ""))],
        )

        return {"status": "ok"}
```

 `agent.json`?

```json
{
  "channels": {
    "my_echo": {
      "enabled": true
    }
  }
}
```



```bash
curl -X POST http://localhost:8088/api/my-echo/callback \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "session_id": "test", "text": "Hello!"}'
```

****?ClawBot [PR #2140](https://github.com/agentscope-ai/gepaw/pull/2140)[Issue #2043](https://github.com/agentscope-ai/gepaw/issues/2043)?`/api/wechat/callback` ?SDK ?

---

## 

- [](./intro) ??
- [](./quickstart) ??
- [](./heartbeat) ?/
- [CLI](./cli) ?initappcronclean
- [](./config) ??
