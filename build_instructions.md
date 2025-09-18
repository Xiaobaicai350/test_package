# Todo管理器 - 打包说明

## 已完成的打包

### macOS版本
- **文件位置**: `dist/Todo管理器.app`
- **使用方式**: 双击运行，或通过终端 `open dist/Todo管理器.app`
- **文件大小**: 约 9.8 MB

### 单独可执行文件
- **文件位置**: `dist/Todo管理器`
- **使用方式**: 通过终端运行 `./dist/Todo管理器`

## 跨平台打包说明

### Windows平台 (.exe文件)
如需要在Windows上打包，请在Windows系统上运行：
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Todo管理器" main.py
```

### Linux平台
在Linux系统上运行：
```bash
pip install pyinstaller
pyinstaller --onefile --name "Todo管理器" main.py
```

## 分发说明

### macOS用户
- 分发 `Todo管理器.app` 文件夹
- 用户可直接双击运行
- 首次运行可能需要在"系统偏好设置 > 安全性与隐私"中允许运行

### Windows用户
- 需要在Windows系统上重新打包生成 `.exe` 文件
- 或者提供Python环境安装说明

### 通用方案
- 分发整个项目文件夹
- 提供 `requirements.txt` 文件
- 用户安装Python后运行 `pip install -r requirements.txt && python main.py`

## 文件结构
```
PythonProject/
├── main.py                 # 主程序
├── todos.json             # 数据文件（运行后生成）
├── dist/                  # 打包输出目录
│   ├── Todo管理器         # 可执行文件
│   └── Todo管理器.app     # macOS应用包
├── build/                 # 打包临时文件
└── Todo管理器.spec        # PyInstaller配置文件
```

## 优化建议
1. 可以添加应用图标 (--icon参数)
2. 可以使用 --onedir 模式减少启动时间
3. 可以排除不需要的模块减小文件大小
