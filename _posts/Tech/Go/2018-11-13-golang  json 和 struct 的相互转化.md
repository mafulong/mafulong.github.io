---
layout: post
category: Go
title:  json 和 struct 的相互转化
---

## Json和struct相互转换

### （1）Json转struct例子

注意json里面的key和struct里面的key要一致，struct中的key的首字母必须大写，而json中大小写都可以。

```go
package main
 
import (
        "fmt"
        "encoding/json"
)
 
type People struct {
        Name string `json:"name_title"`
        Age int `json:"age_size"`
}
 
func JsonToStructDemo(){
        jsonStr := `
        {
                "name_title": "jqw"
                "age_size":12
        }
        `
        var people People
        json.Unmarshal([]byte(jsonStr), &people)
        fmt.Println(people)
}
 
func main(){
        JsonToStructDemo()
}
```


### (2）struct转json

在结构体中引入tag标签，这样匹配的时候json串对应的字段名需要与tag标签中定义的字段名匹配，当然tag中定义的名称不需要首字母大写，且对应的json串中字段名仍然大小写不敏感。此时，结构体中对应的字段名可以不用和匹配的一致，但是首字母必须大写，只有大写才是可对外提供访问的。

```go
package main
 
import (
        "fmt"
        "encoding/json"
)
 
type People struct {
        Name string `json:"name_title"`
        Age int `json:"age_size"`
}
 
func StructToJsonDemo(){
        p := People{
                Name: "jqw",
                Age: 18,
        }
 
        jsonBytes, err := json.Marshal(p)
        if err != nil {
                fmt.Println(err)
        }
        fmt.Println(string(jsonBytes))
}
 
func main(){
        StructToJsonDemo()
}
```

## json和map相互转换

### （1）json转map例子

```go
func JsonToMapDemo(){
        jsonStr := `
        {
                "name": "jqw",
                "age": 18
        }
        `
        var mapResult map[string]interface{}
        err := json.Unmarshal([]byte(jsonStr), &mapResult)
        if err != nil {
                fmt.Println("JsonToMapDemo err: ", err)
        }
        fmt.Println(mapResult)
}
```

### （2）map转Json例子

```go
func MapToJsonDemo1(){
        mapInstances := []map[string]interface{}{}
        instance_1 := map[string]interface{}{"name": "John", "age": 10}
        instance_2 := map[string]interface{}{"name": "Alex", "age": 12}
        mapInstances = append(mapInstances, instance_1, instance_2)

        jsonStr, err := json.Marshal(mapInstances)

        if err != nil {
                fmt.Println("MapToJsonDemo err: ", err)
        }
        fmt.Println(string(jsonStr))
}
```

## 三、map和struct互转

[参考](https://blog.csdn.net/xiaoquantouer/article/details/80233177)