from selenium import webdriver
from selenium.webdriver.common.by import By
import time

## CDC Scraping Function
def scrape_cdc(disease_dic):
    """Scrapes the CDC website for articles related to the diseases in the ICD."""
    driver = webdriver.Chrome()

    for disease in disease_dic:        
            driver.get("https://search.cdc.gov/search/")
            time.sleep(2)
            search = driver.find_element(By.XPATH, '/html/body/main/div/div/div/div/div[1]/div[1]/div[1]/div[1]/div/input[1]')
            button = driver.find_element(By.CLASS_NAME, 'cdc-fa-magnifying-glass')
            search.send_keys(disease['Disease'])
            button.click()
            time.sleep(2)
            res = driver.find_elements(By.CLASS_NAME, 'result')
            for el in res:
                a_tag = el.find_element(By.TAG_NAME, "a")
                if a_tag.get_attribute("href") and "https://wwwnc.cdc.gov/eid/article/" in a_tag.get_attribute("href"):
                    link = a_tag.get_attribute("href")
                    disease["Result Link"].append(link)
    driver.quit()


    driver = webdriver.Chrome()
    for disease in disease_dic:
            for link in disease["Result Link"]:
                if link and "https://wwwnc.cdc.gov/eid/article/" in link:
                    driver.get(link)
                    time.sleep(2)
                    try:
                        article = driver.find_element(By.ID, 'mainbody')
                        disease["Article"].append({
                        "source": "CDC",
                        "content": article.text
                        })
                    except:
                        continue
    driver.quit()
    return disease_dic

## MedlinePlus Scraping Function

def scrape_medline(disease_dic):
    """Scrapes the MedlinePlus website for articles related to the diseases in the ICD."""
    driver = webdriver.Chrome()

    for disease in disease_dic:
        driver.get("https://medlineplus.gov/all_healthtopics.html")
        search = driver.find_element(By.ID, 'searchtext_primary')
        button = driver.find_element(By.XPATH, '/html/body/div[1]/header/div/div[3]/div[2]/form/div/div[2]/button')
        search.send_keys(disease['Disease'])
        button.click()
        time.sleep(2)
        res = driver.find_elements(By.CLASS_NAME, 'title')
        for r in res:
            if r.get_attribute("href") and "medlineplus.gov" in r.get_attribute("href"):
                disease["Result Link"].append(r.get_attribute("href"))
                print(r.get_attribute("href"))
    driver.quit()


    driver = webdriver.Chrome()

    for disease in disease_dic:
        for link in disease["Result Link"]:
            if link and "medlineplus.gov" in link:
                driver.get(link)
                time.sleep(2)
                article = driver.find_element(By.ID, 'mplus-content')
                disease["Article"].append({
            "source": "medlineplus",
            "content": article.text
        })
    driver.quit()
    return disease_dic

## German Federal Ministry of Health Scraping Function

def scrape_german_health(disease_dic):
    """Scrapes the German Federal Ministry of Health website for articles related to the diseases in the ICD."""
    driver = webdriver.Chrome()
    for disease in disease_dic:
        driver.get("https://gesund.bund.de/en/icd-code-suche")
        disease["Result Link"] = []
        search = driver.find_element(By.CLASS_NAME, 'input--text')
        button = driver.find_element(By.XPATH, '//*[@id="app"]/header/a-header/div/div[1]/div/div[3]/form/a-auto-suggest/button[2]')
        search.send_keys(f"{disease['Sub-code']} {disease['Disease']}")
        button.click()
        time.sleep(2)
        res = driver.find_elements(By.CLASS_NAME, 'm-search-result__item-link')
        disease["Result Link"].append([r.get_attribute("href") for r in res][0])
    driver.quit()


    driver = webdriver.Chrome()

    for disease in disease_dic:
        disease["Article"] = []
        for link in disease["Result Link"]:
            driver.get(link)
            time.sleep(2)
            article = driver.find_element(By.XPATH, '//*[@id="standard-textseite-headline-h1"]/section[1]/div[1]')
            disease["Article"].append({
            "source": "Federal Ministry of Health",
            "content": article.text
        })
    driver.quit()
    return disease_dic
    