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
    ├── academic-slides/
    │   ├── SKILL.md
    │   ├── references/
    │   ├── scripts/
    │   └── assets/
    └── skill-update/              # 分组目录，不包含 SKILL.md
        ├── skill-update/          # 手动迭代和待审分支管理
        ├── skill-expcap/          # 跨项目经验采集
        └── logs/                 # 本地经验，不进入 Git，首次采集时创建
```

## Skills

### academic-slides

基于typst来制作学术slide，现在包括单篇论文介绍、多篇论文介绍、领域综述三个种slide，后续将进一步扩展。

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

- “用 skill-update 根据最近经验更新 academic-slides。”
- “用 skill-update 继续推进 academic-slides 的待审核分支。”

`skill-creator` 是修改阶段的依赖，不随本仓库自动安装；缺失时会停止并提示。
`logs/` 被 Git 忽略，不随安装或更新分发。更新仓库代码前请保留 `.gitignore` 中的日志规则。
