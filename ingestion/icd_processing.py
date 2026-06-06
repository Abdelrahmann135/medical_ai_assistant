import re

def process_icd_data(disease):
    """Processes the ICD data to create a list of dictionaries containing the chapter, domain, disease, and sub-code."""
    disease = disease[disease['definition'].duplicated() == False]
    disease.dropna(subset=['definition'], inplace=True)
    disease = disease[disease['sub-code'].str.contains(r'\.')]
    disease = disease[~disease["definition"].str.contains("Other|Unspecified|not elsewhere", case=False)]

    disease_dic = []
    for index, i in disease.iterrows():
        d = {
        "Chapter": re.search(r"\n(.*)\r", i['chapter']).group(1) if re.search(r"\n(.*)\r", i['chapter']) else None,
        "Domain": re.sub(r'[\r\n]+|\s*\(.*?\)', '', i['domain']).strip(),
        "Disease": i['definition'],
        "Sub-code": i['sub-code'],
        }
        disease_dic.append(d)
    return disease_dic