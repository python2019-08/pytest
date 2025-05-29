# import sys
# import time

# try:
#     # Windows
#     import msvcrt
#     def get_key():
#         if msvcrt.kbhit():
#             return msvcrt.getch().decode('utf-8').lower()
#         return None
# except ImportError:
#     # Linux/macOS
#     import tty, termios
#     def get_key():
#         fd = sys.stdin.fileno()
#         old_settings = termios.tcgetattr(fd)
#         try:
#             tty.setraw(sys.stdin.fileno())
#             ch = sys.stdin.read(1)
#         finally:
#             termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#         return ch.lower()
# --
# print("按 ESC 或 q 退出程序...")
# while True:
#     key = get_key()
#     if key == '\x1b':  # ESC 键
#         break
#     elif key == 'q':
#         break
#     # 其他程序逻辑
#     time.sleep(0.1)

# print("程序已退出")



# 在 Python 中捕获键盘按键（如 ESC 或 Q）来退出程序，使用keyboard 库：
# 命令行应用（使用 keyboard 库）,适合交互式命令行工具，可全局监听按键。
# 安装依赖：  pip install keyboard
# python
# 运行
import keyboard
import sys

def on_key_press(e):
    if e.name == 'esc' or (e.name == 'q' and e.event_type == 'down'):
        print("程序已退出")
        sys.exit(0)

def installKeyboardListener():
    # 监听按键事件
    keyboard.on_press(on_key_press)

    # print("按 ESC 或 Q 退出程序...")
    # keyboard.wait()  # 保持程序运行




