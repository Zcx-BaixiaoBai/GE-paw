from pathlib import Path
p = Path('src/gepaw/constant.py')
t = p.read_text(encoding='utf-8')
add = '''
# Built-in QA agent skill names (mirrors qwenpaw defaults)
BUILTIN_QA_AGENT_SKILL_NAMES = (
    "ask_user_question",
    "background_task",
    "convert_schemas",
    "create_file",
    "create_plan",
    "edit_file",
    "enter_plan_mode",
    "file_search",
    "get_current_datetime",
    "glob_files",
    "grep_files",
    "list_files",
    "multi_edit_file",
    "notebook_edit",
    "read_file",
    "schedule_task",
    "search_code",
    "share_memory",
    "skill_manage",
    "task_done",
    "task_kill",
    "task_output",
    "task_status",
    "view_image",
    "view_media",
    "view_video",
    "web_extraction",
    "web_search",
    "write_file",
)
'''
if 'BUILTIN_QA_AGENT_SKILL_NAMES' not in t:
    t = t + add
    p.write_text(t, encoding='utf-8')
    print('added')
else:
    print('exists')
