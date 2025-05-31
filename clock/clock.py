"""
python -X pycache_prefix="~/.pycache"  clock.py
"""

import clock_thread as thrdClk
# import clock_nothread as noThrdClk
# --------------------------------------------
if __name__ == "__main__": 
    # noThrdClk.ringBell_every30Min()
    thrdClk.ringBell_withThread()