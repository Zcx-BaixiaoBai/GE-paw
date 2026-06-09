import subprocess
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
# Check if qwenpaw has agentscope/tool.py
import os
out = subprocess.check_output(['git','-c','core.quotepath=false','ls-tree',ref,'-r','--name-only'], text=True)
as_files = [l for l in out.splitlines() if l.startswith('src/qwenpaw/agentscope/') and l.endswith('.py')]
print('agentscope files in qwenpaw:', len(as_files))
for f in as_files[:20]: print('  ', f)
