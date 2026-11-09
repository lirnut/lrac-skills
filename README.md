# lrac-skills

个人维护的 agent skills 仓库。只收录自己编写、自己维护的 skill；第三方 skill 不进入本仓库，按各自来源单独安装。

## Skills

### academic-slides

用于从研究论文出发制作可追溯的学术幻灯片：论文选择、叙事结构、原图解释、`claim-sources.md` 证据审计、可编辑 Typst/Touying 幻灯片、中文逐页讲稿，以及渲染后的视觉检查。

- 入口：`skills/academic-slides/SKILL.md`
- 参考：`skills/academic-slides/references/`
- 工具：`skills/academic-slides/scripts/`
- 模板：`skills/academic-slides/assets/typst-template/`

## 使用

本机全局链接：

```sh
ln -sfn ~/Repos/lrac-skills/skills/academic-slides \
        ~/.agents/skills/academic-slides
```

某个项目只使用该 skill 时：

```sh
mkdir -p .agents/skills
ln -sfn ~/Repos/lrac-skills/skills/academic-slides \
        .agents/skills/academic-slides
```

更新：

```sh
cd ~/Repos/lrac-skills
git pull
```

软链接指向仓库工作树，拉取后无需重新复制。

## 目录结构

```text
lrac-skills/
├── README.md
├── .gitignore
└── skills/
    └── academic-slides/
        ├── SKILL.md
        ├── references/
        ├── scripts/
        └── assets/
```

新增自己的 skill 时，在 `skills/` 下建立独立目录，并以 `SKILL.md` 作为入口；不要把 skill 嵌套成独立 Git 仓库。

## 运行依赖

这些是 `academic-slides` 的运行环境依赖，不是 skill 之间的依赖：

- Typst 0.15.0
- Python 3.10+
- Python 包：`pymupdf`、`pillow`
- Typst 包：`@preview/sci-brain-slides:0.1.0`（含 Touying 0.7.4）
- 字体：Noto Sans CJK SC、New Computer Modern Math

构建命令示例：

```sh
uv run --with typst==0.15.0 --with pymupdf==2.0 --with pillow==13.0.0 \
  python skills/academic-slides/scripts/build.py <deck-dir>
```

## 维护约定

- `SKILL.md` 的 `name` 与目录名一致。
- 每个 skill 自包含；需要共享代码时再抽到独立目录，不建立隐式跨 skill 依赖。
- 不提交生成物、缓存、虚拟环境或私密数据。
- 第三方 skill 保持独立安装；如需修改第三方 skill，另建 fork 仓库，不混入本仓库。
- 提交和远程仓库由仓库所有者维护。

