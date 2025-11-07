from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_scholar_papers(author_name, max_papers=100):
    # Setup Chrome (headless)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    # Step 1: Open Google Scholar
    driver.get("https://scholar.google.com/")
    wait.until(EC.presence_of_element_located((By.NAME, "q")))

    # Step 2: Search author
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(author_name)
    search_box.send_keys(Keys.RETURN)

    # Step 3: Wait for results and open first profile
    try:
        profile_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/citations?user=')]"))
        )
        profile_link.click()
    except Exception:
        print(f"❌ No author profile found for '{author_name}'.")
        driver.quit()
        return []

    time.sleep(2)

    # Step 4: Extract papers
    papers = []
    while True:
        rows = driver.find_elements(By.CSS_SELECTOR, ".gsc_a_tr")

        for row in rows:
            try:
                link_elem = row.find_element(By.CSS_SELECTOR, ".gsc_a_t a")
                title = link_elem.text.strip()
                link = link_elem.get_attribute("href")
                if title and link:
                    papers.append({"title": title, "link": link})
            except:
                # Skip rows without proper links
                continue

            if len(papers) >= max_papers:
                break

        # Step 5: Click “Next” if available
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

    driver.quit()
    return papers


if __name__ == "__main__":
    author = input("Enter author name: ")
    papers = get_scholar_papers(author)

    if papers:
        print(f"\n📚 Papers by {author}:")
        for i, p in enumerate(papers, 1):
            print(f"{i}. {p['title']}\n   {p['link']}\n")
    else:
        print("No papers found.")
