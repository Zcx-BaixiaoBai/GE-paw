# ?

 gepaw?

|        |                  |                          |          |
| -------------- | ------------------------ | ---------------------------- | ---------------- |
| **pip **   |  Python ?    | ?  | Python 3.10~3.13 |
| ****   |  |  Python  | ?              |
| **Docker**     |      | ?          | Docker           |
| **?ECS** |              |            | ?      |
| **?* | ?    |  |          |
| ****   | ?      |          | ?              |

>  ?[](./intro) [](./console)?

>  **?*?
>
> 1.  [](./console)`http://127.0.0.1:8088/`?
> 2. **** ? ? API Key ?
> 3. ?
> 4. QQ ?app  [](./channels)

---

## pip 

 Python  Python >= 3.10, < 3.14

```bash
pip install gepaw
```

`python -m venv .venv`Linux/macOS ?
`source .venv/bin/activate`Windows ?`.venv\Scripts\Activate.ps1`?`gepaw` ?

?[](#) ?[](#? ?

### ?

 `~/.gepaw` `config.json` ?`HEARTBEAT.md`

- ****
  ```bash
  gepaw init --defaults
  ```
- ****?Skills
  ```bash
  gepaw init
  ```
   [CLI - ](./cli#??

 `gepaw init --force`?
QQ ?[](./channels) ?

### 

```bash
gepaw app
```

 `127.0.0.1:8088`gepaw  app ?

---

## 

 Python ? [uv](https://docs.astral.sh/uv/) ?

### ?

**macOS / Linux?*

```bash
curl -fsSL https://gepaw.agentscope.io/install.sh | bash
```

?`source ~/.zshrc` / `source ~/.bashrc`?

**Windows (CMD):**

```cmd
curl -fsSL https://gepaw.agentscope.io/install.bat -o install.bat && install.bat
```

**WindowsPowerShell**

```powershell
irm https://gepaw.agentscope.io/install.ps1 | iex
```

 gepaw  PATH?

> ** Windows ?LTSC **
>
> ?Windows LTSC PowerShell ?**** 
>
> 1. **?CMD?bat`Path`**
>
>     **** ?
>
>    - ****?
>      - ?`uv`  CMD ?`uv --version` ** gepaw **?`'uv' `?
>      - uv`uv``%USERPROFILE%\.local\bin``%USERPROFILE%\AppData\Local\uv`?Python  `Scripts` ?
>      - gepaw?`%USERPROFILE%\.gepaw\bin` ?
>    - ** Path **?
>      - ?`Win + R`?`sysdm.cpl` "??
>      -  "" -> ""?
>      - ?""  `Path`?""?
>      -  ""?
>
> 2. **?PowerShell?ps1**
>
>  **** `uv`?
>
> - **uv**?[GitHub Release](https://github.com/astral-sh/uv/releases)`uv.exe``%USERPROFILE%\.local\bin``%USERPROFILE%\AppData\Local\uv` Python `python -m pip install -U uv`
> - **`uv`**`uv` `%USERPROFILE%\.gepaw\bin`  `Path` ?
> - ****?`gepaw` ?
> - **`gepaw`** `%USERPROFILE%\.gepaw\bin`  `Path` ?

?

**macOS / Linux?*

```bash
# 
curl -fsSL ... | bash -s -- --version 1.1.0

# ?
curl -fsSL ... | bash -s -- --from-source
```

**WindowsPowerShell**

```powershell
# 
.\install.ps1 -Version 0.0.2

# ?
.\install.ps1 -FromSource
```

 `gepaw uninstall`?

### ?

 `~/.gepaw` `config.json` ?`HEARTBEAT.md`

- ****
  ```bash
  gepaw init --defaults
  ```
- ****?Skills
  ```bash
  gepaw init
  ```
   [CLI - ](./cli#??

 `gepaw init --force`?
QQ ?[](./channels) ?

### 

```bash
gepaw app
```

 `127.0.0.1:8088`gepaw  app ?

---

## Docker

?**Docker Hub**`agentscope/gepaw`?tag`latest``pre`PyPI ?ACR`agentscope-registry.ap-southeast-1.cr.aliyuncs.com/agentscope/gepaw`tag ?



```bash
docker pull agentscope/gepaw:latest
docker run -p 127.0.0.1:8088:8088 \
  -v gepaw-data:/app/working \
  -v gepaw-secrets:/app/working.secret \
  -v gepaw-backups:/app/working.backups \
  agentscope/gepaw:latest
```

 **http://127.0.0.1:8088/**  Skills ?`gepaw-data`  API Key ?`gepaw-secrets`  `gepaw-backups` ?API Key  `docker run`  `-e DASHSCOPE_API_KEY=xxx` ?`--env-file .env`?

---

##  ECS

 gepaw  ECS 

1.  [gepaw ?ECS ](https://computenest.console.aliyun.com/service/instance/create/cn-hangzhou?type=user&ServiceId=service-1ed84201799f40879884)?
2. ?

?[gepaw 3  AI ](https://developer.aliyun.com/article/1713682)?

---

## ?

 Python gepaw 

1.  [](https://modelscope.cn/register?back=%2Fhome) 
2.  [gepaw ](https://modelscope.cn/studios/fork?target=AgentScope/gepaw)?

**** ****?gepaw ?

---

## 

?gepaw  Python ?

### 

- ?**?* Python ?
- ?**?*?Windows 10+ ?macOS 14+ ( Apple Silicon)
- ?**?*

### ?

1. **?*
    [GitHub Releases](https://github.com/agentscope-ai/gepaw/releases) 

   - Windows: `gepaw-Setup-<version>.exe`
   - macOS: `gepaw-<version>-macOS.zip`

2. **?*

   - **Windows**:  `.exe` ?
   - **macOS**:  `.zip`  `gepaw.app`""?

3. ****
   ?10-60  Python ?

### 

 **[](./desktop)** ?

- Windows  vs Debug 
- macOS ?
- ?
- ?

---

## 

? HTTP  Agent  **POST** `/api/agent/process`, JSON, SSE ?

```bash
curl -N -X POST "http://localhost:8088/api/agent/process" \
  -H "Content-Type: application/json" \
  -d '{"input":[{"role":"user","content":[{"type":"text","text":""}]}],"session_id":"session123"}'
```

 `session_id` ?

---

## 

### 

#### ?1. ?

gepaw ?

** A?API Key?*

1.  ** ?**
2.  DashScopeModelScope 
3.  **** ?**API Key**
4.  ****
5. ?** LLM** ?
6.  ****

 [ - ](./models)?

** B API Key**

1. ?

- gepaw Localllama.cpp?gepaw Local  `llama.cpp`?[ - ](./models)?
- Ollama [Ollama ](https://ollama.com/download)  Ollama Ollama ?
- LM Studio [LM Studio ](https://lmstudio.ai/download)  LM Studio LM Studio ?

2. ?

-  gepaw Localllama.cpp GGUF  `~/.gepaw/local_models/models/<org>/<model>`?`~/.gepaw/local_models/models/Qwen/Qwen3-0.6B-GGUF`?
-  Ollama ?LM Studio?gepaw ?

3. 

?** LLM**  **** ?

####  2. 

?****  gepaw ?

---

### ?



####  

QQDiscordiMessage ?app  gepaw ?

1.  ** ?**
2. 
3.  [](./channels) ?
4.  app ?gepaw

####  ?

 gepaw PDF Office 

-  **??** ?**???*
-  Skill Hub ?
-  [Skills](./skills)

####   MCP 

 MCPModel Context Protocol

-  **??MCP**
-  MCP ?
-  [MCP](./mcp)

#### ??

?gepaw ?

- ****?** ?** ?[CLI](./cli) ?`gepaw cron` 
- **** [](./heartbeat)

####  

?

-  ** ??* ?
- 
- 
-  [](./multi-agent)

####  

?[](./config)?
