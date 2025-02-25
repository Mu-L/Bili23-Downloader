# 安装 FFmpeg
程序依赖 FFmpeg 实现音视频合成，格式转换，直播录制等功能，缺少时将影响正常使用。

:::tip
若使用的是附带 FFmpeg 的编译版，无需再次安装。
:::

## Windows 
Windows 用户需手动下载，并创建环境变量。

[官网下载](https://ffmpeg.org/)  
[蓝奏云](https://wwx.lanzout.com/iMJkM2oup3mh) 密码：dnn9（来源于：gyan.dev，版本：7.1）

## Linux
### 方式一：包管理器安装
对于基于 Debain 的系统，在终端中执行以下命令：
```bash
sudo apt update
sudo apt install ffmpeg
```

对于基于 RPM 的系统，在终端中执行以下命令：
```bash
sudo dnf install ffmpeg
```

如果使用 yum 作为包管理器，则执行：
```bash
sudo yum install ffmpeg
```

对于 Arch Linux，在终端执行以下命令：
```bash
sudo pacman -S ffmpeg
```

### 方式二：编译安装
编译安装较为繁琐，具体方法请自行查找。

## macOS
### 方式一：使用 Homebrew 安装
如果没有安装 Homebrew，执行下面的命令安装：
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

随后在终端中执行以下命令：
```bash
brew install ffmpeg
```

### 方式二：使用静态编译文件（不适用于 ARM64）
打开[FFmpeg 官网](https://ffmpeg.org/)，进入 macOS 下载页。

[![pEl2BCj.png](https://s21.ax1x.com/2025/02/23/pEl2BCj.png)](https://imgse.com/i/pEl2BCj)

下载压缩包。

[![pEl25G9.png](https://s21.ax1x.com/2025/02/23/pEl25G9.png)](https://imgse.com/i/pEl25G9)

解压后得到可执行文件，创建环境变量即可。

### 方式三：编译安装
编译安装较为繁琐，具体方法请自行查找。

## 创建环境变量
### Windows
对于 Windows 用户，下载完成 FFmpeg 后，还需将其添加至环境变量。

右键`此电脑`，点击`属性`，在设置中点击`高级系统设置`。

[![pElcRyV.png](https://s21.ax1x.com/2025/02/23/pElcRyV.png)](https://imgse.com/i/pElcRyV)

点击`环境变量`。

[![pElcLy6.png](https://s21.ax1x.com/2025/02/23/pElcLy6.png)](https://imgse.com/i/pElcLy6)

在`系统变量`一栏中找到`Path`并选中，点击`编辑`。

[![pElgMpn.png](https://s21.ax1x.com/2025/02/23/pElgMpn.png)](https://imgse.com/i/pElgMpn)

点击`新建`，填入`ffmpeg.exe`所在的文件夹（例如：`D:/Software/ffmpeg/bin`）即可。

[![pElgUh9.png](https://s21.ax1x.com/2025/02/23/pElgUh9.png)](https://imgse.com/i/pElgUh9)

[![pElgBX6.png](https://s21.ax1x.com/2025/02/23/pElgBX6.png)](https://imgse.com/i/pElgBX6)

最后，在终端中运行`ffmpeg`测试环境变量是否创建成功。

[![pEl2pHU.png](https://s21.ax1x.com/2025/02/23/pEl2pHU.png)](https://imgse.com/i/pEl2pHU)
