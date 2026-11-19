# main.py
import uuid

from dotenv import load_dotenv

load_dotenv()

from app.graph.builder import build_graph

def main(query: str ):
    run_id = f"run_{uuid.uuid4().hex[:8]}"

    graph = build_graph()
    final_state = graph.invoke({
        "run_id": run_id,
        "query": query,
        "keywords": [],
        "search_results": [],
        "draft": "",
    })

    print(f"\nrun_id: {run_id}")
    print(f"search_results: {len(final_state['search_results'])}")
    print(f"draft_chars:    {len(final_state['draft'])}")
    print(f"report:         artifacts/reports/{run_id}.md")


if __name__ == "__main__":
    query=input("请输入要研究的内容: ")
    main(query)