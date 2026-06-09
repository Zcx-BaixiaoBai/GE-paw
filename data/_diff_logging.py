import subprocess
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
q = subprocess.check_output(['git','-c','core.quotepath=false','show',f'{ref}:src/qwenpaw/utils/logging.py']).decode('utf-8')
print('=== qwenpaw ===')
import re
for m in re.finditer(r'^def (\w+)', q, re.MULTILINE):
    print(m.group(1))
print()
g = open('src/gepaw/utils/logging.py', encoding='utf-8').read()
print('=== gepaw ===')
for m in re.finditer(r'^def (\w+)', g, re.MULTILINE):
    print(m.group(1))
