import subprocess, os, re
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
out = subprocess.check_output(['git','-c','core.quotepath=false','show',f'{ref}:src/qwenpaw/constant.py']).decode('utf-8')
# Parse constant names from qwenpaw
names = set(re.findall(r'^([A-Z][A-Z0-9_]+)\s*=', out, re.MULTILINE))
# Parse existing gepaw constant names
gt = open('src/gepaw/constant.py', encoding='utf-8').read()
gnames = set(re.findall(r'^([A-Z][A-Z0-9_]+)\s*=', gt, re.MULTILINE))
missing = names - gnames
print('Missing constants:')
for m in sorted(missing): print(' ', m)
