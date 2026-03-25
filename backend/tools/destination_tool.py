from ddgs import DDGS


def search_destination(destination: str):

    query = f"top tourist attractions in {destination}"

    results = []

    with DDGS() as ddgs:

        search_results = ddgs.text(query, max_results=5)

        for result in search_results:

            results.append({
                "title": result.get("title"),
                "link": result.get("href"),
                "snippet": result.get("body")
            })

    return results