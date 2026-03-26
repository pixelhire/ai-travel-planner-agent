from ddgs import DDGS


def find_weather(destination:str):

    query = f"Find the weather details in {destination}"

    results = []

    with DDGS() as ddgs:
        search_results = ddgs.text(query, max_results = 3)

        for result in search_results:
            results.append({
                "name":result["title"],
                "link":result["href"],
                "description":result["body"],
            })

    return results