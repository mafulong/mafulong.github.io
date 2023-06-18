---
layout: post
category: AWS
title: AWS Cloudformation And CDK
tags: AWS
---

# AWS Cloudformation

cloudFormation以yaml文本的形式记录下一个应用涉及到的各个服务资源配置，放在一个template里面。迁移到不同的region时，只需要一键run coudFormation template, 就可以部署好所有的AWS资源。

也叫AWS 堆栈

## 为什么使用 CloudFormation？

**基础设施即代码：**CloudFormation 使我们只用一个步骤就可以创建一个“资源堆栈”。资源是我们创建的东西（EC2 实例、VPC、子网等等），一组这样的资源称为堆栈。我们可以编写一个模板，使用它可以很容易地按照我们的意愿通过一个步骤创建一个网络堆栈。这比通过管理控制台或 CLI 手动创建网络更快，而且可重复，一致性更好。我们可以将模板签入源代码控制，并在任何时候根据需要把它用于任何目的。



**可升级：**我们可以通过修改 CloudFormation 模板来修改网络堆栈，然后根据修改后的模板修改堆栈。CloudFormation 足够智能，可以通过修改堆栈来匹配模板。



**可重用**：我们可以重用这个模板，在不同时期、不同区域创建多个不用用途的网络。



**漂移检测：**CloudFormation 有一个新特性（截止到 2018 年 11 月），可以让我们知道资源是否已经“漂移”出了最初的配置。这可能发生在管理员手动更改资源时，这通常不是成熟的组织所鼓励的做法。



**用完即弃：**我们很容易在用完之后把堆栈删除。



## 使用

CloudFormation 支持 JSON 或 YAML，我们将使用后者。主要原因是：1）句法不那么讲究，2）能够在工作中添加注释

比如一个[VPC示例](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html)

然后AWS控制台。 登录，选择任何区域。在菜单中找到 CloudFormation，如果需要的话，使用搜索功能。登入后，点击“创建堆栈”。选择“上传你自己的模板”选项，然后单击“下一步”。就可以创建堆栈了，还可以看到事件和资源。

这些事件将显示你的 VPC 是在什么时候创建的，以及它是在什么时候成功创建的。当堆栈中的最后一个资源被创建时，堆栈的状态将更改为已成功创建。

有一个重要的概念需要注意，如果在创建堆栈时遇到任何错误，整个堆栈（所有资源）将回滚。这种行为可以被重写，但通常这样就行！通常情况下，从头开始执行每一步要容易得多。

如果堆栈失败，它仍然会显示在堆栈列表中，即使堆栈中没有资源。这样做是为了给你时间来调查错误。确定问题后，使用“删除堆栈”操作。

## 参考

- [AWS CloudFormation简介](https://juejin.cn/post/7122039768124227614)

- [如何使用 CloudFormation 构建 VPC（第一部分）](https://www.infoq.cn/article/hsaedm*2we5jmh9tfjeg)

# CDK

 AWS **Cloud Development Kit**



The AWS Cloud Development Kit (CDK) provides some of the same benefits of CloudFormation but with a few key differences.

The CDK is an infrastructure-as-code solution that you can use with several popular programming languages. In other words, it's like CloudFormation, but using a language you already know. The CDK also contains command line tools to create infrastructure-as-code templates and to instantiate, update, and tear down stacks.



CDK和Cloud Formation很像，但一个区别是它可以用自己知道的一个语言，比如typescript来写这样。

CDK 把 CloudFormation 抽象了一层。它使用 TypeScript 等程序语言，把 CloudFormation 的模板包装成了一个领域专用语言（domain-specific language），CDK 的编译器会把这个语言再转译成 CloudFormation 模板。

CDK更好用。但底层实际也是CloudFormation。



CDK 教程： [官网](https://aws.amazon.com/cn/getting-started/guides/setup-cdk/module-three/?trk=31aeab24-3bd8-472c-a670-df09849e33f8&sc_channel=el)

**cdk deploy** 命令会将您的 TypeScript 编译为 JavaScript，同时创建一个 CloudFormation 更改集来部署此更改。 



## CDK教程

### cdk命令

```scala
cdk diff        compare deployed stack with current state 将指定的堆栈及其依赖关系与已部署的堆栈或本地 CloudFormation 模板进行比较

cdk deploy 命令会将您的 TypeScript 编译为 JavaScript，同时创建一个 CloudFormation 更改集来部署此更改。  deploy this stack to your default AWS account/region

cdk synth       emits the synthesized CloudFormation template 输出cloudFormation的diff.
cdk init --language typescript
cdk list (ls) 列出应用程序中的堆栈
```

cdk bootstrp只有在用一些kms等特殊资源时才有用





自定义ts主要在lib文件夹中。

## 基础设施



在深入探讨代码的编写之前，我们需要解释和安装 **[AWS CDK 构造库模块](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-construct-library.html)**。 构造可以代表单个 AWS 资源，例如 Amazon Simple Storage Service（Amazon S3）存储桶，也可以是由多个 AWS 相关资源组成的更高级别的抽象。 AWS 构造库由几个模块组成。 对于本教程，我们需要 Amazon EC2 模块，该模块中还包括对 Amazon VPC 的支持。

要安装 Amazon EC2 模块，我们将使用 **npm**。 在项目目录中运行以下命令：

```bash
npm install @aws-cdk/aws-ec2
```

该命令安装所有必需的模块。如果查看您的 **package.json** 文件，就会看到该文件也添加到此处。



事例code

```scala
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class CdkDemoStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    // We have created the VPC object from the VPC class
    new ec2.Vpc(this, 'mainVPC', {
      // This is where you can define how many AZs you want to use
      maxAzs: 2,
      // This is where you can define the subnet configuration per AZ
      subnetConfiguration: [
         {
           cidrMask: 24,
           name: 'public-subnet',
           subnetType: ec2.SubnetType.PUBLIC,
         }
      ]
   });
  }
}
```

app.ts 是所有代码的入口点。通常任何额外的代码都可以通过在扩展 DeploymentStack 类的其他文件中创建类来组织为堆栈

## Cdk toolkit for vscode

[link](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/setup-toolkit.html#setup-prereq)

# 使用former2进行资源配置导出

这是一个AWS 账号里现成资源导出成CDK/cloudformation的开源工具。

https://github.com/iann0036/former2



需要再mac本地上运行，而不用他们提供的外部开放网站，这样更安全。



如何本地运行？

1. mac上启动docker. 

2. ```scala
   git clone git@github.com:iann0036/former2.git
   cd former2
   docker build -t former2_local:1.0 .
   docker run --name former2 -p $host_port:80 -d former2_local:1.0
   ```

3. docker软件里open broswer. 会进入127.0.0.1:xxx的一个网址。

4. 然后aws账号里创建一个iam user,授予读的权限。iam user里的安全凭证下面点击访问密钥，创建一个ak, sk。

5. 然后填入进行scan。scan后就可以看资源，选中，然后点击左上角的generate 就可以看到生成的代码了。

