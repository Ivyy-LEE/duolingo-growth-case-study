# Duolingo 增长与营销运营分析

**项目定位：** 增长运营 / 用户运营 / 产品运营 / 综合运营

随着 Duolingo 用户规模扩大，用户活跃度和商业化表现是否也同步提升？本项目通过 12 个季度的公开数据，对用户增长、活跃表现与商业化增长进行拆解，并将分析结果转化为运营关注重点。

项目工作：明确业务问题，统一指标口径，核对公开数据与计算结果，完成两页 Tableau Dashboard，并将分析发现转化为运营关注重点。

[中文作品页](https://ivyy-lee.github.io/duolingo-growth-case-study/) · [English](https://ivyy-lee.github.io/duolingo-growth-case-study/en/) · [中文 PDF](case_study/Duolingo_Growth_Operations_Case_Study_CN.pdf) · [英文 PDF](case_study/Duolingo_Growth_Operations_Case_Study_EN.pdf)

## 业务问题

仅看用户规模并不能完整判断增长质量。本项目进一步结合 DAU、付费订阅用户和收入表现，观察用户规模扩张是否同时带来了更高的活跃度和更强的商业化表现。

1. 2023 Q1–2025 Q4 期间，用户规模、活跃度、付费订阅和收入分别发生了怎样的变化？
2. DAU、付费订阅用户和收入的增长速度是否高于 MAU？
3. 2026 年初的竞品网站与社媒快照能提供哪些竞争背景？
4. 基于公开数据，增长与运营团队下一步最值得关注和验证的问题是什么？

## 数据范围

- **分析时点：** 2026 年 3 月
- **经营数据范围：** 2023 Q1–2025 Q4 · 共 12 个季度
- **竞品网站数据：** 2026 年 2 月快照
- **竞品社媒数据：** 2026 年 3 月快照

- 分析 2023 Q1–2025 Q4 共 12 个季度的 Duolingo 官方经营数据，来源包括 Investor Relations 和 SEC 披露。
- 对比 MAU、DAU、DAU/MAU、付费订阅用户和季度收入，并计算 QoQ、YoY 和以 2023 Q1 = 100 为基期的增长指数。
- 竞品网站数据为 2026 年 2 月快照，社媒数据为 2026 年 3 月快照，仅用于补充竞争背景。
- 使用 SQL 编写核心指标和增速计算逻辑，Python 用于数据质量检查与结果交叉验证，最终通过 Tableau 展示分析结果。

完整来源见[来源清单](docs/source_manifest.csv)，指标定义见[数据字典](docs/data_dictionary.md)。

## 最终 Tableau Dashboard

中英文案例共用以下两页最终英文 Tableau Dashboard。点击图片可查看完整尺寸。

[查看 Tableau Page 1](https://public.tableau.com/views/Duolingo_Growth_Marketing_Analytics/P1_Growth_Monetisation_Overview?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) · [查看 Tableau Page 2](https://public.tableau.com/views/Duolingo_Growth_Marketing_Analytics/P2_Growth_Diagnostics_Strategic_Context?:showVizHome=no) · [下载最终 Tableau 工作簿](dashboard/final/Duolingo_Growth_Marketing_Analytics.twbx)

链接统一维护于[链接记录](docs/portfolio_links.json)。最终 Dashboard 图片和工作簿保持不变。

### Page 1：用户规模、活跃度与商业化概览

![Tableau Page 1：用户规模、活跃度与商业化概览](dashboard/final/tableau_page1.png)

Page 1：用户规模、活跃度与商业化趋势。

### Page 2：增长诊断与竞争背景

![Tableau Page 2：增长诊断与竞争背景](dashboard/final/tableau_page2.png)

Page 2：增长差异、历史竞品背景与运营重点。

Page 2 保留 Q4 2025 增速差卡片、Indexed Growth Comparison、Engagement Growth Gap、Monetisation Growth Gaps、分别展示的网站流量（2026 年 2 月）和社媒受众（2026 年 3 月）快照，以及 Operational Priorities。

## 关键发现

- 2023 Q1 至 2025 Q4，MAU 增长 83%，DAU 增长 160%。同期 DAU/MAU 从 28.0% 提升至 39.6%，增加 11.6 个百分点，说明日活用户相对于月活用户的占比持续提高，整体活跃强度增强。

- 同期付费订阅用户增长 154%，季度收入增长 145%，增速均明显高于 MAU。公开数据表明商业化增长快于用户规模扩张，但无法据此判断具体是转化率、定价还是其他因素推动。

- 到 2025 Q4，MAU 同比增速已放缓至 14%，但 DAU、付费订阅用户和季度收入仍分别同比增长 30%、28% 和 35%。用户规模增速放缓的同时，活跃和商业化仍保持更快增长。

- 2026 年 2–3 月的历史快照显示，在 Duolingo、Babbel 和 Busuu 三个对比品牌中，Duolingo 的网站流量和社媒受众规模明显领先。由于缺少原始带日期截图，这些历史数值目前无法独立复核，因此仅作为竞争背景参考，不用于判断市场份额或长期竞争趋势。

网站快照中保留的访问量为：Duolingo 50.1M、Babbel 3.9M、Busuu 2.9M；Duolingo 在三个观察社媒平台的受众规模也均领先。这些数据仅用于竞争背景参考。

竞品网站与社媒数据来自原课程项目中记录的历史快照。由于原始带日期截图和部分账户链接未保留，目前无法独立复核其准确采集时间，因此这些数据仅用于补充竞争背景，不用于推断市场份额、转化率、留存或长期趋势。

## 运营重点

以下方向基于公开数据提出，仍需结合内部用户数据和实际测试进一步验证。本项目不声称相关策略已经实施或产生业务效果。

### 1. 关注活跃增长质量

进一步分析 DAU 增速高于 MAU 的原因，并持续观察 DAU/MAU 的提升是否能够维持，避免只用用户规模判断增长质量。

### 2. 强化会员价值沟通

测试更清晰的会员价值表达和更有针对性的试用策略，同时避免仅凭收入增速推断转化效率已经提升。

### 3. 兼顾增长与用户自主性

在推动活跃和商业化增长的同时，保留由用户自主调整的互动设置，并持续观察用户对相关机制的反馈。

本项目将公开数据中的增长变化转化为运营关注重点与验证方向。后续行动仍需结合内部数据和实际测试，并关注免费用户体验与学习体验。

## 分析局限

- 公开汇总数据无法支持同期群留存（cohort retention）或真实免费到付费转化漏斗分析。
- 竞品网站与社媒数据为历史单点快照，且缺少原始带日期截图，因此仅用于竞争背景参考。
- DAU/MAU 反映整体活跃强度，不等同于留存率。
- 仅凭付费订阅用户和收入增长，无法区分转化率、定价或其他因素各自的影响。
- 本项目识别的是描述性关系，不进行因果推断，也不声称运营建议已产生实际业务效果。

MAU、DAU 采用 Duolingo 自有的分析定义和估算口径，本项目未对用户人数进行独立测量。

## 方法与指标口径

- 使用 Duolingo 官方披露的 12 个季度、6 项经营指标，逐项记录数据来源与指标定义。
- 比较期间增长、QoQ、YoY、DAU/MAU 和增长指数；增速差用百分点表示。
- 通过 SQL 计算逻辑与 Python 结果交叉核对 16 个衍生字段，缺少前期数据的比较保留为空值。
- 两页已完成并发布的英文 Tableau Dashboard 为最终交互式展示，中英文案例共用同一组 Dashboard。

增长率根据公开披露的数值计算，并按展示需要四舍五入。MAU、DAU 为季度平均人数，付费订阅用户为期末人数，收入为当季金额。披露数值本身已做过舍入，因此计算增速可能与公司使用未舍入数据公布的增速略有差异。

DAU/MAU 是季度平均 DAU 与季度平均 MAU 的比值，反映整体活跃强度，不等同于留存率，也不能代表某个用户每日使用的概率。增速差用百分点表示，增长指数以 2023 Q1 = 100 为基期。

### 计算与工具说明

SQL 逻辑已通过 SQLite 兼容环境进行结果核对；原生 MySQL 环境未单独执行验证。原始数据、处理后 CSV、指标定义和已确认的分析结论均保持不变。

完整口径与计算说明见[方法说明](docs/methodology.md)；Tableau 文件说明见[交付状态](TABLEAU_HANDOFF.md)和[工作簿维护指南](docs/tableau_build_guide.md)。

## 项目资料

- 中文案例：[HTML](case_study/case_study_cn.html) / [PDF](case_study/Duolingo_Growth_Operations_Case_Study_CN.pdf) / [可编辑 PPTX](case_study/Duolingo_Growth_Operations_Case_Study_CN.pptx)
- 英文案例：[HTML](case_study/case_study_en.html) / [PDF](case_study/Duolingo_Growth_Operations_Case_Study_EN.pdf) / [可编辑 PPTX](case_study/Duolingo_Growth_Operations_Case_Study_EN.pptx)
- [英文 README](README.md)、[方法说明](docs/methodology.md)、[数据字典](docs/data_dictionary.md)、[来源清单](docs/source_manifest.csv)
- [独立审查记录](REVIEW_REPORT.md)、[历史校验记录](FINAL_QA.md)、[修改记录](CHANGELOG.md)、[Tableau 搭建指南](docs/tableau_build_guide.md)

原课程项目提供业务问题的背景。本项目的分析结论来自官方经营数据与明确标注使用边界的竞品历史快照。历史检查记录保留各自的检查时间和范围，不代表本次语言调整新增了数据或业务结果验证。

## 仓库结构

- `data/`：原始数据与处理后数据
- `sql/`：MySQL 8+ 分析脚本
- `notebooks/`：已执行的 Python 数据检查与分析 Notebook
- `dashboard/final/`：最终英文 Tableau Dashboard 图片与工作簿
- `docs/`：来源清单、数据字典、方法说明与历史记录
- `case_study/`：中英文 HTML、PDF 与可编辑 PPTX
- `src/copy_zh_cn.json`：中文文案共享源
- `src/`：数据、中文案例、网页与中文 README 的生成脚本

## 文案与文件维护

中文文案统一维护于 `src/copy_zh_cn.json`。修改文案后，在已配置演示文稿运行环境的项目目录中运行 `node src/build_case_studies.mjs`，更新中文七页 PDF、可编辑 PPTX 和网页；该脚本只处理中文版案例，保留英文案例、原始数据和最终 Tableau 素材。运行环境可通过 `CODEX_RUNTIME_DIR`、`CODEX_RUNTIME_NODE_MODULES`、`CODEX_RUNTIME_PYTHON`、`CODEX_PRESENTATION_SKILL` 等环境变量指定。导出后仍需逐页检查中文排版和可点击链接。

`python src/build_public_pages.py` 根据共享中文文案生成中文首页及相关中文 HTML，并维护 `/en/` 英文入口。`python src/build_chinese_readme.py` 根据同一份中文文案和已批准的 Tableau 链接重新生成本文件。维护时应保持网页、PDF、PPTX 和中文 README 的核心措辞一致。

`src/build_project.py` 用于原有数据检查、Notebook 和早期静态原型的生成。安装 `requirements.txt` 后可用 `python src/build_project.py --check-only` 进行只读数据与 SQL 结果检查；中文文案更新本身不需要重建这些原型。原生 MySQL 环境的验证范围仍以方法说明为准。

来源：Duolingo Investor Relations / SEC。指标定义与完整来源见方法说明、来源清单及演示文稿备注。
