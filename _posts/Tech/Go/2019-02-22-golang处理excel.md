---
layout: post
category: Go
title: golang处理excel
tags: Go
---


## 下载包
```
go get github.com/tealeg/xlsx
```

## 读取excel

```
	countrys := []string{"en", "ja", "pt"}
	tags := []Tag{}
	dir, _ := os.Getwd()
	dir = path.Join(path.Dir(dir), "life", "user_bot", "instagram")
	for _, country := range countrys {
		xlsxFile, err := xlsx.OpenFile(fmt.Sprintf("%s/%s.xlsx", dir, country))
		if err != nil {
			logs.Error("err %+v", err)
		}
		sheet1 := xlsxFile.Sheets[0]
		for _, cell := range sheet1.Rows {
			newtag := strings.Replace(cell.Cells[0].String(), " ", "", 12)
			if len(newtag) == 0 {
				continue
			}
			tags = append(tags, Tag{
				tag:     newtag,
				country: country,
			})
		}
	}
	fmt.Println(tags)
```

## 写入excel

```

func main() {

	//配置
	items := []ins_model.InstagramItem2{}
	videos := []ins_model.InstagramVideo2{}
	db, err := common.TestDb.GetReadConnection()
	if err != nil {
		logs.Error("db错误,%+v", err)
	}
	dir, _ := os.Getwd()
	dir = path.Join(path.Dir(dir), "life", "user_bot", "instagram")
	xlsxFile := xlsx.NewFile()
	sheet1, _ := xlsxFile.AddSheet("item")
	sheet2, _ := xlsxFile.AddSheet("video")
	itemTitle := []string{"id", "标签", "标签", "ins标签", "语言", "item链接", "user链接", "关注数", "发文数", "点赞", "评论数", "发文时间","创建时间", "修改时间", "多图数量"}
	videoTitle := []string{"id", "标签", "标签", "语言", "item链接", "user链接", "关注数", "发文数", "点赞", "观看数", "评论数", "发文时间","创建时间", "修改时间", "视频长度(秒)"}
	sheet1.AddRow().WriteSlice(&itemTitle, len(itemTitle))
	sheet2.AddRow().WriteSlice(&videoTitle, len(videoTitle))

	//读db
	if err := db.Debug().Find(&items).Error; err != nil {
		logs.Error("err %+v", err)
		db.Debug().Find(&items)
	}
	fmt.Println("item数量", len(items))
	for _, item := range items {
		sheet1.AddRow().WriteStruct(&item, reflect.ValueOf(item).NumField())
	}
	if err := db.Debug().Find(&videos).Error; err != nil {
		logs.Error("err %+v", err)
		db.Debug().Find(&videos)
	}
	fmt.Println("视频数量", len(videos))
	for _, video := range videos {
		sheet2.AddRow().WriteStruct(&video, reflect.ValueOf(video).NumField())
	}

	//保存excel
	err = xlsxFile.Save(fmt.Sprintf("%s/%s.xlsx", dir, "抓取数据"))
	if err != nil {
		logs.Error("存储失败")
	}
}

```
