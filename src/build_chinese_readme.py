"""Generate README_CN.md from the curated Chinese copy and approved link record.

This script updates the Chinese README only. It does not calculate metrics or
modify data, dashboards, English deliverables, or any other case-study output.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PUBLIC_BASE = "https://ivyy-lee.github.io/duolingo-growth-case-study/"


def build_readme(copy: dict, links: dict) -> str:
    questions = "\n".join(f"{i}. {text}" for i, text in enumerate(copy["qs"], 1))
    scope = "\n".join(f"- {text}" for text in copy["scope"])
    findings = "\n\n".join(f"- {text}" for text in copy["findings"])
    priorities = "\n\n".join(
        f"### {i}. {heading}\n\n{body}"
        for i, (heading, body) in enumerate(copy["recs"], 1)
    )
    methods = "\n".join(f"- {text}" for text in copy["methods"])
    limits = "\n".join(f"- {text}" for text in copy["limits"])
    labels = copy["labels"]
    page1 = links["tableau_public_url"]
    page2 = links["tableau_public_page2_url"]
    image1 = links["final_dashboard_images"]["page1"]
    image2 = links["final_dashboard_images"]["page2"]
    workbook = links["tableau_workbook"]

    return f"""# {copy['title']}

**项目定位：** {copy['roleLine']}

{copy['cover']}

{copy['role']}

[中文作品页]({PUBLIC_BASE}) · [English]({PUBLIC_BASE}en/) · [中文 PDF](case_study/Duolingo_Growth_Operations_Case_Study_CN.pdf) · [英文 PDF](case_study/Duolingo_Growth_Operations_Case_Study_EN.pdf)

## 业务问题

{copy['context']}

{questions}

## 数据范围

- **分析时点：** {labels['analysisAsOfValue']}
- **经营数据范围：** {labels['corporatePerformanceValue']}
- **竞品网站数据：** 2026 年 2 月快照
- **竞品社媒数据：** 2026 年 3 月快照

{scope}

完整来源见[来源清单](docs/source_manifest.csv)，指标定义见[数据字典](docs/data_dictionary.md)。

## 最终 Tableau Dashboard

{labels['dashboardNote']}

[查看 Tableau Page 1]({page1}) · [查看 Tableau Page 2]({page2}) · [下载最终 Tableau 工作簿]({workbook})

链接统一维护于[链接记录](docs/portfolio_links.json)。最终 Dashboard 图片和工作簿保持不变。

### {labels['dashboardPage1Title']}

![{labels['dashboardPage1Alt']}]({image1})

{labels['dashboardPage1Caption']}

### {labels['dashboardPage2Title']}

![{labels['dashboardPage2Alt']}]({image2})

{labels['dashboardPage2Caption']}

Page 2 保留 Q4 2025 增速差卡片、Indexed Growth Comparison、Engagement Growth Gap、Monetisation Growth Gaps、分别展示的网站流量（2026 年 2 月）和社媒受众（2026 年 3 月）快照，以及 Operational Priorities。

## 关键发现

{findings}

网站快照中保留的访问量为：Duolingo 50.1M、Babbel 3.9M、Busuu 2.9M；Duolingo 在三个观察社媒平台的受众规模也均领先。这些数据仅用于竞争背景参考。

{copy['competitorCaveat']}

## 运营重点

{copy['operationsIntro']}

{priorities}

{copy['positioning']}

## 分析局限

{limits}

{copy['companyDefinition']}

## 方法与指标口径

{methods}

{copy['rounding']}

{copy['definitions']}

### 计算与工具说明

{copy['tech']}

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

{copy['footer']}
"""


def main() -> None:
    copy = json.loads((ROOT / "src/copy_zh_cn.json").read_text(encoding="utf-8"))
    links = json.loads((ROOT / "docs/portfolio_links.json").read_text(encoding="utf-8"))
    output = ROOT / "README_CN.md"
    output.write_text(build_readme(copy, links), encoding="utf-8")
    print("README_CN.md regenerated from src/copy_zh_cn.json.")


if __name__ == "__main__":
    main()
