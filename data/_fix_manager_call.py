from pathlib import Path
p = Path('src/gepaw/app/_app.py')
t = p.read_text(encoding='utf-8')
old = '''    from .scheduler import start_scheduler, stop_scheduler
    from .channels import manager as channel_manager
    start_scheduler()
    channel_manager.start_all()
    try:
        yield
    finally:
        channel_manager.stop_all()
        stop_scheduler()
        logger.info("已退�?)'''
new = '''    from .scheduler import start_scheduler, stop_scheduler
    from .channels.manager import ChannelManager
    channel_manager = ChannelManager()
    start_scheduler()
    await channel_manager.start_all()
    try:
        yield
    finally:
        await channel_manager.stop_all()
        stop_scheduler()
        logger.info("已退�?)'''
if old in t:
    t = t.replace(old, new, 1)
    p.write_text(t, encoding='utf-8')
    print('fixed')
else:
    print('not found')
