# 

gepaw  Agent ?** ?**  `config.json` ?

## 

gepaw ?

```
:
  (Tool Guard) ??
?  YAML  Shell 
?
  (File Guard) ?
?  Agent ?
?
  (Skill Scanner) ?
   ?
```

****: Web  ?

****:

- ****  YAML  Shell ?
- **** ?
- **** 
- **Web ** (? ?

---

## 

****?Agent ****,,?

### 

1. ?Agent ??**`execute_shell_command`**?**YAML **()?**`ShellEvasionGuardian`**(??
2. ?:
   - `rm -rf /` ??
   - SQL 
   -  `$(...)` ?`` `...` ``(Shell ?
   -  `../`
   -  `sudo``su`
   -  ShellFork Unicode ?
     (?YAML Shell ?
3. (CRITICALHIGHMEDIUMLOWINFO)
4. ?CRITICAL ?HIGH ?,,???????`denied_tools` ?

### 

?`config.json` ?

```json
{
  "security": {
    "tool_guard": {
      "enabled": true,
      "guarded_tools": null,
      "denied_tools": [],
      "custom_rules": [],
      "disabled_rules": [],
      "shell_evasion_checks": {
        "command_substitution": false,
        "obfuscated_flags": false,
        "backslash_escaped_whitespace": false,
        "backslash_escaped_operators": false,
        "newlines": false,
        "comment_quote_desync": false,
        "quoted_newline": false
      }
    }
  }
}
```

|                    |                                                                                                                                                                                                                                                                                                                                        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `enabled`              |  `gepaw_TOOL_GUARD_ENABLED` (??                                                                                                                                                                                                                                              |
| `guarded_tools`        | :<br>?`null`() ??br>?`[]` ??br>?`["tool_a", "tool_b"]` ?                                                                                                                                                                                                               |
| `denied_tools`         | :?***?,??                                                                                                                                                                                                                                                      |
| `custom_rules`         | ???                                                                                                                                                                                                                                                                                                          |
| `disabled_rules`       |  YAML  ID ( `TOOL_CMD_*` )?                                                                                                                                                                                                                                                                              |
| `shell_evasion_checks` | Shell ?key ,value ?`true`/`false`?*(`false`)?* ? ? ? ? key:`command_substitution``obfuscated_flags``backslash_escaped_whitespace``backslash_escaped_operators``newlines``comment_quote_desync``quoted_newline`?|

#### ?

 JSON :

```json
{
  "id": "CUSTOM_RULE_ID",
  "tools": ["execute_shell_command"],
  "params": ["command"],
  "category": "command_injection",
  "severity": "HIGH",
  "patterns": ["pattern1", "pattern2"],
  "exclude_patterns": ["safe_pattern"],
  "description": "?,
  "remediation": ""
}
```

|                |             |    |                                                     |
| ------------------ | --------------- | ------ | ------------------------------------------------------- |
| `id`               | string          | **?* | ?)              |
| `tools`            | string ?array | ?    | ??          |
| `params`           | string ?array | ?    | ?"      |
| `category`         | string          | **?* | (?                                |
| `severity`         | string          | **?* | : `CRITICAL``HIGH``MEDIUM``LOW` ?`INFO` |
| `patterns`         | array           | **?* | ()              |
| `exclude_patterns` | array           | ?    | ()          |
| `description`      | string          | ?    | ?                                         |
| `remediation`      | string          | ?    | ?                             |

****: `command_injection``data_exfiltration``path_traversal``sensitive_file_access``network_abuse``credential_exposure``resource_abuse``prompt_injection``code_execution``privilege_escalation`

**?*:

```json
{
  "security": {
    "tool_guard": {
      "enabled": true,
      "custom_rules": [
        {
          "id": "BLOCK_PRODUCTION_DB_ACCESS",
          "tools": ["execute_shell_command"],
          "params": ["command"],
          "category": "sensitive_file_access",
          "severity": "CRITICAL",
          "patterns": ["psql.*prod", "mysql.*production"],
          "description": "?,
          "remediation": ""
        },
        {
          "id": "WARN_NPM_GLOBAL_INSTALL",
          "tools": ["execute_shell_command"],
          "params": ["command"],
          "category": "resource_abuse",
          "severity": "MEDIUM",
          "patterns": ["npm\\s+install\\s+-g", "npm\\s+i\\s+-g"],
          "exclude_patterns": ["npm\\s+install\\s+-g\\s+(typescript|eslint)"],
          "description": " npm ",
          "remediation": "?
        }
      ]
    }
  }
}
```

### approval_level?

 Agent ?`approval_level` (?`agent.json` ?,:

|        |                                          |
| ---------- | -------------------------------------------- |
| **STRICT** |                |
| **SMART**  | ?      |
| **AUTO**   | ()       |
| **OFF**    | ?Agent ??|

?`agent.json` ?

```json
{
  "approval_level": "AUTO"
}
```

?** ??* ?Agent ?

### ?

 ** ? ?** ,?

![tool guard](https://img.alicdn.com/imgextra/i1/O1CN01aAqcPv290Ldjj8NNi_!!6000000008005-2-tps-3822-2070.png)

- **/** ???
- **** ??
- **** ?,
- **** ??
  - **** ??
  - **?* ???
  - **** ?
- **** ??"?****

### 

? `execute_shell_command` ):

**HIGH**

|  ID                       | ?                |                                |
| ----------------------------- | ------------------------ | ---------------------------------- |
| `TOOL_CMD_DANGEROUS_RM`       | `rm`                 |  |
| `TOOL_CMD_DANGEROUS_MV`       | `mv`                 | ?      |
| `TOOL_CMD_UNSAFE_PERMISSIONS` | `chmod -R 777``chattr` |        |

**CRITICAL**

|  ID                   | ?                         |                            |
| ------------------------- | --------------------------------- | ------------------------------ |
| `TOOL_CMD_FS_DESTRUCTION` | `mkfs``dd of=/dev/` |  |

**CRITICAL/HIGH**

|  ID                    |  | ?                                       |                          |
| -------------------------- | -------- | ----------------------------------------------- | ---------------------------- |
| `TOOL_CMD_DOS_FORK_BOMB`   | CRITICAL | Fork  `:(){ :\|:& };:``kill -9 -1`        | ?Fork ?|
| `TOOL_CMD_SYSTEM_REBOOT`   | CRITICAL | `reboot``shutdown``halt``init 0/6`        |                  |
| `TOOL_CMD_SERVICE_RESTART` | HIGH     | `systemctl restart/stop``service ... restart` | ?          |
| `TOOL_CMD_PROCESS_KILL`    | HIGH     | `pkill``killall``kill`?`kill $$`?   | ?          |

**CRITICAL/HIGH**

|  ID                       |  | ?                                                                      |                                                       |
| ----------------------------- | -------- | ------------------------------------------------------------------------------ | --------------------------------------------------------- |
| `TOOL_CMD_PIPE_TO_SHELL`      | CRITICAL | `curl/wget ... \| bash/sh`                                                 | ?                                   |
| `TOOL_CMD_OBFUSCATED_EXEC`    | HIGH     | `base64 -d \| bash`                                                        |  base64 ?                                   |
| `TOOL_CMD_IFS_INJECTION`      | HIGH     | `$IFS``${...IFS...}`                                                         | ?token,?            |
| `TOOL_CMD_CONTROL_CHARS`      | CRITICAL | ??NUL ?                                                      | ?                               |
| `TOOL_CMD_UNICODE_WHITESPACE` | HIGH     | NBSP Unicode                                                   |  Bash                   |
| `TOOL_CMD_PROC_ENVIRON`       | HIGH     | `/proc/self/environ``/proc/<pid>/environ`                                    | ??,           |
| `TOOL_CMD_JQ_SYSTEM`          | HIGH     | ?`system(` ?`jq`                                                           | ?jq ?Shell                                |
| `TOOL_CMD_JQ_FILE_FLAGS`      | HIGH     | `jq` ?`-f`/`--from-file``--rawfile``--slurpfile``-L``--library-path` |  jq                           |
| `TOOL_CMD_ZSH_DANGEROUS`      | HIGH     | `zmodload``emulate ... -c``sysopen`/`zpty`/`ztcp``zf_*``fc ... -e` ? | zsh ?I/O,?|

**CRITICAL/HIGH**

|  ID                         |  | ?                                    |                                |
| ------------------------------- | -------- | -------------------------------------------- | ---------------------------------- |
| `TOOL_CMD_PRIVILEGE_ESCALATION` | CRITICAL | `sudo``su``doas``pkexec`               |                |
| `TOOL_CMD_SYSTEM_TAMPERING`     | HIGH     | `crontab``authorized_keys``/etc/sudoers` | SSH ?sudo  |

**CRITICAL**

|  ID                  | ?                          |                       |
| ------------------------ | ---------------------------------- | ------------------------- |
| `TOOL_CMD_REVERSE_SHELL` | `/dev/tcp``nc -e``socat EXEC:` |  Shell ?|

### Shell 

?`execute_shell_command`  **`ShellEvasionGuardian`**??`` ` ```$()`Zsh `$'...'`/`$"..."`  shell  `find ... -exec ... {} \;`  `\r` ?heredoc`#` ? ID( **HIGH**):

|  ID                              |                                                     |
| ------------------------------------ | ------------------------------------------------------- |
| `SHELL_EVASION_COMMAND_SUBSTITUTION` | ?`'`...`'` /?       |
| `SHELL_EVASION_OBFUSCATED_FLAGS`     | ANSI-C/?|
| `SHELL_EVASION_BACKSLASH_WHITESPACE` |                         |
| `SHELL_EVASION_BACKSLASH_OPERATOR`   |  `; \| & < >` ?                       |
| `SHELL_EVASION_NEWLINE`              |                 |
| `SHELL_EVASION_COMMENT_QUOTE_DESYNC` |  `#` ,      |
| `SHELL_EVASION_QUOTED_NEWLINE`       |  `#` ?                    |

**:** `config.json`  `disabled_rules`  YAML  ID( `TOOL_CMD_*`),**?* `SHELL_EVASION_*`Shell  `shell_evasion_checks` (??)?

****:

- CRITICAL ,?
- HIGH ?
-  `disabled_rules` ?YAML `TOOL_CMD_*` 
-  `shell_evasion_checks`  Shell ?)
-  `custom_rules` ?

---

## 

**** Agent ?***???

### 

"?,?

1. **** ??`tool_guard.enabled = false`), `file_guard.enabled = true`,?
2. **?* ??
   - ****(`read_file``write_file``edit_file` ? ??`file_path` 
   - **Shell **(`execute_shell_command`) ????`>``>>``<`)
   - **** ??
3. **?* ?`~` ,
4. **** ??`/` ?
5. **** ???HIGH ?

****: `{WORKING_DIR}.secret/` ( API ?,`WORKING_DIR` ?`~/.gepaw/`,?`~/.gepaw.secret/`?

### 

?`config.json` ?

```json
{
  "security": {
    "file_guard": {
      "enabled": true,
      "sensitive_files": ["~/.ssh/", "/etc/passwd", "~/.gepaw.secret/"]
    }
  }
}
```

|               |                                                                                                                                                                                  |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `enabled`         | ?: `true`)?                                                                                                                          |
| `sensitive_files` | /?<br>?: `/etc/passwd`<br>?: `secrets/api_keys.json`<br>?: `~/.ssh/`<br>?: ?`/`  |

****:

- 
- `~` 
- ?
- (?`/` )?

### ?

 ** ? ?** ,?

![file guard](https://img.alicdn.com/imgextra/i4/O1CN01EqUuWs1sPDgDvsbeV_!!6000000005758-2-tps-3822-2070.png)

- **/** ???
- **** ??
  - ?
  - ?
  - 
- ****:
  - 
  - ?`~`)
  - ?`/` ?
  - ?Enter ""
- **** ?
- **** ??" `config.json`;****
- **** ?""?

---

## 

****,,?

### 

1. **** ?,:
   - ?
   - ?
   - ?Skill Hub ?
2. ****:
   -  YAML ?
   - ?PatternAnalyzer),?
   - ?ScanPolicy)?
3. **** ?(mtime),?
4. **** ?( 30 ?
5. ****:
   - ,
   - 
   - (?

### 

|              |                                                                      |
| ---------------- | ------------------------------------------------------------------------ |
| **(Block)**  | ,?           |
| **?Warn)** | ?,?) |
| **(Off)**    | ,?                                         |

**?*:  `gepaw_SKILL_SCAN_MODE` > ?> `config.json`

? `block``warn``off`

### 

??****:

- **** ?""?
  - ?
  - ?
  - ?
- **?* ?"",
- **** ?"?
- **** ?""?

:

- ?
- (??
- 
- 

### ?

****:

- ?
  - ?
  - SHA-256 (?
  - 
- **** ??,??
- **?* ??

?

- ?
- ??
- ?

### ?

 ** ? ?** ,?

![skill scanner](https://img.alicdn.com/imgextra/i4/O1CN01c4UGLh1Yd9PbL2bZC_!!6000000003081-2-tps-3822-2070.png)

**?*:

- **** ?""???"
- **** ??5-300?,?

**?* ():

![alarm](https://img.alicdn.com/imgextra/i1/O1CN013IUVEk26x1X9MtFen_!!6000000007727-2-tps-3822-2070.png)

- 
- 
- 
- ?
- ""

**** ():

![white list](https://img.alicdn.com/imgextra/i3/O1CN01aQ0miE1kzO1vB34Vu_!!6000000004754-2-tps-3822-2070.png)

- ?
- ??6)?
- ??

****: ****,?

### ?)

,?

?`src/gepaw/security/skill_scanner/rules/signatures/`  YAML  YAML ?

```python
from gepaw.security.skill_scanner import SkillScanner
from gepaw.security.skill_scanner.scan_policy import ScanPolicy

policy = ScanPolicy.from_yaml("my_org_policy.yaml")
scanner = SkillScanner(policy=policy)
```

:

- `command_injection` ?
- `data_exfiltration` ?
- `hardcoded_secrets` ??
- `prompt_injection` ??
- `social_engineering` ?
- `supply_chain_attack` ??
- `obfuscation` ?
- `resource_abuse` ?
- `unauthorized_tool_use` ??

#### YAML 

 YAML ?

```yaml
# my_custom_signatures.yaml
- id: CUSTOM_API_KEY_LEAK
  category: hardcoded_secrets
  severity: CRITICAL
  patterns:
    - "api_key\\s*=\\s*['\"][a-zA-Z0-9]{32,}['\"]"
    - "API_KEY\\s*=\\s*['\"][a-zA-Z0-9]{32,}['\"]"
  exclude_patterns:
    - "example"
    - "test_api_key"
    - "<your_api_key_here>"
  file_types: [python, javascript, typescript]
  description: "?API "
  remediation: "?

- id: CUSTOM_DANGEROUS_NETWORK_CALL
  category: data_exfiltration
  severity: HIGH
  patterns:
    - "requests\\.post\\([^)]*attacker\\.com"
    - "urllib\\.request\\.urlopen\\([^)]*suspicious"
  file_types: [python]
  description: "?
  remediation: "?
```

****:

|                |    |    |                                                                       |
| ------------------ | ------ | ------ | ------------------------------------------------------------------------- |
| `id`               | string | **?* | ?)                                |
| `category`         | string | **?* | (?                                                      |
| `severity`         | string | **?* | : `CRITICAL``HIGH``MEDIUM``LOW` ?`INFO`                   |
| `patterns`         | array  | **?* | ()                                |
| `exclude_patterns` | array  | ?    | ()                                                    |
| `file_types`       | array  | ?    | : `python``javascript``typescript``bash``json` ?|
| `description`      | string | ?    | ?                                                           |
| `remediation`      | string | ?    | ?                                                       |

****:

- 
-  `exclude_patterns` ?
-  `file_types` ?
- ?`severity: MEDIUM` ??

### 

?`config.json` 

```json
{
  "security": {
    "skill_scanner": {
      "mode": "block",
      "timeout": 30,
      "whitelist": []
    }
  }
}
```

---

## 

 `config.json` :

```json
{
  "security": {
    "tool_guard": {
      "enabled": true,
      "guarded_tools": null,
      "denied_tools": ["execute_shell_command"],
      "custom_rules": [
        {
          "id": "CUSTOM_DANGEROUS_PATTERN",
          "tools": ["write_file"],
          "params": ["content"],
          "category": "data_exfiltration",
          "severity": "HIGH",
          "patterns": ["secret_key.*=", "password.*="],
          "description": "",
          "remediation": "?
        }
      ],
      "disabled_rules": ["TOOL_CMD_PROCESS_KILL"]
    },
    "file_guard": {
      "enabled": true,
      "sensitive_files": [
        "~/.ssh/",
        "~/.gepaw.secret/",
        "/etc/passwd",
        "/etc/shadow",
        ".env",
        "secrets/"
      ]
    },
    "skill_scanner": {
      "mode": "warn",
      "timeout": 30,
      "whitelist": []
    }
  }
}
```

****:

- ?)
- ??
- Docker ? `/app/working/config.json`

---

## Web 

gepaw  Web ,?***, `gepaw_AUTH_ENABLED` ?

![login](https://img.alicdn.com/imgextra/i4/O1CN01VdXCuP1tWpsl0TlQ5_!!6000000005910-2-tps-3822-2070.png)

### 

1. **** ? `gepaw_AUTH_ENABLED=true` ?gepaw
2. ****:
   - ??***
   - (?+ )
   - ?
3. ****:
   - ?****
   - ?(?7 ?
   -  localStorage,?API 
4. ****(?:
   -  `gepaw_AUTH_USERNAME` ?`gepaw_AUTH_PASSWORD` 
   - gepaw ,
   - ?DockerKubernetes
5. **?* ?(`127.0.0.1` / `::1`)?CLI (`gepaw app``gepaw chat` ?

**?*:

-  SHA-256 ,?
- HMAC-SHA256 ,7 ?
- ?Python ?`hashlib``hmac``secrets`),?
- `auth.json` ?`0o600` ()

### 

|                     |                          |  |
| ----------------------- | ---------------------------- | -------- |
| `gepaw_AUTH_ENABLED`  |  `true`          | **?*   |
| `gepaw_AUTH_USERNAME` |  | ?    |
| `gepaw_AUTH_PASSWORD` | ?  | ?    |

### ?

?`config.json` ?`security.allow_no_auth_hosts`  API  IP :

```json
{
  "security": {
    "allow_no_auth_hosts": ["127.0.0.1", "::1"]
  }
}
```

|                   |           | ?                |                                                          |
| --------------------- | ------------- | ---------------------- | ------------------------------------------------------------ |
| `allow_no_auth_hosts` | array[string] | `["127.0.0.1", "::1"]` |  `/api/*`  IP ?|

?** ?** ?

> ****: ?localhost  IP  API,?

****:

- `gepaw_AUTH_ENABLED=true` 
- `gepaw_AUTH_USERNAME` ?`gepaw_AUTH_PASSWORD` :
  -  ?()
  -  ?(?
- ,

### 

####  / pip 

:

**Linux / macOS:**

```bash
# ()
export gepaw_AUTH_ENABLED=true
gepaw app

# ? 
export gepaw_AUTH_ENABLED=true
export gepaw_AUTH_USERNAME=admin
export gepaw_AUTH_PASSWORD=mypassword
gepaw app
```

,?`export`  `~/.bashrc``~/.zshrc` ?

**Windows (CMD):**

```cmd
set gepaw_AUTH_ENABLED=true
rem ? 
rem set gepaw_AUTH_USERNAME=admin
rem set gepaw_AUTH_PASSWORD=mypassword
gepaw app
```

**Windows (PowerShell):**

```powershell
$env:gepaw_AUTH_ENABLED = "true"
# ? 
# $env:gepaw_AUTH_USERNAME = "admin"
# $env:gepaw_AUTH_PASSWORD = "mypassword"
gepaw app
```

#### Docker

 `-e` ?):

```bash
docker run -e gepaw_AUTH_ENABLED=true \
  -e gepaw_AUTH_USERNAME=admin \
  -e gepaw_AUTH_PASSWORD=mypassword \
  -p 127.0.0.1:8088:8088 \
  -v gepaw-data:/app/working \
  -v gepaw-secrets:/app/working.secret \
  -v gepaw-backups:/app/working.backups \
  agentscope/gepaw:latest
```

> ****: , `gepaw_AUTH_USERNAME` ?`gepaw_AUTH_PASSWORD`,?

#### docker-compose.yml

```yaml
services:
  gepaw:
    image: agentscope/gepaw:latest
    ports:
      - "127.0.0.1:8088:8088"
    environment:
      - gepaw_AUTH_ENABLED=true
      - gepaw_AUTH_USERNAME=admin
      - gepaw_AUTH_PASSWORD=mypassword
    volumes:
      - gepaw-data:/app/working
      - gepaw-secrets:/app/working.secret
      - gepaw-backups:/app/working.backups
```

####  (.env)

?`.env` ?

```
gepaw_AUTH_ENABLED=true
gepaw_AUTH_USERNAME=admin
gepaw_AUTH_PASSWORD=mypassword
```

 `--env-file .env`  Docker?`gepaw app`  shell ?source ?

### 

 gepaw?

```bash
# Linux / macOS
unset gepaw_AUTH_ENABLED
gepaw app

# Docker ? -e ?
docker run -p 127.0.0.1:8088:8088 -v gepaw-data:/app/working -v gepaw-secrets:/app/working.secret -v gepaw-backups:/app/working.backups agentscope/gepaw:latest
```

### 

, CLI :

```bash
gepaw auth reset-password
```

:

1. 
2. ?,)
3.  JWT ,**?* ??

**Docker **:

```bash
docker exec -it <? gepaw auth reset-password
```

****:

:

```bash
# 
rm ~/.gepaw.secret/auth.json  # ?$WORKING_DIR.secret/auth.json
#  gepaw,?
gepaw app
```

### ?

?*?*:

- ?localStorage 
- ?
- ?

**?*:

- (7 )
- (?
- ?401 ?

### 

| ?          |                                                                                   |
| -------------- | ------------------------------------------------------------------------------------- |
|        |  SHA-256 ?`auth.json`                                   |
|        | HMAC-SHA256 ? ?                                                       |
|        | ?localStorage 401 ?                                   |
|        | ???Python `hashlib``hmac``secrets`?                            |
|        | `auth.json` ?`0o600` ?                                    |
| ?    |  `127.0.0.1` / `::1` CLI ?                          |
| CORS       | `OPTIONS`                                                         |
| WebSocket  |                                                     |
| ?    | ?`/api/*` ?                                                             |
|        | `/api/auth/login``/api/auth/register``/api/auth/status``/api/version`?|
