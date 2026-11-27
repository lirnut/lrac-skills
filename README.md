# lrac-skills

本项目维护个人化的skills，目的是让agent能够固定真实科研中的经验

## Fast Start
使用如下命令来进行部署:
```
npx skills add lirnut/lrac-skills
```

使用如下明来进行更新i:
```
npx skills update
```

## 目录结构

```text
lrac-skills/
├── README.md
├── .gitignore
└── skills/
    ├── slides/                    # 分组目录，不包含 SKILL.md
    │   ├── _shared/               # 通用规范、模板和工具的维护源
    │   ├── scripts/               # 资源同步与分发检查
    │   ├── slide-share/           # 单篇或多篇论文分享
    │   ├── slide-survey/          # 主题调研与路线比较
    │   └── slide-tech/            # 技术设计、实现与验证
    └── skill-update/              # 分组目录，不包含 SKILL.md
        ├── skill-update/          # 手动迭代和待审分支管理
        ├── skill-expcap/          # 跨项目经验采集
        └── logs/                 # 本地经验，不进入 Git，首次采集时创建
```

## Skills

### Slides

三种 Skill 使用相同的 Typst/Touying 模板、字体、引用、逐页讲稿和质量检查，
但按汇报目的采用不同的故事线和页面布局，不按论文数量判断类型：

| Skill | 用途 | 典型组织方式 |
|---|---|---|
| `slide-share` | 组会单篇或多篇论文分享 | 问题、方法、实验、结果、解释与局限 |
| `slide-survey` | 调研报告、领域概览、技术路线比较 | 范围、分类框架、代表路线、比较与综合判断 |
| `slide-tech` | 技术报告、架构讲解、算法实现 | 问题与约束、设计、实现、验证与权衡 |

默认英文观众页、中文逐页讲稿；用户要求可以覆盖。技术报告不强制要求论文，
必须区分设计设想、实际实现、测试通过和性能测量。

- “用 slide-share 准备这两篇论文的组会分享。”
- “用 slide-survey 做一份这个领域的调研汇报。”
- “用 slide-tech 解释这个系统的架构、关键实现和验证结果。”

各 Skill 的 `common/` 是随安装分发的完整资源副本，可以单独安装，不依赖其他 Skill。
修改共享规范、模板或工具时，只编辑 `skills/slides/_shared/`，然后运行：

```sh
python skills/slides/scripts/sync_common.py --write
python skills/slides/scripts/sync_common.py --check
python skills/slides/scripts/test_distribution.py
```

同步工具只更新清单管理的生成文件，发现用户改动、未知文件或软链接时拒绝覆盖。
构建回归测试使用 `common/references/typst-workflow.md` 中的依赖，运行对应
`common/scripts/self_test.py`，并在交付前实际检查渲染页面。
相同依赖环境下，可运行 `python skills/slides/scripts/type_smoke_test.py --output-dir <新目录>`
构建单篇分享、多篇分享、调研和技术报告的合成排版测试；它验证分发与排版，不验证真实报告内容。

原 `academic-slides` 已拆分为上述三个 Skill，不保留同名入口。
重新安装时可通过 `npx skills add lirnut/lrac-skills --skill slide-share slide-survey slide-tech`
选择新入口。不要假定 `npx skills update` 会自动删除旧名称；先检查执行器中的旧安装，
确认替代入口可用后再通过安装工具移除旧 Skill，不自动删除用户文件。
旧经验的 `academic-slides` 标签应按内容重新归入三种类型，不全部映射为论文分享。

### skill-expcap

在其他项目中完成一个有实质结果的阶段后，自动检查并收集可跨项目复用的通用经验，写入中央开发仓库
`~/Repos/lrac-skills/skills/skill-update/logs/`，不写入安装副本。
需要 Python 3.9+、Git 和 Unix 文件锁（Linux/macOS），不依赖特定 Agent harness。

- 单次记录：“用 skill-expcap 记录刚才这次修复的经验。”
- 自动阶段采集：“使用 skill-expcap，在项目完成阶段后自动记录通用经验。”

加载后无需逐次提醒：Agent 在子任务验收、修复验证或交付物检查完成时判断阶段结束，
并自动筛选通用经验；没有合格经验则不写入，不记录项目进度或专属偏好。
这不是后台定时器，也不保证未加载或跨会话时自动触发；仓库不存在、只读模式或权限不允许时跳过。

### skill-update

手动整理本地经验或直接反馈，加载已安装的 `skill-creator` 修改并验证 Skill，
在 `feat/<skill-id>-skill` 上创建本地提交。未合并分支持续复用，不使用 worktree，
不自动推送或合并。

- “用 skill-update 根据最近经验更新 slide-share。”
- “用 skill-update 继续推进 slide-share 的待审核分支。”

`skill-creator` 是修改阶段的依赖，不随本仓库自动安装；缺失时会停止并提示。
`logs/` 被 Git 忽略，不随安装或更新分发。更新仓库代码前请保留 `.gitignore` 中的日志规则。
