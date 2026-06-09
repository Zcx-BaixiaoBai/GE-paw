<p align="center">
  <img src="https://raw.githubusercontent.com/agentscope-ai/gepaw/main/plugins/bundle/cloudpaw/docs/cloudpaw.png" alt="CloudPaw" width="360" />
</p>

<p align="center">
  <strong>gepaw ?/strong>
</p>

<p align="center">
  <a href="https://github.com/agentscope-ai/CloudPaw/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License" /></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python" /></a>
  <a href="#"><img src="https://img.shields.io/badge/version-0.0.2-green.svg" alt="Version" /></a>
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README_zh.md"></a> | <b>?/b> | <a href="README_ru.md"></a>
</p>

---

CloudPaw ?gepaw ?*gepaw + Aliyun CLI** ?*IaC** ?

CloudPaw ?

- **?*CloudPaw ECS  URL ?
- ****CloudPaw ?
- **API **CloudPaw ?

CloudPaw ?

## 

### 

|  |  |
|------|------|
| **gepaw ?* | **?v1.1.7** |
| **Python** | 3.10 ~ 3.13 |
| **Alibaba Cloud ?* | ?Access Key ?|

> gepaw  [gepaw ](https://gepaw.agentscope.io/docs/quickstart) QwenPaw ?v1.1.7 `pip install --upgrade gepaw>=1.1.7`?

### 1. CloudPaw 

****

1. gepaw `gepaw app`http://127.0.0.1:8088/ ?
2. 
3. 
   - ?URL `https://gepaw-download.oss-ap-southeast-1.aliyuncs.com/files/plugins/cloudpaw/cloudpaw-0.0.2.zip`
   - `cloudpaw/` ZIP CloudPaw ?gepaw v1.1.7+ ?`plugins/bundle/cloudpaw/` 
4. ?

**CLI ?*

```bash
gepaw plugin install /path/to/cloudpaw
# ?URL ?
gepaw plugin install https://gepaw-download.oss-ap-southeast-1.aliyuncs.com/files/plugins/cloudpaw/cloudpaw-0.0.2.zip
```

> ** ?*`Ctrl+Shift+R` / `Cmd+Shift+R`CloudPaw ?UI PRD ?

### 2. 

CloudPaw 

#### ?gepaw ?

 LLM  API Key [gepaw ](https://gepaw.agentscope.io/docs/models) ?

#### ?Alibaba Cloud 

CloudPaw 

- `ALIBABA_CLOUD_ACCESS_KEY_ID` ?Access Key ID
- `ALIBABA_CLOUD_ACCESS_KEY_SECRET` ?Access Key Secret
- `ALIBABA_CLOUD_REGION_ID` ??ID `cn-hangzhou`?

?CLI Access Key  [Alibaba Cloud ](https://help.aliyun.com/document_detail/116401.html) ?Access Key ?

#### ?iac-code ?

CloudPaw ?IaC ?[iac-code](https://github.com/aliyun/iac-code) 0.1.2?*** ?CloudPaw ?gepaw  iac-code ?

CloudPaw  `~/.iac-code/settings.yml` ?`llm_source: gepaw`  iac-code ?gepaw API QwenPaw  iac-code  ??

**** iac-code ?gepaw `IAC_CODE_PROVIDER` gepaw CloudPaw iac-code  [iac-code LLM ](https://aliyun.github.io/iac-code/docs/configuration/llm-providers) ?

### 3. 

 Agent CloudPaw-Master?

> ** ?*
>
> 1. **?*?Alibaba Cloud ?
> 2. **?*?*?*?
> 3. **** AI AI AI AI ?
> 4. ****?

## ?

CloudPaw ?gepaw ?

```
gepaw/
 plugins/
     bundle/
         cloudpaw/           # CloudPaw ?
             plugin.json     # ?
             plugin.py       # ?
             requirements.txt # Python iac-code, httpx-sse?
             ui/             # ?
             skills/         # ?
             tools/          # ?
             modules/        # ?
             agents/         # Agent 
             prompts/        # ?
```

## 

- **IaC **[iac-code](https://github.com/aliyun/iac-code) ?ROS/Terraform ?Alibaba Cloud 
- ****`proposal_choice` 
- **PRD ?*QwenPaw Mission Mode ?PRD `manage_prd` 
- **?Agent **QwenPaw Mission Mode  Agent 
- **Alibaba Cloud Skills  Agent **A2A ?Alibaba Cloud Skills Hub ?Agent 
- **** `iac-code` ?Alibaba Cloud CLI ?

## Alibaba Cloud Skills  Agent 

CloudPaw ?**A2AAgent-to-Agent** ?**Alibaba Cloud Skills Hub** ?Agent  Agent ?

> ****A2A ?CloudPaw Alibaba Cloud Skills Hub ?Agent ?A2A Agent ?

### 

CloudPaw ?A2A Agent ?**2** ?LLM `a2a_call` 

####  1`/a2a` 

?`/a2a` ?Agent ?

```
/a2a <? <?
```



```
/a2a my-agent Node.js  ECS 
```

?LLM `a2a_call` ?

####  2

LLM ?Agent `a2a_call` ?

```
my-agent ?Flask  Alibaba Cloud 
```

LLM  Agent ?

####  Agent ?

?`/a2a` ?A2A Agent ?`/skills` ?

### 

- A2A ?CloudPaw Alibaba Cloud Skills Hub ?Agent ?A2A Agent ?
-  Agent  ??
-  A2A  1 ?

## ?Agent ?

CloudPaw ?gepaw ?**Mission Mode**  Agent  Agent ?Agent  PRD Agent ?

| Agent |  |
|---|---|
| **CloudPaw-Master** | PRD ?|
| **CloudPaw-Executor** | CLI  |
| **CloudPaw-Verifier** | ?|
| **iac-code**?ACP Agent?| IaC ACP ROS/Terraform ?|

## ?

****

> Alibaba Cloud ECS ?

**API **

> API ?/health ?/hello  URL ?

## 

- [iac-code](https://github.com/aliyun/iac-code) ?Alibaba Cloud  AI Infrastructure as Code 
