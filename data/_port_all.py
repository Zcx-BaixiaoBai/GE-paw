import subprocess, os
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
out = subprocess.check_output(['git','-c','core.quotepath=false','ls-tree',ref,'-r','--name-only'], text=True)
all_files = [l for l in out.splitlines() if l.startswith('src/qwenpaw/') and l.endswith('.py')]
print(f'total {len(all_files)} files')
done = 0
for src in all_files:
    dst = src.replace('qwenpaw', 'gepaw')
    if os.path.exists(dst):
        continue
    raw = subprocess.check_output(['git','-c','core.quotepath=false','show',f'{ref}:{src}'])
    text = raw.decode('utf-8').replace('qwenpaw', 'gepaw')
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w', encoding='utf-8').write(text)
    done += 1
print(f'ported {done} new files')
