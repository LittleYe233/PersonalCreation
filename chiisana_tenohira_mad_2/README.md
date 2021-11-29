<!-- Project README Template v1.0.0 for Video -->

# 小さなてのひら MAD 中、日、罗马音字幕内嵌

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

在原视频内嵌 ASS 中文、日文、罗马音字幕，并使用插帧和超分辨率增强。

## 主要更改

- 在原视频底部添加内嵌 ASS 中文、日文和罗马音字幕
- 删去原视频末尾黑幕片段
- 插帧到 50FPS ，并超分辨率到 1080P

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

生成的作品位于 `dist` 文件夹中，**注意此为未进行插帧和超分辨率的作品**。**需要在 FFmpeg 硬编码字幕前对截取后的视频进行插帧和超分辨率**，否则内嵌字幕可能会对插帧和超分辨率等的质量造成影响。

## 实现过程

“获取素材”后的步骤（除“视频增强”小节）可以合并为：

```bash
ffmpeg -i 'in.flv' -ss 0:0:0 -to 0:4:41 -vcodec h264 -b:v 968K -time_base 1/1000 -enc_time_base 1/50 -r 25 -acodec copy -filter_complex "subtitles='in.ass'" 'out.flv'
```

以 *nix 为例，以下是对各步骤的分项说明：

### 前期准备

- [Aegisub](https://aegi.vmoe.info/) 等字幕制作软件
- [FFmpeg](https://ffmpeg.org/) **（需要 libass 支持）**
- [Python 3](https://python.org)
- [you-get](https://you-get.org/)
- [Waifu2x-Extension-GUI](https://github.com/AaronFeng753/Waifu2x-Extension-GUI) **（高级版付费）**

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

### 视频增强

首次使用 `Waifu2x-Extension-GUI` 需要对计算机进行兼容性测试，以确定可用和最佳的模型和插件。

导入上一步生成的视频后，依照下述配置进行插帧和超分辨率。**注意 `Waifu2x-Extension-GUI` 默认先插帧，再超分辨率**；也可以先对原视频插帧，再对插帧后的视频超分辨率。本项目使用后者，但为保证下述配置简洁，以下给出的是前者的参考配置。

```yaml
主页:
  视频插帧(补帧): true
  仅插帧(视频): false
  将图片保存为: png
  图片质量: 100
  图像样式(waifu2x-ncnn-vulkan): 2D动漫
  放大倍率:
    图片: 1.5000
    动态图片: 1.5000
    视频: 1.5000
  降噪等级:
    图片: 2
    动态图片: 2
    视频: 2
  帧率倍率: 2
引擎设置:
  引擎(超分辨率):
    图片: waifu2x-ncnn-vulkan
    动态图片: waifu2x-ncnn-vulkan
    视频: waifu2x-ncnn-vulkan
    waifu2x-ncnn-vulkan:
      模型: upconv_7
      块大小: 380
      版本: 最新版(Alpha通道,TTA,多显卡)
      GPU ID: 0 AMD Radeon(TM) 530
  线程数量(超分辨率):
    图片: 2
    动态图片: 2
    视频: 2
视频设置:
  帧编码: JPEG(无损)
  分段处理视频:
    视频片段时长(秒): 20
  插帧:
    插帧引擎: rife-ncnn-vulkan
    模型: rife-v3.1
    多线程: 自动调整
    GPU ID: 0 AMD Radeon(TM) 530
  动态内存缓冲:
    磁盘大小(MB): 6000
附加设置:
  超线程(HT/SMT): true
  可用显存(MB): 2000
```

注意 `Waifu2x-Extension-GUI` 会对非 MP4 视频预处理为 MP4 视频后，再进行后续处理。由于本项目作者误操作，预处理后的 MP4 视频不慎丢失，以下分别是插帧后和超分辨率后的 MP4 视频经过 `ffprobe` 的结果：

```text
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'out1_W2xEX_VFI_flv.mp4':
  Metadata:
    major_brand     : isom
    minor_version   : 512
    compatible_brands: isomiso2avc1mp41
    encoder         : Lavf58.76.100
  Duration: 00:04:41.00, start: 0.000000, bitrate: 2255 kb/s
    Stream #0:0(und): Video: h264 (High) (avc1 / 0x31637661), yuv420p, 1280x720, 2117 kb/s, 50 fps, 50 tbr, 12800 tbn, 100 tbc (default)
    Metadata:
      handler_name    : VideoHandler
    Stream #0:1(unk): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 127 kb/s (default)
    Metadata:
      handler_name    : SoundHandler
```

```text
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'out1_W2xEX_VFI_flv_waifu2x_1920x1080_2n_mp4.mp4':
  Metadata:
    major_brand     : isom
    minor_version   : 512
    compatible_brands: isomiso2avc1mp41
    encoder         : Lavf58.76.100
  Duration: 00:04:41.00, start: 0.000000, bitrate: 4668 kb/s
    Stream #0:0(und): Video: h264 (High) (avc1 / 0x31637661), yuv420p, 1920x1080, 4530 kb/s, 50 fps, 50 tbr, 12800 tbn, 100 tbc (default)
    Metadata:
      handler_name    : VideoHandler
    Stream #0:1(unk): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 127 kb/s (default)
    Metadata:
      handler_name    : SoundHandler
```

为方便，将 `out1_W2xEX_VFI_flv_waifu2x_1920x1080_2n_mp4.mp4` 重命名为 `out2.mp4`。

### 烧录字幕

将 ASS 字幕烧录（硬编码、内嵌）到视频中，得到最终作品（同样为保证相关参数一致，使用了“截取视频”小节代码中的参数）：

```bash
ffmpeg -i 'out1.flv' -vcodec h264 -b:v 968K -time_base 1/1000 -enc_time_base 1/50 -r 25 -acodec copy -filter_complex "subtitles='in.ass'" 'out.flv'
```

而对于经过 `Waifu2x-Extension-GUI` 处理后的视频，根据上一节输出的视频信息，执行下述命令可得到最终作品：

```bash
ffmpeg -i 'out2.mp4' -vcodec h264 -b:v 4530K -time_base 1/12800 -enc_time_base 1/50 -r 50 -acodec copy -filter_complex "subtitles='in.ass'" 'out.mp4'
```

`ffprobe out.mp4` 得到的结果如下所示：

```text
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'out.mp4':
  Metadata:
    major_brand     : isom
    minor_version   : 512
    compatible_brands: isomiso2avc1mp41
    encoder         : Lavf58.43.100
  Duration: 00:04:41.00, start: 0.000000, bitrate: 4582 kb/s
    Stream #0:0(und): Video: h264 (High) (avc1 / 0x31637661), yuv420p, 1920x1080, 4444 kb/s, 50 fps, 50 tbr, 12800 tbn, 100 tbc (default)
    Metadata:
      handler_name    : VideoHandler
    Stream #0:1(unk): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 127 kb/s (default)
    Metadata:
      handler_name    : SoundHandler
```

## 推广链接

| 站点 | 链接 |
| :-: | :-: |
| 百度贴吧 |  |
| Bilibili | https://www.bilibili.com/video/BV1MY411s7zT/ |
| 博客园 |  |
| CSDN |  |
| 简书 |  |