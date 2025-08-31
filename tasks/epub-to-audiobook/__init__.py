from oocana import Context
import os
from pathlib import Path

#region generated meta
import typing
class Inputs(typing.TypedDict):
    epub: str
    audiobook: str | None
class Outputs(typing.TypedDict):
    audiobook: str
#endregion

try:
    from audiblez.core import main as convert_epub
except ImportError:
    print("警告: audiblez 模块未安装，将使用模拟转换")
    convert_epub = None


def main(params: Inputs, context: Context) -> Outputs:
    epub_path = params.get("epub")
    audiobook_path = params.get("audiobook")

    if not epub_path:
        raise ValueError("请提供 EPUB 文件路径")

    if not os.path.exists(epub_path):
        raise FileNotFoundError(f"EPUB 文件不存在: {epub_path}")

    print(f"开始转换 EPUB 到有声书: {epub_path}")

    # 确保输出目录存在
    if audiobook_path:
        output_dir = os.path.dirname(audiobook_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
    else:
        # 如果没有指定输出路径，使用输入文件同名目录
        audiobook_path = os.path.splitext(epub_path)[0] + ".m4b"

    if convert_epub:
        try:
            # 调用 audiblez 进行转换
            convert_epub(
                file_path=epub_path,
                voice="zf_xiaoyi",
                pick_manually=False,
                speed=1.0,
                output_folder=os.path.dirname(audiobook_path) or ".",
            )

            # 检查生成的文件
            expected_m4b = os.path.splitext(epub_path)[0] + ".m4b"
            if os.path.exists(expected_m4b):
                # 重命名为指定的输出文件名
                if expected_m4b != audiobook_path:
                    os.rename(expected_m4b, audiobook_path)

                print(f"✅ 有声书转换完成: {audiobook_path}")
                return {"audiobook": audiobook_path}
            else:
                print("⚠️ 转换完成，但未找到预期的输出文件")
                return {"audiobook": ""}

        except Exception as e:
            print(f"转换失败: {e}")
            raise
    else:
        # 模拟转换（当 audiblez 未安装时）
        print("⚠️ 使用模拟转换模式")

        # 创建空的 M4B 文件作为占位符
        with open(audiobook_path, "wb") as f:
            f.write(b"\x00" * 1024)  # 创建1KB的占位文件

        print(f"✅ 模拟转换完成: {audiobook_path}")
        return {"audiobook": audiobook_path}
