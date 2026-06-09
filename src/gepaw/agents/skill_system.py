"""gepaw.agents.skill_system exports."""
from pathlib import Path


class SkillConflictError(Exception):
    """Raised when a skill conflicts with an existing one."""


class SkillInfo:
    """Minimal placeholder for :class:`qwenpaw.agents.skill_system.SkillInfo`."""

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class SkillPoolService:
    """Stub skill pool service."""

    def __init__(self, *args, **kwargs) -> None:
        self._state: dict = {}


class SkillService:
    """Stub workspace-level skill service."""

    def __init__(self, *args, **kwargs) -> None:
        self._state: dict = {}


def apply_skill_config_env_overrides(*args, **kwargs):
    return None


def ensure_skill_pool_initialized(*args, **kwargs):
    return None


def ensure_skills_initialized(*args, **kwargs):
    return None


def reconcile_pool_manifest(*args, **kwargs):
    return None


def reconcile_workspace_manifest(*args, **kwargs):
    return None


def resolve_effective_skills(*args, **kwargs):
    return []


def get_skill_pool_dir():
    """Return the configured skill pool directory."""
    from ...constant import WORKING_DIR
    return WORKING_DIR / "skills" / "pool"


def get_workspace_skills_dir(workspace_dir):
    """Return the workspace skill source directory."""
    workspace_dir = Path(workspace_dir)
    preferred = workspace_dir / "skills"
    legacy = workspace_dir / "skill"
    if preferred.exists():
        return preferred
    if legacy.exists():
        return legacy
    preferred.mkdir(parents=True, exist_ok=True)
    return preferred


def read_skill_manifest(*args, **kwargs):
    return None


def read_skill_pool_manifest(*args, **kwargs):
    return None


__all__ = [
    "SkillConflictError",
    "SkillInfo",
    "SkillPoolService",
    "SkillService",
    "apply_skill_config_env_overrides",
    "ensure_skill_pool_initialized",
    "ensure_skills_initialized",
    "get_skill_pool_dir",
    "get_workspace_skills_dir",
    "read_skill_manifest",
    "read_skill_pool_manifest",
    "reconcile_pool_manifest",
    "reconcile_workspace_manifest",
    "resolve_effective_skills",
]