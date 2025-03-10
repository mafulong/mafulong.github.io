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

	// 双向channel可直接转换成单向的channel
  a := make(chan int, 100)
	b := make(chan<- int, 3)
	b = a
	
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
  - 等待接收和发送的goroutine队列（这些 goroutine 由于尝试读取 channel 或向 channel 发送数据而被阻塞） **是双向链表，每个元素就是goroutine的封装**。
  - mutex锁保护所有字段。

- chan本质是值的拷贝，无论是从 sender goroutine 的栈到 chan buf，还是从 chan buf 到 receiver goroutine，或者是直接从 sender goroutine 到 receiver goroutine。

- channel引发goroutine泄露：当且仅当goroutine 操作 channel 后，处于发送或接收阻塞状态，而 channel 处于满或空的状态，一直得不到改变。同时，垃圾回收器也不会回收此类资源，进而导致 gouroutine 会一直处于等待队列中，不见天日。程序运行过程中，对于一个 channel，如果没有任何 goroutine 引用了，gc 会对其进行回收操作，不会引起内存泄漏。

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

- channel是FIFO并且公平的，但select语句是随机的。

- channel的happened-before

  - channel close 一定 `happened before` receiver 得到通知。由于现代编译器、CPU 会做各种优化，包括编译器重排、内存重排等等，在并发代码里，happened-before 限制就非常重要了。

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

**读、写一个 nil channel 都会被阻塞。**





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



## 如何优雅关闭channel



不要从一个 receiver 侧关闭 channel，也不要在有多个 sender 时，关闭 channel。



有两个不那么优雅地关闭 channel 的方法：

1. 使用 defer-recover 机制，放心大胆地关闭 channel 或者向 channel 发送数据。即使发生了 panic，有 defer-recover 在兜底。
2. 使用 sync.Once 来保证只关闭一次。



在 Go 语言中，对于一个 channel，如果最终没有任何 goroutine 引用它，不管 channel 有没有被关闭，最终都会被 gc 回收。所以，在这种情形下，所谓的优雅地关闭 channel 就是不关闭 channel，让 gc 代劳。



### **那到底应该如何优雅地关闭 channel？**

根据 sender 和 receiver 的个数，分下面几种情况：

1. 一个 sender，一个 receiver
2. 一个 sender， M 个 receiver
3. N 个 sender，一个 receiver
4. N 个 sender， M 个 receiver



### 单Sender

对于 1，2，只有一个 sender 的情况就不用说了，直接从 sender 端关闭就好了，没有问题。重点关注第 3，4 种情况。

### 单receiver

第 3 种情形下，优雅关闭 channel 的方法是：the only receiver says “please stop sending more” by closing an additional signal channel。

解决方案就是增加一个传递关闭信号的 channel，receiver 通过信号 channel 下达关闭数据 channel 指令。senders 监听到关闭信号后，停止发送数据。



备注:

- 增加stop channel. 
- sender里select stop channel 和 data channel。这样有写数据时直接退出，不继续写data channel。

```go
func main() {
	rand.Seed(time.Now().UnixNano())

	const Max = 100000
	const NumSenders = 1000

	dataCh := make(chan int, 100)
	stopCh := make(chan struct{})

	// senders
	for i := 0; i < NumSenders; i++ {
		go func() {
			for {
				select {
				case <- stopCh:
					return
				case dataCh <- rand.Intn(Max):
				}
			}
		}()
	}

	// the receiver
	go func() {
		for value := range dataCh {
			if value == Max-1 {
				fmt.Println("send stop signal to senders.")
				close(stopCh)
				return
			}

			fmt.Println(value)
		}
	}()

	select {
	case <- time.After(time.Hour):
	}
}
```



### 多sender, 多receiver

**N 个 sender， M 个 receiver**



和第 3 种情况不同，这里有 M 个 receiver，如果直接还是采取第 3 种解决方案，由 receiver 直接关闭 stopCh 的话，就会重复关闭一个 channel，导致 panic。因此需要增加一个中间人，M 个 receiver 都向它发送关闭 dataCh 的“请求”，中间人收到第一个请求后，就会直接下达关闭 dataCh 的指令（通过关闭 stopCh，这时就不会发生重复关闭的情况，因为 stopCh 的发送方只有中间人一个）。另外，这里的 N 个 sender 也可以向中间人发送关闭 dataCh 的请求。





备注:

- 增加stop channel. 
- sender里select stop channel 和 data channel。这样有写数据时直接退出，不继续写data channel。
- 因此stop channel不能多receiver里重复关闭，因此增加一个toStop channel，是有缓冲区的长度为1。有单独goroutine接收到toStop时，close stop channel。这样stop channel就关闭一次。
- 假设 toStop 声明的是一个非缓冲型的 channel，那么第一个发送的关闭 dataCh 请求可能会丢失。因为无论是 sender 还是 receiver 都是通过 select 语句来发送请求，如果中间人所在的 goroutine 没有准备好，那 select 语句就不会选中，直接走 default 选项，什么也不做。这样，第一个关闭 dataCh 的请求就会丢失。



```go
func main() {
	rand.Seed(time.Now().UnixNano())

	const Max = 100000
	const NumReceivers = 10
	const NumSenders = 1000

	dataCh := make(chan int, 100)
	stopCh := make(chan struct{})

	// It must be a buffered channel.
	toStop := make(chan string, 1)

	var stoppedBy string

	// moderator
	go func() {
		stoppedBy = <-toStop
		close(stopCh)
	}()

	// senders
	for i := 0; i < NumSenders; i++ {
		go func(id string) {
			for {
				value := rand.Intn(Max)
				if value == 0 {
					select {
					case toStop <- "sender#" + id:
					default:
					}
					return
				}

				select {
				case <- stopCh:
					return
				case dataCh <- value:
				}
			}
		}(strconv.Itoa(i))
	}

	// receivers
	for i := 0; i < NumReceivers; i++ {
		go func(id string) {
			for {
				select {
				case <- stopCh:
					return
				case value := <-dataCh:
					if value == Max-1 {
						select {
						case toStop <- "receiver#" + id:
						default:
						}
						return
					}

					fmt.Println(value)
				}
			}
		}(strconv.Itoa(i))
	}

	select {
	case <- time.After(time.Hour):
	}

}
```

