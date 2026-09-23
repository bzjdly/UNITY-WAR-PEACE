# 协作规范

## 分支与合并

- `main` 是始终可拉取、可打开、可构建的稳定分支。
- 工作分支从最新 `main` 创建，完成后通过 PR 合并。
- 分支名使用小写英文和短横线，推荐 `feature/`、`fix/`、`art/`、`tools/`、`docs/` 前缀。
- 默认使用 Squash Merge，保持 `main` 历史清晰。
- 合并后删除远程工作分支。
- 禁止向共享分支强推；需要同步时优先使用 `git pull --rebase` 或普通 merge。

## 提交信息

提交信息使用简短英文，建议采用 Conventional Commits：

```text
feat(network): add session discovery
fix(player): correct spawn position
art(character): import soldier animations
chore(ci): add Unity repository checks
```

一个提交只处理一个清晰目的，不混入无关格式化或资源重导入。

## Pull Request

每个 PR 至少包含：

- 关联的 Issue 或明确目标
- 改动范围和实现方式
- 本地验证步骤与结果
- 场景、Prefab、ScriptableObject 或内容数据的影响说明
- 无法验证或仍需人工检查的事项

至少一名其他成员完成审查后才能合并。涉及存档格式、内容 ID 或公共接口的改动必须由对应模块负责人审查。

## Unity 资源规则

- 所有位于 `Assets/**` 的资源都必须提交对应的 `.meta` 文件。
- 不要手写或批量生成 `.meta`；让 Unity 创建并提交稳定的 GUID。
- 场景和 Prefab 尽量拆小，减少多人同时编辑同一文件。
- 开始编辑共享场景前，在团队频道明确占用，完成并推送后释放。
- 优先在 Prefab Mode 中修改 Prefab，避免在同一场景中长时间并行编辑。
- 合并 Scene 或 Prefab 前，先确认本地已安装 Unity SmartMerge，并执行 `.\Tools\Git\Setup-Git.ps1`。
- 对自动合并结果必须回到 Unity 中逐项检查，不能只以 Git 无冲突为完成标准。

## Git LFS

首次使用仓库时执行：

```powershell
git lfs install
```

图片、音频、视频、模型、字体、压缩包和原生插件按根目录 `.gitattributes` 中的规则进入 Git LFS。

如果文件已经误提交为普通 Git 对象，应在新分支中执行：

```powershell
git lfs migrate import --include="Assets/**/*.fbx,Assets/**/*.png,Assets/**/*.wav"
```

迁移会改写历史。执行前必须通知全部协作者，并使用专门分支审查；不要在共享 `main` 上直接操作。

## 禁止提交

```text
Library/  Temp/  Logs/  UserSettings/  Build/  Builds/
.vs/  .idea/  *.csproj  *.sln  *.user  *.apk  *.aab
```

提交前至少确认：

```powershell
git status --short
git diff --cached --stat
python Tools/ci/check_unity_repo.py
```

## 发布

- 使用 `v<major>.<minor>.<patch>` 标签标记可发布版本。
- Release 中记录目标平台、构建编号、已知问题和升级注意事项。
- 只有通过测试的 `main` 提交可以打正式发布标签。
