## FEATURE:

当前项目是一个使用上下文工程来进行软件开发的模板项目，当前主要解决了新建项目的开发流程。
对于用户已有应用需要有对应的command来进行初始化，使得可以使用上下文工程来开发已有的应用。
请你帮我创建这样一个command(/init-context-engineering)，使得可以在用户项目里初始化上下文工程开发环境。
* 生成/init-context-engineering.md在当前项目的.claude/commands目录下
* 用户执行/init-context-engineering命令时,会指定目标目录,例如/init-context-engineering /path/to/target-project
* 用户执行/init-context-engineering命令时,此命令需要能自动创建项目所需要的上下文工程目录结构
  * 所有上下文工程相关的文档都放入目标项目的context-engineering目录下  
  * 此命令需要能从代码里先学习用户项目的开发规范和代码架构
  * 结合当前上下文工程项目的使用方法和用户项目来初始化上下文工程环境, 后续用户可以直接在其项目工程里迭代开发
  * 新增features目录，用于保存用户每次的需求输入
  * 提供使用方法的文档README.md,方便该项目所有开发者使用
  * 预期用户项目最终的目录结构如下：
    ```
    📦 targert-project
    ├── 📂 .claude
    │   ├── 🎯 settings.local.json
    │   └── 📂 commands
    │       ├── 🎯 generate-prp.md    #用户通过执行/init-context-engineering命令生成; 内容和当前项目一样,可以结合目标项目微调
    │       └── 🎯 execute-prp.md     #用户通过执行/init-context-engineering命令生成; 内容和当前项目一样,可以结合目标项目微调
    ├── 📂 context-engineering         # Context engineering project 用户通过执行/init-context-engineering命令生成
    │   ├── 📂 features/               # Features directory 用户通过执行/init-context-engineering命令生成;用户后续将原始需求放入此目录
    │   │   └── 🎯 INITIAL_EXAMPLE.md  # 用户通过执行/init-context-engineering命令生成, 用于用户参考如何编写原始需求
    │   ├── 📂 PRPs/           #  PRPs directory 用户通过执行/init-context-engineering命令生成; 执行/generate-prp后生成的prp需要放入此目录,生成的prp文件名需要以日期开始
    │   │   └── 📂 templates  # 用户通过执行/init-context-engineering命令生成
    │   │       └── 🎯 prp_base.md    #prp基础模板，在执行/generate-prp时参考; 用户通过执行/init-context-engineering命令生成;  初始内容和当前项目一样, 并基于在目标项目代码学习到的规范和架构知识更新
    │   ├── 📂 examples/     # Examples directory/ 用户通过执行/init-context-engineering命令生成;基于在目标项目代码学习到的规范和架构知识生成
    │   └── 🎯 README.md    # 上下文工程开发指南; 需要使用中文书写
    ├── 🎯 CLAUDDE.md  #用户通过执行/init-context-engineering命令生成; 内容和当前项目一样
    ... 原有项目文件目录
    ```
  * 文件和目录创建尽量不要依赖python, 优先使用claude-code的工具

* 特别注意：我们的目标是生成如上要求的/init-context-engineering命令即可,不用生成无关的代码和测试

## EXAMPLES:

[Provide and explain examples that you have in the `examples/` folder]

## DOCUMENTATION:
- [README.md](README.md)
- [CLAUDE.md](CLAUDE.md)

## OTHER CONSIDERATIONS:

[Any other considerations or specific requirements - great place to include gotchas that you see AI coding assistants miss with your projects a lot]
