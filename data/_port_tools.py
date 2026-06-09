import subprocess, os, re
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
# Scan all gepaw.agents.tools.* usages in qwenpaw
out = subprocess.check_output(['git','-c','core.quotepath=false','ls-tree',ref,'-r','--name-only'], text=True)
files = [l for l in out.splitlines() if l.startswith('src/qwenpaw/agents/tools/') and l.endswith('.py')]
for src in files:
    if not os.path.exists(src.replace('qwenpaw', 'gepaw')):
        raw = subprocess.check_output(['git','-c','core.quotepath=false','show',f'{ref}:{src}'])
        text = raw.decode('utf-8').replace('qwenpaw', 'gepaw')
        dst = src.replace('qwenpaw', 'gepaw')
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'w', encoding='utf-8').write(text)
        print('ported', dst)
