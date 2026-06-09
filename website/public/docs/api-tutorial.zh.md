# RESTful API 

?RESTful API  gepaw ?Agent?

> ****QwenPaw ?API  AgentScope Runtime 
> [AgentScope Runtime ](https://runtime.agentscope.io/zh/protocol.html)

>  ****?
>  gepaw ?*?*?[Web ](./security#Web-)?
>  Agent?
> ?[Web ](#web-? ?

## 

gepaw ?RESTful API  HTTP ?Agent  API?

-  Agent ?
-  Agent 
- 

## API 

?

```
POST /api/console/chat
```

****?`/api/console/chat` ?`/console/chat`?API  `/api` ?

## 

### Agent ID?

 `X-Agent-Id`  Agent?

```bash
-H "X-Agent-Id: default"
```

** Agent ID**?

1. ?Console ?Agent
2. Agent ID ?Agent 
3. ?Agent ID ?`default`

### Localhost ?

 ****?

- ** `localhost` (127.0.0.1 ?::1)  Web **
-  CLI `gepaw`?
- ?Web **?* `Authorization` 
- ?***?

****?

```bash
#  - ?Authorization 
curl -X POST http://localhost:8088/api/console/chat \
  -H "Content-Type: application/json" \
  -H "X-Agent-Id: default" \
  -d '{"input": [...]}'

#  - ?Authorization 
curl -X POST http://your-server.com:8088/api/console/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "X-Agent-Id: default" \
  -d '{"input": [...]}'
```

> **** [Web ](./security#Web-) [Web ](#web-? ?

## 

API ?OpenAI 

```json
{
  "input": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": ""
        }
      ]
    }
  ],
  "session_id": "my-session",
  "user_id": "user-001",
  "channel": "console"
}
```

### 

- **input**
  - `role`: ?"user"
  - `content`: 
    - `type`: ?"text"
    - `text`: ?
- **session_id**?ID?
- **user_id**?ID
- **channel**?"console"

##  cURL  API

### 

```bash
curl -X POST http://localhost:8088/api/console/chat \
  -H "Content-Type: application/json" \
  -H "X-Agent-Id: default" \
  -d '{
    "input": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "?
          }
        ]
      }
    ],
    "session_id": "my-session",
    "user_id": "my-user",
    "channel": "console"
  }' \
  --no-buffer
```

### 

- **URL**`http://localhost:8088/api/console/chat`?
- **Headers**?
  - `Content-Type: application/json`?JSON 
  - `X-Agent-Id: default`?Agent ID `default`
- **--no-buffer**

### 

```bash
curl -X POST http://localhost:8088/api/console/chat \
  -H "Content-Type: application/json" \
  -H "X-Agent-Id: default" \
  -d '{
    "input": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": ""
          }
        ]
      }
    ],
    "session_id": "my-session-001",
    "user_id": "user-001",
    "channel": "console"
  }' \
  --no-buffer
```

## 

API  **Server-Sent Events (SSE)**  `data:` 

```
data: {"sequence_number":0,"object":"response","status":"created",...}

data: {"sequence_number":1,"object":"response","status":"in_progress",...}

data: {"sequence_number":2,"object":"response","status":"in_progress","output":[{"role":"assistant","content":[{"type":"text","text":"?gepaw..."}]}],...}

data: {"sequence_number":3,"object":"response","status":"completed",...}
```

### 

- **sequence_number**: 
- **object**: ?"response"
- **status**: ?
  - `created`: ?
  - `in_progress`: ?
  - `completed`: ?
  - `failed`: 
- **output**: ?
  - `role`: ?"assistant"
  - `content`: 
    - `type`: 
    - `text`: 
- **error**: ?
- **session_id**:  ID
- **usage**: ?

## 

gepaw  `session_id` ?`user_id`  `session_id`

**?*?

```bash
curl -X POST http://localhost:8088/api/console/chat \
  -H "Content-Type: application/json" \
  -H "X-Agent-Id: default" \
  -d '{
    "input": [
      {
        "role": "user",
        "content": [{"type": "text", "text": "?}]
      }
    ],
    "session_id": "my-session-001",
    "user_id": "user-001",
    "channel": "console"
  }'
```

**?* `session_id`

```bash
curl -X POST http://localhost:8088/api/console/chat \
  -H "Content-Type: application/json" \
  -H "X-Agent-Id: default" \
  -d '{
    "input": [
      {
        "role": "user",
        "content": [{"type": "text", "text": ""}]
      }
    ],
    "session_id": "my-session-001",
    "user_id": "user-001",
    "channel": "console"
  }'
```

****?

- ?`input` ?`session_id` ?
-  `session_id` ?`user_id` ?

## 

### 

#### 405 Method Not Allowed

```
{"detail":"Method Not Allowed"}
```

****?

-  `POST` 
-  URL `/api/console/chat`?`/api` ?

#### 400 Bad Request

```json
{
  "detail": "Validation error"
}
```

****?

- 
-  `input` ?
-  JSON 

#### 404 Agent Not Found

```json
{
  "detail": "Agent not found"
}
```

****?

- ?`X-Agent-Id` ?
- ?Agent  Console ?

#### 503 Channel Not Found

```json
{
  "detail": "Channel Console not found"
}
```

****?

-  Console ?
- ?Console ?Settings ?Channels ?

##  Python 

?`urllib` ?`json`  SSE 

```python
import urllib.request
import json

API_URL = "http://localhost:8088/api/console/chat"
AGENT_ID = "default"
AUTH_TOKEN = ""  # ?token

def chat_with_agent(message, session_id="my-session"):
    # 
    headers = {
        "Content-Type": "application/json",
        "X-Agent-Id": AGENT_ID
    }

    # ?auth token?
    if AUTH_TOKEN:
        headers["Authorization"] = f"Bearer {AUTH_TOKEN}"

    data = {
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            }
        ],
        "session_id": session_id,
        "user_id": "python-user",
        "channel": "console"
    }

    # ?
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )

    # 
    try:
        with urllib.request.urlopen(request) as response:
            for line in response:
                line = line.decode('utf-8').strip()
                if line.startswith('data: '):
                    event_data = json.loads(line[6:])  #  'data: ' 

                    # ?
                    status = event_data.get('status')
                    print(f"? {status}")

                    # 
                    if event_data.get('output'):
                        for item in event_data['output']:
                            if item.get('role') == 'assistant':
                                for content in item.get('content', []):
                                    if content.get('type') == 'text':
                                        print(f": {content.get('text')}")

                    # ?
                    if event_data.get('error'):
                        error = event_data['error']
                        print(f": {error.get('message')}")

    except urllib.error.HTTPError as e:
        print(f"HTTP : {e.code} - {e.read().decode('utf-8')}")
    except Exception as e:
        print(f": {e}")

# 
if __name__ == "__main__":
    chat_with_agent("?)
```

###  requests ?

 `requests` ?

```python
import requests
import json

API_URL = "http://localhost:8088/api/console/chat"
LOGIN_URL = "http://localhost:8088/api/auth/login"
AGENT_ID = "default"

def get_auth_token(username, password):
    """?""
    response = requests.post(LOGIN_URL, json={
        "username": username,
        "password": password
    })
    if response.status_code == 200:
        return response.json()["token"]
    return None

def chat_with_agent(message, session_id="my-session", auth_token=None):
    headers = {
        "Content-Type": "application/json",
        "X-Agent-Id": AGENT_ID
    }

    # ?auth token?
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    data = {
        "input": [
            {
                "role": "user",
                "content": [{"type": "text", "text": message}]
            }
        ],
        "session_id": session_id,
        "user_id": "python-user",
        "channel": "console"
    }

    # 
    with requests.post(API_URL, headers=headers, json=data, stream=True) as response:
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    event_data = json.loads(line[6:])
                    status = event_data.get('status')

                    if status == 'in_progress' or status == 'completed':
                        if event_data.get('output'):
                            for item in event_data['output']:
                                if item.get('role') == 'assistant':
                                    for content in item.get('content', []):
                                        if content.get('type') == 'text':
                                            print(content.get('text'), end='', flush=True)

                    if event_data.get('error'):
                        print(f"\n: {event_data['error'].get('message')}")
                        break

# 
# 1. ?
chat_with_agent("?)

# 2. 
# token = get_auth_token("admin", "admin123")
# chat_with_agent("?, auth_token=token)
```

##  JavaScript 

?Node.js ?`fetch` API?

```javascript
const API_URL = "http://localhost:8088/api/console/chat";
const LOGIN_URL = "http://localhost:8088/api/auth/login";
const AGENT_ID = "default";

// ?
async function getAuthToken(username, password) {
  try {
    const response = await fetch(LOGIN_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (response.ok) {
      const data = await response.json();
      return data.token;
    }
  } catch (error) {
    console.error("Login failed:", error);
  }
  return null;
}

async function chatWithAgent(
  message,
  sessionId = "my-session",
  authToken = null,
) {
  const headers = {
    "Content-Type": "application/json",
    "X-Agent-Id": AGENT_ID,
  };

  // ?auth token?
  if (authToken) {
    headers["Authorization"] = `Bearer ${authToken}`;
  }

  const response = await fetch(API_URL, {
    method: "POST",
    headers,
    body: JSON.stringify({
      input: [
        {
          role: "user",
          content: [
            {
              type: "text",
              text: message,
            },
          ],
        },
      ],
      session_id: sessionId,
      user_id: "js-user",
      channel: "console",
    }),
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split("\n");

    for (const line of lines) {
      if (line.startsWith("data: ")) {
        const eventData = JSON.parse(line.slice(6));

        const status = eventData.status;
        console.log("?", status);

        // 
        if (eventData.output) {
          for (const item of eventData.output) {
            if (item.role === "assistant") {
              for (const content of item.content || []) {
                if (content.type === "text") {
                  console.log(":", content.text);
                }
              }
            }
          }
        }

        // ?
        if (eventData.error) {
          console.error(":", eventData.error.message);
        }
      }
    }
  }
}

// 
// 1. ?
chatWithAgent("?).catch((error) =>
  console.error(":", error),
);

// 2. 
// (async () => {
//   const token = await getAuthToken('admin', 'admin123');
//   if (token) {
//     await chatWithAgent('?, 'my-session', token);
//   }
// })();
```

## ?

1. **** `session_id` 
2. **** API 
3. ****?
4. ****
5. ****
6. ****?API 

## 

### ?Agent 

 Agent  `X-Agent-Id` ?

```bash
# ?Agent 1 
curl -X POST http://localhost:8088/api/console/chat \
  -H "Content-Type: application/json" \
  -H "X-Agent-Id: agent-1" \
  -d '{"input":[{"role":"user","content":[{"type":"text","text":""}]}],"channel":"console"}'

# ?Agent 2 
curl -X POST http://localhost:8088/api/console/chat \
  -H "Content-Type: application/json" \
  -H "X-Agent-Id: agent-2" \
  -d '{"input":[{"role":"user","content":[{"type":"text","text":""}]}],"channel":"console"}'
```

### Web 

?[Web ](./security#Web-)`gepaw_AUTH_ENABLED=true`?API ?

#### 

**?*QwenPaw ?

```bash
curl -X POST http://localhost:8088/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

****?

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "admin"
}
```

****?

```bash
# ?
curl -X POST http://localhost:8088/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123",
    "expires_in": 0
  }'
```

****?

- 
- 
-  `{"detail":"User already registered"}` 
-  `expires_in` ?

**?*?

 1?CLI 

```bash
gepaw auth reset-password
```

 2

```bash
# 
rm ~/.gepaw.secret/auth.json

# ?gepaw_SECRET_DIR 
rm "${gepaw_SECRET_DIR}/auth.json"

#  gepaw ?
gepaw app
```

**Docker **?

```bash
# 
docker exec -it <? rm /app/working.secret/auth.json

# ?CLI 
docker exec -it <? gepaw auth reset-password
```

****?

?gepaw ?

```bash
export gepaw_AUTH_ENABLED=true
export gepaw_AUTH_USERNAME=admin
export gepaw_AUTH_PASSWORD=admin123
gepaw app
```

 API?

#### 

** API **

```bash
curl -X POST http://localhost:8088/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

****?

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "admin"
}
```

****?

 `expires_in` 

```bash
#  30 ?
curl -X POST http://localhost:8088/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123",
    "expires_in": 2592000
  }'

# ?00 ?
curl -X POST http://localhost:8088/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123",
    "expires_in": 0
  }'
```

**?*?

- `604800` = 7 ?
- `2592000` = 30 ?
- `31536000` = 1 ?
- `0` ?`-1` = ?00 

** 2 API ?*

 `token` ?`Authorization` ?

```bash
curl -X POST http://localhost:8088/api/console/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-Agent-Id: default" \
  -d '{
    "input": [
      {
        "role": "user",
        "content": [{"type": "text", "text": ""}]
      }
    ],
    "session_id": "my-session",
    "user_id": "my-user",
    "channel": "console"
  }'
```

#### ?

- **?*?
  - ? ?
  -  `expires_in` ?
  - 100 ?
- ****HMAC-SHA256 
- ****?
- **?*?`127.0.0.1` ?`::1` ?
- **?*?
  -  ?
  - ?
  - 

#### 

?

** 1**?

```bash
# ?
curl -X POST http://localhost:8088/api/auth/revoke-token \
  -H "Authorization: Bearer <YOUR_CURRENT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{}'

# ?
curl -X POST http://localhost:8088/api/auth/revoke-token \
  -H "Authorization: Bearer <YOUR_CURRENT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOi..."
  }'
```

****?

```json
{
  "message": "Current token has been revoked. Please login again.",
  "revoked": true,
  "revoked_current_token": true
}
```

** 2?*?

```bash
curl -X POST http://localhost:8088/api/auth/revoke-all-tokens \
  -H "Authorization: Bearer <YOUR_CURRENT_TOKEN>"
```

****?

```json
{
  "message": "All tokens have been revoked. Please login again.",
  "revoked": true
}
```

** 3?*

 JWT ?

```bash
curl -X POST http://localhost:8088/api/auth/update-profile \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "old_password",
    "new_password": "new_password"
  }'
```

****?

|          |  |                      |                |                |
| ------------ | -------- | ------------------------ | ------------------ | ---------------------- |
|  |      |  | ?  |  |
| ?|      | ?      |  | ?    |
|      |      |    |      |            |
|  |      |      |  |            |

****?

- 
- ?
- 
- `expires_in: 0`?

#### 

?Web ?

** 1?*

```bash
# Linux / macOS
unset gepaw_AUTH_ENABLED
gepaw app

# Windows (CMD)
set gepaw_AUTH_ENABLED=
gepaw app

# Windows (PowerShell)
Remove-Item Env:\gepaw_AUTH_ENABLED
gepaw app
```

** 2Docker **

 `-e gepaw_AUTH_ENABLED=true` ?

```bash
docker run -p 127.0.0.1:8088:8088 \
  -v gepaw-data:/app/working \
  -v gepaw-secrets:/app/working.secret \
  -v gepaw-backups:/app/working.backups \
  agentscope/gepaw:latest
```

****?

- ?API **** `Authorization` 
- **?* `Authorization` 
- `GET /api/auth/status`

## 

### 

 gepaw ?

```bash
# ?
curl http://localhost:8088/api/version
```

### 



1. 
2. ?
3. 

### 

 `MODEL_EXECUTION_FAILED` ?

1. ?Console ?Settings ?Models 
2. ?API Key 
3. 
4. 

## 

- [Console ](./console)
- [](./security)
- [](./multi-agent)
- [](./channels)

## 

 API 

1.  [FAQ](./faq) 
2.  [](./community) 
3. ?GitHub ?[Issue](https://github.com/agentscope-ai/gepaw/issues)
