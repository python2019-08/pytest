import os
from huggingface_hub import hf_hub_download
import torch


# --------------------------------------------------------------------
# os.environ["CURL_CA_BUNDLE"] = ""

# 设置代理（根据实际情况替换为你的代理地址和端口）
os.environ["http_proxy"] = "http://127.0.0.1:8123"
os.environ["https_proxy"] = "http://127.0.0.1:8123"

# --------------------------------------------------------------------
def downloadFile_Flux9665_ToucanTTS_AlignerPt():
    """
    download  http://huggingface.co/Flux9665/ToucanTTS/resolve/main/Aligner.pt
    """
    # 从指定的模型仓库下载文件
    MODEL_DIR = 'Models/'    
    # file_path = hf_hub_download(cache_dir=MODEL_DIR, 
    #                             repo_id="Flux9665/ToucanTTS", 
    #                             filename="Aligner.pt")
    
    file_path = hf_hub_download(
        cache_dir=MODEL_DIR,
        repo_id="Flux9665/ToucanTTS",
        filename="Aligner.pt",
        force_download=False
    ) 

    print(f"文件已下载到: {file_path}")
    device="cuda"
    loadRet =torch.load(file_path, map_location=device)
    print(loadRet) 
    # asr_model =loadRet["asr_model"]
    # print(asr_model)

def downloadFile_Flux9665_ToucanTTS_sadWav():
    # 从指定的模型仓库下载文件
    MODEL_DIR = 'Models/' 

    file_path = hf_hub_download(
        cache_dir=MODEL_DIR,
        repo_id="audios/speaker_references_for_testing",
        filename="sad.wav",
        force_download=False
    )
    # audios/speaker_references_for_testing/sad.wav

    print(f"文件已下载到: {file_path}")

# --------------------------------------------------------------------

from huggingface_hub import snapshot_download

def downloadFolder_Flux9665_SpeechCloning():
    '''
        download Flux9665_SpeechCloning
    '''
    #  https://huggingface.co/spaces/Flux9665/SpeechCloning/tree/main
    repo_id = "Flux9665/SpeechCloning"
    local_dir = "./downloaded_SpeechCloning"

    snapshot_download(
        repo_id=repo_id,
        local_dir=local_dir,
        repo_type="space",  # 明确指定为 Spaces 仓库
        revision="main",
        local_dir_use_symlinks=False
    )

    print(f"所有文件已下载到：{local_dir}")

def downloadFolder_Flux9665_SpeechCloning():
    # https://huggingface.co/Flux9665/ToucanTTS/tree/main
    '''
        download Flux9665_SpeechCloning
    ''' 
    repo_id = "Flux9665/ToucanTTS"
    local_dir = "./Flux9665_ToucanTTS"
 
    try:
        # snapshot_download(
        #     repo_id=repo_id,
        #     local_dir=local_dir,
        #     repo_type="model",  # 明确指定为 model 仓库
        #     revision="main",
        #     timeout=180000 , # 增加超时时间到 timeout 秒
        #     local_dir_use_symlinks=False
        # )
        snapshot_download(
            repo_id=repo_id,
            local_dir=local_dir,
            repo_type="model",  # 明确指定为 model 仓库
            revision="main", 
            local_dir_use_symlinks=False
        )


        print(f"所有文件已下载到：{local_dir}")
    except Exception as e:         
        print(f"下载文件时出错: {e}")

def downloadFolder_Flux9665_MassivelyMultilingualTTS():
    #  https://huggingface.co/spaces/Flux9665/MassivelyMultilingualTTS/tree/main
    repo_id = "Flux9665/MassivelyMultilingualTTS"
    local_dir = "./Flux9665_MassivelyMultilingualTTS"
 
    try: 
        snapshot_download(
            repo_id=repo_id,
            local_dir=local_dir,
            repo_type="space",  # 明确指定为 space 仓库
            revision="main", 
            local_dir_use_symlinks=False
        )


        print(f"所有文件已下载到：{local_dir}")
    except Exception as e:         
        print(f"下载文件时出错: {e}")


       

if __name__=="__main__":
    downloadFile_Flux9665_ToucanTTS_AlignerPt()    
