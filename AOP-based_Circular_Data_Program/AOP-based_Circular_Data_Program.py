import argparse
import importlib
import os
import shutil
import sys
from pathlib import Path

'''# parser.add_argument方案
DEFAULT_INPUT_DIR = r"E:\Python\PycharmProject-202505-时间序列仓库\数据-20250926-[csv,dat]\data-v1.02"
DEFAULT_OUTPUT_DIR = r"E:\Python\PycharmProject-202505-时间序列仓库\数据-20250926-[csv,dat]\data-v1.03"
DEFAULT_PROGRAM_DIR = r"E:\Python\PycharmProject-202505-时间序列工厂\dat文件-20260311"
DEFAULT_PROGRAM_NAME = r"a.py"
DEFAULT_CALLED_FUNC = r"main"
'''

def _ensure_and_copy_program(script_dir: Path, program_dir: Path, program_name: str) -> Path:
    source_path = program_dir / program_name
    if not source_path.exists():
        raise FileNotFoundError(f"程序文件不存在: {source_path}")
    target_path = script_dir / "copy_program.py"
    shutil.copy2(source_path, target_path)
    return target_path

def _load_copy_program(script_dir: Path):
    script_dir_str = str(script_dir)
    if script_dir_str not in sys.path:
        sys.path.insert(0, script_dir_str)
    import copy_program  # type: ignore[reportMissingImports]
    return importlib.reload(copy_program)

def _run_one_data_program(called_func, input_dir: Path, output_dir: Path, filename: str):
    in_file = str(input_dir / filename)
    out_file = str(output_dir / filename)
    file_dir_list = [in_file, out_file]
    called_func(file_dir_list)

def _aop_based_circular_data_program():
    '''# parser.add_argument方案
    parser = argparse.ArgumentParser(description="数据文件文件夹程序迭代器（单输入输出文件夹版）")
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR, help="输入数据文件文件夹")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="输出数据文件文件夹")
    parser.add_argument("--program-dir", default=DEFAULT_PROGRAM_DIR, help="程序文件文件夹")
    parser.add_argument("--program-name", default=DEFAULT_PROGRAM_NAME, help="程序文件名")
    parser.add_argument("--called-func", default=DEFAULT_CALLED_FUNC, help="被调用函数")

    script_dir = Path(__file__).resolve().parent
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    program_dir = Path(args.program_dir)
    program_name = args.program_name
    arg_called_func = args.called_func
    
    if not hasattr(copy_program, arg_called_func):
        raise AttributeError(f"copy_program.py 中未找到函数: {arg_called_func}")
    called_func = getattr(copy_program, arg_called_func)
    if not callable(called_func):
        raise TypeError(f"copy_program.py 中的 {arg_called_func} 不是可调用对象")
    '''
    input_dir = Path(r"%s" % input('输入数据文件文件夹：'))
    output_dir = Path(r"%s" % input('输出数据文件文件夹：'))
    program_dir = Path(r"%s" % input('程序文件文件夹：'))
    program_name = input('程序文件名：')

    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    script_dir = Path(__file__).resolve().parent
    _ensure_and_copy_program(script_dir, program_dir, program_name)
    copy_program = _load_copy_program(script_dir)
    called_func = getattr(copy_program, input('被调用函数：'))

    entries = sorted(os.listdir(input_dir))
    for name in entries:
        _run_one_data_program(called_func, input_dir, output_dir, name)
    return
    """# 多线程方案
    parser.add_argument("--workers", type=int, default=min(32, (os.cpu_count() or 1) + 4), help="线程数")
    
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    workers = max(1, int(args.workers))
    if workers == 1 or len(entries) <= 1:
        for name in entries:
            _run_one_data_program(called_func, input_dir, output_dir, name)
        return

    errors = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(_run_one_data_program, called_func, input_dir, output_dir, name) for name in entries]
        for fut in as_completed(futures):
            try:
                fut.result()
            except Exception as exc:
                errors.append(exc)

    if errors:
        raise RuntimeError(f"处理过程中出现 {len(errors)} 个错误，首个错误: {errors[0]}")
    """
if __name__ == "__main__":
    _aop_based_circular_data_program()
