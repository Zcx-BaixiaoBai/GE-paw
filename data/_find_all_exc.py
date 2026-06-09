import subprocess, re
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
text = subprocess.check_output(['git','-c','core.quotepath=false','ls-tree',ref,'-r','--name-only'], text=True)
files = [l for l in text.splitlines() if l.startswith('src/qwenpaw/') and l.endswith('.py')]
classes = set()
for f in files:
    try:
        raw = subprocess.check_output(['git','-c','core.quotepath=false','show',f'{ref}:{f}']).decode('utf-8', errors='replace')
    except: continue
    for m in re.finditer(r'class (\w+)\s*\(', raw):
        if 'Exception' in m.group(1) or 'Error' in m.group(1):
            classes.add(m.group(1))
for c in sorted(classes): print(c)
