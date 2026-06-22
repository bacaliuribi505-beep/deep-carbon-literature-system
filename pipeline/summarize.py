import os
import re
from datetime import datetime


def safe_filename(text, max_length=80):
    """
    把论文标题转换成安全的文件名，避免 Windows 文件名非法字符。
    """
    text = text.strip()
    text = re.sub(r'[\\/:*?"<>|]', "", text)
    text = re.sub(r"\s+", "_", text)
    return text[:max_length]


def write_obsidian_note(paper, output_dir="output/obsidian_notes"):
    """
    把单篇论文信息写成 Obsidian Markdown 笔记。
    """

    os.makedirs(output_dir, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")

    title = paper.get("title", "Untitled Paper")
    filename_title = safe_filename(title)

    filename = f"{today}_{filename_title}.md"
    filepath = os.path.join(output_dir, filename)

    journal = paper.get("journal", "")
    year = paper.get("publication_year", "")
    date = paper.get("publication_date", "")
    doi = paper.get("doi", "")
    is_oa = paper.get("is_oa", False)
    oa_url = paper.get("oa_url", "")
    cited_by_count = paper.get("cited_by_count", 0)
    abstract = paper.get("abstract", "")
    matched_keywords = paper.get("matched_keywords", [])
    relevance_score = paper.get("relevance_score", "")

    content = f"""# {title}

## 基本信息

- 期刊：{journal}
- 发表年份：{year}
- 发表日期：{date}
- DOI：{doi}
- 是否开放获取：{is_oa}
- OA 链接：{oa_url}
- 引用次数：{cited_by_count}

## 自动筛选信息

- 相关性分数：{relevance_score}
- 匹配关键词：{", ".join(matched_keywords)}

## 摘要

{abstract}

## 与深部碳循环 / 碳通量的关系

- 待人工阅读后补充。
- 可重点关注是否涉及：
  - 深部碳循环
  - 克拉通岩石圈
  - 富 CO2 岩浆
  - 碳酸岩 / 碱性岩
  - 俯冲碳循环
  - 地幔挥发分释放

## 可能提取的数据

- 岩石类型：
- 构造背景：
- 年代：
- 主量元素：
- 微量元素：
- 同位素：
- CO2 / 挥发分数据：
- P-T 条件：
- 岩石圈厚度：

## 机器学习用途判断

- 是否可用于训练集：待判断
- 可能标签：
  - craton carbon flux
  - mantle carbon
  - carbonatite
  - alkaline magma
  - subduction carbon
  - volatile cycling

## 我的笔记

-

---

## 标签

#literature #deep-carbon-cycle #carbon-flux #obsidian
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


if __name__ == "__main__":
    test_paper = {
        "title": "Mantle carbon flux beneath cratons",
        "journal": "Nature Geoscience",
        "publication_year": 2026,
        "publication_date": "2026-06-21",
        "doi": "https://doi.org/10.xxxx/example",
        "is_oa": True,
        "oa_url": "https://example.com/paper.pdf",
        "cited_by_count": 12,
        "abstract": "This study investigates deep carbon cycle and CO2-rich magmatism beneath cratons.",
        "matched_keywords": ["deep carbon cycle", "carbon flux", "craton carbon"],
        "relevance_score": 3
    }

    path = write_obsidian_note(test_paper)
    print("Obsidian note saved:", path)