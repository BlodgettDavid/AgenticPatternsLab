def search_tool(query: str) -> str:
    q = query.lower()

    if "france" in q and "capital" in q:
        return "Paris"

    if "paris" in q and "population" in q:
        return "2 million"

    if "2+2" in q:
        return "4"

    return "No results found"