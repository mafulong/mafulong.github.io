---
layout: post
category: Tools
title: Goland的external tool
tags: Tools
---

## Goland的external tool

goland external open in xx 配置

```scala


​```scala
shell 用zsh

下面open 参数： 
-c
"REPO_ROOT=$(git -C \"$ProjectFileDir$\" rev-parse --show-toplevel); PROJECT=$(basename \"$REPO_ROOT\"); BRANCH=$(git -C \"$REPO_ROOT\" rev-parse --abbrev-ref HEAD); FILE=\"$FilePathRelativeToProjectRoot$\"; LINE=$LineNumber$; URL=\"xxxxxx/$PROJECT/-/blob/$BRANCH/$FILE?ref_type=heads#L$LINE\"; open \"$URL\""

下面copy 参数

-c
"REPO_ROOT=$(git -C \"$ProjectFileDir$\" rev-parse --show-toplevel); PROJECT=$(basename \"$REPO_ROOT\"); BRANCH=$(git -C \"$REPO_ROOT\" rev-parse --abbrev-ref HEAD); FILE=\"$FilePathRelativeToProjectRoot$\"; LINE=$LineNumber$; URL=\"xxxx/$PROJECT/-/blob/$BRANCH/$FILE?ref_type=heads#L$LINE\"; echo \"$URL\" | pbcopy"

​```
```

