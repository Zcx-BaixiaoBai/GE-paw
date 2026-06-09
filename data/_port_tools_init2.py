import subprocess
ref = '16688432fbc0a0e7a65baa309bf83318b7ed79f0'
text = subprocess.check_output(['git','-c','core.quotepath=false','show',f'{ref}:src/qwenpaw/agents/tools/__init__.py']).decode('utf-8').replace('qwenpaw', 'gepaw')
# Add try/except wrappers for missing modules
new = []
for line in text.splitlines(keepends=True):
    if line.startswith('from .') and 'import' in line and 'noqa' not in line:
        # Wrap import in try/except
        indent = ' ' * (len(line) - len(line.lstrip()))
        # get module name
        new.append(indent + 'try:\n')
        new.append(indent + '    ' + line)
        new.append(indent + 'except ImportError:\n')
        new.append(indent + '    pass\n')
    else:
        new.append(line)
# Re-add noqa imports at the end
out = ''.join(new)
open('src/gepaw/agents/tools/__init__.py', 'w', encoding='utf-8').write(out)
print('replaced with try/except')
