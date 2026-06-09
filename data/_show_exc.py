import subprocess
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
# Look for exception.py in qwenpaw
try:
    text = subprocess.check_output(['git','-c','core.quotepath=false','show',f'{ref}:src/qwenpaw/agentscope_runtime/engine/schemas/exception.py']).decode('utf-8')
    print(text[:5000])
except subprocess.CalledProcessError:
    print('no exception.py in qwenpaw')
