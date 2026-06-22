from pipeline.fetch_papers import fetch_papers
from pipeline.filter_papers import filter_papers
from pipeline.summarize import write_obsidian_note


def main():
    """
    主程序：
    1. 从 OpenAlex 抓取论文
    2. 根据关键词筛选深部碳循环相关论文
    3. 自动生成 Obsidian Markdown 笔记
    """

    query = "deep carbon cycle carbon flux mantle CO2 craton carbonatite"

    print("=" * 80)
    print("开始从 OpenAlex 抓取论文...")
    print("搜索关键词:", query)

    papers = fetch_papers(query, per_page=20)

    print(f"抓取完成，共获得 {len(papers)} 篇论文")

    print("=" * 80)
    print("开始筛选深部碳循环 / 碳通量相关论文...")

    filtered_papers = filter_papers(papers, min_score=1)

    print(f"筛选完成，保留 {len(filtered_papers)} 篇相关论文")

    if not filtered_papers:
        print("没有筛选到相关论文。可以尝试增加关键词或扩大搜索范围。")
        return

    print("=" * 80)
    print("开始生成 Obsidian 笔记...")

    for paper in filtered_papers:
        path = write_obsidian_note(paper)
        print("已生成:", path)

    print("=" * 80)
    print("全部完成！")
    print("请查看 output/obsidian_notes 文件夹。")


if __name__ == "__main__":
    main()