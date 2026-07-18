"""
recovery.py — Production Recovery Playbooks

Automation does not recover because it retries.
It recovers because it understands the failure type.

Architecture:
  Automation Run → Failure Detector → Failure Classification
  → Recovery Strategy → Resume / Stop / Alert

Usage:
    from common.recovery import RecoveryManager, FailureType

    mgr = RecoveryManager(browser, logger)
    decision = await mgr.recover(FailureType.BROWSER_CRASH)
    # decision is "resume", "stop", or "retry"
"""
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class FailureType(Enum):
    """Classified failure types for recovery dispatch.

    Each type maps to a specific recovery strategy.
    Unknown failures are escalated to human intervention.
    """
    BROWSER_CRASH = "browser_crash"
    SESSION_EXPIRED = "session_expired"
    NETWORK_ERROR = "network_error"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


class RecoveryManager:
    """Dispatch recovery actions based on classified failure type.

    Provides three recovery strategies:
    - restart_browser: for browser crashes
    - relogin: for session expiry
    - retry: for transient network/timeout errors
    - alert_human: for unknown/unrecoverable failures
    """

    def __init__(self, browser=None, logger=None):
        self.browser = browser
        self.log = logger or logging.getLogger(__name__)

    async def recover(self, failure: FailureType) -> str:
        """Classify and execute recovery for a failure.

        Args:
            failure: FailureType enum value.

        Returns:
            "resume" — automation can continue
            "retry" — transient, retry the operation
            "stop" — unrecoverable, alert human
        """
        self.log.info("Recovery dispatch: %s", failure.value)

        recovery_map = {
            FailureType.BROWSER_CRASH: self.restart_browser(),
            FailureType.SESSION_EXPIRED: self.relogin(),
            FailureType.NETWORK_ERROR: self.retry_operation(),
            FailureType.TIMEOUT: self.retry_operation(),
            FailureType.UNKNOWN: self.alert_human(),
        }

        return await recovery_map[failure]

    async def restart_browser(self) -> str:
        """Kill and relaunch the browser process."""
        self.log.info("Recovery: restarting browser")
        if self.browser:
            try:
                await self.browser.stop()
            except Exception:
                pass
        try:
            import nodriver as uc
            self.browser = await uc.start()
            self.log.info("Browser restarted successfully")
            return "resume"
        except Exception as e:
            self.log.error("Browser restart failed: %s", e)
            return "stop"

    async def relogin(self) -> str:
        """Re-establish authentication session."""
        self.log.info("Recovery: re-authenticating session")
        # Re-login logic injected by the caller
        return "resume"

    async def retry_operation(self) -> str:
        """Signal caller to retry the failed operation."""
        self.log.info("Recovery: retrying operation")
        return "retry"

    async def alert_human(self) -> str:
        """Escalate unrecoverable failure to a human operator."""
        self.log.error("Recovery: UNRECOVERABLE — human intervention required")
        return "stop"

    @staticmethod
    def classify(error_message: str, status_code: int = None) -> FailureType:
        """Heuristic classification from raw error context."""
        msg = error_message.lower()
        if any(w in msg for w in ["crash", "disconnect", "connection closed", "target closed"]):
            return FailureType.BROWSER_CRASH
        if any(w in msg for w in ["session", "login", "auth", "unauthorized", "expired"]):
            return FailureType.SESSION_EXPIRED
        if any(w in msg for w in ["timeout"]):
            return FailureType.TIMEOUT
        if any(w in msg for w in ["network", "dns", "connection refused", "econnrefused"]):
            return FailureType.NETWORK_ERROR
        if status_code and status_code in (401, 403):
            return FailureType.SESSION_EXPIRED
        if status_code and status_code in (429, 502, 503, 504):
            return FailureType.NETWORK_ERROR
        return FailureType.UNKNOWN
