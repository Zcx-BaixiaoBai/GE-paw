# 

[English](README.md)

 gepaw FastAPI ?HTTP ?
?gepaw app ?, ??
?API key ?

---

## 

```bash
# (~3 )
make test-integration
# ?
pytest tests/integration/ --no-cov

# (PR  /  / )
pytest tests/integration/ -m p0 --no-cov   # ~2 ,PR 
pytest tests/integration/ -m p1 --no-cov   #  / 
pytest tests/integration/ -m p2 --no-cov   # ?

# ?
pytest tests/integration/test_agents.py -v --no-cov

# ?
pytest tests/integration/test_agents.py::test_api_agents_list_create_get_delete -v --no-cov
```

( `pytest-xdist` ?`--no-cov` ;
?[](#??

---

## ?marker

?**?* ,:

> *"??"*
> ??`p1` ?`p2`; ?`p0`?

### `p0` ?(PR )

? PR ?

- **?* ?`/api/messages/send` ?agent 
- **Agent / Chat / Skills  CRUD** ?system
  prompt 
- **** ?MCP CRUDworkspace ?
- ** Guard** ?file guardtool guardskill scanner
- **Tools ** ? agent ?
- **API version** ??

:`pytest -m p0`(?22 ?~2 )?

### `p1` ?? / )

,?

- ** scoped ** ??/
  /Guard ?agent-scoped 
- **Workspace ** ?/ CRUD,zip ,scoped ?
- **ACP / LLM ** ??
- **Plan / Cron** ?
- **** ?token ?agent auth ?
- ** API** ?agent ?

:`pytest -m p1`(?53 ??

### `p2` ?()

,?

- **** ?`*_rejected` (?payload zip )
- **404 ** ?`*_returns_404``missing_*` 
- **** ?
- **** ?`*_isolated_*` agent 
- **HEAD ?* ?`*_minimal_contract`?HEAD
- **?* ?PEP 440 

:`pytest -m p2`(?30 ??

---

## 

|  |  |
|---|---|
| `test_agents.py` | Agent CRUD?|
| `test_chats_global.py` |  `/api/chats`(CRUD? |
| `test_chats_agent_scoped.py` | Agent-scoped chats |
| `test_workspace_files.py` | /zip  |
| `test_workspace_running_config.py` | ? + scoped) |
| `test_workspace_agent_settings.py` | Agent-scoped workspace (prompt? |
| `test_heartbeat.py` | ( + scoped) |
| `test_channels_config.py` |  + / |
| `test_security_config.py` | File guardtool guardskill scanner |
| `test_agent_routing_config.py` | ACPLLM ?|
| `test_skills_global.py` |  skills(CRUD? |
| `test_skills_agent_scoped.py` | Agent-scoped skills |
| `test_mcp.py` | MCP ?|
| `test_messages_files.py` | ?+  |
| `test_plan.py` | Plan  |
| `test_cron.py` | Agent-scoped cron  |
| `test_console.py` | Console (chat stopupload) |
| `test_console_metadata.py` | //token /auth/agent  |
| `test_settings_envs.py` | Settings + ?|
| `test_tools.py` | Tools ?|
| `test_app_startup.py` | App console /fallback |
| `test_version.py` | ( app ? |

---

## `app_server` 

`tests/integration/conftest.py::app_server` ?**module-scoped** fixture:
?gepaw app ?),?
?+  tmp ?

**?id**(
`agent_id = "integ_<scope>_01"`) ?
?

Fixture :

- ?11 ?`OPENAI_API_KEY``DASHSCOPE_API_KEY`?
  ?IM token ?
-  `gepaw_AUTH_ENABLED=false` ?`NO_PROXY=*`
-  `socket.bind(0)` 
-  `/api/version` ?60 ?
- ?**SIGINT**( SIGTERM),?uvicorn ?atexit ?
  flush(?SIGTERM ?
- HTTP  **15 ?*,? ACP getter ?4-5
  ?

---

## ??

 `pytest --cov` ??app 
**app ?*:

```bash
gepaw_INTEGRATION_COVERAGE=1 pytest tests/integration/ --no-cov
```

:

1. ?`.integration_coverage/`  coverage rcfile, ****
   `source=?src/gepaw`
2.  `COVERAGE_PROCESS_START` ?`COVERAGE_FILE` 
3. ?
   `htmlcov-integration/index.html`

>   `--no-cov` ? `pytest-cov` ?
> ?`fail_under=30` ? fail ?

?* `pytest-xdist` ?*?

---

## ?

1. **?*(?[](#))?
   `test_<subdomain>.py`?
2. **?* ?`@pytest.mark.integration` + `p0` / `p1` / `p2`
   (?[?marker](#?marker))?
3. ** id**( `integ_<feature>_<seq>`)?
4. **?*,?purpose / flow / API endpoints?
   :

   ```python
   @pytest.mark.integration
   @pytest.mark.p1
   def test_my_feature_put_get_roundtrip(app_server) -> None:
       """Test purpose:
       - Verify ...

       Test flow:
       1. ...

       API endpoints:
       - PUT ...
       - GET ...
       """
   ```

5. **?`app_server.logs_tail()`**,
   :

   ```python
   assert resp.status_code == 200, app_server.logs_tail()
   ```

---

## 

- **?*: `pytest-xdist` ?
- ****: app ?~4 ?setup) 3
  ,P0 ?2 ?
- ** LLM**:?`console` ,?provider?
- ** I/O**:,IM webhook / long-poll
  ?
- **?worker**:`gepaw_INTEGRATION_COVERAGE=1` ?
  `pytest-xdist` ?
