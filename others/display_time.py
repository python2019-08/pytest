import time
import os
import sys
from datetime import datetime

# 检查系统是否支持 ANSI 转义序列
def is_ansi_terminal():
    if os.name == 'nt':  # Windows 系统
        return 'ANSICON' in os.environ or sys.stdout.isatty()
    return sys.stdout.isatty()

# 使用 ANSI 转义序列实现原地更新
def display_time_ansi():
    try:
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # \r 将光标移到行首，\033[K 清除当前行
            sys.stdout.write(f"\r\033[K{current_time}")
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n程序已停止")

# 使用 curses 库实现原地更新（适用于 Linux/macOS）
def display_time_curses():
    try:
        import curses
        stdscr = curses.initscr()
        curses.cbreak()
        stdscr.nodelay(1)  # 设置非阻塞模式
        
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            stdscr.addstr(0, 0, current_time)
            stdscr.clrtoeol()  # 清除到行尾
            stdscr.refresh()
            time.sleep(1)
            
            # 检测按键退出
            key = stdscr.getch()
            if key == ord('q') or key == 27:  # q 键或 ESC 键
                break
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        if 'curses' in sys.modules:
            curses.endwin()
        print("\n程序已停止")

def display_time():
    if is_ansi_terminal():
        display_time_ansi()
    else:
        display_time_curses()    

if __name__ == "__main__":
    display_time()