import ctypes
import ctypes.wintypes
import logging
logger = logging.getLogger(__name__)

WS_EX_TOOLWINDOW = 0x00000080
WS_EX_APPWINDOW = 0x00040000
WS_EX_NOACTIVATE = 0x08000000
GWL_EXSTYLE = -20
ProcessHideFromInfo = 0x1D

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
ntdll = ctypes.windll.ntdll

def hide_process() -> bool:
    """Hide this process from Task Manager and all enumeration APIs."""
    try:
        current = kernel32.GetCurrentProcess()
        nt_set_info = ntdll.NtSetInformationProcess
        nt_set_info.restype = ctypes.c_long
        nt_set_info.argtypes = [
            ctypes.wintypes.HANDLE,
            ctypes.c_uint,
            ctypes.c_void_p,
            ctypes.c_ulong
        ]
        flag = ctypes.c_ulong(1)
        result = nt_set_info(current, ProcessHideFromInfo, ctypes.byref(flag), ctypes.sizeof(flag))
        if result == 0:
            logger.info("[ANTI-FORENSIC] Process hidden from enumeration")
            return True
        logger.warning(f"[ANTI-FORENSIC] NtSetInfo returned 0x{result:08X}")
        return False
    except Exception as e:
        logger.error(f"[ANTI-FORENSIC] Exception: {e}")
        return False

def cloak_window(window) -> bool:
    """Remove from Alt+Tab, taskbar, and prevent focus stealing."""
    try:
        win_id = int(window.winId())
        style = user32.GetWindowLongW(win_id, GWL_EXSTYLE)
        new_style = style | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE
        new_style &= ~WS_EX_APPWINDOW
        result = user32.SetWindowLongW(win_id, GWL_EXSTYLE, new_style)
        if result:
            logger.info(f"[ANTI-FORENSIC] Window cloaked (HWND {win_id})")
            return True
        logger.warning(f"[ANTI-FORENSIC] SetWindowLongW failed, error {ctypes.get_last_error()}")
        return False
    except Exception as e:
        logger.error(f"[ANTI-FORENSIC] Exception: {e}")
        return False

def apply_all_stealth(window) -> dict:
    """Apply ALL stealth measures: anti-capture + process hide + window cloak."""
    from utils.screen_protect import apply_anti_capture
    results = {
        "anti_capture": apply_anti_capture(int(window.winId())),
        "process_hide": hide_process(),
        "window_cloak": cloak_window(window),
    }
    ok = sum(1 for v in results.values() if v)
    logger.info(f"[ANTI-FORENSIC] Stealth: {ok}/3 active")
    return results
