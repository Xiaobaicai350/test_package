#!/bin/bash
# 移除腾讯云转码工具的隔离属性
# 双击此文件运行，或在终端中执行: bash 移除隔离属性.sh

echo "正在移除隔离属性..."
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_PATH="$SCRIPT_DIR/腾讯云转码工具.app"

# 检查应用是否存在
if [ ! -d "$APP_PATH" ]; then
    echo "❌ 错误: 找不到 腾讯云转码工具.app"
    echo "请确保此脚本和 .app 文件在同一目录下"
    exit 1
fi

# 移除隔离属性
xattr -cr "$APP_PATH"

if [ $? -eq 0 ]; then
    echo "✅ 成功移除隔离属性！"
    echo ""
    echo "现在可以尝试打开应用了："
    echo "1. 右键点击 '腾讯云转码工具.app'"
    echo "2. 选择 '打开'"
    echo ""
else
    echo "❌ 移除隔离属性失败"
    exit 1
fi
