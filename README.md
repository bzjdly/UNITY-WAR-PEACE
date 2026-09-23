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

## 协作流程

1. 从最新的 `main` 创建短生命周期分支。
2. 只提交 `Assets`、`Packages`、`ProjectSettings`、工具脚本和文档等源文件。
3. 通过 Pull Request 合并，至少经过一名其他成员审查并确认验证结果。
4. 不直接向 `main` 推送，不使用强推覆盖共享分支历史。

分支命名示例：

```text
feature/network-session
fix/sync-transform
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
