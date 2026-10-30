from ddgs import DDGS

def search_web(query):

    results = []

    with DDGS() as ddgs:

        data = ddgs.text(
            query,
            max_results=5
        )

        for item in data:

            results.append({
                "title": item.get("title", "Untitled"),
                "url": item.get("href", ""),
                "snippet": item.get("body", "")
            })

    return results