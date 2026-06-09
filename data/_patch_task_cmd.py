from pathlib import Path
import shutil

p = Path('src/gepaw/cli/task_cmd.py')
t = p.read_text(encoding='utf-8')

old1 = '        (tmp_path / "skills").symlink_to(resolved)'
new1 = '''        # Windows lacks admin-only symlink privileges; fall back to a copy so
        # the overlay workspace still resolves skills correctly.
        try:
            (tmp_path / "skills").symlink_to(resolved)
        except (OSError, NotImplementedError):
            shutil.copytree(resolved, tmp_path / "skills")'''
if old1 in t:
    t = t.replace(old1, new1, 1)

old2 = '''                if not target.exists():
                    target.symlink_to(item)'''
new2 = '''                if not target.exists():
                    try:
                        target.symlink_to(item)
                    except (OSError, NotImplementedError):
                        if item.is_dir():
                            shutil.copytree(item, target)
                        else:
                            shutil.copy2(item, target)'''
if old2 in t:
    t = t.replace(old2, new2, 1)

p.write_text(t, encoding='utf-8')
print('patched')
