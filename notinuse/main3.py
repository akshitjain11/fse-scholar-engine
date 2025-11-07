import csv
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ----------------- SELENIUM SETUP -----------------
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# ----------------- GOOGLE SCHOLAR FUNCTIONS -----------------
def get_author_profile(driver, author_name):
    driver.get("https://scholar.google.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))

    search_box = driver.find_element(By.NAME, "q")
    search_box.clear()
    search_box.send_keys(author_name)
    search_box.send_keys(Keys.RETURN)

    try:
        profile_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/citations?user=')]"))
        )
        profile_link.click()
        time.sleep(2)
        return True
    except:
        print(f"❌ No Google Scholar profile found for '{author_name}'.")
        return False


def is_affiliated_with_asu(driver):
    try:
        aff_elem = driver.find_element(By.ID, "gsc_prf_i")
        affiliation_text = aff_elem.text.lower()
        return ("arizona state university" in affiliation_text) or ("asu" in affiliation_text)
    except:
        return False


def get_scholar_papers(driver, max_papers=100):
    papers = []
    while True:
        rows = driver.find_elements(By.CSS_SELECTOR, ".gsc_a_tr")

        for row in rows:
            try:
                link_elem = row.find_element(By.CSS_SELECTOR, ".gsc_a_t a")
                title = link_elem.text.strip()
                link = link_elem.get_attribute("href")
                year_elem = row.find_element(By.CSS_SELECTOR, ".gsc_a_y span").text.strip()
                if title:
                    papers.append({"title": title, "link": link, "year": year_elem})
            except:
                continue

            if len(papers) >= max_papers:
                break

        try:
            next_button = driver.find_element(By.ID, "gsc_bpf_next")
            if "disabled" in next_button.get_attribute("class"):
                break
            next_button.click()
            time.sleep(2)
        except:
            break

        if len(papers) >= max_papers:
            break

    return papers


# ----------------- SEMANTIC SCHOLAR ENRICHMENT -----------------
def enrich_with_semantic_scholar(paper_title):
    """Fetch metadata from Semantic Scholar API for a given paper title."""
    try:
        url = (
            f"https://api.semanticscholar.org/graph/v1/paper/search"
            f"?query={paper_title}&limit=1&fields=title,url,year,venue,abstract,authors"
        )
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get("data"):
            paper = data["data"][0]
            return {
                "ss_title": paper.get("title"),
                "ss_url": paper.get("url"),
                "ss_venue": paper.get("venue"),
                "ss_year": paper.get("year"),
                "ss_authors": ", ".join([a["name"] for a in paper.get("authors", [])]),
                "ss_abstract": paper.get("abstract", "")
            }
    except Exception as e:
        print(f"⚠️ Semantic Scholar API error for '{paper_title}': {e}")
    return {}


# ----------------- MAIN PROCESS -----------------
def process_authors(author_list):
    driver = setup_driver()
    results = []

    for author in author_list:
        print(f"\n🔍 Checking author: {author}")
        if not get_author_profile(driver, author):
            continue

        if is_affiliated_with_asu(driver):
            print(f"✅ {author} is affiliated with ASU.")
            papers = get_scholar_papers(driver)
            print(f"📚 Found {len(papers)} papers for {author}. Enriching via Semantic Scholar...")

            for p in papers:
                enriched = enrich_with_semantic_scholar(p["title"])
                results.append({"author": author, **p, **enriched})
                time.sleep(0.8)  # be polite to the API
        else:
            print(f"🚫 {author} is not affiliated with ASU.")

        time.sleep(2)

    driver.quit()
    return results


# ----------------- SAVE TO CSV -----------------
def save_to_csv(results, filename="asu_authors_enriched_papers.csv"):
    keys = [
        "author", "title", "year", "link",
        "ss_title", "ss_url", "ss_venue", "ss_year", "ss_authors", "ss_abstract"
    ]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
    print(f"\n💾 Saved results to {filename}")


# ----------------- RUN SCRIPT -----------------
if __name__ == "__main__":
    authors = [
        "Huan Liu",
        "Subbarao Kambhampati",
        "Paulo Shakarian",
        "Yezhou Yang",
        "Chitta Baral"
    ]

    results = process_authors(authors)
    if results:
        save_to_csv(results)
    else:
        print("No ASU-affiliated authors found.")
