---
layout: post
category: Tools
title: mac mini做nas+小米电视
tags: Tools
---

## mac mini做nas+小米电视





## nas

```scala 
docker run -d \
  --name=emby \
  --restart=unless-stopped \
  -v /Users/mafulong/Downloads:/mnt/NAS \
  -v emby_config:/config \
  -p 8096:8096 \
  linuxserver/emby


自己ip

ipconfig getifaddr en1
```

## adb

adb可以远程connect

```scala
adb connect 192.168.31.148
adb devices
# 安装软件
adb install TVBox_takagen99_20250706-1456-arm64-generic-java.apk

# 传输文件 但小米电视无法读adb的文件。
adb push "/Users/mafulong/Downloads/爱、死亡与机器人.Love.Death.and.Robots.S01E01.中英字幕.WEBrip.720P-人人影视.V2.mp4" /mnt/sdcard/Movies/
```

