# DXF 转 pdf


### 二、方案2：基于 ezdxf + reportlab（轻量但有局限）
该方案无需安装 DWG TrueView，但仅支持 **DXF 文件（DWG 需先转 DXF）**，且仅能渲染简单的 2D 图形（复杂图纸、块、图层可能丢失），适合简单场景。

#### 前置安装
```bash
pip install ezdxf reportlab
```

#### 代码示例
```python
import ezdxf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pathlib import Path

def dxf_to_pdf(dxf_file_path, pdf_output_path):
    """
    将 DXF 文件（DWG 需先转 DXF）转换为 PDF（仅支持简单 2D 图形）
    """
    dxf_file = Path(dxf_file_path)
    if not dxf_file.exists() or dxf_file.suffix.lower() not in ['.dxf', '.dwg']:
        print("错误：输入文件不存在或不是 DXF/DWG 文件（DWG 需先转 DXF）")
        return False

    # 注意：ezdxf 不支持直接读取 DWG，需先将 DWG 转 DXF（可通过 DWG TrueView 或其他工具）
    if dxf_file.suffix.lower() == '.dwg':
        print("错误：ezdxf 不支持 DWG，请先将 DWG 转换为 DXF")
        return False

    # 读取 DXF 文件
    doc = ezdxf.readfile(dxf_file_path)
    msp = doc.modelspace()

    # 创建 PDF 画布
    c = canvas.Canvas(pdf_output_path, pagesize=A4)
    width, height = A4

    # 简单缩放（适配 A4 页面）
    scale = 0.1  # 根据图纸大小调整
    offset_x = width / 2
    offset_y = height / 2

    # 绘制直线（仅示例，可扩展为圆、多段线等）
    for entity in msp:
        if entity.dxftype() == 'LINE':
            start = entity.dxf.start
            end = entity.dxf.end
            c.line(
                start[0]*scale + offset_x, start[1]*scale + offset_y,
                end[0]*scale + offset_x, end[1]*scale + offset_y
            )
        # 可扩展支持 CIRCLE、POLYLINE 等实体，需自行实现

    # 保存 PDF
    c.save()
    print(f"成功：DXF 转换为 PDF，输出路径：{pdf_output_path}")
    return True

# 测试
if __name__ == "__main__":
    dxf_to_pdf(r"C:\test\sample.dxf", r"C:\test\sample.pdf")
```

### 总结
1. **推荐方案1**：基于 DWG TrueView 的自动化方案，**免费、稳定、支持所有 DWG 版本、无水印**，适合生产环境使用，核心是调用官方的 `DWGToPDF.exe` 命令行工具。
2. **方案2仅作补充**：仅支持 DXF 文件，且仅能渲染简单 2D 图形，适合快速处理简单图纸，不推荐用于复杂 DWG 转换。
3. **关键注意点**：
   - 方案1仅支持 Windows 系统（DWG TrueView 无 macOS/Linux 版本）；
   - 批量转换时注意设置合理的超时时间，避免大图纸转换被中断。

<!-- ----------------------------------------------------  -->
==============================================================
<!-- ----------------------------------------------------  -->

# 2 DWG 文件转换为 PNG 图片

你需要用 Python 实现 DWG 文件转换为 PNG 图片的功能，我依然推荐基于 **DWG TrueView（Autodesk 官方免费工具）** 的自动化方案（稳定、无水印、兼容性最好），同时补充轻量替代方案（适合简单场景）。

### 一、方案1：基于 DWG TrueView 自动化（推荐）
DWG TrueView 本身不直接输出 PNG，但可以先导出为 PDF，再通过 Python 转换 PDF 为 PNG（全程自动化，无人工干预），这是 Windows 下最可靠的免费方案。

#### 前置条件
1. 已安装 **DWG TrueView**（官网下载：https://www.autodesk.com.cn/viewers）；
2. 安装依赖库（用于 PDF 转 PNG）：
   ```bash
   pip install pdf2image pillow
   ```
3. 下载并配置 **poppler**（pdf2image 依赖，Windows 版本：https://github.com/oschwartz10612/poppler-windows/releases），解压后记录 `bin` 目录路径。

#### 完整 Python 代码
```python
import os
import subprocess
import sys
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image

def dwg_to_pdf(dwg_file_path, pdf_output_path, dwg_to_pdf_exe_path=None):
    """
    第一步：DWG 转 PDF（基于 DWG TrueView）
    """
    dwg_file = Path(dwg_file_path)
    if not dwg_file.exists() or dwg_file.suffix.lower() != '.dwg':
        print(f"错误：输入文件 {dwg_file_path} 不存在或不是 DWG 文件")
        return False

    pdf_file = Path(pdf_output_path)
    pdf_file.parent.mkdir(parents=True, exist_ok=True)

    # 自动查找 DWGToPDF.exe 路径
    if dwg_to_pdf_exe_path is None:
        default_exe_paths = [
            r"C:\Program Files\Autodesk\DWG TrueView 2024 - English\GSTARCAD\DWGToPDF.exe",
            r"C:\Program Files\Autodesk\DWG TrueView 2024\AcPlugs\DWGToPDF\DWGToPDF.exe",
            r"C:\Program Files\Autodesk\DWG TrueView 2023 - English\GSTARCAD\DWGToPDF.exe"
        ]
        for exe_path in default_exe_paths:
            if Path(exe_path).exists():
                dwg_to_pdf_exe_path = exe_path
                break
        if dwg_to_pdf_exe_path is None:
            print("错误：未找到 DWGToPDF.exe，请手动指定路径")
            return False

    # 构造 DWG 转 PDF 命令
    cmd = [
        dwg_to_pdf_exe_path,
        "/INPUT", str(dwg_file.absolute()),
        "/OUTPUT", str(pdf_file.absolute()),
        "/PRINT_CONFIG", "DWG To PDF.pc3",
        "/PLOT_STYLE_TABLE", "acad.ctb"
    ]

    try:
        startupinfo = None
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        result = subprocess.run(
            cmd, startupinfo=startupinfo, capture_output=True, text=True, timeout=300
        )

        if result.returncode == 0 and pdf_file.exists():
            print(f"DWG 转 PDF 成功：{pdf_file.absolute()}")
            return True
        else:
            print(f"DWG 转 PDF 失败，返回码：{result.returncode}，错误：{result.stderr}")
            return False
    except Exception as e:
        print(f"DWG 转 PDF 异常：{str(e)}")
        return False

def pdf_to_png(pdf_file_path, png_output_path, poppler_path=None, dpi=300):
    """
    第二步：PDF 转 PNG（高清）
    :param pdf_file_path: PDF 文件路径
    :param png_output_path: PNG 输出路径
    :param poppler_path: poppler 的 bin 目录路径
    :param dpi: 图片分辨率（默认 300 DPI，越高越清晰）
    :return: 转换成功返回 True
    """
    pdf_file = Path(pdf_file_path)
    if not pdf_file.exists():
        print(f"错误：PDF 文件 {pdf_file_path} 不存在")
        return False

    png_file = Path(png_output_path)
    png_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        # 转换 PDF 为图片（支持多页，这里取第一页）
        images = convert_from_path(
            pdf_file_path,
            dpi=dpi,
            poppler_path=poppler_path,  # 替换为你的 poppler/bin 路径
            fmt="png",
            first_page=1,
            last_page=1  # 仅转换第一页，如需多页可调整
        )

        # 保存 PNG
        if images:
            images[0].save(png_output_path, "PNG")
            print(f"PDF 转 PNG 成功：{png_file.absolute()}")
            # 删除临时 PDF 文件（可选）
            # pdf_file.unlink()
            return True
        else:
            print("错误：未从 PDF 中提取到图片")
            return False
    except Exception as e:
        print(f"PDF 转 PNG 异常：{str(e)}")
        return False

def dwg_to_png(dwg_file_path, png_output_path, dwg_to_pdf_exe_path=None, poppler_path=None, dpi=300):
    """
    整合：DWG 直接转 PNG（先转 PDF 再转 PNG）
    """
    # 临时 PDF 文件路径（和 PNG 同目录）
    temp_pdf = Path(png_output_path).parent / (Path(dwg_file_path).stem + "_temp.pdf")

    # 第一步：DWG 转 PDF
    if not dwg_to_pdf(dwg_file_path, str(temp_pdf), dwg_to_pdf_exe_path):
        return False

    # 第二步：PDF 转 PNG
    if not pdf_to_png(str(temp_pdf), png_output_path, poppler_path, dpi):
        return False

    return True

# ------------------- 测试使用 -------------------
if __name__ == "__main__":
    # 替换为你的文件路径
    INPUT_DWG = r"C:\test\sample.dwg"       # 输入 DWG 文件
    OUTPUT_PNG = r"C:\test\sample.png"      # 输出 PNG 文件
    POPPLER_PATH = r"C:\poppler-24.02.0\Library\bin"  # 替换为你的 poppler/bin 路径
    DWG_TO_PDF_EXE = None  # 自动查找，如需手动指定则替换路径

    # 调用转换函数
    success = dwg_to_png(
        dwg_file_path=INPUT_DWG,
        png_output_path=OUTPUT_PNG,
        dwg_to_pdf_exe_path=DWG_TO_PDF_EXE,
        poppler_path=POPPLER_PATH,
        dpi=300  # 分辨率，可调整为 150/600 等
    )

    if success:
        print("✅ DWG 转 PNG 完成！")
    else:
        print("❌ DWG 转 PNG 失败！")
```

#### 代码关键说明
1. **路径配置**：
   - `POPPLER_PATH` 需替换为你下载的 poppler 解压后的 `bin` 目录；
   - `DWG_TO_PDF_EXE` 如自动查找失败，手动指定 DWG TrueView 安装目录下的 `DWGToPDF.exe`；
2. **分辨率控制**：`dpi` 参数控制 PNG 清晰度，300 DPI 是打印级高清，150 DPI 适合预览；
3. **多页支持**：如需转换多页 DWG 导出的 PDF，可修改 `pdf_to_png` 中的 `first_page`/`last_page` 参数；
4. **临时文件**：代码生成的临时 PDF 可选择保留或删除（注释中有取消注释即可）。

### 二、方案2：基于 LibreOffice（跨平台替代）
如果你的系统是 macOS/Linux（无 DWG TrueView），可使用 LibreOffice 先将 DWG 转 PDF（需安装 LibreOffice + DWG 插件），再转 PNG，核心代码如下：
```python
import os
import subprocess
from pathlib import Path
from pdf2image import convert_from_path

def dwg_to_png_libreoffice(dwg_file_path, png_output_path, libreoffice_path=None, poppler_path=None, dpi=300):
    """
    跨平台方案：LibreOffice + pdf2image 实现 DWG 转 PNG（需安装 LibreOffice 和 DWG 插件）
    """
    if libreoffice_path is None:
        libreoffice_path = "libreoffice"  # Linux/macOS 直接用命令，Windows 需指定安装路径

    dwg_file = Path(dwg_file_path)
    temp_pdf = Path(png_output_path).parent / (dwg_file.stem + "_temp.pdf")

    # 第一步：LibreOffice 转 PDF
    cmd = [
        libreoffice_path,
        "--headless", "--convert-to", "pdf",
        "--outdir", str(temp_pdf.parent),
        str(dwg_file.absolute())
    ]
    subprocess.run(cmd, capture_output=True, text=True)

    # 第二步：PDF 转 PNG（和方案1一致）
    images = convert_from_path(str(temp_pdf), dpi=dpi, poppler_path=poppler_path)
    images[0].save(png_output_path, "PNG")
    temp_pdf.unlink()  # 删除临时 PDF
    print(f"转换成功：{png_output_path}")

# 测试（Linux/macOS）
# dwg_to_png_libreoffice("/test/sample.dwg", "/test/sample.png", poppler_path="/usr/bin")
```

### 三、方案3：轻量方案（仅支持简单 DXF）
和之前 DWG 转 PDF 的轻量方案类似，仅支持 DXF（DWG 需先转 DXF），且仅能渲染简单 2D 图形，适合快速测试：
```python
import ezdxf
import matplotlib.pyplot as plt
from pathlib import Path

def dxf_to_png(dxf_file_path, png_output_path, dpi=300):
    """
    仅支持 DXF 文件，渲染简单 2D 图形为 PNG
    """
    dxf_file = Path(dxf_file_path)
    if not dxf_file.exists() or dxf_file.suffix.lower() != '.dxf':
        print("仅支持 DXF 文件，DWG 需先转 DXF")
        return False

    doc = ezdxf.readfile(dxf_file_path)
    msp = doc.modelspace()

    # 创建绘图画布
    fig, ax = plt.subplots(figsize=(10, 10), dpi=dpi)
    ax.set_aspect('equal')
    ax.axis('off')

    # 绘制直线（可扩展圆、多段线等）
    for entity in msp:
        if entity.dxftype() == 'LINE':
            x = [entity.dxf.start[0], entity.dxf.end[0]]
            y = [entity.dxf.start[1], entity.dxf.end[1]]
            ax.plot(x, y, 'k-', linewidth=0.5)

    # 保存 PNG
    plt.tight_layout(pad=0)
    plt.savefig(png_output_path, dpi=dpi, bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"DXF 转 PNG 成功：{png_output_path}")
    return True

# 测试
# dxf_to_png(r"C:\test\sample.dxf", r"C:\test\sample.png")
```

### 总结
1. **首选方案1**：基于 DWG TrueView + pdf2image，**Windows 下最稳定、高清、无水印**，支持所有版本 DWG，适合生产环境；
2. **跨平台选择**：方案2（LibreOffice）适合 macOS/Linux，但需额外安装 DWG 插件，兼容性略差；
3. **轻量测试**：方案3仅支持 DXF，适合简单 2D 图纸，不推荐复杂 DWG；
4. **关键注意点**：
   - 方案1需配置 poppler 路径，否则 pdf2image 无法运行；
   - 分辨率 `dpi` 越高，PNG 文件越大，根据需求调整（预览用 150 DPI，打印用 300+ DPI）。   

======================================================================================

# 3.LibreOffice 的 DWG 插件如何安装

LibreOffice 本身**没有官方 DWG 插件**，但可以通过两种方式实现 DWG 支持：
1. **安装图形过滤器组件**（内置 **DXF** 支持，DWG 需先转 DXF）
2. **安装 LibreDWG**（开源 DWG 读写库，让 LibreOffice 可直接读 DWG）

---

### 一、安装 LibreOffice 图形过滤器（DXF 支持）
#### Windows
1. 关闭所有 LibreOffice 窗口
2. 运行安装程序 → 选择 **修改（Modify）**
3. 在组件列表中展开：
   - **可选组件（Optional Components）** → **图形过滤器（Graphic Filters）**
4. 勾选 **AutoCAD Import（DXF）** → 完成安装
5. 重启 LibreOffice，即可在 Draw 中打开 **.dxf**

#### Linux（Ubuntu/Debian）
```bash
# 安装图形过滤器包（含 DXF 导入）
sudo apt update
sudo apt install libreoffice-graphicfilter
```

#### Linux（Fedora/RHEL）
```bash
sudo dnf install libreoffice-graphicfilter
```

---

### 二、安装 LibreDWG（实现 DWG 直接支持）
#### 1. Ubuntu/Debian 安装
```bash
# 安装依赖与编译工具
sudo apt update
sudo apt install build-essential libtool autoconf automake

# 下载、编译、安装 LibreDWG
git clone https://github.com/LibreDWG/libredwg.git
cd libredwg
./autogen.sh
./configure
make
sudo make install

# 刷新库缓存
sudo ldconfig
```

#### 2. Fedora/RHEL 安装
```bash
sudo dnf install libredwg libredwg-tools
```

#### 3. 配置 LibreOffice 关联 LibreDWG
1. 打开 LibreOffice Draw → **工具 → 选项 → 加载/保存 → 通用**
2. 找到 **文件类型** → 勾选 **AutoCAD DWG (.dwg)**
3. 或在终端用 LibreDWG 命令行转 DXF：
   ```bash
   dwg2dxf input.dwg output.dxf
   ```
   再用 LibreOffice Draw 打开 `output.dxf`

---

### 三、使用 LibreOffice 打开 DWG/DXF
1. 打开 **LibreOffice Draw**
2. **文件 → 打开**，选择 `.dxf` 或 `.dwg`（需 LibreDWG）
3. 打开后可：
   - 编辑图形
   - 导出为 **PDF/PNG**（用于你之前的 DWG 转 PNG 需求）

---

### 四、常见问题与替代方案
- **DWG 打开乱码/缺失**：LibreDWG 对新版 DWG 支持有限，优先用 **dwg2dxf** 转 DXF 再打开
- **跨平台批量转换**：结合 LibreOffice 命令行 + LibreDWG：
  ```bash
  # 批量 DWG → DXF → PDF
  dwg2dxf file.dwg file.dxf
  libreoffice --headless --convert-to pdf file.dxf
  ```
- **Windows 稳定方案**：仍推荐 **DWG TrueView + pdf2image**（兼容性最好）

需要我给你一个可直接运行的 **Python 批量脚本**，自动调用 LibreDWG + LibreOffice 实现 DWG→DXF→PDF→PNG 吗？