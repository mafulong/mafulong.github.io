---
layout: post
category: Go
title: go之channel
tags: Go
---

## go之channel

[Go 语言问题集(Go Questions)](https://www.bookstack.cn/books/qcrao-Go-Questions)





```go
	// 记法 <-chan<- 箭头一直朝左, 读取<-c1<-赋值
	var c chan int
	var c1 <-chan int
	var c2 chan<- int
	c = make(chan int, 1)
	c1 = make(<-chan int, 2)

	// 写入
	c <- 3
	// 读取
	d := <-c1
	<-c1

	select {
	case c <- 3:
		return
	case e := <-c:
		println(e)
		return
	default:
		return
	}
```



## Channel

- CSP，Communicating Sequential Processes， 通信顺序处理。不要通过共享内存来通信，而要通过通信来实现内存共享。相比于内存共享（如mutex)，不需要考虑数据所有权，不需要保护结构的内部状态，不需要协调多个逻辑。

- chan结构:
  - 一个循环数组（实际是循环链表），有发送、接收offset
  - 等待接收和发送的goroutine队列（这些 goroutine 由于尝试读取 channel 或向 channel 发送数据而被阻塞）
  - mutex锁保护所有字段。

- chan本质是值的拷贝，无论是从 sender goroutine 的栈到 chan buf，还是从 chan buf 到 receiver goroutine，或者是直接从 sender goroutine 到 receiver goroutine。

- channel引发goroutine泄露：当且仅当goroutine 操作 channel 后，处于发送或接收阻塞状态，而 channel 处于满或空的状态，一直得不到改变。同时，垃圾回收器也不会回收此类资源，进而导致 gouroutine 会一直处于等待队列中，不见天日。

- channel应用
  - 停止信号
  - 任务定时，time.Ticker()
  
  ```go
  // 超时控制
  select {
      case <-time.After(100 * time.Millisecond):
      case <-s.stopc:
          return false
  }
  
  // 定时
  func worker() {
      ticker := time.Tick(1 * time.Second)
      for {
          select {
          case <- ticker:
              // 执行定时任务
              fmt.Println("执行 1s 定时任务")
          }
      }
  }
  ```
  
  
  
  - 解耦生产方和消费放，当并发任务队列使用。服务启动时，启动 n 个 worker，100个生产者，5个消费者同时消费。
  
  ```go
  func main() {
      taskCh := make(chan int, 100)
      go worker(taskCh)
      // 塞任务
      for i := 0; i < 10; i++ {
          taskCh <- i
      }
  }
  func worker(taskCh <-chan int) {
      const N = 5
      // 启动 5 个工作协程
      for i := 0; i < N; i++ {
          go func(id int) {
              for {
                  task := <- taskCh
                  fmt.Printf("finish task: %d by worker %d\n", task, id)
                  time.Sleep(time.Second)
              }
          }(i)
      }
  }
  ```
  
  
  
  - 控制并发数，比如len=3的chan.
  
  ```go
  var limit = make(chan int, 3)
  func main() {
      // …………
      for _, w := range work {
          go func() {
              limit <- 1
              w()
              <-limit
          }()
      }
      // …………
  }
  ```
  
  
  
- channel关闭后读取可以读到零值

- channel的happened-before
  - channel close 一定 `happened before` receiver 得到通知。
  
- 关闭chan过程
  - 对于等待接收者而言，会收到一个相应类型的零值。对于等待发送者，会直接 panic。
  - close 函数先上一把大锁，接着把所有挂在这个 channel 上的 sender 和 receiver 全都连成一个 sudog 链表，再解锁。最后，再将所有的 sudog 全都唤醒。唤醒之后，该干嘛干嘛。sender 会继续执行 chansend 函数里 goparkunlock 函数之后的代码，很不幸，检测到 channel 已经关闭了，panic。receiver 则比较幸运，进行一些扫尾工作后，返回。
  
- chan发送过程
  - 如果close, panic
  - 如果能从等待接收队列 recvq 里出队一个 sudog（代表一个 goroutine），说明此时 channel 是空的，没有元素，所以才会有等待接收者。这时会调用 send 函数将元素直接从发送者的栈拷贝到接收者的栈
  - 如果 `c.qcount < c.dataqsiz`，说明缓冲区可用（肯定是缓冲型的 channel）。先通过函数取出待发送元素应该去到的位置
  - 如果没有命中以上条件的，说明 channel 已经满了。不管这个 channel 是缓冲型的还是非缓冲型的，都要将这个 sender “关起来”（goroutine 被阻塞）。
  - 先构造一个 sudog，将其入队（channel 的 sendq 字段）。然后调用 `goparkunlock` 将当前 goroutine 挂起，并解锁，等待合适的时机再唤醒。
  
- 如何关闭chan
  - 不要从一个 receiver 侧关闭 channel，也不要在有多个 sender 时，关闭 channel。
  
  - 本质：don’t close (or send values to) closed channels.
  
  - 对于N 个 sender，一个 reciver： 增加一个中间人，增加一个传递关闭信号的 channel，receiver 通过信号 channel 下达关闭数据 channel 指令
  
  - 对于N 个 sender， M 个 receiver： 需要增加一个中间人，M 个 receiver 都向它发送关闭 dataCh 的“请求”，中间人收到第一个请求后，就会直接下达关闭 dataCh 的指令
  
    

总结一下操作 channel 的结果：

| 操作     | nil channel | closed channel     | not nil, not closed channel                                  |
| :------- | :---------- | :----------------- | :----------------------------------------------------------- |
| close    | panic       | panic              | 正常关闭                                                     |
| 读 <- ch | 阻塞        | 读到对应类型的零值 | 阻塞或正常读取数据。缓冲型 channel 为空或非缓冲型 channel 没有等待发送者时会阻塞 |
| 写 ch <- | 阻塞        | panic              | 阻塞或正常写入数据。非缓冲型 channel 没有等待接收者或缓冲型 channel buf 满时会被阻塞 |

总结一下，发生 panic 的情况有三种：向一个关闭的 channel 进行写操作；关闭一个 nil 的 channel；重复关闭一个 channel。

读、写一个 nil channel 都会被阻塞。



## 应用考题

极客上一道有意思的题，假设有4个 `goroutine`，编号为1，2，3，4。每秒钟会有一个 `goroutine` 打印出它自己的编号。现在让你写一个程序，要求输出的编号总是按照1，2，3，4这样的顺序打印。类似下图，

```go
package main

import (
  "fmt"
  "time"
)

type token struct{}

func main() {
  num := 4
  var chs []chan token
  // 4 个work
  for i := 0; i < num; i++ {
    chs = append(chs, make(chan token))
  }
  for j := 0; j < num; j++ {
    go worker(j, chs[j], chs[(j+1)%num])
  }
  // 先把令牌交给第一个
  chs[0] <- struct{}{}
  select {}
}

func worker(id int, ch chan token, next chan token) {
  for {
    // 对应work 取得令牌
    token := <-ch
    fmt.Println(id + 1)
    time.Sleep(1 * time.Second)
    // 传递给下一个
    next <- token
  }
}
```



## 读写流程

> 向 channel 写数据:
>
> 1. 若等待接收队列 recvq 不为空，则缓冲区中无数据或无缓冲区，将直接从 recvq 取出 G ，并把数据写入，最后把该 G 唤醒，结束发送过程。
> 2. 若缓冲区中有空余位置，则将数据写入缓冲区，结束发送过程。
> 3. 若缓冲区中没有空余位置，则将发送数据写入 G，将当前 G 加入 sendq ，进入睡眠，等待被读 goroutine 唤醒。

> 从 channel 读数据
>
> 1. 若等待发送队列 sendq 不为空，且没有缓冲区，直接从 sendq 中取出 G ，把 G 中数据读出，最后把 G 唤醒，结束读取过程。
> 2. 如果等待发送队列 sendq 不为空，说明缓冲区已满，从缓冲区中首部读出数据，把 G 中数据写入缓冲区尾部，把 G 唤醒，结束读取过程。
> 3. 如果缓冲区中有数据，则从缓冲区取出数据，结束读取过程。
> 4. 将当前 goroutine 加入 recvq ，进入睡眠，等待被写 goroutine 唤醒。

> 关闭 channel
>
> 1.关闭 channel 时会将 recvq 中的 G 全部唤醒，本该写入 G 的数据位置为 nil。将 sendq 中的 G 全部唤醒，但是这些 G 会 panic。
>
> panic 出现的场景还有：
>
> - 关闭值为 nil 的 channel
> - 关闭已经关闭的 channel
> - 向已经关闭的 channel 中写数据



