# 进阶使用
## 使用代理
在设置中切换到`代理`选项卡进行相关设置。

<img src="https://s21.ax1x.com/2025/02/23/pElRGi4.png" alt="pElRGi4.png" style="width: 400px;">

如果代理需要进行身份验证，开启`启用代理身份验证`即可。

:::tip
选择`不使用代理`时，所有请求均不使用代理。  
选择`跟随系统`时，自动使用 IE 代理设置。  
选择`手动设置`时，将使用下方的代理设置。  
:::

:::warning
使用代理时，请关闭`替换音视频流 CDN`选项。
:::

## 并行下载
在下载窗口或设置窗口中将并行下载数调高，同时开启单个视频限速功能，设置具体的限速值，可避免下载速度分配不均的问题，提升批量下载的体验。

<img src="https://s21.ax1x.com/2025/02/23/pElRdL6.png" alt="pElRdL6.png" style="width: 400px;">

## 替换音视频流 CDN host
因 B 站默认分配的 CDN 线路不稳定，容易导致下载失败，因此建议开启`替换音视频流 CDN host`功能。

[![pE1MEKf.png](https://s21.ax1x.com/2025/02/24/pE1MEKf.png)](https://imgse.com/i/pE1MEKf)

程序提供 13 个大厂 CDN host（华为云、腾讯云、阿里云等）供选择，如有其他需要，也可自定义添加。

点击`Ping 测试`即可测试全部 CDN host 的连通性。

<img src="https://s21.ax1x.com/2025/02/24/pE1Jeld.png" alt="pE1Jeld.png" style="width: 550px;">

:::tip
设置为`自动切换`时，将根据预定顺序依次优先选择可用的 CDN host。   
设置为`手动选择`时，选择用户指定的 CDN host。
:::

:::warning
如果开启了此功能仍然出现下载失败的问题，请尝试关闭此功能或更换其他 CDN host。
:::