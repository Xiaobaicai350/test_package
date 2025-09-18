# Todo管理器

一个简单易用的Todo任务管理应用，支持任务分类、状态管理和数据持久化。

## 功能特性

- ✅ 添加、删除、修改Todo任务
- 📂 任务分类（工作、个人、学习、生活）
- 🔍 按分类和状态筛选任务
- 💾 自动保存到JSON文件
- 🖥️ 跨平台支持（Windows、macOS、Linux）
- 🎨 现代化GUI界面

## 快速开始

### 方式1: 下载可执行文件 (推荐)

1. 访问 [Releases页面](../../releases)
2. 下载适合您系统的版本：
   - Windows: `Todo管理器-Windows.exe`
   - macOS: `Todo管理器-macOS`
   - Linux: `Todo管理器-Linux`
3. 双击运行

### 方式2: 源码运行

```bash
# 克隆项目
git clone <repository-url>
cd PythonProject

# 运行应用
python main.py
```

## 跨平台打包

### 自动化构建 (GitHub Actions)

项目已配置GitHub Actions，每次提交代码会自动为Windows、macOS、Linux构建可执行文件。

### 本地构建

```bash
# 安装打包工具
pip install pyinstaller

# 使用本地构建脚本
python build_local.py

# 或手动构建当前平台
pyinstaller --onefile --windowed --name "Todo管理器" main.py
```

### macOS用户构建Windows版本

由于PyInstaller的限制，在macOS上无法直接构建Windows exe文件。推荐方案：

1. **使用GitHub Actions** (推荐)
   - 提交代码到GitHub
   - Actions自动构建所有平台版本

2. **使用Windows虚拟机**
   - 安装Windows虚拟机
   - 在虚拟机中运行构建命令

3. **云服务构建**
   - 使用GitHub Codespaces
   - 使用其他云端Windows环境

## 文件结构

```
PythonProject/
├── main.py                    # 主程序
├── todos.json                 # 数据文件 (自动生成)
├── requirements.txt           # 依赖列表
├── build_local.py            # 本地构建脚本
├── build_instructions.md     # 详细构建说明
├── .github/
│   └── workflows/
│       └── build.yml         # GitHub Actions配置
└── dist/                     # 构建输出目录
```

## 开发说明

- Python 3.6+
- 使用Tkinter GUI框架
- JSON数据存储
- 面向对象设计

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
