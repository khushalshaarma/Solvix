import ctypes
import ctypes.wintypes
import logging
logger = logging.getLogger(__name__)

WDA_EXCLUDEFROMCAPTURE = 0x00000011
user32 = ctypes.windll.user32

def apply_anti_capture(win_id: int) -> bool:
    """Make window invisible to ALL screenshots, recordings, screen sharing."""
    try:
        result = user32.SetWindowDisplayAffinity(
            ctypes.wintypes.HWND(win_id),
            ctypes.wintypes.DWORD(WDA_EXCLUDEFROMCAPTURE)
        )
        if result:
            logger.info(f"[ANTI-CAPTURE] Applied WDA_EXCLUDEFROMCAPTURE to HWND {win_id}")
        else:
            logger.warning(f"[ANTI-CAPTURE] Failed, error {ctypes.get_last_error()}")
        return bool(result)
    except Exception as e:
        logger.error(f"[ANTI-CAPTURE] Exception: {e}")
        return False
