import requests


def restore_abstract(abstract_inverted_index):
    """
    OpenAlex 的 abstract 默认是 inverted index 格式，
    这个函数把它还原成正常摘要文本。
    """
    if not abstract_inverted_index:
        return ""

    words = []

    for word, positions in abstract_inverted_index.items():
        for position in positions:
            words.append((position, word))

    words.sort(key=lambda x: x[0])

    return " ".join(word for _, word in words)


def fetch_papers(query, per_page=10):
    """
    从 OpenAlex 获取论文信息。
    query: 搜索关键词
    per_page: 每次返回多少篇论文
    """

    url = "https://api.openalex.org/works"

    params = {
        "search": query,
        "per-page": per_page,
        "sort": "publication_date:desc"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    papers = []

    for item in data.get("results", []):
        primary_location = item.get("primary_location") or {}
        source = primary_location.get("source") or {}

        paper = {
            "title": item.get("display_name", ""),
            "doi": item.get("doi", ""),
            "publication_year": item.get("publication_year", ""),
            "publication_date": item.get("publication_date", ""),
            "journal": source.get("display_name", ""),
            "is_oa": item.get("open_access", {}).get("is_oa", False),
            "oa_url": item.get("open_access", {}).get("oa_url", ""),
            "cited_by_count": item.get("cited_by_count", 0),
            "abstract": restore_abstract(item.get("abstract_inverted_index"))
        }

        papers.append(paper)

    return papers


if __name__ == "__main__":
    query = "deep carbon cycle mantle CO2 craton"

    papers = fetch_papers(query, per_page=5)

    for i, paper in enumerate(papers, start=1):
        print("=" * 80)
        print(f"{i}. {paper['title']}")
        print("Journal:", paper["journal"])
        print("Year:", paper["publication_year"])
        print("Date:", paper["publication_date"])
        print("DOI:", paper["doi"])
        print("Open Access:", paper["is_oa"])
        print("OA URL:", paper["oa_url"])
        print("Cited by:", paper["cited_by_count"])
        print("Abstract:", paper["abstract"][:500])