# GitHub 项目管理设置

## 当前远程

```text
origin  https://github.com/bzjdly/UNITY-WAR-PEACE.git
```

仓库使用 HTTPS；首次推送时由 Git Credential Manager 完成 GitHub 登录并缓存凭据。上表是规范的上游地址：如果本地是通过镜像克隆的，先用 `git remote -v` 核对，必要时执行 `git remote set-url origin <规范地址>` 改回来。

如果以后配置 SSH，可切换为：

```powershell
git remote set-url origin git@github.com:bzjdly/UNITY-WAR-PEACE.git
```

部分网络拒绝 22 端口时，可使用 GitHub 的 443 端口：

```text
ssh://git@ssh.github.com:443/bzjdly/UNITY-WAR-PEACE.git
```

## 分支保护

在 GitHub 仓库的 `Settings > Rules > Rulesets` 中为 `main` 建立保护规则：

- 禁止直接推送和删除分支。
- 所有改动必须经过 Pull Request。
- 至少需要 1 个批准。
- 新提交后自动取消过期批准。
- 所有 review conversation 必须解决。
- 必须通过 `Repository checks` 状态检查。
- 优先启用 Squash Merge，并自动删除已合并分支。

团队扩大后，可以提高批准人数或为网络、构建、核心系统目录指定额外审查。

## 仓库权限

推荐角色：

- Maintainer：项目负责人、构建负责人。
- Write：正式开发成员。
- Triage：负责整理和分流 Issue，但不能直接改主干。
- Read：外部测试和使用者。

不要在仓库内共享 Unity License、GitHub Token、私钥或其他凭据。CI 凭据统一放入 `Settings > Secrets and variables > Actions`。

## Issue 和 Project

建议建立 GitHub Project，使用以下状态：

```text
Backlog -> Ready -> In Progress -> In Review -> QA -> Done
```

建议标签：

| 标签 | 用途 |
| --- | --- |
| `bug` | 可复现的缺陷（“缺陷报告”模板自动应用） |
| `enhancement` | 功能建议（“功能建议”模板自动应用） |
| `task` | 开发、美术、测试或工具任务（“开发任务”模板自动应用） |
| `triage` | 新建 Issue 待分流，由负责分流的人在确认内容后移除（“缺陷报告”和“功能建议”模板自动应用） |
| `gameplay` | 核心玩法 |
| `art` | 美术和动画 |
| `network` | 联机和同步。当前设计为纯单机，此标签暂时保留备用 |
| `blocked` | 有明确外部阻塞 |
| `good first issue` | 适合新成员 |
| `priority:high` | 高优先级 |

Issue 模板会自动应用上表中的标签，请先在仓库 `Settings > Labels` 中确认存在同名标签，否则模板不会带上它们。

Issue 标题保持可搜索，PR 通过 `Closes #123` 自动关联。

## Code Owners

确定 GitHub 用户名或团队后创建 `.github/CODEOWNERS`。示例：

```text
*                                @bzjdly
/Assets/Scripts/Modules/Battle/  @battle-owner
/Assets/Scripts/Core/            @architecture-owner
/ProjectSettings/                @build-owner
/.github/                        @project-owner
```

必须先保证用户名和团队名真实存在，否则 GitHub 不会建立有效审查规则。

## CI

当前 `Repository checks` 检查：

- Unity 生成的目录没有被提交：`Library`、`Temp`、`Logs`、`UserSettings`、`MemoryCaptures`、`Recordings`、`Build`、`Builds`、`obj`、`.gradle`、`.vs`、`.idea`。
- `Assets/**` 与 `.meta` 文件一一对应。
- 二进制扩展名已配置 Git LFS（清单与根目录 `.gitattributes` 一致）。
- 超过 5 MB 的普通 Git 文件已由 LFS 管理。
- 必需的项目文件存在：`.gitattributes`、`.gitignore`、`Packages/manifest.json`、`Packages/packages-lock.json`、`ProjectSettings/ProjectVersion.txt`。
- 文本文件中没有未解决的合并冲突标记。当前覆盖 `.asset`、`.asmdef`、`.asmref`、`.cs`、`.json`、`.md`、`.meta`、`.txt`、`.unity`、`.yaml`、`.yml`；`Tools` 下的 `.py`、`.ps1`、`.sh` 脚本不在覆盖范围内。

后续启用 Unity 编译和测试 CI 前，需要准备：

1. 可用的 Runner，并通过 Unity Hub 安装 `ProjectSettings/ProjectVersion.txt` 记录的版本（当前为 `2022.3.57f1c2`，中国版）。GameCI 官方镜像通常只提供国际版，中国版建议自建 Runner 或自备镜像。
2. Unity License 对应的 GitHub Actions Secrets。
3. 项目的 EditMode、PlayMode 和多端构建检查命令。

不要在没有验证 Runner 与许可证的情况下把 Unity CI 设为 `main` 的必过检查。

## 发布管理

- 使用 GitHub Releases 记录版本、构建号、平台、变更和已知问题。
- 正式标签格式为 `v0.1.0`、`v0.2.0` 等。
- 大型美术包或试玩构建使用 GitHub Release Assets；不要把生成安装包提交到 Git 历史。
