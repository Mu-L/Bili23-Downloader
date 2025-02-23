# 安装程序
## 下载发行版
用户可前往[GitHub Release](https://github.com/ScottSloan/Bili23-Downloader/releases/)页面查看历史版本。  
也可以在下方列表中根据需要选择下载。

| 文件名 | 平台架构 | 下载地址 | 备注 |
| -- | -- | -- | -- |
| Bili23_Downloader_v1.55_release.zip | 通用 | - | 源码版 |
| Bili23-Downloader-1.55.0-win-amd64.zip | Windows x64 | <a href="https://github.com/ScottSloan/Bili23-Downloader/releases/tag/v1.55.0" target="_blank" rel="noreferer">GitHub</a> <br> <a href="https://wwx.lanzout.com/iJNAV2m5jdna" target="_blank" rel="noreferer">蓝奏云</a> | 编译版，附带 FFmpeg |
| Bili23-Downloader_v1.55_win_x64.zip | Windows x64 | - | 编译版，不附带 FFmpeg |

文件 SHA1 值校验
| 文件名 | SHA1 |
| -- | -- |
| Bili23-Downloader-1.55.0-win-amd64.zip | a272880fe688597b1419633f4a75808273d360a2 |

:::tip
下载完成后建议校验 SHA1 值，防止程序被篡改。  

本程序完全开源免费，若是从其他渠道付费获取的，无法保证其安全性和完整性。
:::

## 源码版使用
### 安装 Python 环境
从[Python官网](https://www.python.org/)下载系统对应的 Python，建议使用 3.11 及以上版本，最低支持 3.10 版本。  

若下载速度缓慢，建议使用国内[华为云镜像源](https://mirrors.huaweicloud.com/python/)下载。  

安装时注意勾选`Add python.exe to PATH`，创建环境变量。  

[![pElIuQJ.png](https://s21.ax1x.com/2025/02/23/pElIuQJ.png)](https://imgse.com/i/pElIuQJ)

完成 Python 环境安装后，建议执行下面的命令更换 pip 源为清华源，加快 pip 包下载速度：
```bash
pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

### 克隆仓库
若已安装 git，执行以下命令克隆仓库即可：
```bash
git clone https://github.com/ScottSloan/Bili23-Downloader.git
cd Bili23-Downloader
```

若系统未安装 git，请下载 tar.gz 格式源码并解压，进入到 requirements.txt 同一级目录。

### 安装依赖
执行下面的命令一键安装所需依赖：

```bash
pip install -r requirements.txt
```

下表为程序所需依赖：
| 包 | 版本 | 备注 |
| -- | -- | -- |
| requests | >=2.30.0 | - |
| wxPython | >=4.2.0 | - |
| qrcode[pil] | ==7.4.2 | 必须附带 [pil]，否则程序可能无法运行，不建议使用 8.0 及以上版本。 |

用户也可以手动安装：
```bash
pip install wxPython qrcode[pil]==7.4.2 requests
```

### 运行程序
直接运行 GUI.py 即可打开程序：

```bash
cd src
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
下载完成后，解压压缩包，`以管理员身份`运行 GUI.exe，即可开始使用。 

:::tip
若出现应用程序错误等问题，请尝试修复 DirectX 和 C++ 运行库。  
:::