---
layout: post
category: Go
title: goroutine
tags: Go
---

[讲的很好的一篇](https://segmentfault.com/a/1190000021951119)

## 协程，线程，进程

  * 进程

进程是具有一定独立功能的程序关于某个数据集合上的一次运行活动,进程是系统进行资源分配和调度的一个独立单位。每个进程都有自己的独立内存空间，不同进程通过进程间通信来通信。由于进程比较重量，占据独立的内存，所以上下文进程间的切换开销（栈、寄存器、虚拟内存、文件句柄等）比较大，但相对比较稳定安全。

  * 线程

线程是进程的一个实体,是CPU调度和分派的基本单位,它是比进程更小的能独立运行的基本单位.线程自己基本上不拥有系统资源,只拥有一点在运行中必不可少的资源(如程序计数器,一组寄存器和栈),但是它可与同属一个进程的其他的线程共享进程所拥有的全部资源。线程间通信主要通过共享内存，上下文切换很快，资源开销较少，但相比进程不够稳定容易丢失数据。

  * 协程

协程是一种用户态的轻量级线程，协程的调度完全由用户控制。协程拥有自己的寄存器上下文和栈。协程调度切换时，将寄存器上下文和栈保存到其他地方，在切回来的时候，恢复先前保存的寄存器上下文和栈，直接操作栈则基本没有内核切换的开销，可以不加锁的访问全局变量，所以上下文的切换非常快。

## goroutines和线程区别

goroutine和操作系统的线程区别。尽管两者的区别实际上只是一个量的区别，但量变会引起质变的道理同样适用于goroutine和线程。现在正是我们来区分开两者的最佳时机。

### 1. 动态栈

每一个OS线程都有一个固定大小的内存块(一般会是2MB)来做栈，这个栈会用来存储当前正在被调用或挂起(指在调用其它函数时)的函数的内部变量。这个固定大小的栈同时很大又很小。因为2MB的栈对于一个小小的goroutine来说是很大的内存浪费，比如对于我们用到的，一个只是用来WaitGroup之后关闭channel的goroutine来说。而对于go程序来说，同时创建成百上千个gorutine是非常普遍的，如果每一个goroutine都需要这么大的栈的话，那这么多的goroutine就不太可能了。除去大小的问题之外，固定大小的栈对于更复杂或者更深层次的递归函数调用来说显然是不够的。修改固定的大小可以提升空间的利用率允许创建更多的线程，并且可以允许更深的递归调用，不过这两者是没法同时兼备的。

相反，一个goroutine会以一个很小的栈开始其生命周期，一般只需要2KB。一个goroutine的栈，和操作系统线程一样，会保存其活跃或挂起的函数调用的本地变量，但是和OS线程不太一样的是一个goroutine的栈大小并不是固定的；栈的大小会根据需要动态地伸缩。而goroutine的栈的最大值有1GB，比传统的固定大小的线程栈要大得多，尽管一般情况下，大多goroutine都不需要这么大的栈。

### 2. Goroutine调度
OS线程会被操作系统内核调度。每几毫秒，一个硬件计时器会中断处理器，这会调用一个叫作scheduler的内核函数。这个函数会挂起当前执行的线程并保存内存中它的寄存器内容，检查线程列表并决定下一次哪个线程可以被运行，并从内存中恢复该线程的寄存器信息，然后恢复执行该线程的现场并开始执行线程。因为操作系统线程是被内核所调度，所以从一个线程向另一个“移动”需要完整的上下文切换，也就是说，保存一个用户线程的状态到内存，恢复另一个线程的到寄存器，然后更新调度器的数据结构。这几步操作很慢，因为其局部性很差需要几次内存访问，并且会增加运行的cpu周期。

Go的运行时包含了其自己的调度器，这个调度器使用了一些技术手段，比如m:n调度，因为其会在n个操作系统线程上多工(调度)m个goroutine。Go调度器的工作和内核的调度是相似的，但是这个调度器只关注单独的Go程序中的goroutine(译注：按程序独立)。

和操作系统的线程调度不同的是，Go调度器并不是用一个硬件定时器而是被Go语言"建筑"本身进行调度的。例如当一个goroutine调用了time.Sleep或者被channel调用或者mutex操作阻塞时，调度器会使其进入休眠并开始执行另一个goroutine直到时机到了再去唤醒第一个goroutine。因为因为这种调度方式不需要进入内核的上下文，所以重新调度一个goroutine比调度一个线程代价要低得多。

### 3. GOMAXPROCS
Go的调度器使用了一个叫做GOMAXPROCS的变量来决定会有多少个操作系统的线程同时执行Go的代码。其默认的值是运行机器上的CPU的核心数，所以在一个有8个核心的机器上时，调度器一次会在8个OS线程上去调度GO代码。(GOMAXPROCS是前面说的m:n调度中的n)。在休眠中的或者在通信中被阻塞的goroutine是不需要一个对应的线程来做调度的。在I/O中或系统调用中或调用非Go语言函数时，是需要一个对应的操作系统线程的，但是GOMAXPROCS并不需要将这几种情况计数在内。

你可以用GOMAXPROCS的环境变量吕显式地控制这个参数，或者也可以在运行时用runtime.GOMAXPROCS函数来修改它。我们在下面的小程序中会看到GOMAXPROCS的效果，这个程序会无限打印0和1。

```
for {
    go fmt.Print(0)
    fmt.Print(1)
}

$ GOMAXPROCS=1 go run hacker-cliché.go
111111111111111111110000000000000000000011111...

$ GOMAXPROCS=2 go run hacker-cliché.go
010101010101010101011001100101011010010100110...

```

在第一次执行时，最多同时只能有一个goroutine被执行。初始情况下只有main goroutine被执行，所以会打印很多1。过了一段时间后，GO调度器会将其置为休眠，并唤醒另一个goroutine，这时候就开始打印很多0了，在打印的时候，goroutine是被调度到操作系统线程上的。在第二次执行时，我们使用了两个操作系统线程，所以两个goroutine可以一起被执行，以同样的频率交替打印0和1。我们必须强调的是goroutine的调度是受很多因子影响的，而runtime也是在不断地发展演进的，所以这里的你实际得到的结果可能会因为版本的不同而与我们运行的结果有所不同。



注意，这个上限是10000，当遇到阻塞时，P会调度到一个新的M上，因此数量会增加。

### 4. Goroutine没有ID号
在大多数支持多线程的操作系统和程序语言中，当前的线程都有一个独特的身份(id)，并且这个身份信息可以以一个普通值的形式被被很容易地获取到，典型的可以是一个integer或者指针值。这种情况下我们做一个抽象化的thread-local storage(线程本地存储，多线程编程中不希望其它线程访问的内容)就很容易，只需要以线程的id作为key的一个map就可以解决问题，每一个线程以其id就能从中获取到值，且和其它线程互不冲突。

goroutine没有可以被程序员获取到的身份(id)的概念。这一点是设计上故意而为之，由于thread-local storage总是会被滥用。比如说，一个web server是用一种支持tls的语言实现的，而非常普遍的是很多函数会去寻找HTTP请求的信息，这代表它们就是去其存储层(这个存储层有可能是tls)查找的。这就像是那些过分依赖全局变量的程序一样，会导致一种非健康的“距离外行为”，在这种行为下，一个函数的行为可能不是由其自己内部的变量所决定，而是由其所运行在的线程所决定。因此，如果线程本身的身份会改变——比如一些worker线程之类的——那么函数的行为就会变得神秘莫测。

Go鼓励更为简单的模式，这种模式下参数对函数的影响都是显式的。这样不仅使程序变得更易读，而且会让我们自由地向一些给定的函数分配子任务时不用担心其身份信息影响行为。



## GMP模型

> [可以看这篇文章 ](https://juejin.im/post/6844904130398404616)

Go语言在语言层面实现并发。Go编写一个并发编程程序很简单，只需要在函数调用之前使用一个`go`关键字即可启动一个goroutine执行并发。    

    func main() {
        go func(){
            fmt.Println("Hello,World!")
        }()
    }


虽然使用一个`go`关键字即可实现并发编程，但是是这个关键字的背后的实现非常复杂。

### 前导：并发与并行

通常说的并发编程，是指允许多个任务同时执行，但实际上并不一定在同一时刻被执行。在单核处理器上，通过多线程共享CPU时间片 **串行执行**
。而并行编程则依赖于多核处理器，让多个任务可以实现 **并行执行** 。

简单的说

  * **并发** : 逻辑上同时处理多个任务。

  * **并行** : 物理上同时处理多个任务。

### Go语言的并发模型

Go语言的并发处理参考了CSP（Communicating Sequential
Process）模型。CSP并发模型不同于传统的多线程通过共享内存来通信，CSP讲究的是“以通信的方式来共享内存”。

> Don’t communicate by sharing memory; share memory by communicating.
>
> 不要以共享内存的方式来通信，要通过通信来共享内存。

golang的CSP模型实现与原始的CSP实现有点差别：原始的CSP中channel里的任务都是立即执行的，而go语言为其增加了一个缓存，即任务可以先暂存起来，等待执行线程准备好再顺序执行。

### Go调度器

go语言运行时环境提供了非常强大的管理goroutine和系统内核线程的调度器，
内部提供了三种对象：Goroutine，Machine，Processor。

- **Goroutine** : 指应用创建的goroutine 。每个Goroutine对应一个G结构体，G保存Goroutine的运行堆栈，即并发任务状态。G并非执行体，每个G需要绑定到P才能被调度执行。stack的size默认设置为2k。底层是使用协程(coroutine)实现，coroutine是一种运行在用户态的用户线程（参考操作系统原理：内核态，用户态）

- **Machine** : 指系统内核线程。 Machine, OS线程抽象，负责调度任务，和某个P绑定，从P的runq中不断取出G，切换堆栈并执行，M本身不具备执行状态，在需要任务切换时，M将堆栈状态写回G，任何其它M都能据此恢复执行。

  个数是不定的，由Go Runtime调整，默认最大限制为10000个。

  - runtime/debug 中的 SetMaxThreads 函数，设置 M 的最大数量
  - 一个 M 阻塞了，会创建新的 M。

- **Processor** : 指承载多个goroutine的运行器。对G来说，P相当于CPU核，G只有绑定到P(在P的local runq中)才能被调度。对M来说，P提供了相关的执行环境(Context)，如内存分配状态(mcache)，任务队列(G)等，个数由系统几核决定，比如8核cpu那就是8，因此限制最大并发数。可调整，GOMAXPROCS参数，实际应该就是几核。

  在宏观上说，Goroutine与Machine因为Processor的存在，形成了多对多（M:N）的关系。

**额外还有sched**：全局资源池和任务池，全局只有一个 schedt 类型的实例，负责保存M空闲列表，G 全局运行队列, P 空闲列表。有多个Lock是非常必须的，如果M或P等做一些非局部的操作，它们一般需要先锁住调度器。在新的调度器中依然有全局 G 队列，但功能已经被弱化了，当 M 执行 work stealing 从其他 P 偷不到 G 时，它可以从全局 G 队列获取 G。





三者与内核级线程的关系如下图所示：

![](https://cdn.jsdelivr.net/gh/mafulong/mdPic@master/images/dc2a71ec365985552475b70edc5f28a3.jpeg)

一个Machine会对应一个内核线程（K），同时会有一个Processor与它绑定。一个Processor连接一个或者多个Goroutine。Processor有一个运行时的Goroutine（上图中绿色的G），其它的Goroutine处于等待状态。

可通过GOMAXPROCS限制同时执行用户级任务的操作系统线程，其实就是P的数量。GOMAXPROCS值默认是CPU的可用核心数，但是其数量是可以指定的。



- 全局队列（Global Queue）：存放等待运行的 G。
- P 的本地队列：同全局队列类似，存放的也是等待运行的 G，存的数量有限，不超过 256 个。新建 G’时，G’优先加入到 P 的本地队列，如果队列满了，则会把本地队列中一半的 G 移动到全局队列。
- P 列表：所有的 P 都在程序启动时创建，并保存在数组中，最多有 GOMAXPROCS(可配置) 个。
- M：线程想运行任务就得获取 P，从 P 的本地队列获取 G，P 队列为空时，M 也会尝试从全局队列拿一批 G 放到 P 的本地队列，或从其他 P 的本地队列偷一半放到自己 P 的本地队列。M 运行 G，G 执行之后，M 会从 P 获取下一个 G，不断重复下去。



抢占：在 coroutine 中要等待一个协程主动让出 CPU 才执行下一个协程，在 Go 中，一个 goroutine 最多占用 CPU 10ms，防止其他 goroutine 被饿死，这就是 goroutine 不同于 coroutine 的一个地方。

### go func () 调度流程

![img](https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv8/v8/202501120001743.jpg)

从上图我们可以分析出几个结论：

 1、我们通过 go func () 来创建一个 goroutine；

 2、有两个存储 G 的队列，一个是局部调度器 P 的本地队列、一个是全局 G 队列。新创建的 G 会先保存在 P 的本地队列中，如果 P 的本地队列已经满了就会保存在全局的队列中；

 3、G 只能运行在 M 中，一个 M 必须持有一个 P，M 与 P 是 1：1 的关系。M 会从 P 的本地队列弹出一个可执行状态的 G 来执行，如果 P 的本地队列为空，就会想其他的 MP 组合偷取一个可执行的 G 来执行；

 4、一个 M 调度 G 执行的过程是一个循环机制；

 5、当 M 执行某一个 G 时候如果发生了 syscall 或则其余阻塞操作，M 会阻塞，如果当前有一些 G 在执行，runtime 会把这个线程 M 从 P 中摘除 (detach)，然后再创建一个新的操作系统的线程 (如果有空闲的线程可用就复用空闲线程) 来服务于这个 P；

 6、当 M 系统调用结束时候，这个 G 会尝试获取一个空闲的 P 执行，并放入到这个 P 的本地队列。如果获取不到 P，那么这个线程 M 变成休眠状态， 加入到空闲线程中，然后这个 G 会被放入全局队列中。



### Go调度器调度过程



当一个Goroutine创建被创建时，Goroutine对象被压入 **Processor的本地队列** 或者 **Go运行时
全局Goroutine队列** 。Processor唤醒一个Machine，如果Machine的waiting队列没有等待被
唤醒的Machine，则创建一个（只要不超过Machine的最大值，10000），Processor获取到Machine后，与此Machine绑定，并执行此Goroutine。

Machine执行过程中，随时会发生上下文切换。当发生上下文切换时，需要对执行现场进行保护，以便下次被调度执行时进行现场恢复。Go调度器中Machine的栈保存在Goroutine对象上，只需要将Machine所需要的寄存器(堆栈指针、程序计数器等)保存到Goroutine对象上即可。如果此时Goroutine任务还没有执行完，Machine可以将Goroutine重新压入Processor的队列，等待下一次被调度执行。

如果执行过程遇到阻塞并阻塞超时（调度器检测这种超时），Machine会与Processor分离，并等待阻塞结束。此时Processor可以继续唤醒Machine执行其它的Goroutine，当阻塞结束时，Machine会尝试”偷取”一个Processor，如果失败，这个Goroutine会被加入到全局队列中，然后Machine将自己转入Waiting队列，等待被再次唤醒。

在各个Processor运行完本地队列的任务时，会从全局队列中获取任务，调度器也会定期检查全局队列，否则在并发较高的情况下，全局队列的Goroutine会因为得不到调度而”饿死”。如果全局队列也为空的时候，会去分担其它Processor的任务，一次分一半任务，比如，ProcessorA任务完成了，ProcessorB还有10个任务待运行，Processor在获取任务的时候，会一次性拿走5个。（是不是觉得Processor相互之间很友爱啊
^_^）。



本质上是个抢占式调度。Go scheduler 会启动一个后台线程 sysmon，用来检测长时间（超过 10 ms）运行的 goroutine，将其调度到 global runqueues。这是一个全局的 runqueue，优先级比较低，以示惩罚。



M状态变化: 

<img src="https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv3/v3/20210523140241.png" alt="M 的状态流转图" style="zoom: 33%;" />

M 只有自旋和非自旋两种状态。自旋的时候，会努力找工作：检查全局队列，查看 network poller，试图执行 gc 任务，或者“偷”工作。；找不到的时候会进入非自旋状态，之后会休眠，直到有工作需要处理时，被其他工作线程唤醒，又进入自旋状态。



### 调度器的生命周期

[参考](https://www.topgoer.com/%E5%B9%B6%E5%8F%91%E7%BC%96%E7%A8%8B/GMP%E5%8E%9F%E7%90%86%E4%B8%8E%E8%B0%83%E5%BA%A6.html#4-%E8%B0%83%E5%BA%A6%E5%99%A8%E7%9A%84%E7%94%9F%E5%91%BD%E5%91%A8%E6%9C%9F)

特殊的 M0 和 G0

M0

M0 是启动程序后的编号为 0 的主线程，这个 M 对应的实例会在全局变量 runtime.m0 中，不需要在 heap 上分配，M0 负责执行初始化操作和启动第一个 G， 在之后 M0 就和其他的 M 一样了。

G0

G0 是每次启动一个 M 都会第一个创建的 gourtine，G0 仅用于负责调度的 G，G0 不指向任何可执行的函数，每个 M 都会有一个自己的 G0。在调度或系统调用时会使用 G0 的栈空间，全局变量的 G0 是 M0 的 G0。



调度器的生命周期几乎占满了一个 Go 程序的一生，runtime.main 的 goroutine 执行之前都是为调度器做准备工作，runtime.main 的 goroutine 运行，才是调度器的真正开始，直到 runtime.main 结束而结束。

### 一些优化

- 资源复用，池子。
- 无锁结构。

### C10K问题
一个服务器处理10000个连接后，性能会急剧下降。

为了减少线程切换开销，有了多路io复用.

典型的IO多路复用编程模式为Reactor模式(这也是C++20协程设计思路)：
  1. 专门的线程(或者进程)采用IO多路复用的模式负责批量的处理网络IO，实现吞吐量最大化；
  2. 专门的线程(或者进程)负责处理请求；
  3. IO线程通过消息队列或者其他的方式将请求发送给业务线程；

### goroutine数据结构

G: 

```go
type g struct {
    // goroutine 使用的栈
    stack       stack   // offset known to runtime/cgo
    // 用于栈的扩张和收缩检查，抢占标志
    stackguard0 uintptr // offset known to liblink
    stackguard1 uintptr // offset known to liblink
    _panic         *_panic // innermost panic - offset known to liblink
    _defer         *_defer // innermost defer
    // 当前与 g 绑定的 m
    m              *m      // current m; offset known to arm liblink
    // goroutine 的运行现场
    sched          gobuf
    syscallsp      uintptr        // if status==Gsyscall, syscallsp = sched.sp to use during gc
    syscallpc      uintptr        // if status==Gsyscall, syscallpc = sched.pc to use during gc
    stktopsp       uintptr        // expected sp at top of stack, to check in traceback
    // wakeup 时传入的参数
    param          unsafe.Pointer // passed parameter on wakeup
    atomicstatus   uint32
    stackLock      uint32 // sigprof/scang lock; TODO: fold in to atomicstatus
    goid           int64
    // g 被阻塞之后的近似时间
    waitsince      int64  // approx time when the g become blocked
    // g 被阻塞的原因
    waitreason     string // if status==Gwaiting
    // 指向全局队列里下一个 g
    schedlink      guintptr
    // 抢占调度标志。这个为 true 时，stackguard0 等于 stackpreempt
    preempt        bool     // preemption signal, duplicates stackguard0 = stackpreempt
    paniconfault   bool     // panic (instead of crash) on unexpected fault address
    preemptscan    bool     // preempted g does scan for gc
    gcscandone     bool     // g has scanned stack; protected by _Gscan bit in status
    gcscanvalid    bool     // false at start of gc cycle, true if G has not run since last scan; TODO: remove?
    throwsplit     bool     // must not split stack
    raceignore     int8     // ignore race detection events
    sysblocktraced bool     // StartTrace has emitted EvGoInSyscall about this goroutine
    // syscall 返回之后的 cputicks，用来做 tracing
    sysexitticks   int64    // cputicks when syscall has returned (for tracing)
    traceseq       uint64   // trace event sequencer
    tracelastp     puintptr // last P emitted an event for this goroutine
    // 如果调用了 LockOsThread，那么这个 g 会绑定到某个 m 上
    lockedm        *m
    sig            uint32
    writebuf       []byte
    sigcode0       uintptr
    sigcode1       uintptr
    sigpc          uintptr
    // 创建该 goroutine 的语句的指令地址
    gopc           uintptr // pc of go statement that created this goroutine
    // goroutine 函数的指令地址
    startpc        uintptr // pc of goroutine function
    racectx        uintptr
    waiting        *sudog         // sudog structures this g is waiting on (that have a valid elem ptr); in lock order
    cgoCtxt        []uintptr      // cgo traceback context
    labels         unsafe.Pointer // profiler labels
    // time.Sleep 缓存的定时器
    timer          *timer         // cached timer for time.Sleep
    gcAssistBytes int64
}
```

关键数据结构：

- 数据栈：栈顶，栈低。
- gobuf: 各种pc, sp寄存器。
- m:  线程信息，包含了自身使用的栈信息、G信息、P信息。

## Key Points

[参考](https://www.bookstack.cn/read/qcrao-Go-Questions/goroutine%20%E8%B0%83%E5%BA%A6%E5%99%A8-%E4%BB%80%E4%B9%88%E6%98%AF%20go%20shceduler.md)

### goroutine 调度时机

在四种情形下，goroutine 可能会发生调度，但也并不一定会发生，只是说 Go scheduler 有机会进行调度。

| 情形            | 说明                                                         |
| :-------------- | :----------------------------------------------------------- |
| 使用关键字 `go` | go 创建一个新的 goroutine，Go scheduler 会考虑调度           |
| GC              | 由于进行 GC 的 goroutine 也需要在 M 上运行，因此肯定会发生调度。当然，Go scheduler 还会做很多其他的调度，例如调度不涉及堆访问的 goroutine 来运行。GC 不管栈上的内存，只会回收堆上的内存 |
| 系统调用        | 当 goroutine 进行系统调用时，会阻塞 M，所以它会被调度走，同时一个新的 goroutine 会被调度上来 |
| 内存同步访问    | atomic，mutex，channel 操作等会使 goroutine 阻塞，因此会被调度走。等条件满足后（例如其他 goroutine 解锁了）还会被调度上来继续运行 |

### 什么是 sheduler

Go 程序的执行由两层组成：Go Program，Runtime，即用户程序和运行时。它们之间通过函数调用来实现内存管理、channel 通信、goroutines 创建等功能。用户程序进行的系统调用都会被 Runtime 拦截，以此来帮助它进行调度以及垃圾回收相关的工作。

一个展现了全景式的关系如下图：

<img src="https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv3/v3/20220423175440.png" alt="runtime overall" style="zoom:50%;" />

Go scheduler 是 Go runtime 的一部分，它内嵌在 Go 程序里，和 Go 程序一起运行。因此它运行在用户空间，在 kernel 的上一层。和 Os scheduler 抢占式调度（preemptive）不一样，Go scheduler 采用协作式调度（cooperating）。

但是由于在 Go 语言里，goroutine 调度的事情是由 Go runtime 来做，并非由用户控制，所以我们依然可以将 Go scheduler 看成是抢占式调度，因为用户无法预测调度器下一步的动作是什么。

<img src="https://cdn.jsdelivr.net/gh/mafulong/mdPic@vv3/v3/20220423175721.png" alt="goroutine workflow" style="zoom:67%;" />

### GMP

Go的`GOMAXPROCS`默认值已经设置为 CPU的核数。可以通过设置这个参数设置P的数量

M和P数量默认为GOMAXPROCS， 但M由于调度阻塞是可以动态加的， 但P不能自己动态增加数量。





### Goroutine 的阻塞

**(1) Goroutine 内部的同步阻塞**

- **示例**：`channel` 的读写操作、`select` 等。

- 线程行为

  - 当 Goroutine 因 `channel`、`mutex` 或其他 Go 的同步原语而阻塞时，该 Goroutine 会被 **挂起**，对应的线程会释放资源继续执行其他 Goroutine。
- Go 的调度器（GMP 模型）会将阻塞的 Goroutine 标记为等待状态，并把线程从阻塞的 Goroutine 中解放出来执行其他任务。
  - 比如因为channel阻塞，当channel有数据时才会唤醒这个阻塞的goroutine，然后如果当前 P 仍然有可用的 OS 线程（M），则直接运行它，否则就创建新的线程

**(2) 系统调用（Syscall）导致的阻塞**。这个特殊，是线程阻塞。

- **示例**：执行 I/O 操作、文件读写、网络调用等。调用http等返回。

- 线程行为

  - 如果 Goroutine 调用了一个会导致操作系统层面阻塞的系统调用（如 I/O），那么该系统调用会阻塞整个线程。这是操作系统的规则，系统调用必须阻塞线程。

  - Go 运行时会通过调度机制将阻塞线程上的其他 Goroutine 转移到空闲线程上继续执行。

  - 核心机制

    - 如果一个线程因为系统调用而阻塞，Go 会启动新的线程（如果必要）以保证其他 Goroutine 不受影响。

**(3) 主 Goroutine 阻塞**

- **示例**：主 Goroutine 调用 `time.Sleep()` 或等待 `channel`。

- 线程行为

  - 主 Goroutine 的阻塞不会直接导致所有线程阻塞。
- 其他线程上的 Goroutine 仍然可以正常执行，因为 Go 的调度器会继续调度其他 Goroutine。





总结

- **如果 Goroutine 导致 OS 线程阻塞（如 syscall）**，Go 运行时会 **分离 P，并释放 M**，创建新的 M 继续调度。

- **如果 Goroutine 只是逻辑阻塞（如 Mutex、Channel、Sleep）**，Go 运行时 **仅分离 P，不释放 M**，M 仍然等待 Goroutine 解除阻塞。

- 线程阻塞场景。**Go 线程（M）不会轻易阻塞**，但 **系统调用、CGO、GC、资源竞争、死锁等情况会导致线程阻塞**。

  - 系统调用
  - gc影响
  - goroutine太多影响，压垮系统

- 线程创建时机

  - 默认创建 `GOMAXPROCS` 个 P（Processor），尝试创建 `N` 个 M（线程）。  
  - 发生 I/O 阻塞、系统调用，当前 M 线程可能被阻塞，Go 运行时会创建新 M 线程。
  - 若 Goroutines 过多，Go 运行时可能创建新的 M 线程来执行任务。
  - CGO 调用 C 代码会绑定 Goroutine 到 M 线程，Go 运行时可能创建额外 M。
  - 绑定 Goroutine 到当前 OS 线程，可能触发新 M 创建。

  

  

### 