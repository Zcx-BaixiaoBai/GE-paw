import subprocess, os
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
out = subprocess.check_output(['git','-c','core.quotepath=false','ls-tree',ref,'-r','--name-only'], text=True)
files = [l for l in out.splitlines() if l.startswith('src/qwenpaw/agents/tools/') and l.endswith('.py')]
print('total tools files:', len(files))
print('already exist:', sum(1 for f in files if os.path.exists(f.replace('qwenpaw', 'gepaw'))))
