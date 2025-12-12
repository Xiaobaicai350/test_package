#!/usr/bin/env python3
"""
腾讯云转码工具打包脚本
用于在macOS上打包成.app应用
"""

import os
import sys
import subprocess
import platform


def run_command(command, description=""):
    """执行命令并处理错误"""
    print(f"执行: {description}")
    print(f"命令: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ 成功: {description}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 失败: {description}")
        print(f"错误: {e.stderr}")
        return False


def check_pyinstaller():
    """检查PyInstaller是否安装"""
    return run_command("pyinstaller --version", "检查PyInstaller版本")


def build_app():
    """构建Mac应用"""
    system = platform.system()
    print(f"\n🏗️ 为当前平台构建: {system}")
    
    if system != "Darwin":
        print("⚠️  警告: 此脚本专为macOS设计")
        print("在其他平台上可能无法正常工作")
    
    # 使用spec文件打包
    cmd = 'pyinstaller tencent_decode_tool.spec'
    return run_command(cmd, "构建Mac应用")


def main():
    print("🚀 腾讯云转码工具打包工具")
    print("=" * 50)
    
    # 检查PyInstaller
    if not check_pyinstaller():
        print("请先安装PyInstaller: pip install pyinstaller")
        return
    
    # 检查spec文件是否存在
    if not os.path.exists("tencent_decode_tool.spec"):
        print("❌ 错误: 找不到 tencent_decode_tool.spec 文件")
        return
    
    # 检查主程序文件是否存在
    if not os.path.exists("tencent_decode_tool.py"):
        print("❌ 错误: 找不到 tencent_decode_tool.py 文件")
        return
    
    # 构建应用
    if build_app():
        print("\n✅ 构建完成！")
        print("📁 输出目录: dist/")
        
        # 显示生成的文件
        if os.path.exists("dist"):
            print("🎯 生成的文件:")
            for item in os.listdir("dist"):
                item_path = os.path.join("dist", item)
                if os.path.isdir(item_path):
                    print(f"  - {item}/ (目录)")
                else:
                    size = os.path.getsize(item_path) / 1024 / 1024  # MB
                    print(f"  - {item} ({size:.1f} MB)")
        
        print("\n💡 提示: 可以在 dist/ 目录中找到 '腾讯云转码工具.app'")
    else:
        print("\n❌ 构建失败，请检查错误信息")


if __name__ == "__main__":
    main()
