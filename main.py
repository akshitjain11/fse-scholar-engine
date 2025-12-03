from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


def get_author_profile(driver, author_name):
    driver.get("https://scholar.google.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))

    search_box = driver.find_element(By.NAME, "q")
    search_box.clear()
    search_box.send_keys(author_name)
    search_box.send_keys(Keys.RETURN)

    try:
        profile_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@href, '/citations?user=')]")
            )
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
        return ("arizona state university" in affiliation_text) or (
            "asu" in affiliation_text
        )
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
                year_elem = row.find_element(
                    By.CSS_SELECTOR, ".gsc_a_y span"
                ).text.strip()
                if title and link:
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


def process_authors(author_list):
    driver = setup_driver()
    results = []
    total_authors = len(author_list)
    asu_affiliated_count = 0

    for author in author_list:
        print(f"\n🔍 Checking author: {author}")
        if not get_author_profile(driver, author):
            continue

        if is_affiliated_with_asu(driver):
            print(f"✅ {author} is affiliated with ASU.")
            asu_affiliated_count += 1
            papers = get_scholar_papers(driver)
            for p in papers:
                results.append({"author": author, **p})
            print(f"📚 Extracted {len(papers)} papers for {author}.")
        else:
            print(f"🚫 {author} is not affiliated with ASU.")
        time.sleep(1)

    driver.quit()
    return results, asu_affiliated_count, total_authors


def save_to_csv(results, filename="asu_authors_papers.csv"):
    keys = ["author", "title", "link", "year"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
    print(f"\n💾 Saved results to {filename}")


if __name__ == "__main__":
    authors = [
        "Yezhou Yang",
        "Adam Doupé",
        "Adil Ahmad",
        "Aman Arora",
        "Andrea Richa",
        "Ariane Middel",
        "Arunabha Sen",
        "Aviral Shrivastava",
        "Bing Si",
        "Chitta Baral",
        "Chris Bryan",
        "Dimitri Bertsekas",
        "Douglas Montgomery",
        "Feng Ju",
        "Fish Wang",
        "Gail-Joon Ahn",
        "George Runger",
        "Geunyeong Byeon",
        "Giulia Pedrielli",
        "Guoliang Xue",
        "Hani Ben Amor",
        "Hao Yan",
        "Hasan Davulcu",
        "Hessam Sarjoughian",
        "Huan Liu",
        "James Collofello",
        "Jedidiah Crandall",
        "Joshua Daymude",
        "K. Selcuk Candan",
        "Kevin Gary",
        "Lacy Greening",
        "Michel Kinsy",
        "Ming Zhao",
        "Nakul Gopalan",
        "Paul Grogan",
        "Rakibul Hasan",
        "Rida Bazzi",
        "Robert Atkinson",
        "Rong Pan",
        "Ross Maciejewski",
        "Sandeep Gupta",
        "Sarma Vrudhula",
        "Sethuraman Panchanathan",
        "Siddharth Srivastava",
        "Srividya Bansal",
        "Stephanie Forrest",
        "Stephen Yau",
        "Subbarao Kambhampati",
        "Ted Pavlic",
        "Teresa Wu",
        "Tiffany Bao",
        "Violet Syrotiuk",
        "Vivek Gupta",
        "Xusheng Xiao",
        "Yalin Wang",
        "Yan Shoshitaishvili",
        "Yanjie Fu",
        "YooJung Choi",
        "Yu Zhang",
        "Zhichao Cao",
    ]

    results, asu_count, total = process_authors(authors)
    if results:
        save_to_csv(results)
    else:
        print("No ASU-affiliated authors found.")

    print(f"\n🏫 ASU-affiliated authors: {asu_count}/{total}")
