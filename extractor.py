from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
)
from webdriver_manager.chrome import ChromeDriverManager
import time


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


try:
    driver = setup_driver()
    url = "https://faculty.engineering.asu.edu/directory/scai/rank/"
    driver.get(url)
    time.sleep(3)  # initial load wait

    professor_names = set()  # use set to avoid duplicates

    while True:
        # Collect names from current page
        name_elements = driver.find_elements(By.CSS_SELECTOR, "a.person-name")
        for el in name_elements:
            name = el.text.strip()
            if name:
                professor_names.add(name)

        # Try to find and click "Next Page"
        try:
            next_button = driver.find_element(
                By.CSS_SELECTOR, 'button[aria-label="Next Page"]'
            )
            disabled = next_button.get_attribute("aria-disabled")

            if disabled == "true":
                break  # stop if button is disabled (end of pages)

            # Click next page
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(10)  # allow time for new page to load

        except (NoSuchElementException, ElementClickInterceptedException):
            break

    # Print results
    print(f"Total professors found: {len(professor_names)}\n")
    for name in sorted(professor_names):
        print(name)

finally:
    driver.quit()
