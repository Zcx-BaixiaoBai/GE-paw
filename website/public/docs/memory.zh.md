# 

**** ?gepaw ?Markdown ?

> ?[OpenClaw](https://github.com/openclaw/openclaw)
>  [ReMe](https://github.com/agentscope-ai/ReMe) ?**ReMeLight** ?Markdown
> ?

---

## 

```mermaid
graph TB
    User[ / Agent] --> MM[MemoryManager]
    MM --> MemoryMgmt[]
    MemoryMgmt --> FileTools[]
    MemoryMgmt --> Watcher[]
    MemoryMgmt --> SearchLayer[]
    FileTools --> LTM[MEMORY.md]
    FileTools --> DailyLog[memory/YYYY-MM-DD.md]
    Watcher --> Index[]
    SearchLayer --> VectorSearch[]
    SearchLayer --> BM25[BM25 ]
```

?

|            |                                                                                     |
| -------------- | --------------------------------------------------------------------------------------- |
| **?* | `read` / `write` / `edit` Markdown ?|
| ****   |  `watchfile` ?& ?               |
| ****   |  + BM25 ?                                       |
| ****   | ?Memory Markdown                  |
| ****   | ?MEMORY.md?                             |

---

## 

?Markdown Agent 

```
{}/
 MEMORY.md              ?Auto-Dream
?  
?
 memory/                ?Auto-Memory?
?   2026-04-20.md
?   2026-04-21.md      ?Auto-Dream
?   ...
?
 backup/                ?Auto-Dream?
     memory_backup_20260421_230000.md
     ...                ??
```

### MEMORY.md

?

- ****`{working_dir}/MEMORY.md`
- **?*?
- ****Agent  `write` / `edit`  **Auto-Dream** 

### memory/YYYY-MM-DD.md

?

- ****`{working_dir}/memory/YYYY-MM-DD.md`
- **?*?
- ****Agent  `write` / `edit` ?
- ****?**Auto-Dream** 

### backup/

 Auto-Dream  MEMORY.md ?

- ****`{working_dir}/backup/`
- **?*?Auto-Dream ?
- ****`memory_backup_YYYYMMDD_HHMMSS.md`

>  Auto-MemoryAuto-DreamAuto-Memory-Search ?Proactive
>  [](./memory-evolving-and-proactive.zh.md)?

---

## 

Agent ?

|      |             |                            |                         |
| -------- | --------------- | ---------------------------------- | --------------------------- |
|  | `memory_search` | ?| "?    |
|  | `read_file`     |    |  `memory/2025-02-13.md` |

### ?

** + BM25 ?*?

#### 



|                    |                        |                      |
| ---------------------- | ---------------------------------- | -------------------------------- |
| ""     | " PostgreSQL  MySQL" |  |
| "" | "?       | ??    |
| ""   | "P99 ?800ms ?200ms"    |  ?    |

**?token**  token ?

#### BM25 ?

 token ?

|                        | BM25 ?           | BM25 ?                   |
| -------------------------- | ---------------------- | ------------------------------ |
| `handleWebSocketReconnect` | ?| "WebSocket " |
| `ECONNREFUSED`             | ?| ""             |

****?

```
base_score =  / ?          #  [0, 1]
phrase_bonus = 0.2
score = min(1.0, base_score + phrase_bonus)  #  1.0
```

?`"? "`  "? ?"" ??`base_score = 2/3 ?0.67` ?
`score = 0.67`

>  ChromaDB `$contains` ?

#### ?

?BM25 ****?`0.7`BM25  `0.3`

1. ****?`candidate_multiplier`?3  200?
2. **** BM25 
3. **** chunk `path + start_line + end_line`?
   -  ?`final_score = vector_score  0.7`
   -  BM25  ?`final_score = bm25_score  0.3`
   - **?* ?`final_score = vector_score  0.7 + bm25_score  0.3`
4. **** `final_score` ?top-N 

****?`"handleWebSocketReconnect "`

|                                                |  | BM25  |                        |  |
| ------------------------------------------------------ | -------- | --------- | ------------------------------ | ---- |
| "handleWebSocketReconnect  WebSocket " | 0.85     | 1.0       | 0.850.7 + 1.00.3 = **0.895** | 1    |
| ""                         | 0.78     | 0.0       | 0.780.7 = **0.546**           | 2    |
| "?handleWebSocketReconnect "         | 0.40     | 0.5       | 0.400.7 + 0.50.3 = **0.430** | 3    |

```mermaid
graph LR
    Query[] --> Vector[ x0.7]
    Query --> BM25[BM25 ?x0.3]
    Vector --> Merge[?chunk  + ]
    BM25 --> Merge
    Merge --> Sort[]
    Sort --> Results[ top-N ]
```

> ****?

---

## 

### 

 `agent.json` ?`running.reme_light_memory_config` 

| ?                         |                                                                         | ?        |
| ------------------------------- | --------------------------------------------------------------------------- | -------------- |
| `summarize_when_compact`        |  `summary_memory` ?       | `true`         |
| `auto_memory_interval`          |  N null                     | `null`         |
| `dream_cron`                    | ?Cron ?                         | `"0 23 * * *"` |
| `rebuild_memory_index_on_start` | ?`false`  | `false`        |
| `recursive_file_watcher`        | ?`memory/subdirectory/*`?               | `false`        |

### 

?`running.reme_light_memory_config.auto_memory_search_config` 

| ?       |                                         | ? |
| ------------- | ------------------------------------------- | ------- |
| `enabled`     |             | `false` |
| `max_results` | ?                 | `1`     |
| `min_score`   | 0.0 ~ 1.0?| `0.1`   |
| `timeout`     | ?                     | `10.0`  |

### Embedding 

Embedding ?`running.reme_light_memory_config.embedding_model_config`?

| ?            |                                   | ?  |
| ------------------ | ------------------------------------- | -------- |
| `backend`          | Embedding                     | `openai` |
| `api_key`          | Embedding ?API Key              | ``       |
| `base_url`         | Embedding ?URL                  | ``       |
| `model_name`       | Embedding                     | ``       |
| `dimensions`       | ?       | `1024`   |
| `enable_cache`     |  Embedding                | `true`   |
| `use_dimensions`   | ?API ?dimensions  | `false`  |
| `max_cache_size`   | Embedding               | `3000`   |
| `max_input_length` |  Embedding ?          | `8192`   |
| `max_batch_size`   | Embedding ?             | `10`     |

> `use_dimensions`  vLLM ?dimensions  `false` ?

#### Fallback?

?fallback?

|                |                      | ?|
| ---------------------- | ------------------------ | ------ |
| `EMBEDDING_API_KEY`    | Embedding ?API Key | ``     |
| `EMBEDDING_BASE_URL`   | Embedding ?URL     | ``     |
| `EMBEDDING_MODEL_NAME` | Embedding        | ``     |

> `base_url` ?`model_name` `api_key` ?

### ?

 `FTS_ENABLED`  BM25 

|       |              | ?|
| ------------- | ---------------- | ------ |
| `FTS_ENABLED` | ?| `true` |

> ?Embedding BM25 ?

### ?

 `MEMORY_STORE_BACKEND` ?

|                |                                                    | ?|
| ---------------------- | ------------------------------------------------------ | ------ |
| `MEMORY_STORE_BACKEND` | ?`auto``local``chroma``sqlite` | `auto` |

**?*

|      |                                                                          |
| -------- | ---------------------------------------------------------------------------- |
| `auto`   | Windows  `local`?`chroma`                        |
| `local`  | ?                                      |
| `chroma` | Chroma ?Windows ?core dump |
| `sqlite` | SQLite ?+  macOS 14          |

> **** `auto` ?

---

##  Memory Backend

gepaw ?Backend  ReMeLight `memory_manager_backend` ?

### ADBPGAnalyticDB for PostgreSQL?

?

**?*

- **** ??
- **?* ??ADBPG  LLM 
- **?API ** ? SQL ?REST API 
- **** ?ADBPG  Agent 

**?*

 Agent  `adbpg` `adbpg_memory_config` ?API ?

![adbpg-backend](https://img.alicdn.com/imgextra/i3/O1CN01bH1Rj41wwQs3v04U6_!!6000000006372-2-tps-2954-1484.png)

>  ?gepaw ?

#### REST 

 HTTP API  ADBPG  Python ?

ADBPG TabAPI ?`REST API` `REST Base URL` ?`REST API Key`?

![adbpg-rest-mode](https://img.alicdn.com/imgextra/i4/O1CN01gTvYJI238hAc4fcvr_!!6000000007211-2-tps-2996-1478.png)

| ?            |                                                    | ?  |
| ------------------ | ------------------------------------------------------ | -------- |
| `api_mode`         | API ?`"rest"`                                | `"rest"` |
| `rest_base_url`    | ADBPG ?REST API                          | `""`     |
| `rest_api_key`     | REST API ?                                   | `""`     |
| `memory_isolation` | `true` ?Agent `false` ?| `true`   |
| `search_timeout`   | ?                                | `10.0`   |

#### SQL 

 psycopg2  ADBPG `pip install gepaw[adbpg]`?

ADBPG TabAPI ?`SQL (Direct)` /  / ?/  / ?LLMEmbedding ?

![adbpg-sql-mode](https://img.alicdn.com/imgextra/i2/O1CN01K8Og0P27WkQvGWHvZ_!!6000000007805-2-tps-2988-1498.png)

| ?              |                             | ? |
| -------------------- | ------------------------------- | ------- |
| `api_mode`           | API ?`"sql"`          | `"sql"` |
| `host`               | ADBPG                 | `""`    |
| `port`               | ?                     | `5432`  |
| `user`               |                     | `""`    |
| `password`           | ?                     | `""`    |
| `dbname`             | ?                     | `""`    |
| `llm_model`          |  LLM ?| `""`    |
| `llm_api_key`        | LLM ?API Key              | `""`    |
| `llm_base_url`       | LLM ?Base URL             | `""`    |
| `embedding_model`    | Embedding               | `""`    |
| `embedding_api_key`  | Embedding ?API Key        | `""`    |
| `embedding_base_url` | Embedding ?Base URL       | `""`    |
| `embedding_dims`     |                         | `1024`  |
| `memory_isolation`   |                     | `true`  |
| `search_timeout`     | ?         | `10.0`  |
| `pool_minconn`       |                 | `1`     |
| `pool_maxconn`       |                 | `5`     |

**?*

?`agent.json` ?`running.adbpg_memory_config` ?

```json
{
  "running": {
    "memory_manager_backend": "adbpg",
    "adbpg_memory_config": {
      "host": "gp-xxxxxxxxx-master.gpdb.rds.aliyuncs.com",
      "port": 5432,
      "user": "your_db_user",
      "password": "your_db_password",
      "dbname": "your_db_name",
      "llm_model": "qwen-plus",
      "llm_api_key": "sk-xxxxxxxx",
      "llm_base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
      "embedding_model": "text-embedding-v3",
      "embedding_api_key": "sk-xxxxxxxx",
      "embedding_base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
      "embedding_dims": 1024,
      "api_mode": "sql",
      "rest_api_key": "",
      "rest_base_url": "",
      "memory_isolation": true,
      "search_timeout": 10.0,
      "pool_minconn": 1,
      "pool_maxconn": 5
    }
  }
}
```

>   Console ?`agent.json`?

---

## 

- [](./memory-evolving-and-proactive.zh.md) ?Auto-MemoryAuto-DreamAuto-Memory-SearchProactive ?
- [](./intro.zh.md) ??
- [](./console.zh.md) ??
- [Skills](./skills.zh.md) ?
- [](./config.zh.md) ??config
