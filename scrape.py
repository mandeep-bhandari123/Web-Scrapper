# scrape.py

from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC   # FIXED
from selenium.webdriver.common.by import By                        # FIXED
import time                                                         # FIXED


def scrape_website(website, wait_seconds=6):
    print("Launching Chrome browser...")

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")   # enable if needed
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(website)

        # Wait until fully loaded
        WebDriverWait(driver, wait_seconds).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Wait for body tag
        WebDriverWait(driver, wait_seconds).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        time.sleep(0.5)
        print("Page loaded...")
        return driver.page_source

    finally:
        driver.quit()


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.body
    return str(body_content) if body_content else "No body content found."


def clean_bodycontent(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')

    # Remove script and style
    for tag in soup(['script', 'style']):
        tag.extract()

    cleaned = soup.get_text(separator="\n")
    cleaned = '\n'.join(line.strip() for line in cleaned.splitlines() if line.strip())
    return cleaned


def split_dom_content(dom_content, max_length=5000):
    return [
        dom_content[i:i + max_length]
        for i in range(0, len(dom_content), max_length)
    ]
