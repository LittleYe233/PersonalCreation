<!-- Project README Template v1.0.0 for Video -->

# 音频简易可视化

## 基本信息

- **项目名称：** 音频简易可视化
- **项目来源：** 原创
- **项目作者：** [LittleYe233](https://github.com/LittleYe233)

## 项目需求

对给定音频可视化，并附有其他设计。

## 主要更改

- 对给定音频可视化为柱状图或波形图；
- 添加音频信息、进度条、背景图等；
- 酌情添加额外特效。

## 下载地址

[GitHub Releases](https://github.com/LittleYe233/PersonalCreation/releases/tag/audio_visualization-creation-v1.0.0)

## 解决方案

以 *nix 为例：

```bash
git clone -b dev_audio_visualization --depth 1 https://github.com/LittleYe233/PersonalCreation.git
cd PersonalCreation/audio_visualization

```

生成的作品位于 `dist` 文件夹中。

## 实现过程

本项目不依赖于其他视频，因此有关视频的相关参数均需要自行控制。依照本项目提供的解决方案，主要仅控制如下参数：

- 画布尺寸： 1920*1080 （1080P）
- 帧率： 60FPS

音频流的相关参数详见后文。

以 *nix 为例，以下是对各步骤的分项说明：

### 前期准备

- [FFmpeg](https://ffmpeg.org/) **（需要 libass 支持）**
- [Python 3](https://python.org) **（需要 PIL、OpenCV、NumPy 支持）**

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

## 推广链接

| 站点 | 链接 |
| :-: | :-: |
| 百度贴吧 |  |
| Bilibili |  |
| 博客园 |  |
| CSDN |  |
| 简书 |  |