"""
在 Ubuntu 上，可以使用 Python 的 `playsound` 库来播放铃声
（前提是你已经安装了这个库，如果没有安装，可以使用 `  pip install  playsound  ` 进行安装）。 
"""
# import schedule
import os
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
    def __init__(self , aSoundFile ):
        threading.Thread.__init__(self)
        self.sound_file1 = aSoundFile
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
                    print(f"\n播放铃声: {self.sound_file}")
                    curDirPath = self.get_current_dir_path()
                    soundFile = curDirPath + "/" + self.sound_file
                    # print(f"\n soundFile={soundFile}")

                    playsound(soundFile)
                    time.sleep(30)    
                finally:
                    self.is_playing = False
            #----
            time.sleep(1)  # seelp 1秒
            
    def startPlay(self , aSoundFile="./cock-dawn.mp3" ):
        self.sound_file =aSoundFile
        self.is_playing = True       

    def stopPlay(self):
        """
        stop 方法将 is_playing 标志设置为 False，虽然 playsound 本身没有直接的停止方法，
        但通过这种方式可以在一定程度上控制线程的状态，并且在示例中通过 join 方法等待线程结束。  
        """
        # 这里对于playsound库本身没有直接停止播放的方法，
        # 但可以通过终止线程来达到类似中断的效果（在某些系统上可能有副作用）
        self.is_playing = False

    def get_current_dir_path(self):
        # 使用os模块
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 或者使用pathlib模块
        # current_dir = Path(__file__).resolve().parent
        return current_dir

def ringBell_withThread():
    # getk.installKeyboardListener()
    

    sound_file = "cock-dawn.mp3"  # 请将此处替换为实际的音频文件路径
    player = SoundPlayerThread(sound_file)
    player.start()


    while True:
        current_time = time.localtime()
        minute = current_time.tm_min
        # if minute % 30 == 0:
        # if minute == 38 or minute == 40 or minute == 45 :

        # if minute == 38 : 
        #     player.startPlay("cuckoo4s.mp3")
        if minute == 38 :
            # player.startPlay("cock-dawn.mp3")
            pass
        elif minute == 45 :
            player.startPlay("steam-train-whistle30s.mp3")            
        else :
            player.stopPlay() ## stop
         
        # 其他程序逻辑
        time.sleep(1)     
        dispTm.display_time()

 
    # player.stopPlay()
    # player.join()

    print("音频播放已处理完毕或已中断")