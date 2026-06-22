def load_keywords(path="config/keywords.txt"):
    """
    从 config/keywords.txt 读取关键词
    """
    with open(path, "r", encoding="utf-8") as f:
        keywords = [line.strip().lower() for line in f if line.strip()]
    return keywords


def filter_papers(papers, keywords=None, min_score=1):
    """
    根据标题、摘要和期刊信息筛选论文。

    papers: 从 OpenAlex 抓取到的论文列表
    keywords: 关键词列表
    min_score: 最低匹配分数
    """

    if keywords is None:
        keywords = load_keywords()

    filtered = []

    for paper in papers:
        title = paper.get("title", "").lower()
        abstract = paper.get("abstract", "").lower()
        journal = paper.get("journal", "").lower()

        text = f"{title} {abstract} {journal}"

        matched_keywords = []
        score = 0

        for keyword in keywords:
            if keyword in text:
                matched_keywords.append(keyword)
                score += 1

        if score >= min_score:
            paper["matched_keywords"] = matched_keywords
            paper["relevance_score"] = score
            filtered.append(paper)

    filtered = sorted(
        filtered,
        key=lambda x: x.get("relevance_score", 0),
        reverse=True
    )

    return filtered


if __name__ == "__main__":
    test_papers = [
        {
            "title": "Mantle carbon flux beneath cratons",
            "abstract": "This study investigates deep carbon cycle and CO2-rich magmatism.",
            "journal": "Nature Geoscience"
        },
        {
            "title": "Zircon geochronology of granites",
            "abstract": "This paper focuses on crustal evolution.",
            "journal": "Lithos"
        }
    ]

    results = filter_papers(test_papers)

    for paper in results:
        print(paper["title"])
        print("Matched:", paper["matched_keywords"])
        print("Score:", paper["relevance_score"])