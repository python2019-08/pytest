"""
在 Ubuntu 上，可以使用 Python 的 `schedule` 库来实现定时任务，并使用 `playsound` 库来播放铃声
（前提是你已经安装了这两个库，如果没有安装，可以使用 `  pip install schedule playsound  ` 进行安装）。
以下是实现每个小时的第 45 分钟响铃一次，并且铃声可以设置的代码示例：
"""
 
import schedule
import time
from playsound import playsound
import display_time as dispTm 
 

# ---------------------------------------------

def ring_bell():
    """播放铃声的函数
      `ring_bell` 函数用于播放指定的铃声文件，你需要将 sound_file 替换为你实际的铃声文件路径，
      可以是 MP3 格式或其他 `playsound` 库支持的音频格式。
    """
    # 在这里指定铃声文件的路径，你可以根据需要修改为自己的铃声文件
    sound_file = "/home/abner/Music/60s.mp3"
    print(f"\n播放铃声: {sound_file}")
    try:
        playsound(sound_file)
    except Exception as e:
        print(f"播放铃声时出错: {e}")

# -------------------------------------------- 
def ringBell_everyHour45Min(): 
    # 这行代码设置了一个定时任务，使得 `ring_bell` 函数在每个小时的第 45 分钟执行。
    # schedule.every().hour.at(":45").do(ring_bell)
    #  **notWork**
    schedule.every().hour.at(":35").do(ring_bell)

    #     最后通过一个无限循环 `while True` 来不断检查是否有任务需要执行，并通过 
    # `time.sleep(1)` 让程序每隔 1 秒检查一次。
    print("定时任务已启动，按 Ctrl+C 停止...")
    while True:
        schedule.run_pending()
        time.sleep(1)

# --------------------------------------------
def ringBell_every30Min():
    """    
    使用 while True 构建一个无限循环，在循环中，通过 time.localtime() 获取当前的
    本地时间，提取出当前分钟数 minute。

    判断 minute 是否为 30 的倍数（即 minute % 30 == 0），如果是，则调用 ring_bell 
    函数播放铃声。

    最后通过 time.sleep(1) 让程序暂停 1 秒，以控制检查时间的频率为每秒一次。 
    """
    while True:
        current_time = time.localtime()
        minute = current_time.tm_min
        # if minute % 30 == 0:
        if minute == 47:
            ring_bell()
        time.sleep(1)  # 每秒检查一次当前时间 
        
        dispTm.display_time()


# --------------------------------------------
if __name__ == "__main__":
    ringBell_every30Min() 