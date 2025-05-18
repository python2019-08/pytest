import torch
import torchvision.models as models

import os
import tensorrt as trt


def export_onnx():
    """
    ### **步骤 1: 准备 PyTorch 模型**
    """
    os.environ['TORCH_HOME'] = '/home/abner/abner2/zdev/ai/pytest/data/resnet50'

    # 加载预训练 ResNet50 模型
    model = models.resnet50(pretrained=True).eval()
    # 导出为 ONNX 格式（TensorRT 支持的中间格式）
    input_tensor = torch.randn(1, 3, 224, 224)  # 输入尺寸 (batch, channel, H, W)
    torch.onnx.export(model, input_tensor, "data/resnet50/resnet50.onnx", opset_version=11)



def build_inferenceEngine():
    """
    ### **步骤 2: 使用 TensorRT 构建推理引擎**
    """
    # 初始化 TensorRT 日志记录器
    TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

    # 构建引擎：读取 ONNX 文件并配置优化参数
    with trt.Builder(TRT_LOGGER) as builder, builder.create_network(
        trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH
    ) as network, trt.OnnxParser(network, TRT_LOGGER) as parser:
        
        # 配置优化参数（如使用 FP16 精度）
        builder.max_workspace_size = 1 << 30  # 工作空间大小（1GB）
        builder.fp16_mode = True  # 启用 FP16 优化
        
        # 解析 ONNX 文件
        with open("data/resnet50/resnet50.onnx", "rb") as f:
            parser.parse(f.read())
        
        # 生成优化后的引擎
        engine = builder.build_cuda_engine(network)

    # 保存引擎（可选，避免重复构建）
    with open("data/resnet50/resnet50.engine", "wb") as f:
        f.write(engine.serialize())    


def infer_byTensorRTInferEngine():
    """
    ### **步骤 3：使用 TensorRT 引擎推理**
    """    
    import numpy as np
    import pycuda.driver as cuda
    import pycuda.autoinit  # 自动初始化 CUDA 环境

    # 加载引擎
    with open("resnet50.engine", "rb") as f, trt.Runtime(TRT_LOGGER) as runtime:
        engine = runtime.deserialize_cuda_engine(f.read())

    # 创建推理上下文
    context = engine.create_execution_context()

    # 准备输入数据（随机图像，需预处理为模型所需格式）
    input_data = np.random.randn(1, 3, 224, 224).astype(np.float32)
    # 计算输入/输出在 GPU 上的缓冲区
    input_idx = engine.get_binding_index("0")  # ONNX 输入节点名通常为 "0"
    output_idx = engine.get_binding_index("1000")  # ResNet50 输出节点名（根据模型而定）

    # 分配 GPU 内存
    d_input = cuda.mem_alloc(input_data.nbytes)
    d_output = cuda.mem_alloc(1 * np.float32(0).nbytes * engine.get_binding_shape(output_idx)[1])
    bindings = [int(d_input), int(d_output)]

    # 执行推理
    stream = cuda.Stream()
    # 复制数据到 GPU
    cuda.memcpy_htod_async(d_input, input_data, stream)
    # 运行推理
    context.execute_async_v2(bindings, stream.handle, None)
    # 复制结果到 CPU
    output = np.empty(engine.get_binding_shape(output_idx), dtype=np.float32)
    cuda.memcpy_dtoh_async(output, d_output, stream)
    stream.synchronize()

    # 输出结果（示例：打印前 5 个类别概率）
    print("Top 5 classes:", np.argsort(output)[0][-5:][::-1])
 
if __name__=="__main__":
    build_inferenceEngine()