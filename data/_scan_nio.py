import subprocess, re
files = subprocess.check_output(['git','-c','core.quotepath=false','ls-files','src/gepaw'], text=True).splitlines()
nio_imports = {}
for f in files:
    if not f.endswith('.py'):
        continue
    try:
        text = open(f, encoding='utf-8').read()
    except Exception:
        continue
    for m in re.finditer(r'from nio[.\w]* import (.*)', text):
        names = re.findall(r'[A-Za-z_]\w*', m.group(1))
        for n in names:
            nio_imports.setdefault(n, set()).add(f)
for n in sorted(nio_imports):
    print(n, '|', sorted(nio_imports[n]))
