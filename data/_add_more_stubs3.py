import subprocess, os
# port all agentscope_runtime.engine.schemas from qwenpaw
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
for src in [
    'src/qwenpaw/agentscope_runtime/engine/schemas/exception.py',
]:
    raw = subprocess.check_output(['git','-c','core.quotepath=false','show',f'{ref}:{src}'])
    text = raw.decode('utf-8').replace('qwenpaw', 'gepaw')
    dst = src.replace('qwenpaw', 'gepaw')
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w', encoding='utf-8').write(text)
    print(dst)

# Port token_usage/model_wrapper
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
text = subprocess.check_output(['git','-c','core.quotepath=false','show',f'{ref}:src/qwenpaw/token_usage/model_wrapper.py']).decode('utf-8')
text = text.replace('qwenpaw', 'gepaw')
open('src/gepaw/token_usage/model_wrapper.py', 'w', encoding='utf-8').write(text)
print('token_usage.model_wrapper replaced')
