# OSP (Open Source Processing) Project

![GitHub license](https://img.shields.io/github/license/LittleYe233/PersonalCreation?style=flat-square) ![Platform](https://img.shields.io/badge/platform-Windows%20|%20Linux%20|%20OS%20X-lightgrey?style=flat-square) ![GitHub search hit counter](https://img.shields.io/github/search/LittleYe233/PersonalCreation/main?style=flat-square&label=main%20hit%20counter&color=blueviolet) ![GitHub repo size](https://img.shields.io/github/repo-size/LittleYe233/PersonalCreation?style=flat-square&color=pink) ![GitHub all releases](https://img.shields.io/github/downloads/LittleYe233/PersonalCreation/total?style=flat-square) ![GitHub Sponsors](https://img.shields.io/github/sponsors/LittleYe233?style=flat-square) ![GitHub milestones](https://img.shields.io/github/milestones/all/LittleYe233/PersonalCreation?style=flat-square&color=red) ![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/w/LittleYe233/PersonalCreation/main?color=darkgreen&label=main%20commit%20activity&style=flat-square) ![GitHub last commit](https://img.shields.io/github/last-commit/LittleYe233/PersonalCreation?style=flat-square) ![GitHub Release Date](https://img.shields.io/github/release-date/LittleYe233/PersonalCreation?style=flat-square)

Language: [简体中文](/README.zh-chs.md) English

## Introduction

This project aims to share how I create some video and audio works, share almost all the source code and project files using an open source license. We hope that others can learn about or get hints from it.

## Structures

### Branches

This repository has multiple branches. Major features of them are as below:

- `main` branch is used for intergrating with all creation folder trees.
- Branches beginning with `dev` are used for test and development or creating all works, which avoids destroying `main` branch.
  - `dev` branch has an influence on the **initial** status of all creation branches, including `.gitignore`, templates, etc. Other creation branches probably have to pull it if there are key changes (latest `dev` branch will be pulled on that occasion).
  - `dev_<ASCII identifier>` branches store related source code, project files, etc. of all creations, where `<ASCII identifier>` means an "identifier" of one creation.

### Folder Trees

There are `templates` folders in `main` and `dev` branches, storing templates of some files (e.g, `README.md` in creation folders).

The major structure of creation folders is as below:

- `templates` folder: store templates of some files
- `<ASCII identifier>` folder: store data related to creations
  - `README.md`: related introductions, procedures and ways of creating works, etc.
  - `build.sh`, `clean.sh`, `download.sh`, etc.: automatic scripts
  - `src` folder: store data which can't directly access from the Internet and project files of some applications (e.g., Adobe Premiere), etc.

## Usage

Follow the instructions of `README.md` in creation folders.

## Localization

`README.md` in the root folder of the repository use two language (English and Simplified Chinese). `README.md` in creation folders use Simplified Chinese. Generally, others use original language or English.

## Sponsorship

This project isn't worth any sponsorship at present.

## Index

Below are identifiers and titles (the first-level titles of `README.md` in creation folders) of all creations in alphabetical order, where hyperlinks in "Identifiers" column point to corresponding branches and those in "Titles" column point to corresponding creation folders.

| Identifiers | Titles |
| :-: | :-: |
| [chiisana_tenoira_mad](https://github.com/LittleYe233/PersonalCreation/tree/dev_chiisana_tenohira_mad) | [小さなてのひら MAD 中文字幕内嵌](https://github.com/LittleYe233/PersonalCreation/tree/dev_chiisana_tenohira_mad/chiisana_tenohira_mad) |
| [chiisana_tenoira_mad_2](https://github.com/LittleYe233/PersonalCreation/tree/dev_chiisana_tenohira_mad_2) | [小さなてのひら MAD 中、日、罗马音字幕内嵌](https://github.com/LittleYe233/PersonalCreation/tree/dev_chiisana_tenohira_mad_2/chiisana_tenohira_mad_2) |
| [audio_visualization](https://github.com/LittleYe233/PersonalCreation/tree/dev_audio_visualization) | [音频简易可视化](https://github.com/LittleYe233/PersonalCreation/tree/dev_audio_visualization/audio_visualization) |