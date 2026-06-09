"""Cron 调度。"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from ..constant import CRON_FAILURE_DISABLE_THRESHOLD
from ..models import CronJob, CronRun
from ..utils.logging import get_logger
from .db import session_scope

logger = get_logger("scheduler")
_SCHEDULER: Optional[BackgroundScheduler] = None


def _execute_cron(cron_id: str) -> None:
    with session_scope() as db:
        job: Optional[CronJob] = db.get(CronJob, cron_id)
        if job is None or not job.enabled:
            return
        run = CronRun(cron_id=job.id, status="running")
        db.add(run); db.flush()
        try:
            from ..wiki.llm_client import chat_for_org
            messages = [
                {"role": "system", "content": "你是 GE-paw 定时助手，根据用户提示词产生简明的执行结果。"},
                {"role": "user", "content": job.prompt_template},
            ]
            res = chat_for_org(db, job.org_id, messages, temperature=0.2, max_tokens=1024)
            run.status = "succeeded"
            run.output_excerpt = (res.content or "")[:2000]
            run.tokens_in = res.prompt_tokens
            run.tokens_out = res.completion_tokens
            job.failure_count = 0
            job.last_status = "succeeded"
        except Exception as e:
            logger.exception("cron %s 失败: %s", job.id, e)
            run.status = "failed"
            run.error = str(e)[:2000]
            job.failure_count += 1
            job.last_status = "failed"
            if job.failure_count >= CRON_FAILURE_DISABLE_THRESHOLD:
                job.enabled = False
                logger.warning("cron %s 连续失败 %d 次，已自动禁用", job.id, job.failure_count)
        run.finished_at = datetime.now(timezone.utc).replace(tzinfo=None)
        job.last_run_at = datetime.now(timezone.utc).replace(tzinfo=None)
        db.commit()


def _reload_jobs(scheduler: BackgroundScheduler) -> None:
    scheduler.remove_all_jobs()
    with session_scope() as db:
        rows = db.query(CronJob).filter(CronJob.enabled == True).all()  # noqa: E712
        for j in rows:
            try:
                scheduler.add_job(
                    _execute_cron, CronTrigger.from_crontab(j.schedule_cron),
                    id=j.id, args=[j.id], replace_existing=True, misfire_grace_time=300,
                )
            except Exception as e:
                logger.warning("cron %s 注册失败: %s", j.id, e)


def start_scheduler() -> None:
    global _SCHEDULER
    if _SCHEDULER is not None:
        return
    s = BackgroundScheduler(timezone="UTC")
    s.start()
    _reload_jobs(s)
    _SCHEDULER = s
    logger.info("cron 调度器已启动（UTC）")


def stop_scheduler() -> None:
    global _SCHEDULER
    if _SCHEDULER is not None:
        _SCHEDULER.shutdown(wait=False)
        _SCHEDULER = None


def reload() -> None:
    if _SCHEDULER is not None:
        _reload_jobs(_SCHEDULER)
