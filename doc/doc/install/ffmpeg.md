# 安装 FFmpeg
程序依赖 FFmpeg 实现音视频合成，格式转换，直播录制等功能，缺少时将影响正常使用。

:::tip
编译版已经集成 FFmpeg，无需再次下载。
:::

## Windows 
Windows 用户需手动下载，并创建环境变量。

[官网下载](https://ffmpeg.org/)  
[蓝奏云](https://wwx.lanzout.com/iW4GP2azpdzg) 密码：e82q（来源于：gyan.dev，版本：7.0.1）

## Linux
在终端中执行以下命令：
```bash
sudo apt install ffmpeg
```

## macOS
在终端中执行以下命令：
```bash
brew install ffmpeg
```

## 创建环境变量
Windows 用户下载完成 FFmpeg 后，还需将其添加至环境变量。

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