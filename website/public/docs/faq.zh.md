# FAQ 

?

---

### gepaw ?OpenClaw ?

?[](/docs/comparison) ?

### gepaw

gepaw ?[](https://gepaw.agentscope.io/docs/quickstart)?

1.  Python 

```
# macOS / Linux:
curl -fsSL https://gepaw.agentscope.io/install.sh | bash
# WindowsPowerShell?
irm https://gepaw.agentscope.io/install.ps1 | iex
# pip?
```

2. pip 

Python?>= 3.10?3.14

```
pip install gepaw
```

3. Docker 

Docker http://127.0.0.1:8088/ ?

```
docker pull agentscope/gepaw:latest
docker run -p 127.0.0.1:8088:8088 \
  -v gepaw-data:/app/working \
  -v gepaw-secrets:/app/working.secret \
  -v gepaw-backups:/app/working.backups \
  agentscope/gepaw:latest
```

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
>      - ?`Win + R`?`sysdm.cpl` ?
>      -  ?-> ?
>      - ?? `Path`??
>      -  ?
>
> 2. **?PowerShell?ps1**
>
>  **** `uv`?
>
> - **uv**?[GitHub Release](https://github.com/astral-sh/uv/releases)`uv.exe``%USERPROFILE%\.local\bin``%USERPROFILE%\AppData\Local\uv` Python `python -m pip install -U uv`
> - **`uv`**`uv` `%USERPROFILE%\.gepaw\bin`  `Path` ?
> - ****?`gepaw` ?
> - **`gepaw`** `%USERPROFILE%\.gepaw\bin`  `Path` ?

### gepaw

?gepaw ?

1. ?

2.  pip 

```
gepaw update
```

3. ?

```
cd gepaw
git pull origin main
cd console && npm ci && npm run build
cd .. && mkdir -p src/gepaw/console
cp -R console/dist/. src/gepaw/console/
pip install -e .
```

4. ?Docker?

```
docker pull agentscope/gepaw:latest
docker run -p 127.0.0.1:8088:8088 \
  -v gepaw-data:/app/working \
  -v gepaw-secrets:/app/working.secret \
  -v gepaw-backups:/app/working.backups \
  agentscope/gepaw:latest
```

5. exe/zip?
   -  gepaw
   - https://gepaw.agentscope.io/downloads
   - 

?gepaw app?

?CoPaw  gepaw gepaw  CoPaw ?

### gepaw

?

```bash
gepaw init --defaults
```

?

```bash
gepaw app
```

?`http://127.0.0.1:8088/`[](https://gepaw.agentscope.io/docs/quickstart)?

### Windows  8088 

?Windows Hyper-V ?WSL2  gepaw ?**8088** pip Docker?

**?*

- `Address already in use` ?`OSError: [Errno 98] Address already in use`
- `An attempt was made to access a socket in a way forbidden by its access permissions`
- gepaw ?`http://127.0.0.1:8088/`

**?8088 ?Windows ?*

?PowerShell ?CMD 

```powershell
netsh interface ipv4 show excludedportrange protocol=tcp
```

 8088 ?

**?*

**pip  / ?*

```bash
gepaw app --port 8090
```

 `http://127.0.0.1:8090/`?

**Docker ?*

```bash
docker run -p 127.0.0.1:8090:8088 \
  -v gepaw-data:/app/working \
  -v gepaw-secrets:/app/working.secret \
  -v gepaw-backups:/app/working.backups \
  agentscope/gepaw:latest
```

 `http://127.0.0.1:8090/`?

**Windows ?*

 8088 

1.  `gepaw app --port 8090`
2.  Windows ?8088

**?Windows  8088 **

?PowerShell 

```powershell
#  8088
netsh int ipv4 set dynamicport tcp start=49152 num=16384
#  Windows ?
```

>  ****?

### WSL2 NAT ?APITimeoutError 

?WSL2 ?gepaw  NAT  Windows ?VPN

```
agent error: APITimeoutError: Request timed out.
```

**?* WSL2 ?MTU?500 NAT  VPN ?

**?* ?WSL2 ?MTU ?**1350**?

1. **?WSL2 ?MTU?*

   ```bash
   ip link show eth0 | grep mtu
   ```

2. ** MTU ?1350**

   ```bash
   sudo ip link set eth0 mtu 1350
   ```

3. **** ??`/etc/wsl.conf` 

   ```ini
   [boot]
   command = /sbin/ip link set eth0 mtu 1350
   ```

   ?PowerShell ?CMD ?WSL2?

   ```powershell
   wsl --shutdown
   ```

4. ****?

   ```bash
   ip link show eth0 | grep mtu
   # ? mtu 1350
   ```

gepaw ?

### 

gepaw ?
`https://github.com/agentscope-ai/gepaw`

### ?

 [](https://gepaw.agentscope.io/release-notes/?lang=zh) ?gepaw GitHub  [Releases](https://github.com/agentscope-ai/gepaw/releases) ?

### 

 ** ?**  [](https://gepaw.agentscope.io/docs/models)?

-  API Key ModelScopeDashScope ?
- ?`llama.cpp`LM Studio ?Ollama?

?** LLM** ?

 **** ?

?`gepaw models` ?[CLI ???gepaw models](https://gepaw.agentscope.io/docs/cli#gepaw-models)?

###  gepaw-Flash 

gepaw-Flash ?gepaw  gepaw ?2B, 4B ?9B  4 bit ?8 bit ?

gepaw-Flash ?[ModelScope](https://www.modelscope.cn/organization/AgentScope?tab=model)  [Hugging Face](https://huggingface.co/agentscope-ai/models) ?

gepaw  gepaw-Flash ?

**gepaw Local (llama.cpp)**

?gepaw Local  gepaw-Flash ?

![Start Model](https://img.alicdn.com/imgextra/i2/O1CN01Nl0aQb1a3XqqosqAC_!!6000000003274-2-tps-1342-1682.png)

> gepaw Local  GitHub  issue ?
>  gepaw Local Ollama ?LM Studio  gepaw-Flash ?

**Ollama**:

1. ?[ModelScope](https://www.modelscope.cn/organization/AgentScope?tab=model) ?[Hugging Face](https://huggingface.co/agentscope-ai/models)  gepaw-Flash ?`Q8_0` ?`Q4_K_M`?[gepaw-Flash-4B-Q4_K_M](https://www.modelscope.cn/models/AgentScope/gepaw-Flash-4B-Q4_K_M)?

   -  ModelScope CLI ?

     ```bash
     modelscope download --model AgentScope/gepaw-Flash-4B-Q4_K_M README.md --local_dir ./dir
     ```

   -  Hugging Face CLI ?

     ```bash
     hf download agentscope-ai/gepaw-Flash-4B-Q4_K_M --local_dir ./dir
     ```

2. ?[Ollama](https://ollama.com/download)  Ollama ?

3.  Ollama ?`ollama create` ?Ollama?

 `gepaw-flash.txt` `/path/to/your/gepaw-xxx.gguf` ?gepaw-Flash ?`.gguf` 

```
FROM /path/to/your/gepaw-xxx.gguf
TEMPLATE {{ .Prompt }}
RENDERER qwen3.5
PARSER qwen3.5
PARAMETER presence_penalty 1.5
PARAMETER temperature 1
PARAMETER top_k 20
PARAMETER top_p 0.95
```

?

```bash
ollama create gepaw-flash -f gepaw-flash.txt
```

4. ?gepaw  Ollama ?

**LM Studio**:

1. ?Ollama ?1  gepaw-Flash ?

2. ?[LM Studio](https://lmstudio.ai/)  LM Studio ?

3.  LM Studio?

```bash
lms import /path/to/your/gepaw-xxx.gguf -c -y --user-repo AgentScope/gepaw-Flash
```

4. ?gepaw  LM Studio ?

###  Ollama / LM Studio ?gepaw 

 gepaw **?*?

 Ollama ?LM Studio ?`context length` QwenPaw 

- 
- 
- 
- ?

**?*

-  gepaw ?`context length` ?* 32K**
- ** 32K**

>  ** gepaw ?32K **
>
>  Ollama ?LM Studio  gepaw  **32K ?* ?
>
>  / ?

**Ollama **

![Ollama context length ](https://img.alicdn.com/imgextra/i3/O1CN01JrqRjE1l6FxuO3IMl_!!6000000004769-2-tps-699-656.png)

**LM Studio **

![LM Studio context length ](https://img.alicdn.com/imgextra/i4/O1CN01LWyG6o21E4Zovqv4G_!!6000000006952-2-tps-923-618.png)

### 

 ** ?** ?

![cron](https://img.alicdn.com/imgextra/i2/O1CN018UMwzM1stRomiHjJt_!!6000000005824-2-tps-3822-2064.png)

gepawgepawQwenPaw?



1.  gepaw ?

2. ?**?* ?**?*?

   ![enable](https://img.alicdn.com/imgextra/i2/O1CN01K16c611eHWOs6GKlQ_!!6000000003846-2-tps-3236-888.png)

3. ?**DispatchChannel** ?consoledingtalkfeishudiscordimessage ?

   ![channel](https://img.alicdn.com/imgextra/i3/O1CN01G55gOc1YvveHrxqTY_!!6000000003122-2-tps-3234-876.png)

4. **DispatchTargetUserID** ?**DispatchTargetSessionID** ?

   ![id](https://img.alicdn.com/imgextra/i1/O1CN01iohIk41N0G0CN6sVq_!!6000000001507-2-tps-3234-874.png)

    ** ?**?**UserID** ?**SessionID**  **DispatchTargetUserID** ?**DispatchTargetSessionID** ?

   ![id](https://img.alicdn.com/imgextra/i1/O1CN01svdDS41a2d3fqShLx_!!6000000003272-2-tps-3236-1068.png)

5.  **Cron?*?

   ![cron](https://img.alicdn.com/imgextra/i3/O1CN01BtYIqK1Xb1xdYmcai_!!6000000002941-2-tps-3242-892.png)

6. ?****?gepaw ?

   ![exec](https://img.alicdn.com/imgextra/i3/O1CN01a1IIsY1PhQZ5YXlCe_!!6000000001872-2-tps-3232-890.png)

### Skill

?**???*? Skills Hub ?[Skills](https://gepaw.agentscope.io/docs/skills)?

### MCP

?**??MCP**?MCP ///?[MCP](https://gepaw.agentscope.io/docs/mcp)?

### 

1. You didn't provide an API key

?

Error: Unknown agent error: AuthenticationError: Error code: 401 - {'error': {'message': "You didn't provide an API key. You need to provide your API key in an Authorization header using Bearer auth (i.e. Authorization: Bearer YOUR_KEY). ", 'type': 'invalid_request_error', 'param': None, 'code': None}, 'request_id': 'xxx'}

1?API key?API key?*?? ?**?

2 key  `base_url``api key` ?

gepaw  Coding Plan ?API key

- `base_url` ?
- API key 
- ?


https://help.aliyun.com/zh/model-studio/coding-plan-quickstart#2531c37fd64f9

---

### 

 gepaw ?GitHub  [issue](https://github.com/agentscope-ai/gepaw/issues)?

?

Error: Unknown agent error: AuthenticationError: Error code: 401 - {'error': {'message': "You didn't provide an API key. You need to provide your API key in an Authorization header using Bearer auth (i.e. Authorization: Bearer YOUR_KEY). ", 'type': 'invalid_request_error', 'param': None, 'code': None}, 'request_id': 'xxx'}(Details: /var/folders/.../gepaw_query_error_qzbx1mv1.json)

`/var/folders/.../gepaw_query_error_qzbx1mv1.json`?gepaw ?
