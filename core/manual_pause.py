"""
manual_pause.py — Core Manual Pause
=====================================
Pauses script execution and waits for human input.
Used at OTP step and any other manual checkpoint in flow scripts.

Current scope : OTP pause in Direct Booking flow
Future scope  : Any manual checkpoint across all modules
"""

from colorama import Fore, init

init(autoreset=True)


def manual_pause(message="Action required — press ENTER to continue..."):
    """
    Pauses the script and waits for human to press ENTER.
    Prints a clear message so you know exactly what to do.

    Usage:
        manual_pause("Enter OTP in browser then press ENTER")
    """
    print()
    print(Fore.YELLOW + "─" * 55)
    print(Fore.YELLOW + f"  ⏸  MANUAL STEP REQUIRED")
    print(Fore.YELLOW + f"  →  {message}")
    print(Fore.YELLOW + "─" * 55)
    input(Fore.WHITE + "  Press ENTER when done... ")
    print(Fore.GREEN + "  ✓ Resuming automation")
    print()