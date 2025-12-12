#!/bin/bash
# 快速修复脚本 - 移除隔离属性并打开应用
# 双击此文件即可运行

cd "$(dirname "$0")"

echo "=========================================="
echo "  腾讯云转码工具 - 快速修复"
echo "=========================================="
echo ""

APP_NAME="腾讯云转码工具.app"
APP_PATH="./$APP_NAME"

# 检查应用是否存在
if [ ! -d "$APP_PATH" ]; then
    # 尝试在 dist 目录中查找
    if [ -d "dist/$APP_NAME" ]; then
        APP_PATH="dist/$APP_NAME"
    else
        echo "❌ 错误: 找不到 $APP_NAME"
        echo "请确保此脚本和 .app 文件在同一目录下"
        echo ""
        read -p "按回车键退出..."
        exit 1
    fi
fi

echo "📦 找到应用: $APP_PATH"
echo ""
echo "🔧 正在移除隔离属性..."
xattr -cr "$APP_PATH"

if [ $? -eq 0 ]; then
    echo "✅ 隔离属性已移除！"
    echo ""
    echo "🚀 正在打开应用..."
    open "$APP_PATH"
    echo ""
    echo "✅ 完成！应用应该已经打开了。"
else
    echo "❌ 移除隔离属性失败"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi

echo ""
read -p "按回车键退出..."
