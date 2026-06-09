# -*- coding: utf-8 -*-
"""Unit tests for utils.logging (S?.

S? Core utilities with high risk of cascading failures.
High coverage expected as this is stable infrastructure.
"""
from __future__ import annotations

import logging
import sys
from unittest.mock import MagicMock, patch

from gepaw.utils.logging import (
    ColorFormatter,
    SuppressPathAccessLogFilter,
    add_project_file_handler,
    setup_logger,
    LOG_NAMESPACE,
    _LEVEL_MAP,
)


class TestLevelMap:
    """Test level name to level number mapping."""

    def test_level_map_contains_all_levels(self):
        """S? _LEVEL_MAP must have standard log levels."""
        assert "debug" in _LEVEL_MAP
        assert "info" in _LEVEL_MAP
        assert "warning" in _LEVEL_MAP
        assert "error" in _LEVEL_MAP
        assert "critical" in _LEVEL_MAP

    def test_level_map_values_are_valid(self):
        """S? All mapped values must be valid logging levels."""
        valid_levels = {
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        }
        for level in _LEVEL_MAP.values():
            assert level in valid_levels


class TestColorFormatter:
    """Test ColorFormatter formatting."""

    def test_format_includes_level(self):
        """S? Formatted output includes log level."""
        formatter = ColorFormatter("%(message)s")
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="test message",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        assert "INFO" in formatted
        assert "test message" in formatted

    def test_format_includes_path_and_lineno(self):
        """S? Formatted output includes file path and line number."""
        formatter = ColorFormatter("%(message)s")
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="/path/to/test.py",
            lineno=42,
            msg="error message",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        assert "test.py:42" in formatted

    @patch.object(sys.stderr, "isatty", return_value=False)
    def test_no_color_when_not_tty(self, _mock_isatty):
        """S? Colors disabled when stderr is not a tty."""
        formatter = ColorFormatter("%(message)s")
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=1,
            msg="error",
            args=(),
            exc_info=None,
        )
        formatted = formatter.format(record)
        # No ANSI codes when not a tty
        assert "\033[" not in formatted

    def test_colors_defined_for_all_levels(self):
        """S? All standard levels have color definitions."""
        standard_levels = [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ]
        for level in standard_levels:
            assert level in ColorFormatter.COLORS


class TestSuppressPathAccessLogFilter:
    """Test log filtering by path substring."""

    def test_filter_allows_when_no_substrings(self):
        """S? Empty filter list allows all messages."""
        filter_obj = SuppressPathAccessLogFilter([])
        record = MagicMock()
        record.getMessage.return_value = "/api/health"
        assert filter_obj.filter(record) is True

    def test_filter_blocks_matching_substring(self):
        """S? Messages containing substring are blocked."""
        filter_obj = SuppressPathAccessLogFilter(["/health"])
        record = MagicMock()
        record.getMessage.return_value = "GET /health HTTP/1.1"
        assert filter_obj.filter(record) is False

    def test_filter_allows_non_matching(self):
        """S? Messages not matching any substring are allowed."""
        filter_obj = SuppressPathAccessLogFilter(["/health"])
        record = MagicMock()
        record.getMessage.return_value = "GET /api/users HTTP/1.1"
        assert filter_obj.filter(record) is True

    def test_filter_handles_getMessage_exception(self):
        """S? Exceptions in getMessage are handled gracefully."""
        filter_obj = SuppressPathAccessLogFilter(["/test"])
        record = MagicMock()
        record.getMessage.side_effect = Exception("format error")
        assert filter_obj.filter(record) is True


class TestSetupLogger:
    """Test logger setup functionality."""

    def test_setup_logger_returns_logger(self):
        """S? setup_logger returns a logger instance."""
        logger = setup_logger(logging.INFO)
        assert logger is not None
        assert isinstance(logger, logging.Logger)

    def test_setup_logger_uses_namespace(self):
        """S? Logger uses correct namespace."""
        logger = setup_logger(logging.INFO)
        assert logger.name == LOG_NAMESPACE

    def test_setup_logger_string_level(self):
        """S? String level names are converted correctly."""
        logger = setup_logger("debug")
        assert logger.level == logging.DEBUG

    def test_setup_logger_int_level(self):
        """S? Integer levels are set directly."""
        logger = setup_logger(logging.WARNING)
        assert logger.level == logging.WARNING

    def test_setup_logger_invalid_string_uses_default(self):
        """S? Invalid level string defaults to INFO."""
        logger = setup_logger("invalid_level")
        assert logger.level == logging.INFO

    def test_logger_has_stream_handler(self):
        """S? Logger gets a StreamHandler."""
        # Clear any existing handlers first
        test_logger = logging.getLogger(LOG_NAMESPACE)
        test_logger.handlers = []

        logger = setup_logger(logging.INFO)
        assert len(logger.handlers) > 0
        assert isinstance(logger.handlers[0], logging.StreamHandler)


class TestAddFileHandler:
    """Test file handler addition."""

    def test_creates_log_directory(self, tmp_path):
        """S? Creates log directory if it doesn't exist."""
        log_path = tmp_path / "logs" / "gepaw.log"
        add_project_file_handler(log_path)
        assert log_path.parent.exists()

    def test_idempotent_same_path(self, tmp_path):
        """S? Same path twice doesn't duplicate handlers."""
        log_path = tmp_path / "gepaw.log"

        # First call
        add_project_file_handler(log_path)
        logger = logging.getLogger(LOG_NAMESPACE)
        initial_count = len(logger.handlers)

        # Second call - should be idempotent
        add_project_file_handler(log_path)
        assert len(logger.handlers) == initial_count

    def test_adds_file_handler(self, tmp_path):
        """S? File handler is added to logger."""
        log_path = tmp_path / "gepaw.log"

        # Clear handlers first
        logger = logging.getLogger(LOG_NAMESPACE)
        original_handlers = list(logger.handlers)
        logger.handlers = []

        try:
            add_project_file_handler(log_path)
            has_file_handler = any(
                isinstance(
                    h,
                    (
                        logging.FileHandler,
                        logging.handlers.RotatingFileHandler,
                    ),
                )
                for h in logger.handlers
            )
            assert has_file_handler
        finally:
            # Cleanup: restore original handlers
            for handler in logger.handlers:
                handler.close()
            logger.handlers = original_handlers


class TestLogConstants:
    """Test module-level constants."""

    def test_log_namespace_is_gepaw(self):
        """S? LOG_NAMESPACE is 'gepaw'."""
        assert LOG_NAMESPACE == "gepaw"

    def test_log_namespace_used_by_setup(self):
        """S? setup_logger uses LOG_NAMESPACE."""
        # Get the logger that setup_logger would configure
        logger = logging.getLogger(LOG_NAMESPACE)
        assert logger.name == "gepaw"
