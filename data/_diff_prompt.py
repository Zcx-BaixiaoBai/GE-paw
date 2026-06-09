import subprocess, re
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
q = subprocess.check_output(['git','-c','core.quotepath=false','show',f'{ref}:src/qwenpaw/agents/prompt.py']).decode('utf-8')
for m in re.finditer(r'^def (\w+)', q, re.MULTILINE):
    print(m.group(1))
