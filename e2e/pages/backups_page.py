# -*- coding: utf-8 -*-
"""
gepaw Backups page object.

Wraps all interactions on the backup management page and exposes business-level
methods.
"""
from __future__ import annotations

import logging
from typing import Optional, List
from playwright.sync_api import Page, Locator, expect

from pages.base_page import BasePage
from config.settings import config

logger = logging.getLogger(__name__)


class BackupsPage(BasePage):
    """
    Backups page object.

    Wraps all user interactions on the backup management page:
    - Page navigation and loading
    - Backup list display and search
    - Create backup (full or partial)
    - Restore backup
    - Import backup
    - Delete and export backup
    """

    PAGE_TITLE = "gepaw Console"
    PAGE_URL = f"{config.base_url}/backups"

    # ========== Selector definitions ==========

    # Page container and loading markers
    PAGE_CONTAINER = 'div[class*="backups"], div[class*="Backups"], [class*="backup"]'
    PAGE_LOAD_INDICATOR = '.gepaw-table, [class*="backup"]'
    BREADCRUMB_PARENT = 'span[class*="breadcrumbParent"]'
    BREADCRUMB_CURRENT = 'span[class*="breadcrumbCurrent"]'

    # Backup list table
    BACKUP_TABLE = ".gepaw-table"
    BACKUP_TABLE_ROW = ".gepaw-table-tbody tr"
    BACKUP_TABLE_HEADER = ".gepaw-table-thead th"
    EMPTY_STATE = ".gepaw-empty, [class*='empty']"

    # Action buttons
    CREATE_BACKUP_BUTTON = 'button:has-text("Create Backup"), button:has-text("")'
    IMPORT_BUTTON = 'button:has-text("Import"), button:has-text("")'
    SEARCH_INPUT = '.gepaw-input-search input, input[placeholder*="search"], input[placeholder*=""], input[placeholder*="Search"]'

    # Row-level actions
    EXPORT_BUTTON = 'button:has-text("Export"), button:has-text(""), [class*="export"]'
    RESTORE_BUTTON = 'button:has-text("Restore"), button:has-text("")'
    DELETE_BUTTON = 'button:has-text("Delete"), button:has-text("")'

    # Modal
    MODAL = ".gepaw-modal"
    MODAL_TITLE = ".gepaw-modal-title"
    MODAL_OK_BUTTON = '.gepaw-modal-footer button.gepaw-btn-primary, .gepaw-modal-footer button:has-text("OK"), .gepaw-modal-footer button:has-text("")'
    MODAL_CANCEL_BUTTON = '.gepaw-modal-footer button:has-text("Cancel"), .gepaw-modal-footer button:has-text("")'
    MODAL_CLOSE = ".gepaw-modal-close"

    # Create backup modal
    CREATE_MODAL = '.gepaw-modal:has-text("Create Backup"), .gepaw-modal:has-text("")'
    FULL_BACKUP_OPTION = 'label:has-text("Full"), label:has-text(""), [data-value="full"]'
    PARTIAL_BACKUP_OPTION = 'label:has-text("Partial"), label:has-text(""), [data-value="partial"]'
    BACKUP_NAME_INPUT = 'input[placeholder*="name"], input[placeholder*=""], .gepaw-modal input.gepaw-input'
    AGENT_SELECT = '.gepaw-modal [class*="agent"] .gepaw-select, .gepaw-modal [class*="Agent"]'
    PROGRESS_BAR = '.gepaw-progress, [class*="progress"]'

    # Restore backup modal
    RESTORE_MODAL = '.gepaw-modal:has-text("Restore"), .gepaw-modal:has-text("")'
    FULL_RESTORE_OPTION = 'label:has-text("Full"), label:has-text("")'
    CUSTOM_RESTORE_OPTION = 'label:has-text("Custom"), label:has-text("?)'
    PRE_RESTORE_CONFIRM = '.gepaw-modal:has-text("snapshot"), .gepaw-modal:has-text("")'

    # Import conflict modal
    CONFLICT_MODAL = '.gepaw-modal:has-text("conflict"), .gepaw-modal:has-text(""), .gepaw-modal:has-text("Conflict")'
    OVERWRITE_BUTTON = 'button:has-text("Overwrite"), button:has-text("")'

    # Toast messages
    SUCCESS_TOAST = '.gepaw-message-success, .gepaw-notification-success'
    ERROR_TOAST = '.gepaw-message-error, .gepaw-notification-error'

    # Generic switch and loading
    SWITCH = ".gepaw-switch"
    CHECKBOX = ".gepaw-checkbox"
    SPIN = ".gepaw-spin"

    # ========== Initialization ==========

    def __init__(self, page: Page):
        super().__init__(page)
        logger.info("BackupsPage initialized")

    # ========== Page navigation ==========

    def open(self) -> "BackupsPage":
        """Open the backup management page."""
        logger.info("Opening Backups page")
        self.goto()
        self.wait_for_page_loaded()
        return self

    def wait_for_page_loaded(self, timeout: Optional[int] = None) -> "BackupsPage":
        """Wait for the page to finish loading."""
        timeout = timeout or self.timeout
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        self.page.wait_for_timeout(1000)
        return self

    # ========== Breadcrumb verification ==========

    def get_breadcrumb_text(self) -> str:
        """Return the breadcrumb text."""
        breadcrumb = self.page.locator('[class*="breadcrumb"], [class*="Breadcrumb"]').first
        if breadcrumb.is_visible(timeout=3000):
            return breadcrumb.inner_text().strip()
        return ""

    def verify_breadcrumb(self) -> bool:
        """Verify the breadcrumb contains Settings and Backups."""
        text = self.get_breadcrumb_text()
        has_settings = "Settings" in text or "" in text
        has_backups = "Backups" in text or "" in text
        return has_settings and has_backups

    # ========== Backup list operations ==========

    def get_backup_rows(self) -> List[Locator]:
        """Return all rows in the backup list."""
        rows = self.page.locator(self.BACKUP_TABLE_ROW).all()
        logger.info(f"Found {len(rows)} backup rows")
        return rows

    def get_backup_count(self) -> int:
        """Return the backup count."""
        return len(self.get_backup_rows())

    def is_empty_state(self) -> bool:
        """Return whether the empty state is displayed."""
        empty = self.page.locator(self.EMPTY_STATE).first
        return empty.is_visible(timeout=3000)

    def search_backup(self, keyword: str) -> "BackupsPage":
        """Search backups by keyword."""
        search_input = self.page.locator(self.SEARCH_INPUT).first
        if search_input.is_visible(timeout=5000):
            search_input.fill(keyword)
            self.page.wait_for_timeout(1000)
            logger.info(f"Searched backups with keyword: {keyword}")
        else:
            logger.warning("Search input not found")
        return self

    def get_table_headers(self) -> List[str]:
        """Return the table header texts."""
        headers = self.page.locator(self.BACKUP_TABLE_HEADER).all()
        return [header.inner_text().strip() for header in headers if header.inner_text().strip()]

    # ========== Create backup ==========

    def click_create_backup(self) -> "BackupsPage":
        """Click the create backup button."""
        create_btn = self.page.locator(self.CREATE_BACKUP_BUTTON).first
        expect(create_btn).to_be_visible(timeout=5000)
        create_btn.click()
        self.page.wait_for_timeout(500)
        logger.info("Clicked create backup button")
        return self

    def is_create_modal_visible(self) -> bool:
        """Return whether the create backup modal is visible."""
        modal = self.page.locator(self.MODAL).first
        return modal.is_visible(timeout=5000)

    def select_full_backup(self) -> "BackupsPage":
        """Select full backup mode."""
        full_option = self.page.locator(self.FULL_BACKUP_OPTION).first
        if full_option.is_visible(timeout=3000):
            full_option.click()
            logger.info("Selected full backup mode")
        return self

    def select_partial_backup(self) -> "BackupsPage":
        """Select partial backup mode."""
        partial_option = self.page.locator(self.PARTIAL_BACKUP_OPTION).first
        if partial_option.is_visible(timeout=3000):
            partial_option.click()
            logger.info("Selected partial backup mode")
        return self

    def fill_backup_name(self, name: str) -> "BackupsPage":
        """Fill in the backup name."""
        name_input = self.page.locator(self.BACKUP_NAME_INPUT).first
        if name_input.is_visible(timeout=3000):
            name_input.fill(name)
            logger.info(f"Filled backup name: {name}")
        return self

    def confirm_create_backup(self) -> "BackupsPage":
        """Confirm backup creation."""
        ok_btn = self.page.locator(self.MODAL_OK_BUTTON).first
        if ok_btn.is_visible(timeout=3000):
            ok_btn.click()
            logger.info("Confirmed create backup")
            self.page.wait_for_timeout(2000)
        return self

    def cancel_create_backup(self) -> "BackupsPage":
        """Cancel backup creation."""
        cancel_btn = self.page.locator(self.MODAL_CANCEL_BUTTON).first
        if cancel_btn.is_visible(timeout=3000):
            cancel_btn.click()
            logger.info("Cancelled create backup")
        return self

    def is_progress_visible(self) -> bool:
        """Return whether the progress bar is visible."""
        progress = self.page.locator(self.PROGRESS_BAR).first
        return progress.is_visible(timeout=3000)

    # ========== Import backup ==========

    def click_import_button(self) -> "BackupsPage":
        """Click the import button."""
        import_btn = self.page.locator(self.IMPORT_BUTTON).first
        if import_btn.is_visible(timeout=5000):
            import_btn.click()
            logger.info("Clicked import button")
            self.page.wait_for_timeout(500)
        return self

    # ========== Row-level actions ==========

    def click_row_restore(self, row: Locator) -> "BackupsPage":
        """Click the restore button on the given row."""
        restore_btn = row.locator(self.RESTORE_BUTTON).first
        if restore_btn.is_visible(timeout=3000):
            restore_btn.click()
            logger.info("Clicked row restore button")
            self.page.wait_for_timeout(500)
        return self

    def click_row_delete(self, row: Locator) -> "BackupsPage":
        """Click the delete button on the given row."""
        delete_btn = row.locator(self.DELETE_BUTTON).first
        if delete_btn.is_visible(timeout=3000):
            delete_btn.click()
            logger.info("Clicked row delete button")
            self.page.wait_for_timeout(500)
        return self

    def click_row_export(self, row: Locator) -> "BackupsPage":
        """Click the export button on the given row."""
        export_btn = row.locator(self.EXPORT_BUTTON).first
        if export_btn.is_visible(timeout=3000):
            export_btn.click()
            logger.info("Clicked row export button")
            self.page.wait_for_timeout(500)
        return self

    # ========== Modal operations ==========

    def confirm_modal(self) -> "BackupsPage":
        """Confirm the modal."""
        ok_btn = self.page.locator(self.MODAL_OK_BUTTON).first
        if ok_btn.is_visible(timeout=5000):
            ok_btn.click()
            self.page.wait_for_timeout(1000)
            logger.info("Confirmed modal action")
        return self

    def cancel_modal(self) -> "BackupsPage":
        """Cancel the modal."""
        cancel_btn = self.page.locator(self.MODAL_CANCEL_BUTTON).first
        if cancel_btn.is_visible(timeout=3000):
            cancel_btn.click()
            self.page.wait_for_timeout(500)
            logger.info("Cancelled modal action")
        return self

    def close_modal(self) -> "BackupsPage":
        """Close the modal."""
        close_btn = self.page.locator(self.MODAL_CLOSE).first
        if close_btn.is_visible(timeout=3000):
            close_btn.click()
            self.page.wait_for_timeout(500)
            logger.info("Closed modal")
        return self

    def is_modal_visible(self) -> bool:
        """Return whether any modal is visible."""
        modal = self.page.locator(self.MODAL).first
        return modal.is_visible(timeout=3000)

    # ========== Restore backup ==========

    def is_restore_modal_visible(self) -> bool:
        """Return whether the restore modal is visible."""
        modal = self.page.locator(self.RESTORE_MODAL).first
        return modal.is_visible(timeout=5000)

    def is_pre_restore_confirm_visible(self) -> bool:
        """Return whether the pre-restore snapshot confirmation is visible."""
        confirm = self.page.locator(self.PRE_RESTORE_CONFIRM).first
        return confirm.is_visible(timeout=3000)

    # ========== Toast assertions ==========

    def wait_for_success_message(self, timeout: Optional[int] = None) -> bool:
        """Wait for the success toast to appear."""
        try:
            self.page.locator(self.SUCCESS_TOAST).first.wait_for(
                state="visible", timeout=timeout or 10000
            )
            return True
        except Exception:
            return False

    def wait_for_error_message(self, timeout: Optional[int] = None) -> bool:
        """Wait for the error toast to appear."""
        try:
            self.page.locator(self.ERROR_TOAST).first.wait_for(
                state="visible", timeout=timeout or 5000
            )
            return True
        except Exception:
            return False

    # ========== Assertion methods ==========

    def assert_page_loaded(self, timeout: Optional[int] = None) -> "BackupsPage":
        """Assert that the page has loaded."""
        timeout = timeout or self.timeout
        page_indicator = self.page.locator(
            f'{self.CREATE_BACKUP_BUTTON}, {self.BACKUP_TABLE}, {self.EMPTY_STATE}'
        ).first
        expect(page_indicator).to_be_visible(timeout=timeout)
        return self

    def assert_backup_count(self, expected: int, timeout: Optional[int] = None) -> "BackupsPage":
        """Assert the backup count."""
        expect(self.page.locator(self.BACKUP_TABLE_ROW)).to_have_count(
            expected, timeout=timeout or self.timeout
        )
        return self
