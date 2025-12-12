#!/bin/bash
# 创建腾讯云转码工具的 DMG 安装包
# 使用 macOS 自带的 hdiutil 工具

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

APP_NAME="腾讯云转码工具"
APP_PATH="dist/${APP_NAME}.app"
DMG_NAME="${APP_NAME}.dmg"
DMG_PATH="dist/${DMG_NAME}"

# 检查应用是否存在
if [ ! -d "$APP_PATH" ]; then
    echo "❌ 错误: 找不到 $APP_PATH"
    echo "请先运行打包脚本: python build_tencent_decode_tool.py"
    exit 1
fi

echo "📦 开始创建 DMG 安装包..."
echo ""

# 创建临时目录
TEMP_DIR=$(mktemp -d)
echo "📁 临时目录: $TEMP_DIR"

# 复制应用和说明文件到临时目录
echo "📋 复制文件..."
cp -R "$APP_PATH" "$TEMP_DIR/"

# 复制使用说明（如果存在）
if [ -f "使用说明.md" ]; then
    cp "使用说明.md" "$TEMP_DIR/"
    echo "  ✅ 已复制使用说明.md"
fi

# 复制快速修复脚本（如果存在）
if [ -f "快速修复.command" ]; then
    cp "快速修复.command" "$TEMP_DIR/"
    chmod +x "$TEMP_DIR/快速修复.command"
    echo "  ✅ 已复制快速修复.command"
fi

# 创建 Applications 的符号链接（可选）
ln -s /Applications "$TEMP_DIR/Applications"
echo "  ✅ 已创建 Applications 链接"

# 移除旧的 DMG（如果存在）
if [ -f "$DMG_PATH" ]; then
    echo "🗑️  删除旧的 DMG 文件..."
    rm "$DMG_PATH"
fi

# 创建 DMG
echo ""
echo "🔨 正在创建 DMG..."
hdiutil create -volname "$APP_NAME" \
    -srcfolder "$TEMP_DIR" \
    -ov \
    -format UDZO \
    "$DMG_PATH"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ DMG 创建成功！"
    echo "📁 文件位置: $DMG_PATH"
    
    # 获取文件大小
    SIZE=$(du -h "$DMG_PATH" | cut -f1)
    echo "📊 文件大小: $SIZE"
    
    # 清理临时目录
    rm -rf "$TEMP_DIR"
    echo ""
    echo "🎉 完成！可以将 $DMG_NAME 分发给其他用户了。"
else
    echo ""
    echo "❌ DMG 创建失败"
    rm -rf "$TEMP_DIR"
    exit 1
fi
