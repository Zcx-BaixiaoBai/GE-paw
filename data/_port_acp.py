import subprocess
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
# Look for qwenpaw test files that import acp to find names
text = subprocess.check_output(['git','-c','core.quotepath=false','ls-tree',ref,'-r','--name-only'], text=True)
acp_files = [l for l in text.splitlines() if 'acp' in l and l.endswith('.py')]
import re
names = set()
for f in acp_files:
    raw = subprocess.check_output(['git','-c','core.quotepath=false','show',f'{ref}:{f}']).decode('utf-8', errors='replace')
    for m in re.finditer(r'from acp import \(([^)]+)\)', raw, re.DOTALL):
        for line in m.group(1).split(chr(10)):
            for n in re.findall(r'[A-Za-z_]\w*', line):
                names.add(n)
for n in sorted(names): print(n)
