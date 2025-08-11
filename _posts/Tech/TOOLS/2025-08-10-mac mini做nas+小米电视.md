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

