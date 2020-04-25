## aydl

使用`aria2`加速`youtuble-dl`下载

> 在gfw的封锁下,中国访问youtube需要使用魔法
> 
> 然而在晚高峰的时候容易堵车
> 
> 这时候用youtube-dl下载视频很可能速度感人
> 
> 于是我写了这个脚本,使用用aria2技术,多线程下载,加快了速度

## 食用方法

首先你得安装`youtube-dl`,`aria2c`,还有`ffmpeg`(用于合并视频)

若有代理,请先开启:

linux:

```
export http_proxy="http://127.0.0.1:xxxx"
export https_proxy="http://127.0.0.1:xxxx"
export all_proxy="http://127.0.0.1:xxxx"
```

windows:

```
set http_proxy="http://127.0.0.1:xxxx"
```

准备好后,运行`aydl.py`

```plain
url: (输入网址)

a/auto: 自动下载最高分辨率(默认)
c/custom: 自定义视频质量和音频质量
i/itag: 下载指定itag
```

当然也支持直接下载[B站](https://www.bilibili.com)视频