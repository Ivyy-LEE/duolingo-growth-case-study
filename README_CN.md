# Duolingo 增长与营销运营分析

**项目定位：** 增长运营 / 用户运营 / 产品运营 / 综合运营

本项目在原 Digital Marketing Strategy 课程中 Duolingo 案例的基础上，进一步补充数据分析层。重点不是展示复杂技术，而是回答一个增长运营问题：**在用户规模扩大的同时，Duolingo 的活跃质量和商业化表现是否也同步增强？**

[阅读案例](case_study/case_study_cn.html) · [PDF](case_study/Duolingo_Growth_Operations_Case_Study_CN.pdf) · [可编辑幻灯片](case_study/Duolingo_Growth_Operations_Case_Study_CN.pptx) · [English](README.md)

## 核心业务问题

1. 2023-2025 年，Duolingo 的用户规模、日常活跃、付费订阅用户和收入如何变化？
2. 活跃与商业化增速是否高于整体用户规模增速？
3. 2026 年 2-3 月的竞品数字表现快照能提供什么战略背景？
4. 对增长/运营团队而言，下一步最值得持续监控和补充分析的是什么？

## 数据范围

- **分析时点：** 2026 年 3 月
- **公司经营趋势：** 2023 Q1-2025 Q4，共 12 个季度
- **竞品网站数据：** 2026 年 2 月快照
- **社交媒体数据：** 2026 年 3 月快照

公司经营数据来自 Duolingo Investor Relations 与 SEC 官方披露；竞品快照保留从历史课程作业快照继承的数值。仓库中缺少原作业及带日期的截图，因此无法独立核实竞品快照的历史来源。完整来源见[来源清单](docs/source_manifest.csv)。

## 最终 Tableau Dashboard

本项目以已完成的两页英文 Tableau Dashboard 为最终可视化版本，中英文案例复用同一组图表。可打开 Tableau Public 的 [Page 1](https://public.tableau.com/views/Duolingo_Growth_Marketing_Analytics/P1_Growth_Monetisation_Overview?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) / [Page 2](https://public.tableau.com/views/Duolingo_Growth_Marketing_Analytics/P2_Growth_Diagnostics_Strategic_Context?:showVizHome=no)，或下载[最终原生工作簿](dashboard/final/Duolingo_Growth_Marketing_Analytics.twbx)。**2026 年 10 月 18 日**已在未登录状态下取得两页的公开图片导出；本次未测试浏览器中的交互标签页。链接统一维护于[链接记录](docs/portfolio_links.json)。

### Page 1 - 增长与商业化概览

![Dashboard Page 1](dashboard/final/tableau_page1.png)

### Page 2 - 增长质量诊断与战略背景

![Dashboard Page 2](dashboard/final/tableau_page2.png)

最终 Page 2 包含 Q4 2025 增速差卡片、**指数化增长比较（Indexed Growth Comparison）**、**活跃增速差（Engagement Growth Gap）**、**商业化增速差（Monetisation Growth Gaps）**、独立展示的 **网站流量（Website Traffic，2026 年 2 月）**与**社交媒体受众（Social Audience，2026 年 3 月）**背景快照，以及**运营优先事项（Operational Priorities）**。

## 关键业务洞察

- **活跃增长明显快于用户规模。** 2023 Q1 至 2025 Q4，MAU 增长 **83%**，DAU 增长 **160%**；DAU/MAU 从 **28.0% 提升至 39.6%，增加 11.6 个百分点**。
- **商业化扩张快于整体用户增长。** 同期付费订阅用户增长 **154%**，季度收入增长 **145%**，均明显高于 MAU 增速。
- **2025 年增长结构发生变化。** 到 Q4，MAU 同比增速放缓至 **14%**，但 DAU、付费用户和收入仍分别同比增长 **30%、28% 和 35%**。
- **所提供的 2026 年 2-3 月快照中，Duolingo 的数字触达领先。** 2 月网站访问量为 50.1M，Babbel 为 3.9M、Busuu 为 2.9M；Duolingo 在三个社媒平台上的规模也均领先。这些继承的数值仅用于单点背景，原始历史截图未经核实，不能据此判断市场份额、转化或留存。

## 运营含义

1. **保护活跃质量（Protect engagement quality）。** 调查 DAU 增长快于 MAU 的驱动因素，持续监控更高的活跃强度能否保持。
2. **强化会员价值沟通（Strengthen premium value communication）。** 测试更清晰的订阅价值沟通和定向试用机会；收入增长更快并不能证明转化改善。
3. **兼顾增长与用户自主控制（Balance growth with user control）。** 保留可配置的互动设置，并在活跃与商业化持续扩张时监控用户反应。

以上优先事项与最终 Tableau Dashboard 一致。拟议的运营复盘和实验需要获授权的内部证据及免费体验保护指标，不代表已确认产品存在缺陷，也不声称已产生实际业务收益。

## 局限

- 仅使用公开汇总数据，没有内部用户级数据。
- 无法进行真实 free-to-paid funnel、campaign ROI 或留存 cohort 分析。
- 竞品网站和社媒数据是继承的单点历史快照，原始带日期截图缺失。
- MAU/DAU 使用 Duolingo 自有分析系统定义和估算口径，并非第三方独立验证。
- 项目结论为描述性分析，不做因果推断。

## 方法与工具

- **SQL / Python：** 计算季度 KPI、同比/环比、指数化增长和增速差，并以独立计算核对结果；数据口径与分析结论保持冻结。
- **Tableau：** 以最终两页工作簿展示发现，详见[交付状态](TABLEAU_HANDOFF.md)和[工作簿维护指南](docs/tableau_build_guide.md)。
- **校验边界：** SQL 公式通过已说明的 SQLite 兼容适配执行，尚未验证原生 MySQL 执行；完整口径和检查见[方法说明](docs/methodology.md)。

本项目以公开证据支持运营判断，不虚构漏斗、投放指标或已落地的业务收益。

## 仓库结构

- `data/` 原始及处理后的数据
- `sql/` MySQL 8+ 分析脚本
- `notebooks/` 已执行的 Python 校验与分析 Notebook
- `dashboard/final/` 最终英文 Tableau Dashboard 图片
- 早期静态原型仅在工作仓库保留，最终交付 ZIP 不包含旧图
- `docs/` 来源清单、数据字典与方法说明
- `case_study/` 双语作品集案例文件

## 交付物与校验

- 英文案例：[HTML](case_study/case_study_en.html) / [PDF](case_study/Duolingo_Growth_Operations_Case_Study_EN.pdf) / [可编辑幻灯片](case_study/Duolingo_Growth_Operations_Case_Study_EN.pptx)
- 中文案例：[HTML](case_study/case_study_cn.html) / [PDF](case_study/Duolingo_Growth_Operations_Case_Study_CN.pdf) / [可编辑幻灯片](case_study/Duolingo_Growth_Operations_Case_Study_CN.pptx)
- [英文 README](README.md)、[方法说明](docs/methodology.md)、[数据字典](docs/data_dictionary.md)
- [独立审查](REVIEW_REPORT.md)、[最终校验](FINAL_QA.md)、[修改记录](CHANGELOG.md)、[Tableau 搭建指南](docs/tableau_build_guide.md)

原课程作业仅作为问题的背景。本仓库的结论来自官方公司数据与明确标注来源限制的竞品快照。

## 重建与维护

在隔离的 Python 环境中安装 `requirements.txt`，然后从项目目录运行 `python src/build_project.py`。该命令执行校验 Notebook 并重建旧版静态原型。已正确的处理后 CSV 按原字节保留；原始输入、SQL、来源文档及案例文字不会被覆盖。`--check-only` 用于只读数据与 SQL 校验；`--only dashboards` / `--only notebook` 用于单独刷新一类输出。需要中文字体；无法自动发现时可用 `--cn-font-path` 指定本地字体文件。

单独的 `src/build_case_studies.mjs` 使用 Codex 演示文稿运行环境与无界面渲染器，更新已有七页模板、对应 PDF 与 HTML。脚本说明了运行环境路径的覆盖方式。修改内容或图片后需检查导出页面。最终 Tableau 工作簿及其图片仍是展示依据。历史校验记录说明此前完成的检查；本次发布验证覆盖两页最终视图的未登录公开图片导出。
