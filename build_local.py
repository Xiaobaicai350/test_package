#!/usr/bin/env python3
"""
本地跨平台打包脚本
使用Docker在macOS上为Windows打包exe文件
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

def check_docker():
    """检查Docker是否安装并运行"""
    return run_command("docker --version", "检查Docker版本")

def build_windows_exe():
    """使用Docker为Windows构建exe文件"""
    print("\n🏗️ 开始为Windows构建exe文件...")
    
    # 创建Dockerfile
    dockerfile_content = '''
FROM python:3.11-windowsservercore

# 安装PyInstaller
RUN pip install pyinstaller

# 设置工作目录
WORKDIR /app

# 复制源码
COPY main.py .

# 构建exe
RUN pyinstaller --onefile --windowed --name "Todo管理器-Windows" main.py

# 输出目录
VOLUME ["/app/dist"]
'''
    
    with open('Dockerfile.windows', 'w', encoding='utf-8') as f:
        f.write(dockerfile_content)
    
    commands = [
        "docker build -f Dockerfile.windows -t todo-windows .",
        "docker run --rm -v $(pwd)/dist-windows:/app/dist todo-windows",
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Docker构建步骤"):
            return False
    
    return True

def build_current_platform():
    """为当前平台构建"""
    system = platform.system()
    print(f"\n🏗️ 为当前平台构建: {system}")
    
    if system == "Darwin":  # macOS
        cmd = 'pyinstaller --onefile --windowed --name "Todo管理器-macOS" main.py'
    elif system == "Windows":
        cmd = 'pyinstaller --onefile --windowed --name "Todo管理器-Windows" main.py'
    else:  # Linux
        cmd = 'pyinstaller --onefile --name "Todo管理器-Linux" main.py'
    
    return run_command(cmd, f"构建{system}版本")

def main():
    print("🚀 Todo应用跨平台打包工具")
    print("=" * 50)
    
    # 检查PyInstaller
    if not run_command("pyinstaller --version", "检查PyInstaller"):
        print("请先安装PyInstaller: pip install pyinstaller")
        return
    
    # 为当前平台构建
    build_current_platform()
    
    # 如果是macOS且安装了Docker，尝试构建Windows版本
    if platform.system() == "Darwin":
        print("\n🤔 检测到macOS系统，尝试使用Docker构建Windows版本...")
        
        if check_docker():
            print("⚠️  注意: Docker方式构建Windows exe可能不稳定")
            print("推荐使用GitHub Actions进行跨平台构建")
            
            choice = input("是否继续使用Docker构建Windows版本? (y/N): ").lower()
            if choice == 'y':
                build_windows_exe()
            else:
                print("跳过Docker构建")
        else:
            print("❌ Docker未安装，无法本地构建Windows版本")
            print("\n📋 推荐方案:")
            print("1. 使用GitHub Actions自动构建 (推荐)")
            print("2. 在Windows虚拟机中构建")
            print("3. 让Windows用户自行安装Python环境")
    
    print("\n✅ 构建完成！")
    print("📁 输出目录: dist/")
    
    # 显示生成的文件
    if os.path.exists("dist"):
        print("🎯 生成的文件:")
        for file in os.listdir("dist"):
            file_path = os.path.join("dist", file)
            size = os.path.getsize(file_path) / 1024 / 1024  # MB
            print(f"  - {file} ({size:.1f} MB)")

if __name__ == "__main__":
    main()
