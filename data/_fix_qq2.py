# -*- coding: utf-8 -*-
from pathlib import Path
p = Path('src/gepaw/app/channels/qq/channel.py')
t = p.read_text(encoding='utf-8')
# Replace chinese with [] to match gepaw test
t = t.replace(chr(0x3010) + chr(0x94fe) + chr(0x63a5) + chr(0x5df2) + chr(0x7701) + chr(0x7565) + chr(0x3011), '[]')
p.write_text(t, encoding='utf-8')
print('fixed')
