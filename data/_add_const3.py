from pathlib import Path
p = Path('src/gepaw/constant.py')
t = p.read_text(encoding='utf-8')
add = '''

# ---------------- additional channels/CLI/runtime constants ----------------
BUILTIN_QA_AGENT_ID = 'qa-bot'
BUILTIN_QA_AGENT_NAME = 'Q&A Bot'
LEGACY_QA_AGENT_ID = 'qa_bot'

CODING_PROJECT_SUBDIR = 'coding_projects'

CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']

CUSTOM_CHANNELS_DIR = WORKING_DIR / 'custom_channels'

DEBUG_HISTORY_FILE = WORKING_DIR / 'debug_history.jsonl'

DEFAULT_LOCAL_PROVIDER_DIR = WORKING_DIR / 'local_models'

HEARTBEAT_TARGET_INBOX = 'inbox'
HEARTBEAT_TARGET_LAST = 'last'

MAX_LOAD_HISTORY_COUNT = 100

MEMORY_COMPACT_KEEP_RECENT = 20
MEMORY_COMPACT_RATIO = 0.5

MODELS_DIR = WORKING_DIR / 'models'

MODEL_PROVIDER_CHECK_TIMEOUT = 5.0

PLUGINS_DIR = WORKING_DIR / 'plugins'

TOKEN_USAGE_FILE = WORKING_DIR / 'token_usage.jsonl'
'''
if 'CUSTOM_CHANNELS_DIR' not in t:
    t = t + add
    p.write_text(t, encoding='utf-8')
    print('added')
else:
    print('exists')
