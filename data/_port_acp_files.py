import subprocess, re
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
text = subprocess.check_output(['git','-c','core.quotepath=false','ls-tree',ref,'-r','--name-only'], text=True)
all_files = [l for l in text.splitlines() if l.endswith('.py')]
acp_names = {}
for f in all_files:
    try:
        raw = subprocess.check_output(['git','-c','core.quotepath=false','show',f'{ref}:{f}']).decode('utf-8', errors='replace')
    except: continue
    for m in re.finditer(r'from (acp[\w.]*) import \(([^)]+)\)', raw, re.DOTALL):
        mod = m.group(1)
        acp_names.setdefault(mod, set())
        for line in m.group(2).split(chr(10)):
            for n in re.findall(r'[A-Za-z_]\w*', line):
                acp_names[mod].add(n)
    for m in re.finditer(r'from (acp[\w.]*) import (\w+)', raw):
        mod = m.group(1)
        acp_names.setdefault(mod, set())
        acp_names[mod].add(m.group(2))
for k in sorted(acp_names):
    print(k, '|', sorted(acp_names[k]))
