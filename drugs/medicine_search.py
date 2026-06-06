from app.resources import google_search

def drug_search(query: str):
    """Search for drug information."""
    trusted_query = f"""
    site:mayoclinic.org OR
    site:nlm.nih.gov OR
    site:nhs.uk/medicines OR
    site:open.fda.gov/apis/drug OR
    site:dailymed.nlm.nih.gov
    {query}
    """
    search = google_search()
    return search.run(trusted_query)