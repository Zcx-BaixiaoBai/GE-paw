from pathlib import Path
p = Path('src/gepaw/app/channels/registry.py')
t = p.read_text(encoding='utf-8')
if 'CHANNEL_KINDS' not in t:
    t = t + '''

CHANNEL_KINDS = (
    'telegram',
    'discord',
    'feishu',
    'dingtalk',
    'wecom',
    'wechat',
    'onebot',
    'qq',
    'matrix',
    'imessage',
    'mattermost',
    'mqtt',
    'xiaoyi',
    'yuanbao',
    'sip',
    'voice',
    'console',
)
'''
    p.write_text(t, encoding='utf-8')
    print('added')
