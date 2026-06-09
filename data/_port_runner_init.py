import subprocess
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
text = subprocess.check_output(['git','-c','core.quotepath=false','show',f'{ref}:src/qwenpaw/app/runner/__init__.py']).decode('utf-8')
text = text.replace('qwenpaw', 'gepaw')
open('src/gepaw/app/runner/__init__.py', 'w', encoding='utf-8').write(text)
print('replaced')
