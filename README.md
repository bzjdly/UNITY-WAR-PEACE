# WAR-PEACE

Unity 多人协作项目。仓库只保存可复现的项目源文件，Unity 生成的缓存、构建产物和个人编辑器配置不进入版本库。

## 开发环境

- Unity Editor：`2022.3.57f1c2`
- 版本控制：Git + Git LFS
- 默认分支：`main`
- 包源：`https://packages.unity.cn`

首次拉取仓库后，在仓库根目录执行：

```powershell
git lfs install
.\Tools\Git\Setup-Git.ps1
```

然后通过 Unity Hub 使用项目文件中记录的 Unity 版本打开此目录。

## 文档导航

设计与协作文档都随代码一起提交、一起审查。**`大纲.md` 是设计的唯一事实来源**：任何结论先在大纲中确认，其他文档只做派生、追踪或实现说明。

| 文档 | 作用 | 主要读者 | 当前版本 |
| --- | --- | --- | --- |
| [大纲.md](大纲.md) | 游戏整体设计：当前共识、暂定方向和待决定事项 | 全员 | v0.16 |
| [docs/设计问答.md](docs/设计问答.md) | 设计问答追踪：按依赖顺序提问、记录状态、回填大纲 | 制作人、设计 | Q01-Q16 |
| [docs/代码框架设计.md](docs/代码框架设计.md) | 代码架构基线：模块、契约、状态归属、数据流和实施顺序 | 程序 | v0.1 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 分支、提交、PR、Unity 资源和 LFS 规则 | 全员 | — |
| [docs/GITHUB_SETUP.zh-CN.md](docs/GITHUB_SETUP.zh-CN.md) | 仓库权限、分支保护、Issue、标签和 CI 设置 | 维护者 | — |

建议阅读顺序：`大纲.md` → `docs/设计问答.md`（先看哪些还没定）→ `docs/代码框架设计.md`（程序）→ `CONTRIBUTING.md`。

文档维护规则：

1. 设计问题先登记在 `docs/设计问答.md`；得到明确答复后**先回填 `大纲.md`**，再在问答条目上标注状态和回填位置。
2. `大纲.md` 区分“当前共识 / 暂定方向 / 待决定”，未确认内容不得写入共识段落。
3. `docs/代码框架设计.md` 只写模块、契约、状态归属和数据流，不写具体 C# 实现；实现细节以代码为准。
4. 每份文档头部保留元信息（版本、状态、最后更新、依据），修改时同步更新。
5. 文档与代码之间、文档彼此之间出现矛盾时按缺陷处理，随相关 PR 一起修正。

## 协作流程

1. 从最新的 `main` 创建短生命周期分支。
2. 只提交 `Assets`、`Packages`、`ProjectSettings`、工具脚本和文档等源文件。
3. 通过 Pull Request 合并，至少经过一名其他成员审查并确认验证结果。
4. 不直接向 `main` 推送，不使用强推覆盖共享分支历史。

分支命名示例：

```text
feature/battle-formation-command
fix/formation-selection
art/character-animation
tools/build-pipeline
docs/github-workflow
```

详细规则见 [CONTRIBUTING.md](CONTRIBUTING.md)，GitHub 仓库设置见 [docs/GITHUB_SETUP.zh-CN.md](docs/GITHUB_SETUP.zh-CN.md)。

## 版本库边界

必须提交：

- `Assets/**` 及其对应的 `.meta`
- `Packages/manifest.json`、`Packages/packages-lock.json`
- `ProjectSettings/**`
- 构建脚本、测试、CI 和协作文档

不得提交：

- `Library/`、`Temp/`、`Logs/`、`UserSettings/`
- IDE 生成的 `*.csproj`、`*.sln`、`.vs/`
- 构建目录和 Unity 崩溃报告
- 未配置 Git LFS 的大体积二进制资产
