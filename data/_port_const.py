import subprocess, re
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
out = subprocess.check_output(['git','-c','core.quotepath=false','show',f'{ref}:src/qwenpaw/constant.py']).decode('utf-8').replace('qwenpaw', 'gepaw')
# Remove the original top-level imports section to avoid clashes
# We will extract constants only
constants = []
in_block = False
for line in out.splitlines(keepends=True):
    s = line.strip()
    if s.startswith('from ') or s.startswith('import '):
        continue
    if re.match(r'^[A-Z][A-Z0-9_]+\s*=', line):
        in_block = True
    if in_block:
        constants.append(line)
const_text = ''.join(constants)
print(const_text[:2000])
open('data/_qconst.py', 'w', encoding='utf-8').write(const_text)
