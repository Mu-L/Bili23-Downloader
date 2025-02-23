# 安装程序
## 下载发行版
用户可前往[GitHub Release](https://github.com/ScottSloan/Bili23-Downloader/releases/)页面查看历史版本。
也可以在下方列表中下载。

| 文件名 | 平台架构 | 下载地址 | 备注 |
| -- | -- | -- | -- |
| - | 通用 | - | 源码版 |
| Bili23-Downloader-1.55.0-win-amd64.zip | Windows x64 | <a href="https://github.com/ScottSloan/Bili23-Downloader/releases/tag/v1.55.0" target="_blank" rel="noreferer">GitHub</a> <br> <a href="https://wwx.lanzout.com/iJNAV2m5jdna" target="_blank" rel="noreferer">蓝奏云</a> | 编译版，附带 FFmpeg |
| - | Windows x64 | - | 编译版，不附带 FFmpeg |

| 文件名 | SHA1 |
| -- | -- |
| Bili23-Downloader-1.55.0-win-amd64.zip | a272880fe688597b1419633f4a75808273d360a2 |

## 源码版使用
Python 版本需要为 3.10 及以上。

### 克隆仓库
```bash
git clone https://github.com/ScottSloan/Bili23-Downloader.git
cd Bili23-Downloader
```

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行程序
```bash
python3 GUI.py
```

### 安装 wxPython
对于 Linux 用户，pip 源中可能没有提供 wxPython 的包，需要手动编译或[从此下载](https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-22.04/)。  

手动编译请执行以下代码：

```bash
sudo apt install libgtk-3-dev

pip install wxPython
```

## 编译版使用
下载完成后，解压压缩包，以管理员身份运行 GUI.exe，即可开始使用。 

:::tip
若出现应用程序错误等问题，请尝试修复 DirectX 和 C++ 运行库。  
:::