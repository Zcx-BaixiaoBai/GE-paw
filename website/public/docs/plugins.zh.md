# 

gepaw  gepaw ?

## 

?

- **Provider **?LLM Provider ?
- **Hook **/
- **Command **?`/command` 
- **HTTP API ** FastAPI `APIRouter` ?`/api`  REST 
- ****
- ****?
- ****?

## 

### 



```bash
gepaw plugin install /path/to/plugin
```

?URL ?ZIP 

```bash
gepaw plugin install https://example.com/plugin.zip
```

?

```bash
gepaw plugin install /path/to/plugin --force
```

**** gepaw ?

### ?

```bash
gepaw plugin list
```

?

```
Installed Plugins:
==================

my-provider (v1.0.0)
  Custom LLM provider integration
  Author: Developer Name
  Path: /Users/user/.gepaw/plugins/my-provider
```

### 

```bash
gepaw plugin info <plugin-id>
```

### 

```bash
gepaw plugin uninstall <plugin-id>
```

## ?

### 

#### 



```
my-plugin/
 plugin.json      # ?
 plugin.py        # ?
 README.md        # 
```

#### plugin.json

```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "type": "general",
  "description": "Plugin description",
  "author": "Your Name",
  "entry": {
    "backend": "plugin.py"
  },
  "dependencies": [],
  "min_version": "0.1.0",
  "meta": {}
}
```

#### 

|              |             |  |                                                                                                                                              |
| ---------------- | --------------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `id`             | `string`        | ?  | ?                                                                                          |
| `version`        | `string`        | ?  | ?`1.0.0`?                                                                                                              |
| `name`           | `string` ?| ?  |  `id`?`{"zh-CN": "...", "en-US": "..."}`?"?                                    |
| `type`           | `string`        | ?  | `tool``provider``hook``command``frontend``general` `meta` / `entry` ?|
| `description`    | `string` ?| ?  | ?`name`?                                                                                         |
| `author`         | `string`        | ?  | ?                                                                                                                                |
| `entry.backend`  | `string`        | \* | ?Python ?`plugin`?                                                                                     |
| `entry.frontend` | `string`        | \* |  bundle  `dist/index.js`?                                                                                                |
| `dependencies`   | `string[]`      | ?  | Python  pip / uv ?                                                                                                 |
| `min_version`    | `string`        | ?  | ?gepaw ?`0.1.0`?                                                                                                         |
| `meta`           | `object`        | ?  | ?UI ?`type`  `meta.tools[]``meta.hook_type``meta.provider_id`?                                         |
| `entry_point`    | `string`        | ?  | **?* ?`entry.backend` `entry.backend`?                                                       |

\* `entry.backend``entry.frontend` `entry_point`?

#### `type` ?

| ?      |                                              |
| ---------- | ---------------------------------------------------- |
| `tool`     |  Agent LLM ?     |
| `provider` | ?LLM ?/ ?                  |
| `hook`     | ?/ ?                       |
| `command`  |  `/slash` ?                            |
| `frontend` |  JS bundle UI ?                |
| `general`  | ?|

#### plugin.py

```python
# -*- coding: utf-8 -*-
"""My Plugin Entry Point."""

from gepaw.plugins.api import PluginApi
import logging

logger = logging.getLogger(__name__)


class MyPlugin:
    """My Plugin."""

    def register(self, api: PluginApi):
        """Register plugin capabilities.

        Args:
            api: PluginApi instance
        """
        logger.info("Registering my plugin...")

        # 
        # api.register_provider(...)
        # api.register_startup_hook(...)
        # api.register_shutdown_hook(...)

        logger.info("?My plugin registered")


# Export plugin instance
plugin = MyPlugin()
```

### 

#### 



```
my-plugin/
 plugin.json      # ?
 src/
?   index.tsx    # ?
 package.json     # 
 tsconfig.json    # TypeScript 
 vite.config.ts   # 
```

#### plugin.json

```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "type": "frontend",
  "author": "Your Name",
  "entry": { "frontend": "dist/index.js" }
}
```

#### src/index.tsx

```tsx
const { React, antd } = (window as any).gepaw.host;

class MyPlugin {
  readonly id = "my-plugin";

  setup(): void {
    // ?
    // (window as any).gepaw.registerRoutes?.(this.id, [...]);
    // ?
    // (window as any).gepaw.registerToolRender?.(this.id, {...});
    // ?
    // const mod = (window as any).gepaw?.modules?.['xxxx'];
  }
}

new MyPlugin().setup();
```

#### package.json

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "scripts": { "build": "vite build" },
  "devDependencies": {
    "vite": "^5.0.0",
    "typescript": "^5.0.0",
    "@vitejs/plugin-react": "^4.0.0"
  }
}
```

#### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react",
    "strict": false,
    "skipLibCheck": true
  }
}
```

#### vite.config.ts

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react({ jsxRuntime: "classic" })],
  build: {
    lib: {
      entry: "src/index.tsx",
      formats: ["es"],
      fileName: () => "index.js",
    },
    rollupOptions: { external: ["react", "react-dom"] },
  },
});
```

#### ?

```bash
npm install && npm run build
cp -r . ~/.gepaw/plugins/my-plugin/
gepaw app
```

****`window.gepaw.host` ?

|               |                        |                |
| ----------------- | -------------------------- | ------------------ |
| `React`           | `typeof React`             | React ?      |
| `antd`            | `typeof antd`              | Ant Design ? |
| `getApiUrl(path)` | `(path: string) => string` | ?API URL   |
| `getApiToken()`   | `() => string`             |  Token |

****?

- `jsxRuntime: "classic"` ??JSX ?`React.createElement` `React`
- `external: ["react", "react-dom"]` ??React?

**`window.gepaw.modules`** `src/pages/` ?

>  ****`modules`  API ?

## 

###  1 Provider

 LLM ?

#### 1. 

```bash
mkdir my-llm-provider
cd my-llm-provider
```

#### 2.  plugin.json

```json
{
  "id": "my-llm-provider",
  "name": "My LLM Provider",
  "version": "1.0.0",
  "type": "provider",
  "description": "Custom LLM provider for enterprise",
  "author": "Your Name",
  "entry": {
    "backend": "plugin.py"
  },
  "dependencies": ["httpx>=0.24.0"],
  "min_version": "0.1.0",
  "meta": {
    "api_key_url": "https://example.com/get-api-key",
    "api_key_hint": "Get your API key from example.com"
  }
}
```

#### 3.  provider.py

```python
# -*- coding: utf-8 -*-
"""My LLM Provider Implementation."""

from gepaw.providers.openai_provider import OpenAIProvider
from gepaw.providers.provider import ModelInfo
from typing import List


class MyLLMProvider(OpenAIProvider):
    """My custom LLM provider (OpenAI-compatible)."""

    def __init__(self, **kwargs):
        """Initialize provider."""
        super().__init__(**kwargs)

    @classmethod
    def get_default_models(cls) -> List[ModelInfo]:
        """?""
        return [
            ModelInfo(
                id="my-model-v1",
                name="My Model V1",
                supports_multimodal=False,
                supports_image=False,
                supports_video=False,
            ),
            ModelInfo(
                id="my-model-v2",
                name="My Model V2",
                supports_multimodal=True,
                supports_image=True,
                supports_video=False,
            ),
        ]
```

#### 4.  plugin.py

```python
# -*- coding: utf-8 -*-
"""My LLM Provider Plugin Entry Point."""

import importlib.util
import logging
import os

from gepaw.plugins.api import PluginApi

logger = logging.getLogger(__name__)


class MyLLMProviderPlugin:
    """My LLM Provider Plugin."""

    def register(self, api: PluginApi):
        """Register the provider.

        Args:
            api: PluginApi instance
        """
        logger.info("Registering My LLM Provider...")

        #  provider 
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        provider_path = os.path.join(plugin_dir, "provider.py")

        spec = importlib.util.spec_from_file_location(
            "my_provider", provider_path
        )
        provider_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(provider_module)

        MyLLMProvider = provider_module.MyLLMProvider

        # Register provider
        api.register_provider(
            provider_id="my-llm",
            provider_class=MyLLMProvider,
            label="My LLM",
            base_url="https://api.example.com/v1",
            metadata={},
        )

        logger.info("?My LLM Provider registered")


# Export plugin instance
plugin = MyLLMProviderPlugin()
```

#### 5. ?

```bash
# 
gepaw plugin install my-llm-provider

#  gepaw
gepaw app

# ?Web UI ?API Key
# ?Provider ?
```

###  2?

?gepaw ?

#### 1. 

```bash
mkdir monitoring-hook
cd monitoring-hook
```

#### 2.  plugin.json

```json
{
  "id": "monitoring-hook",
  "name": "Monitoring Hook",
  "version": "1.0.0",
  "type": "hook",
  "description": "Initialize monitoring service at startup",
  "author": "Your Name",
  "entry": {
    "backend": "plugin.py"
  },
  "dependencies": [],
  "min_version": "0.1.0"
}
```

#### 3.  plugin.py

```python
# -*- coding: utf-8 -*-
"""Monitoring Hook Plugin Entry Point."""

from gepaw.plugins.api import PluginApi
import logging

logger = logging.getLogger(__name__)


class MonitoringHookPlugin:
    """Monitoring Hook Plugin."""

    def register(self, api: PluginApi):
        """Register the monitoring hook.

        Args:
            api: PluginApi instance
        """
        logger.info("Registering monitoring hook...")

        def startup_hook():
            """Startup hook to initialize monitoring."""
            try:
                logger.info("=== Monitoring Service Initialization ===")

                # ?
                # from my_monitoring import init_monitoring
                # init_monitoring(app_name="gepaw")

                logger.info("?Monitoring initialized successfully")

            except Exception as e:
                logger.error(
                    f"Failed to initialize monitoring: {e}",
                    exc_info=True,
                )

        # priority=0 ?
        api.register_startup_hook(
            hook_name="monitoring_init",
            callback=startup_hook,
            priority=0,
        )

        logger.info("?Monitoring hook registered")


# Export plugin instance
plugin = MonitoringHookPlugin()
```

#### 4. 

```bash
gepaw plugin install monitoring-hook
gepaw app
```

###  3

?`/status` ?

#### 1. 

```bash
mkdir status-command
cd status-command
```

#### 2.  plugin.json

```json
{
  "id": "status-command",
  "name": "Status Command",
  "version": "1.0.0",
  "type": "command",
  "description": "Custom status command",
  "author": "Your Name",
  "entry": {
    "backend": "plugin.py"
  },
  "dependencies": [],
  "min_version": "0.1.0"
}
```

#### 3.  query_rewriter.py

```python
# -*- coding: utf-8 -*-
"""Query rewriter for status command."""


class StatusQueryRewriter:
    """Rewrite /status queries to agent prompts."""

    @staticmethod
    def should_rewrite(query: str) -> bool:
        """Check if query should be rewritten."""
        if not query:
            return False
        return query.strip().lower().startswith("/status")

    @staticmethod
    def rewrite(query: str) -> str:
        """Rewrite /status query to agent prompt."""
        return """?

1.  Provider
2. 
3. 
4. 

?""
```

#### 4.  plugin.py

```python
# -*- coding: utf-8 -*-
"""Status Command Plugin Entry Point."""

import logging

from gepaw.plugins.api import PluginApi

logger = logging.getLogger(__name__)


class StatusCommandPlugin:
    """Status Command Plugin."""

    def register(self, api: PluginApi):
        """Register the status command.

        Args:
            api: PluginApi instance
        """
        logger.info("Registering status command...")

        # Register startup hook to patch query handler
        api.register_startup_hook(
            hook_name="status_query_rewriter",
            callback=self._patch_query_handler,
            priority=50,
        )

        logger.info("?Status command registered: /status")

    def _patch_query_handler(self):
        """Patch AgentRunner.query_handler to rewrite /status queries."""
        from gepaw.app.runner.runner import AgentRunner
        from .query_rewriter import StatusQueryRewriter

        original_query_handler = AgentRunner.query_handler

        async def patched_query_handler(self, msgs, request=None, **kwargs):
            """Patched query handler."""
            if msgs and len(msgs) > 0:
                last_msg = msgs[-1]
                if hasattr(last_msg, 'content'):
                    content_list = (
                        last_msg.content
                        if isinstance(last_msg.content, list)
                        else [last_msg.content]
                    )
                    for content_item in content_list:
                        if (
                            isinstance(content_item, dict)
                            and content_item.get('type') == 'text'
                        ):
                            text = content_item.get('text', '')
                            if StatusQueryRewriter.should_rewrite(text):
                                rewritten = StatusQueryRewriter.rewrite(text)
                                logger.info("Rewriting /status query")
                                content_item['text'] = rewritten
                                break

            async for result in original_query_handler(
                self,
                msgs,
                request,
                **kwargs,
            ):
                yield result

        AgentRunner.query_handler = patched_query_handler
        logger.info("?Patched AgentRunner.query_handler for /status")


# Export plugin instance
plugin = StatusCommandPlugin()
```

#### 5. ?

```bash
gepaw plugin install status-command
gepaw app

# 
/status
```

###  4

?

#### 1. 

```bash
mkdir welcome-plugin && cd welcome-plugin
```

#### 2.  plugin.json

```json
{
  "id": "welcome-plugin",
  "name": "Welcome Plugin",
  "version": "1.0.0",
  "type": "frontend",
  "description": "Welcome page plugin",
  "author": "Your Name",
  "entry": { "frontend": "dist/index.js" }
}
```

#### 3.  src/index.tsx

```tsx
const { React, antd } = (window as any).gepaw.host;
const { Typography, Card } = antd;
const { Title, Paragraph } = Typography;

function WelcomePage() {
  return (
    <Card style={{ maxWidth: 480, margin: "40px auto" }}>
      <Title level={2}>Welcome to gepaw </Title>
      <Paragraph>?/Paragraph>
    </Card>
  );
}

class WelcomePlugin {
  readonly id = "welcome-plugin";

  setup(): void {
    (window as any).gepaw.registerRoutes?.(this.id, [
      {
        path: "/plugin/welcome-plugin/home",
        component: WelcomePage,
        label: "Welcome",
        icon: "",
        priority: 5,
      },
    ]);
  }
}

new WelcomePlugin().setup();
```

#### 4.  package.json

```json
{
  "name": "welcome-plugin",
  "version": "1.0.0",
  "scripts": { "build": "vite build" },
  "devDependencies": {
    "vite": "^5.0.0",
    "typescript": "^5.0.0",
    "@vitejs/plugin-react": "^4.0.0"
  }
}
```

#### 5.  tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react",
    "strict": false,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

#### 6.  vite.config.ts

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react({ jsxRuntime: "classic" })],
  build: {
    lib: {
      entry: "src/index.tsx",
      formats: ["es"],
      fileName: () => "index.js",
    },
    rollupOptions: { external: ["react", "react-dom"] },
  },
});
```

#### 7. ?

```bash
npm install && npm run build
cp -r . ~/.gepaw/plugins/welcome-plugin/
gepaw app
```

###  5

?Agent ?

#### 1. 

```bash
mkdir tool-render-plugin && cd tool-render-plugin
```

#### 2.  plugin.json

```json
{
  "id": "tool-render-plugin",
  "name": "Tool Render Plugin",
  "version": "1.0.0",
  "type": "frontend",
  "description": "Custom tool result renderer",
  "author": "Your Name",
  "entry": { "frontend": "dist/index.js" }
}
```

#### 3.  src/index.tsx

```tsx
const { React, antd } = (window as any).gepaw.host;
const { Card } = antd;

function MyToolCard({ result }) {
  return (
    <Card style={{ marginTop: 8 }}>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </Card>
  );
}

class ToolRenderPlugin {
  readonly id = "tool-render-plugin";

  setup(): void {
    (window as any).gepaw.registerToolRender?.(this.id, {
      my_tool_name: MyToolCard, // key = tool name returned by Agent
    });
  }
}

new ToolRenderPlugin().setup();
```

#### 4. 

 4  `package.json``tsconfig.json``vite.config.ts` `name`  `tool-render-plugin`?

#### 5. ?

```bash
npm install && npm run build
cp -r . ~/.gepaw/plugins/tool-render-plugin/
gepaw app
```

###  6?



#### 1. 

```bash
mkdir custom-greeting-plugin && cd custom-greeting-plugin
```

#### 2.  plugin.json

```json
{
  "id": "custom-greeting-plugin",
  "name": "Custom Greeting",
  "version": "1.0.0",
  "type": "frontend",
  "description": "Customize chat greeting",
  "author": "Your Name",
  "entry": { "frontend": "dist/index.js" }
}
```

#### 3.  src/index.tsx

```tsx
class CustomGreetingPlugin {
  readonly id = "custom-greeting-plugin";

  setup(): void {
    const mod = (window as any).gepaw?.modules?.[
      "Chat/OptionsPanel/defaultConfig"
    ];
    if (!mod?.configProvider) {
      console.warn("configProvider not found");
      return;
    }

    // ?
    mod.configProvider.getGreeting = () => " gepaw ";

    // 
    mod.configProvider.getDescription = () => "?;

    // ?
    mod.configProvider.getPrompts = (t: any) => [
      { value: "" },
      { value: "? },
      { value: "" },
    ];
  }
}

new CustomGreetingPlugin().setup();
```

#### 4. 

 4  `package.json``tsconfig.json``vite.config.ts` `name`  `custom-greeting-plugin`?

#### 5. ?

```bash
npm install && npm run build
cp -r . ~/.gepaw/plugins/custom-greeting-plugin/
gepaw app
```

###  7?FastAPI 

 `fastapi.APIRouter` ?HTTP ?
`/api` ?gepaw  API ?FastAPI ?
 CORS `/openapi.json` ?`/docs` ?

 `/api/pets` ?

#### 1. 

```bash
mkdir pet-api-plugin && cd pet-api-plugin
```

#### 2.  plugin.json

```json
{
  "id": "pet-api-plugin",
  "name": "Pet API Plugin",
  "version": "1.0.0",
  "type": "general",
  "description": "Expose a small REST API under /api/pets",
  "author": "Your Name",
  "entry": {
    "backend": "plugin.py"
  },
  "dependencies": [],
  "min_version": "1.1.5"
}
```

#### 3.  plugin.py

```python
# -*- coding: utf-8 -*-
"""Pet API Plugin Entry Point."""

import logging
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from gepaw.plugins.api import PluginApi

logger = logging.getLogger(__name__)


class Pet(BaseModel):
    """Pet model."""

    id: int
    name: str
    species: str


class PetCreate(BaseModel):
    """Pet creation payload."""

    name: str
    species: str


_PETS: List[Pet] = [
    Pet(id=1, name="Mochi", species="cat"),
    Pet(id=2, name="Bao", species="dog"),
]


def build_router() -> APIRouter:
    """Build the plugin's APIRouter.

    Routes are mounted under ``/api`` + the prefix passed to
    ``register_http_router``. With ``prefix="/pets"`` the handlers
    below are served at ``/api/pets`` and ``/api/pets/{pet_id}``.
    """
    router = APIRouter()

    @router.get("", response_model=List[Pet])
    def list_pets() -> List[Pet]:
        """Return all pets."""
        return list(_PETS)

    @router.get("/{pet_id}", response_model=Pet)
    def get_pet(pet_id: int) -> Pet:
        """Return a single pet by id."""
        for pet in _PETS:
            if pet.id == pet_id:
                return pet
        raise HTTPException(status_code=404, detail="Pet not found")

    @router.post("", response_model=Pet, status_code=201)
    def create_pet(payload: PetCreate) -> Pet:
        """Create a new pet."""
        new_id = (max((p.id for p in _PETS), default=0)) + 1
        pet = Pet(id=new_id, name=payload.name, species=payload.species)
        _PETS.append(pet)
        return pet

    return router


class PetApiPlugin:
    """Pet API Plugin."""

    def register(self, api: PluginApi):
        """Register the HTTP router.

        Args:
            api: PluginApi instance
        """
        logger.info("Registering Pet API plugin...")

        api.register_http_router(
            build_router(),
            prefix="/pets",
            tags=["pets"],
        )

        logger.info("?Pet API registered at /api/pets")


# Export plugin instance
plugin = PetApiPlugin()
```

#### 4. ?

```bash
gepaw plugin install pet-api-plugin
```

 gepaw ?`curl` ?`8088`

```bash
# 
curl http://127.0.0.1:8088/api/pets

# ?id 
curl http://127.0.0.1:8088/api/pets/1

# POST ?/api/pets?
curl -X POST http://127.0.0.1:8088/api/pets \
  -H "Content-Type: application/json" \
  -d '{"name": "Luna", "species": "rabbit"}'
```

**?*

- `prefix` ?`/` ?`/` `/pets`?`/api` +  `prefix`?
- ?`ValueError`?
- `tags`  OpenAPI  `plugin:< id>` ?
- ?

## 

###  requirements.txt

 Python  `requirements.txt`?

```
httpx>=0.24.0
pydantic>=2.0.0
```

?

### ?PyPI ?

```
--index-url https://custom-pypi.example.com/simple
my-package>=1.0.0
```

## ?

### 1. 

- ** ID**?`my-plugin`
- **?*?.0.0, 1.1.0, 2.0.0?

### 2. 



```python
def startup_hook():
    try:
        # ?
        pass
    except Exception as e:
        logger.error(f"Initialization failed: {e}", exc_info=True)
        #  raise
```

### 3. 

 Python logging ?

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Plugin loaded")
logger.debug("Debug information")
logger.error("Error occurred", exc_info=True)
```

### 4. 

?README.md 

- 
- 
- 
- 
- 

## ?

### Hook ?

?

- ****
- Priority 0 = 
- Priority 100 = ?
- Priority 200 = 

****?

```python
# ?
api.register_startup_hook("early", callback, priority=0)

# 
api.register_startup_hook("normal", callback, priority=100)

# ?
api.register_startup_hook("late", callback, priority=200)
```

## 

### ?

1. ?

   ```bash
   gepaw plugin list
   ```

2.  gepaw ?

   ```bash
   tail -f ~/.gepaw/logs/gepaw.log | grep -i plugin
   ```

3. ?
   ```bash
   gepaw plugin info <plugin-id>
   ```

### 

1. ?`requirements.txt` 
2. ?
   ```bash
   pip install -r /path/to/plugin/requirements.txt
   ```
3.  `--force` 

### Provider ?

1.  gepaw
2. ?Web UI ?
3.  provider 

### ?

1. ?
2. ?startup hook 
3.  patch 

## 

1. **?*?gepaw ?
2. **?*
3. ****?
4. ****??gepaw 

## PluginApi ?

### register_provider

?LLM Provider?

```python
api.register_provider(
    provider_id: str,          # Provider ?
    provider_class: Type,      # Provider ?
    label: str,                # 
    base_url: str,             # API base URL
    metadata: Dict[str, Any],  # ?
)
```

### register_startup_hook

?

```python
api.register_startup_hook(
    hook_name: str,      # 
    callback: Callable,  # 
    priority: int = 100, # ?
)
```

### register_shutdown_hook

?

```python
api.register_shutdown_hook(
    hook_name: str,      # 
    callback: Callable,  # 
    priority: int = 100, # ?
)
```

### register_http_router

?`fastapi.APIRouter` ?`/api` + _prefix_ ?

```python
api.register_http_router(
    router: APIRouter,             # fastapi.APIRouter 
    *,
    prefix: str,                   # /api ?"/pets"
    tags: Optional[List[str]] = None,  # OpenAPI 
)
```

?7?FastAPI ?

## 

### Monkey Patch

?gepaw  monkey patch?

```python
def _patch_query_handler(self):
    """Patch AgentRunner to intercept queries."""
    from gepaw.app.runner.runner import AgentRunner

    original_handler = AgentRunner.query_handler

    async def patched_handler(self, msgs, request=None, **kwargs):
        # 
        #  msgs ?

        #  handler
        async for result in original_handler(self, msgs, request, **kwargs):
            yield result

    AgentRunner.query_handler = patched_handler
```

### ?

 `api.runtime` 

```python
def my_hook():
    #  provider manager
    provider_manager = api.runtime.provider_manager

    # ?providers
    providers = provider_manager.list_provider_info()
```

## 

 ZIP ?

```bash
cd /path/to/plugins
zip -r my-plugin-1.0.0.zip my-plugin/
```

 URL ?

```bash
gepaw plugin install https://example.com/my-plugin-1.0.0.zip
```

## 

### Q:  gepaw API?

A:  `PluginApi` 

- Provider 
- Hook 
- HTTP `register_http_router`?
- Runtime helpersprovider_manager 

### Q:  gepaw ?

A:  monkey patch ?hook ?

### Q: ?

A: ?provider_id ?command_name?ID?

## 

### GPT Image 2 

 gepaw agents  OpenAI GPT Image 2 ?

**?*

- gepaw `1.1.5`

**?*

```bash
#  gepaw 
git clone https://github.com/agentscope-ai/gepaw.git
cd gepaw

# 
gepaw plugin install plugins/tool/gpt-image2
```

**?*

1.  gepaw
2.  Agent  ?
3.  "generate_image_gpt" 
4. ""?OpenAI API Key
5. ?

**?*

agent 

```
: 
Agent: [ generate_image_gpt ]
       []
```

****

- ?024x1024, 1024x1792, 1792x1024
- low, medium, high, auto
-  API Key
- Per-agent ?agent ?API Key?

?`plugins/tool/gpt-image2/README.md`?
