<!-- Project README Template v1.0.0 for Video -->

# 小さなてのひら MAD 中文字幕内嵌 2

## 基本信息

- **项目名称：** (CLANNAD)小さなてのひら(720p)
- **项目来源：** 转载
  - Bilibili：[(CLANNAD)小さなてのひら(720p)](https://www.bilibili.com/video/av53288473/)
- **项目作者：** [LittleYe233](https://github.com/LittleYe233)
- **原视频：**
  - 时长： 00:04:49.21
  - 比特率： 1102 kb/s
  - 视频流： h264 (High), yuv420p(progressive), 1280x720 [SAR 1:1 DAR 16:9], 968 kb/s, 25 fps, 25 tbr, 1k tbn, 50 tbc
  - 音频流： aac (LC), 44100 Hz, stereo, fltp, 126 kb/s

## 项目需求

在原视频内嵌 ASS 中文、日文、罗马音字幕。

## 主要更改

- 在原视频底部添加内嵌 ASS 中文、日文和罗马音字幕
- 删去原视频末尾黑幕片段

## 下载地址

[GitHub Releases](https://github.com/LittleYe233/PersonalCreation/releases/tag/dev_chiisana_tenohira_mad_2-creation-v1.0.0)

## 解决方案

以 *nix 为例：

```bash
git clone -b dev_chiisana_tenohira_mad_2 --depth 1 https://github.com/LittleYe233/PersonalCreation.git
cd PersonalCreation/chiisana_tenohira_mad_2
chmod +x build.sh download.sh clean.sh
./download.sh && ./build.sh
# 可选，清除无用文件
# chmod +x clean.sh
# ./clean.sh
```

生成的作品位于 `dist` 文件夹中。

## 实现过程

“获取素材”后的步骤可以合并为：

```bash
ffmpeg -i 'in.flv' -ss 0:0:0 -to 0:4:41 -vcodec h264 -b:v 968K -time_base 1/1000 -enc_time_base 1/50 -r 25 -acodec copy -filter_complex "subtitles='in.ass'" 'out.flv'
```

以 *nix 为例，以下是对各步骤的分项说明：

### 前期准备

- [Aegisub](https://aegi.vmoe.info/) 等字幕制作软件
- [FFmpeg](https://ffmpeg.org/) （需要 libass 支持）
- [Python 3](https://python.org)
- [you-get](https://you-get.org/)

### 制作字幕

使用 Aegisub 等软件制作 ASS 字幕，保存为 `in.ass` 。为控制字幕的行距和字体，本项目在同一时间段内同时插入三条字幕，并放置在不同层。为使字幕美观，本项目使用特殊代码 `{\fad(500,500)}` 为每条字幕加入 500 毫秒的淡入淡出效果。

### 获取素材

使用 `you-get` 获取相关素材。

查看可获取的资源格式列表：

```bash
you-get -i https://www.bilibili.com/video/av53288473/
```

选择合适的格式下载：

```bash
# format:        flv720
# container:     flv
# quality:       高清 720P
# size:          38.0 MiB (39840995 bytes)
you-get --format=flv720 https://www.bilibili.com/video/av53288473/ -O in
```

**注意：** `you-get` 的 `-O` 参数后不带扩展名，且下载后包含 `*.cmt.xml` 弹幕文件，该文件名不会受 `-O` 影响。

### 截取视频

<!-- https://blog.csdn.net/ternence_hsu/article/details/109705234 -->

本项目作品中只保留原视频 4 分 41 秒前的内容。为避免 FFmpeg 截取视频时造成丢帧等问题，本项目将对视频重新编码为 MP4 文件格式，并尽可能保持原视频的时间基相关参数。原视频的相关参数如下：

- 编码： H264
- 比特率： 968 Kb/s
- 帧率： 25
- TBR： 25
- TBN： 1K
- TBC： 50

而音频流无需特意改动。最终得到的代码如下：

```bash
ffmpeg -i 'in.flv' -ss 0:0:0 -to 0:4:41 -vcodec h264 -b:v 968K -time_base 1/1000 -enc_time_base 1/50 -r 25 -acodec copy 'out1.flv'
```

此时 `ffprobe out1.flv` 可以得到类似如下的输出：

```text
h264 (High), yuv420p(progressive), 1280x720 [SAR 1:1 DAR 16:9], 968 kb/s, 25 fps, 25 tbr, 1k tbn, 100 tbc
```

对应的相关参数如下：

- 编码： H264
- 比特率： 968 Kb/s
- 帧率： 25
- TBR： 25
- TBN： 1K
- TBC： 100

### 烧录字幕

将 ASS 字幕烧录（硬编码、内嵌）到视频中，得到最终作品（同样为保证相关参数一致，使用了“截取视频”小节代码中的参数）：

```bash
ffmpeg -i 'out1.flv' -vcodec h264 -b:v 968K -time_base 1/1000 -enc_time_base 1/50 -r 25 -acodec copy -filter_complex "subtitles='in.ass'" 'out.flv'
```

## 推广链接

| 站点 | 链接 |
| :-: | :-: |
| 百度贴吧 |  |
| Bilibili | https://www.bilibili.com/video/BV1MY411s7zT/ |
| 博客园 |  |
| CSDN |  |
| 简书 |  |