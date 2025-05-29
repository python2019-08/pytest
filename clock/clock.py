"""
在 Ubuntu 上，可以使用 Python 的 `schedule` 库来实现定时任务，并使用 `playsound` 库来播放铃声
（前提是你已经安装了这两个库，如果没有安装，可以使用 `  pip install schedule playsound  ` 进行安装）。
以下是实现每个小时的第 45 分钟响铃一次，并且铃声可以设置的代码示例：
"""
 
# import schedule
import time
from playsound import playsound
import display_time as dispTm
import get_key as getk

# --------------------------------------------
"""
playsound 库在播放音频时，默认情况下是阻塞式的，即播放过程中程序会暂停在播放函数处，
直到音频播放完毕。如果想要中断正在播放的音频，可以使用多线程的方式来实现，通过在主线
程中控制线程的状态来达到中断播放的目的。以下是一个简单的示例代码，展示如何使用 playsound 
并在一定条件下中断音频播放： 
"""
 
import threading
  
class SoundPlayerThread(threading.Thread):
    """
    定义了一个 SoundPlayer 类，继承自 threading.Thread，用于在单独的线程中播放音频。

    请注意，直接终止线程可能会导致一些问题，例如资源未正确释放等，在实际应用中可能需要更
    完善的处理方式。 
    """
    def __init__(self, sound_file):
        threading.Thread.__init__(self)
        self.sound_file = sound_file
        self.is_playing = False

    def run(self):
        """
        run 方法在启动线程时执行，设置 is_playing 标志为 True，然后调用 playsound 
        播放音频， 播放结束后将 is_playing 设置为 False。
        """
        while True:    
            #----  
            if self.is_playing == True :
                try:
                    playsound(self.sound_file)
                finally:
                    self.is_playing = False
            #----
            time.sleep(1)  # seelp 1秒
            
    def startPlay(self):
        self.is_playing = True       

    def stopPlay(self):
        """
        stop 方法将 is_playing 标志设置为 False，虽然 playsound 本身没有直接的停止方法，
        但通过这种方式可以在一定程度上控制线程的状态，并且在示例中通过 join 方法等待线程结束。  
        """
        # 这里对于playsound库本身没有直接停止播放的方法，
        # 但可以通过终止线程来达到类似中断的效果（在某些系统上可能有副作用）
        self.is_playing = False


def ringBell_withThread():
    # getk.installKeyboardListener()

    sound_file = "/home/abner/Music/60s.mp3"  # 请将此处替换为实际的音频文件路径
    player = SoundPlayerThread(sound_file)
    player.start()


    while True:
        current_time = time.localtime()
        minute = current_time.tm_min
        # if minute % 30 == 0:
        if minute == 40:
            player.startPlay()
         
        # 其他程序逻辑
        time.sleep(1)     
        dispTm.display_time()

 
    # player.stopPlay()
    # player.join()

    print("音频播放已处理完毕或已中断")

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
    # ringBell_every30Min()
    ringBell_withThread()