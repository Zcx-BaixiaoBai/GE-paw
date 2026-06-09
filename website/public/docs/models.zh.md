# 

?gepaw gepaw ?** -> ** ?

![](https://img.alicdn.com/imgextra/i1/O1CN01mi22sP1uCyJu22bLc_!!6000000006002-2-tps-3822-2070.png)

gepaw  LLM 

- **?*llama.cpp / Ollama / LM Studio?
- ****?API Key?
- ****

gepaw ?

- [gepaw Local (llama.cpp)](https://github.com/ggml-org/llama.cpp)
- [Ollama](https://ollama.com/)
- [LM Studio](https://lmstudio.ai/)

 gepaw Local (llama.cpp) ?gepaw Ollama ?LM Studio ?

gepaw ?gepaw-Flash ?2B?B ?9B ?4 bit ?8 bit  [ModelScope](https://www.modelscope.cn/organization/AgentScope?tab=model) ?[Hugging Face](https://huggingface.co/agentscope-ai/models) ?gepaw-Flash?

## gepaw Local (llama.cpp) 

> gepaw Local  GPU ?GPU ?Ollama ?LM Studio ?

gepaw Local ?llama.cpp ?**** ?

![gepaw Local ](https://img.alicdn.com/imgextra/i4/O1CN01eFCOm91cn0Ofu4v4r_!!6000000003644-2-tps-3822-2070.png)

 gepaw Local  llama.cpp  ** llama.cpp** QwenPaw ?llama.cpp ?gepaw Local ?

![ llama.cpp](https://img.alicdn.com/imgextra/i2/O1CN01zN4QFs1RGyvkxM8lE_!!6000000002085-2-tps-1550-1308.png)

gepaw QwenPaw-Flash CPU / NVIDIA GPU / Apple M  gepaw-Flash _ ID_  __  ID ?ModelScope / Hugging Face  `Qwen/Qwen3-0.6B-GGUF`?ModelScope ?Hugging Face ?

![](https://img.alicdn.com/imgextra/i2/O1CN01io6OUC1kBvFn3RA8U_!!6000000004646-2-tps-1346-1694.png)

 ****  gepaw ?

![](https://img.alicdn.com/imgextra/i2/O1CN01Nl0aQb1a3XqqosqAC_!!6000000003274-2-tps-1342-1682.png)

 **** ?

![](https://img.alicdn.com/imgextra/i4/O1CN01u6zmTW1lCfW2lsXAh_!!6000000004783-2-tps-1354-1796.png)

gepaw Local  gepaw gepaw Local  gepaw ?

## Ollama 

?Ollama  [Ollama](https://ollama.com/download)?Context Length ?32k?

![Ollama ](https://gw.alicdn.com/imgextra/i4/O1CN01pWWxlV1QiApLwDzbU_!!6000000002009-2-tps-1912-1510.png)

 Ollama ?gepaw Ollama  **** ?**** ?gepaw ?Ollama ?

> ?gepaw ?Docker ?Ollama ?Docker ?Ollama  `docker run` ?`--add-host=host.docker.internal:host-gateway` API ?`http://host.docker.internal:11434` ?

 Ollama ?gepaw-Flash `Q8_0` ?`Q4_K_M` 

1. ?[ModelScope](https://www.modelscope.cn/organization/AgentScope?tab=model) ?[Hugging Face](https://huggingface.co/agentscope-ai/models)  gepaw-Flash ?`AgentScope/gepaw-Flash-4B-Q4_K_M`?

ModelScope CLI?

```bash
modelscope download --model AgentScope/gepaw-Flash-4B-Q4_K_M --local_dir ./dir
```

Hugging Face CLI?

```bash
hf download agentscope-ai/gepaw-Flash-4B-Q4_K_M --local_dir ./dir
```

2. ?`gepaw-flash.txt`?`/path/to/your/gepaw-xxx.gguf` ?`.gguf` ?

```text
FROM /path/to/your/gepaw-xxx.gguf
TEMPLATE {{ .Prompt }}
RENDERER qwen3.5
PARSER qwen3.5
PARAMETER presence_penalty 1.5
PARAMETER temperature 1
PARAMETER top_k 20
PARAMETER top_p 0.95
```

3.  Ollama?

```bash
ollama create gepaw-flash -f gepaw-flash.txt
```

4.  gepaw ?Ollama  ****  gepaw?

Ollama  gepaw Ollama  **** ?****  Ollama ?**** ?

![Ollama ](https://img.alicdn.com/imgextra/i3/O1CN01cxqKOB1siui8vYlvp_!!6000000005801-2-tps-1504-1720.png)

## LM Studio 

?LM Studio  [LM Studio](https://lmstudio.ai/download)?

LM Studio ?API  LM Studio ?**Developer -> Local Server**  API  `http://localhost:1234`?

![LM Studio ](https://gw.alicdn.com/imgextra/i3/O1CN01kLXu3D1VwRF3lokZz_!!6000000002717-2-tps-1654-1256.png)

 gepaw  LM Studio ?**Settings -> Model Defaults**  **Default Context Length** ?32768?**Settings -> Developer**  **Experimental Settings**  "When applicable, separate `reasoning_content` and `content` in API responses" ?

![LM Studio ](https://gw.alicdn.com/imgextra/i4/O1CN011jc2q71hc51etcf7x_!!6000000004297-2-tps-1654-1256.png)

![LM Studio ](https://gw.alicdn.com/imgextra/i4/O1CN01dInPGl1oDX6nOH0Wh_!!6000000005191-2-tps-1654-1256.png)

 LM Studio  gepaw LM Studio  **** ?LM Studio ?API ?LM Studio ?**Developer -> Local Server**  `/v1`?`http://localhost:1234/v1`?

 LM Studio ?gepaw-Flash `Q8_0` ?`Q4_K_M` 

1. ?[ModelScope](https://www.modelscope.cn/organization/AgentScope?tab=model) ?[Hugging Face](https://huggingface.co/agentscope-ai/models)  gepaw-Flash ?`AgentScope/gepaw-Flash-4B-Q4_K_M`?

ModelScope CLI?

```bash
modelscope download --model AgentScope/gepaw-Flash-4B-Q4_K_M --local_dir ./dir
```

Hugging Face CLI?

```bash
hf download agentscope-ai/gepaw-Flash-4B-Q4_K_M --local_dir ./dir
```

2. ?`.gguf`  LM Studio?

```bash
lms import /path/to/your/gepaw-xxx.gguf -c -y --user-repo AgentScope/gepaw-Flash
```

3.  gepaw ?LM Studio  ****  gepaw?

?Ollama ?**** ?gepaw ?LM Studio ?LM Studio ?**** ?LM Studio ?**** ?

> ?gepaw ?Docker ?LM Studio ?Docker ?LM Studio  `docker run` ?`--add-host=host.docker.internal:host-gateway` API ?`http://host.docker.internal:1234/v1` ?

## 

gepaw 

- ModelScope
- DashScope
- Aliyun Coding Plan
- OpenRouter
- OpenAI
- Azure OpenAI
- Anthropic
- Google Gemini
- DeepSeek
- Kimi
- MiniMax
- Zhipu
- SiliconFlow
- OpenCode

> ?API 

![](https://img.alicdn.com/imgextra/i2/O1CN010o2p2y1Qj5cbfpqto_!!6000000002011-2-tps-3826-2076.png)

?API ?API Key ?

![ API Key](https://img.alicdn.com/imgextra/i1/O1CN01dIMlx51XuizaWQOqA_!!6000000002984-2-tps-1170-862.png)

 API Key  ****  API Key ?

![](https://img.alicdn.com/imgextra/i3/O1CN01PCK2ai1fpFBDiqPAp_!!6000000004055-2-tps-1218-1060.png)

 **** ?

![](https://img.alicdn.com/imgextra/i3/O1CN01fmAwzz1l0lDanBi4b_!!6000000004757-2-tps-1278-1394.png)

 **** ?** ID**API  ****  **** ?

![](https://img.alicdn.com/imgextra/i1/O1CN014GTNqr1t4tipsb3OF_!!6000000005849-2-tps-1260-1588.png)

## 

gepaw ?

### ?

?** ->  -> ?*  **?* ?**?ID**?gepaw ?**?* ?API ?OpenAI `chat.completions`  Anthropic `messages` ?

![](https://img.alicdn.com/imgextra/i3/O1CN01palLpz1fGtTWePlTS_!!6000000003980-2-tps-3826-2076.png)

### ?

?****  API ?_ URL_  _API _ ?

![](https://img.alicdn.com/imgextra/i1/O1CN01qwzsQy1ch3FTHnNaq_!!6000000003631-2-tps-3826-2076.png)

### 

 **** ?**** ?** ID**API  ****  **** ?

> ?vLLM ?vLLM ?`http://localhost:8000`?vLLM  `/path/to/Qwen3.5`  API ?OpenAI `chat.completions` URL ?`http://localhost:8000/v1` ID  `/path/to/Qwen3.5`?`Qwen3.5` gepaw ?vLLM ?

## 

?** ->  ->  LLM**  **** ?gepaw QwenPaw ?

![](https://img.alicdn.com/imgextra/i2/O1CN01yvndw51U9904SNmLx_!!6000000002474-2-tps-3804-968.png)

gepaw ?**** gepaw ?

![](https://img.alicdn.com/imgextra/i3/O1CN01UpOvxZ1MlbKYCtNAv_!!6000000001475-2-tps-3826-2076.png)

## 

### 

gepaw  `$gepaw_SECRET_DIR/providers` ?`~/.gepaw.secret/providers`?`builtin` ?`custom` ?JSON  ID ID ?`Qwen`  `Qwen.json` API ?gepaw ?

### 

?gepaw Local (llama.cpp) gepaw  `$gepaw_WORKING_DIR/local_models` ?`~/.gepaw/local_models` llama.cpp 

- **?*?`$gepaw_WORKING_DIR/local_models/bin` ?llama.cpp  gepaw ?llama.cpp  llama.cpp ?
- **?* `$gepaw_WORKING_DIR/local_models/models` ?ID?ID ?`Qwen/Qwen3-0.6B-GGUF` ?`$gepaw_WORKING_DIR/local_models/models/Qwen/Qwen3-0.6B-GGUF` GGUF  GGUF  `models` ?`?` ?GGUF ?gepaw Local  gepaw Local  `Qwen3-0.6B.gguf` ?`$gepaw_WORKING_DIR/local_models/models/Qwen/Qwen3-0.6B-GGUF/Qwen3-0.6B.gguf`?
- ****?`$gepaw_WORKING_DIR/local_models/logs`  llama.cpp  `llama-server.log` ?

### 

 `temperature`?`top_p`?`max_tokens`gepaw ?**** ****?JSON 

```json
{
  "temperature": 0.7,
  "top_p": 0.9,
  "max_tokens": 4096
}
```

?****QwenPaw ?

![](https://img.alicdn.com/imgextra/i2/O1CN01XreaTi1VPSj9sMQtp_!!6000000002645-2-tps-1170-1476.png)
