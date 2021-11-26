<!-- Project README Template v1.0.0 -->

# 小さなてのひら MAD 中文字幕内嵌

## 基本信息

- **项目名称：** 【感動のMAD】CLANNAD 挿入曲『小さなてのひら』歌詞入り
- **项目来源：** 转载
  - YouTube：[【感動のMAD】CLANNAD 挿入曲『小さなてのひら』歌詞入り](https://www.youtube.com/watch?v=R6xAQxgA1sQ)
- **项目作者：** [LittleYe233](https://github.com/LittleYe233)
- **原视频：**
  - 时长： 00:04:53.59
  - 比特率： 1250 kb/s
  - 视频流： h264 (High) (avc1 / 0x31637661), yuv420p(tv, bt709), 1280x720 [SAR 1:1 DAR 16:9], 1115 kb/s, 30 fps, 30 tbr, 15360 tbn, 60 tbc (default)
  - 音频流： aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 127 kb/s (default)

## 项目需求

在原视频顶部添加内嵌 ASS 中文字幕。字幕源为萌娘百科“小さなてのひら”词条。

## 解决方案

以 *nix 为例：

```bash
git clone -b dev_chiisana_tenohira_mad --depth 1 https://github.com/LittleYe233/PersonalCreation.git
cd PersonalCreation/chiisana_tenohira_mad
chmod +x build.sh download.sh clean.sh
./download.sh && ./build.sh
# 可选，清除无用文件
# chmod +x clean.sh
# ./clean.sh
```

生成的作品位于 `dist` 文件夹中。

## 主要更改

- 添加内嵌 ASS 中文字幕；
- 删去尾部部分片段。

## 实现过程

以 *nix 为例，“获取素材”后的步骤可以合并为：

```bash
ffmpeg -i 'in.mp4' -i 'in.m4a' -ss 0:0:0 -to 0:4:37 -vcodec libx264 -acodec copy -filter_complex "subtitles='in.ass'" out.mp4
```

以下是对各步骤的分项说明：

### 前期准备

```bash
cd /path/to/workspace
apt install ffmpeg
# ffmpeg -version
python3 -m pip install youtube-dl
# 或 python3 -m pip install you-get
# youtube-dl --version
```

### 获取素材

使用 `you-get` 或 `youtube-dl` 获取相关素材。下以 `youtube-dl` 为例：

查看可获取的资源格式列表：

```bash
youtube-dl -F https://www.youtube.com/watch?v=R6xAQxgA1sQ
```

选择合适的格式下载：

```bash
# 获取视频：mp4 1280x720 720p 1118k , mp4_dash container, avc1.64001f@1118k, 30fps, video only, 39.13MiB
youtube-dl --format 136 https://www.youtube.com/watch?v=R6xAQxgA1sQ -o in.mp4
# 获取音频：m4a audio only tiny 129k , m4a_dash container, mp4a.40.2@129k (44100Hz), 4.53MiB
youtube-dl --format 140 https://www.youtube.com/watch?v=R6xAQxgA1sQ -o in.m4a
```

### 合并音轨

下载得到的视频是无音轨的。将下载得到的音频文件合并入视频中：

```bash
ffmpeg -i 'in.mp4' -i 'in.m4a' -vcodec copy -acodec copy 'out1.mp4'
```

### 截取视频

为保证歌曲和视频的完整性和纯净性，本项目作品中只保留原视频 4 分 37 秒前的内容。为避免 FFmpeg 截取视频时造成丢帧等问题，本项目将对视频重新编码为 H264：

```bash
ffmpeg -i 'out1.mp4' -ss 0:0:0 -to 0:4:37 -vcodec libx264 -acodec copy 'out2.mp4'
```

### 烧录字幕

将 ASS 字幕烧录（硬编码、内嵌）到视频中，得到最终作品：

```bash
ffmpeg -i 'out2.mp4' -filter_complex "subtitles='in.ass'" 'out.mp4'
```

## 推广链接

| 站点 | 链接 |
| :-: | :-: |
| 百度贴吧 |  |
| Bilibili |  |
| 博客园 |  |
| CSDN |  |
| 简书 |  |