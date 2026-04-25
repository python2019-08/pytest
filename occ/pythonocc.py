# ```bash
# # conda activate pythonocc
# conda install -c conda-forge pythonocc-core
# ```

from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_SOLID


def extract_physical_params(step_fileName: str,cnPath: str):
    print("-------------------------------------")
    print(f"计算{cnPath}/{step_fileName} 文件的物理参数：")
    # 1. 读取文件
    step_reader = STEPControl_Reader()
    dirPath = "/home/abner/Documents/jobs/dqm/task05agent-darui/POC/"
    step_file_path = dirPath + step_fileName
    status = step_reader.ReadFile(step_file_path)

    if status != 1:  # 读取成功 
        print("错误：无法读取 STP 文件")
        return

    step_reader.TransferRoots()
    shape = step_reader.OneShape()

    explorer = TopExp_Explorer(shape, TopAbs_SOLID)
    total_volume = 0
    total_surface_area = 0
    solids_data = []

    iShp =0
    while explorer.More():
        s = explorer.Current()

        # -------------------------
        props = GProp_GProps()
        # 计算体积属性
        brepgprop.VolumeProperties(s, props) 
        curVolume = props.Mass() # 对于体积属性，Mass() 返回的就是体积值

        # 计算表面积
        surface_props = GProp_GProps()
        brepgprop.SurfaceProperties(s, surface_props)
        curSurfaceArea = surface_props.Mass()   
 
        print(f"{iShp} 体积: {curVolume:.2f} mm³  表面积: {curSurfaceArea:.2f} mm²")
        solids_data.append({
            "vol": curVolume,
            "area": curSurfaceArea
        })        

        # # 3. 计算边界框 (Bounding Box) - 用于了解长宽高
        # bbox = Bnd_Box()
        # brepbndlib.Add(shape, bbox)
        # xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()

        # ----移动到下一个实体 (必须放在最后)
        iShp += 1
        explorer.Next()      

    # 找到体积最大的那个零件
    if solids_data:
        main_part = max(solids_data, key=lambda x: x["vol"])
        print(f"识别到主零件的 体积: {main_part['vol']:.2f} mm³, 面积: {main_part['area']:.2f} mm²") 
     


def extract_physical_params_1(step_fileName: str, cnPath: str):
    print("-------------------------------------")
    step_reader = STEPControl_Reader()
    dirPath = "/home/abner/Documents/jobs/dqm/task05agent-darui/POC/"
    step_file_path = dirPath + step_fileName
    status = step_reader.ReadFile(step_file_path)
    

    if status != 1:
        print(f"错误：无法读取文件 {step_fileName}")
        return

    step_reader.TransferRoots()
    shape = step_reader.OneShape()

    # --- 改进方案：直接对整体进行计算，避免遗漏非 SOLID 零件 ---
    # 计算体积
    v_props = GProp_GProps()
    brepgprop.VolumeProperties(shape, v_props, 1e-6)
    total_volume = v_props.Mass()

    # 计算表面积
    s_props = GProp_GProps()
    brepgprop.SurfaceProperties(shape, s_props)
    total_surface_area = s_props.Mass()

    # 计算边界框（长宽高）
    bbox = Bnd_Box()
    brepbndlib.Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    length = xmax - xmin
    width = ymax - ymin
    height = zmax - zmin

    # --- 单位换算 (mm -> dm) ---
    vol_dm3 = total_volume / 1_000_000
    area_dm2 = total_surface_area / 10_000

    
    print(f"路径标记: {cnPath}")
    print(f"文件名: {step_fileName}")
    print(f"体积: {total_volume:>12.2f} mm³  ({vol_dm3:.4f} dm³)")
    print(f"表面积: {total_surface_area:>12.2f} mm²  ({area_dm2:.4f} dm²)")
    print(f"尺寸: {length:.1f} x {width:.1f} x {height:.1f} mm")

if __name__ == "__main__":
    extract_physical_params("520201-03753.stp","520201-03753-连续模铝巴-连续模冲压-清洗-分选-浸粉-耐压检测-全检-包装")
    extract_physical_params("520201-05597.stp","520201-05597-连续模铝巴-连续模冲压-清洗-全检-包装")
    extract_physical_params("520502-01986.stp","520502-01986-单工位铜巴-单工位冲压-分选-清洗&浸粉-电镀-耐压检测-缠陶瓷带-套耐磨网管-电工胶布固定-贴泡棉-贴二维码标签-检具全检-全检-包装")
    extract_physical_params("520602-11082.stp","520602-11082-单工位铜巴-单工位冲压-分选-清洗-电镀-铆接-检具全检-全检-包装")
