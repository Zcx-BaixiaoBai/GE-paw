# -*- coding: utf-8 -*-
"""模型网关核心服务 —— 关键词屏蔽 + 语义识别。

所有模型通信经过此服务进行内容审查。支持：
- 精确关键词匹配（exact）
- 正则表达式匹配（regex）
- 语义相似度匹配（semantic，基于编辑距离+同义词）
"""
from __future__ import annotations

import logging
import re
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import List, Optional, Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session

from ...models.llm import GatewayFilter, GatewayLog

logger = logging.getLogger(__name__)

# ---------- 常见同义词映射表（语义识别用） ----------
_SYNONYM_GROUPS: list[set[str]] = [
    {"绕过", "bypass", "越狱", "jailbreak", "注入", "prompt injection"},
    {"忽略", "ignore", "无视", "disregard", "不要管", "forget"},
    {"系统提示", "system prompt", "系统指令", "system instruction", "初始指令"},
    {"角色扮演", "roleplay", "扮演", "pretend", "假装"},
    {"假装你是", "pretend you are", "假设你是", "imagine you are", "你是一个"},
    {"泄露", "leak", "暴露", "expose", "透露", "reveal", "disclose"},
    {"密码", "password", "口令", "passphrase", "密钥", "secret key"},
    {"删库", "drop database", "删除数据", "rm -rf", "格式化"},
    {"自杀", "suicide", "自残", "self-harm", "结束生命"},
    {"炸弹", "bomb", "爆炸", "explosion", "制造武器", "weapon"},
]

# 构建关键词 -> 同义词集合的索引
_KEYWORD_SYNONYMS: dict[str, set[str]] = {}
for _group in _SYNONYM_GROUPS:
    for _word in _group:
        _KEYWORD_SYNONYMS[_word.lower()] = _group


@dataclass
class FilterHit:
    """单条过滤命中记录。"""
    filter_id: str
    keyword: str
    match_mode: str
    severity: str
    matched_text: str
    confidence: float  # 0.0 ~ 1.0


@dataclass
class GatewayResult:
    """网关审查结果。"""
    passed: bool  # True = 允许通过
    hits: List[FilterHit]
    blocked: bool  # True = 请求被拦截
    warn: bool  # True = 有警告但未拦截


class GatewayService:
    """模型网关服务。"""

    def __init__(self, db: Session, org_id: str = "default"):
        self.db = db
        self.org_id = org_id

    # ---- 公开接口 ----

    def check_messages(
        self,
        messages: list[dict],
        *,
        session_id: str = "",
        user_id: str = "",
        model_name: str = "",
    ) -> GatewayResult:
        """审查一组消息（请求侧）。

        遍历所有消息内容，检查是否包含屏蔽词。
        """
        filters = self._get_active_filters()
        if not filters:
            return GatewayResult(passed=True, hits=[], blocked=False, warn=False)

        # 合并所有消息文本
        text_parts: list[str] = []
        for msg in messages:
            content = msg.get("content", "")
            if isinstance(content, str):
                text_parts.append(content)
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))

        full_text = "\n".join(text_parts)
        hits = self._scan_text(full_text, filters)

        # 更新统计
        self._update_stats(filters, hits, len(messages))

        # 记录日志
        blocked = False
        warn = False
        for hit in hits:
            action = hit.severity
            if hit.severity == "block":
                blocked = True
                action = "blocked"
            elif hit.severity == "warn":
                warn = True
                action = "warned"
            else:
                action = "logged"

            self._log_hit(hit, action, session_id, user_id, model_name)

        return GatewayResult(
            passed=not blocked,
            hits=hits,
            blocked=blocked,
            warn=warn,
        )

    def check_response(
        self,
        response_text: str,
        *,
        session_id: str = "",
        user_id: str = "",
        model_name: str = "",
    ) -> GatewayResult:
        """审查模型响应（响应侧）。"""
        filters = self._get_active_filters()
        if not filters:
            return GatewayResult(passed=True, hits=[], blocked=False, warn=False)

        hits = self._scan_text(response_text, filters)

        self._update_stats(filters, hits, 1)

        blocked = False
        warn = False
        for hit in hits:
            action = hit.severity
            if hit.severity == "block":
                blocked = True
                action = "blocked"
            elif hit.severity == "warn":
                warn = True
                action = "warned"
            else:
                action = "logged"
            self._log_hit(hit, action, session_id, user_id, model_name)

        return GatewayResult(
            passed=not blocked,
            hits=hits,
            blocked=blocked,
            warn=warn,
        )

    # ---- 内部方法 ----

    def _get_active_filters(self) -> list[GatewayFilter]:
        """获取当前 org 下所有启用的过滤规则。"""
        return (
            self.db.query(GatewayFilter)
            .filter(GatewayFilter.org_id == self.org_id, GatewayFilter.enabled == True)
            .all()
        )

    def _scan_text(self, text: str, filters: list[GatewayFilter]) -> list[FilterHit]:
        """对文本执行所有过滤规则。"""
        hits: list[FilterHit] = []
        text_lower = text.lower()

        for f in filters:
            if f.match_mode == "exact":
                hit = self._match_exact(text, text_lower, f)
            elif f.match_mode == "regex":
                hit = self._match_regex(text, f)
            elif f.match_mode == "semantic":
                hit = self._match_semantic(text, text_lower, f)
            else:
                hit = self._match_exact(text, text_lower, f)

            if hit:
                hits.append(hit)

        return hits

    def _match_exact(
        self, text: str, text_lower: str, f: GatewayFilter
    ) -> Optional[FilterHit]:
        """精确关键词匹配。"""
        keyword_lower = f.keyword.lower()
        if keyword_lower in text_lower:
            # 提取上下文
            idx = text_lower.index(keyword_lower)
            start = max(0, idx - 20)
            end = min(len(text), idx + len(f.keyword) + 20)
            context = text[start:end]
            return FilterHit(
                filter_id=f.id,
                keyword=f.keyword,
                match_mode="exact",
                severity=f.severity,
                matched_text=context,
                confidence=1.0,
            )
        return None

    def _match_regex(self, text: str, f: GatewayFilter) -> Optional[FilterHit]:
        """正则表达式匹配。"""
        try:
            pattern = re.compile(f.keyword, re.IGNORECASE)
            match = pattern.search(text)
            if match:
                start = max(0, match.start() - 20)
                end = min(len(text), match.end() + 20)
                context = text[start:end]
                return FilterHit(
                    filter_id=f.id,
                    keyword=f.keyword,
                    match_mode="regex",
                    severity=f.severity,
                    matched_text=context,
                    confidence=1.0,
                )
        except re.error:
            logger.warning("Invalid regex in gateway filter %s: %s", f.id, f.keyword)
        return None

    def _match_semantic(
        self, text: str, text_lower: str, f: GatewayFilter
    ) -> Optional[FilterHit]:
        """语义相似度匹配。

        策略：
        1. 先查同义词表
        2. 再用编辑距离做模糊匹配（阈值 0.75）
        3. 对短文本做子串包含检查
        """
        keyword_lower = f.keyword.lower()

        # 1. 同义词匹配
        synonym_hit = self._check_synonyms(text_lower, keyword_lower)
        if synonym_hit:
            idx = text_lower.find(synonym_hit)
            if idx < 0:
                # 可能 synonym_hit 是同义词而非原文
                for syn in _KEYWORD_SYNONYMS.get(keyword_lower, set()):
                    idx = text_lower.find(syn)
                    if idx >= 0:
                        synonym_hit = syn
                        break
            if idx >= 0:
                start = max(0, idx - 20)
                end = min(len(text), idx + len(synonym_hit) + 20)
                context = text[start:end]
                return FilterHit(
                    filter_id=f.id,
                    keyword=f.keyword,
                    match_mode="semantic",
                    severity=f.severity,
                    matched_text=context,
                    confidence=0.85,
                )

        # 2. 滑动窗口编辑距离
        kw_len = len(keyword_lower)
        if kw_len < 2:
            return None

        best_ratio = 0.0
        best_start = 0
        window = kw_len + max(3, kw_len // 3)
        step = max(1, kw_len // 4)

        for i in range(0, len(text_lower) - kw_len + 1, step):
            chunk = text_lower[i : i + window]
            ratio = SequenceMatcher(None, keyword_lower, chunk).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_start = i

        if best_ratio >= 0.75:
            start = max(0, best_start - 20)
            end = min(len(text), best_start + window + 20)
            context = text[start:end]
            return FilterHit(
                filter_id=f.id,
                keyword=f.keyword,
                match_mode="semantic",
                severity=f.severity,
                matched_text=context,
                confidence=round(best_ratio, 2),
            )

        return None

    def _check_synonyms(self, text_lower: str, keyword_lower: str) -> Optional[str]:
        """检查关键词或其同义词是否出现在文本中。"""
        # 直接同义词查找
        synonyms = _KEYWORD_SYNONYMS.get(keyword_lower, set())
        for syn in synonyms:
            if syn.lower() in text_lower:
                return syn.lower()

        # 反向查找：文本中的词是否属于关键词的同义词组
        for group in _SYNONYM_GROUPS:
            if keyword_lower in {w.lower() for w in group}:
                for word in group:
                    if word.lower() != keyword_lower and word.lower() in text_lower:
                        return word.lower()

        return None

    def _update_stats(
        self,
        filters: list[GatewayFilter],
        hits: list[FilterHit],
        message_count: int,
    ) -> None:
        """更新过滤规则的统计字段。"""
        hit_filter_ids = {h.filter_id for h in hits}
        hit_counts: dict[str, int] = {}
        block_counts: dict[str, int] = {}
        for h in hits:
            hit_counts[h.filter_id] = hit_counts.get(h.filter_id, 0) + 1
            if h.severity == "block":
                block_counts[h.filter_id] = block_counts.get(h.filter_id, 0) + 1

        for f in filters:
            f.total_checks += message_count
            if f.id in hit_filter_ids:
                f.detect_count += hit_counts.get(f.id, 1)
            if f.id in block_counts:
                f.block_count += block_counts.get(f.id, 1)

        try:
            self.db.flush()
        except Exception:
            self.db.rollback()

    def _log_hit(
        self,
        hit: FilterHit,
        action: str,
        session_id: str,
        user_id: str,
        model_name: str,
    ) -> None:
        """记录一条拦截日志。"""
        log = GatewayLog(
            org_id=self.org_id,
            filter_id=hit.filter_id,
            keyword=hit.keyword,
            matched_text=hit.matched_text[:1000],
            match_mode=hit.match_mode,
            severity=hit.severity,
            action_taken=action,
            session_id=session_id or None,
            user_id=user_id or None,
            model_name=model_name or None,
        )
        self.db.add(log)
        try:
            self.db.flush()
        except Exception:
            self.db.rollback()
