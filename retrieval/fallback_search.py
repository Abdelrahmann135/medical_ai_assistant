from app.resources import google_search

def web_search(query: str):
    """Search inside a specific website."""
    trusted_query = f"""
    site:who.int OR
    site:cdc.gov OR
    site:nih.gov OR
    site:mayoclinic.org OR
    site:pubmed.ncbi.nlm.nih.gov
    {query}
    """
    search = google_search()
    return search.run(trusted_query)