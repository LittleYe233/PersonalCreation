# OSP (Open Source Processing) Project

![GitHub license](https://img.shields.io/github/license/LittleYe233/PersonalCreation?style=flat-square) ![Platform](https://img.shields.io/badge/platform-Windows%20|%20Linux%20|%20OS%20X-lightgrey?style=flat-square) ![GitHub search hit counter](https://img.shields.io/github/search/LittleYe233/PersonalCreation/main?style=flat-square&label=main%20hit%20counter&color=blueviolet) ![GitHub repo size](https://img.shields.io/github/repo-size/LittleYe233/PersonalCreation?style=flat-square&color=pink) ![GitHub all releases](https://img.shields.io/github/downloads/LittleYe233/PersonalCreation/total?style=flat-square) ![GitHub Sponsors](https://img.shields.io/github/sponsors/LittleYe233?style=flat-square) ![GitHub milestones](https://img.shields.io/github/milestones/all/LittleYe233/PersonalCreation?style=flat-square&color=red) ![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/w/LittleYe233/PersonalCreation/main?color=darkgreen&label=main%20commit%20activity&style=flat-square) ![GitHub last commit](https://img.shields.io/github/last-commit/LittleYe233/PersonalCreation?style=flat-square) ![GitHub Release Date](https://img.shields.io/github/release-date/LittleYe233/PersonalCreation?style=flat-square)

语言：[English](https://github.com/LittleYe233/PersonalCreation) 简体中文

## 简介

本工程旨在分享制作一些视频、音频作品的过程，并将绝大多数代码和工程文件开源。希望其他人能从中得到启发。

## 结构

### 分支

本仓库具有多分支。主要功能有：

- `main` 分支用以汇总其他分支的目录树结构
- 以 `dev` 开头的分支用以测试和开发，避免对 `main` 分支的内容造成破坏，或是进行各个作品的制作
  - `dev` 分支影响各个作品分支的**初始**状态，涉及 `.gitignore` 、模板等部分内容，如果是较为关键的更改（例如对 `.gitignore` 的修改），其他作品分支可能需要拉取之（此时将会拉取最新的 `dev` 分支）
  - `dev_<ASCII identifier>` 分支保存各个作品的相关代码和工程等， `<ASCII identifier>` 记为该作品的“标识符”

### 目录树

`main` 和 `dev` 分支有 `templates` 文件夹，存储部分文件（例如作品目录下 `README.md`）的模板。

作品分支的目录树的主要结构如下：

- `templates` 文件夹：存储部分文件的模板
- `<ASCII identifier>` 文件夹：存放作品的相关数据
  - `README.md`：有关该作品的简介、制作过程、作品生成方法等
  - `build.sh` 、 `clean.sh` 、 `download.sh` 等：自动化脚本
  - `src` 文件夹：存放无法在网络上直接获取的数据，以及一些应用程序（例如 Adobe Premiere）的工程文件等

## 使用

遵循各作品目录下的 `README.md` 。

## 本地化

仓库根目录的 `README.md` 使用两种语言的文字书写（英文和简体中文）；各作品目录下的 `README.md` 使用简体中文；其他情况一般均保持原状或使用英文。

## 赞助

本工程尚未达到值得任何人赞助的程度。

## 索引

以下是目前所有的作品的标识符和标题名（作品目录下 `README.md` 的一级标题），按照标识符字典序排列。其中“标识符”一栏下方的超链接可以跳转至对应分支，“标题名”一栏下方的超链接可以跳转至对应作品目录。

| 标识符 | 标题名 |
| :-: | :-: |
| [chiisana_tenoira_mad](https://github.com/LittleYe233/PersonalCreation/tree/dev_chiisana_tenohira_mad) | [小さなてのひら MAD 中文字幕内嵌](https://github.com/LittleYe233/PersonalCreation/tree/dev_chiisana_tenohira_mad/chiisana_tenohira_mad) |
| [chiisana_tenoira_mad_2](https://github.com/LittleYe233/PersonalCreation/tree/dev_chiisana_tenohira_mad_2) | [小さなてのひら MAD 中、日、罗马音字幕内嵌](https://github.com/LittleYe233/PersonalCreation/tree/dev_chiisana_tenohira_mad_2/chiisana_tenohira_mad_2) |