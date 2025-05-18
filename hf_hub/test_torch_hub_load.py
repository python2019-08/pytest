import torch
import os

# 设置自定义的缓存目录
os.environ['TORCH_HOME'] = '/home/abner/abner2/zdev/ai/pytest/'

silero_model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                          model='silero_vad',
                                          force_reload=False,
                                          onnx=False,
                                          verbose=False)
print("silero_model=",silero_model, "utils=",utils)