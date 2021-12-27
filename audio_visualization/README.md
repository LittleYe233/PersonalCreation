<!-- Project README Template v1.0.0 for Original Video -->

# 音频简易可视化

## 基本信息

- **项目名称：** 音频简易可视化
- **项目来源：** 原创
- **项目作者：** [LittleYe233](https://github.com/LittleYe233)

## 项目需求

对给定音频可视化，并附有其他设计。

## 主要更改

- 对给定音频可视化为时域图；
- 添加背景图；
- 酌情添加额外特效。

## 待定更新

- [ ] 对给定音频可视化为频域图；
- [ ] 添加进度条等；
- [ ] 更灵活的文字显示功能；
- [ ] 更多样的特效。

## 下载地址

[GitHub Releases](https://github.com/LittleYe233/PersonalCreation/releases/tag/audio_visualization-creation-v1.0.0)

## 解决方案

以 *nix 为例：

```bash
git clone -b dev_audio_visualization --depth 1 https://github.com/LittleYe233/PersonalCreation.git
cd PersonalCreation/audio_visualization
chmod +x build.sh clean.sh
./build.sh
# 可选，清除无用文件
# chmod +x clean.sh
# ./clean.sh
```

生成的作品位于 `dist` 文件夹中。

## 实现过程

本项目不依赖于其他视频，因此有关视频的相关参数均需要自行控制。依照本项目提供的解决方案，主要控制如下参数：

- 画布尺寸： 1920*1080 （1080P）
- 帧率： 60FPS
- 视频流编码： H264
- 视频流比特率： 10 kb/s
- 音频流编码： AAC

考虑到本作品所需数学知识较深，特决定在本项目中另写一文章较详细地描述构建本作品所需代码的过程和注意事项，便于事后反思。该文仍在创作中。

以 *nix 为例，以下是对各步骤的分项说明：

### 前期准备

- [FFmpeg](https://ffmpeg.org/)
- [Python 3](https://python.org) **（需要 PIL、matplotlib、NumPy、pylrc、srt 模块支持）**

### 处理素材

本项目将以 [夏恋花火 (By 40mP,シャノ)](https://music.163.com/#/song?id=28968092) 为例实现需求，但只需对代码中的相关参数稍作修改即可对任何音频生效。本项目使用的音频文件附于作品目录下的 `audio` 文件夹中。

以下是有关该音频的详细信息：

- 时长： 00:04:40.67
- 格式： FLAC
- 比特深度： 16bit
- 音轨： 立体声（stereo）
- 采样率： 44.1 kHz

为后期处理方便起见，需要将该音频转化为 WAV 格式文件：

```bash
ffmpeg -i in.flac in.wav
```

检查 `in.wav` 的相关参数如下：

```text
pcm_s16le ([1][0][0][0] / 0x0001), 44100 Hz, 2 channels, s16, 1411 kb/s
```

本项目使用的歌词文件来自网易云音乐上[该歌曲某一版本](https://music.163.com/#/song?id=22821023)的歌词，在原文基础上增删部分标点和空白字符，并对时间轴略作调整。

### 生成作品

目前暂时只考虑时域图（柱形图）的作品。

生成本作品的绝大多数工作已在 `src` 目录下的相关 Python 脚本中实现。一些参数的控制放置在 `src/wave.py` 中。也可以将其放置在 `src/build.sh` 中将其作为命令行参数传递给 Python 脚本。

```bash
python3 -m wave
```

最终实现的效果主要如下：

- 背景图淡入，柱形图基线从中向左右两侧延长；
- 对应时域的柱形和音频同时开始（由于音频本身在开头有无声部分，柱形的出现和声音响起并非同时）；
- 柱形上下各有中文和日文歌词字幕，并根据前后每句歌词的时间戳和时长自动调整淡入淡出的位置（淡入淡出持续时长均为 0.5 秒）；
- 音频结束后柱形继续移动，保证所有柱形全部自左侧消失后结束视频。

`ffprobe` 得到最终作品的相关参数如下：

- 时长： 00:04:52.00
- 音频流
  - 编码： AAC
  - 采样率： 44100 Hz
  - 声道：双声道
  - 比特率： 125 kb/s
- 视频流
  - 编码： H264
  - 色彩空间： yuvj420p
  - 画布大小： 1920x1080
  - 比特率： 9754 kb/s
  - 帧率： 60
  - TBR： 60
  - TBN： 15360
  - TBC： 120

## 推广链接

| 站点 | 链接 |
| :-: | :-: |
| Bilibili | https://www.bilibili.com/video/BV1bi4y1R7hR/ |
<!-- | 百度贴吧 |  |
| 博客园 |  |
| CSDN |  |
| 个人博客 |  |
| 简书 |  | -->