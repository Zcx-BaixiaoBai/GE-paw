import subprocess, os
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
out = subprocess.check_output(['git','-c','core.quotepath=false','ls-tree',ref,'-r','--name-only'], text=True)
all_files = [l for l in out.splitlines() if l.startswith('src/qwenpaw/') and l.endswith('.py')]
# Find all imports from gepaw.* in the ported files to identify missing modules
gepaw_imports = set()
for src in all_files:
    raw = subprocess.check_output(['git','-c','core.quotepath=false','show',f'{ref}:{src}'])
    text = raw.decode('utf-8').replace('qwenpaw', 'gepaw')
    import re
    for m in re.finditer(r'(?:from|import) (gepaw[\w.]*)', text):
        gepaw_imports.add(m.group(1).rstrip(','))
# Existing gepaw files
existing = set()
for root, dirs, fs in os.walk('src/gepaw'):
    for f in fs:
        if not f.endswith('.py'): continue
        p = os.path.relpath(os.path.join(root,f), 'src').replace(os.sep,'/')[:-3]
        existing.add(p)
# missing modules
missing = sorted(gepaw_imports - existing)
print('Missing modules:')
for m in missing: print(' ', m)
