import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager


driver = None


def get_driver():
    """
    Initialize Chrome driver only once
    """

    global driver

    if driver is None:

        chrome_options = Options()

        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver


def extract_company_from_domain(domain):

    parts = domain.split(".")

    if len(parts) >= 3:
        return parts[-3].capitalize()

    if len(parts) >= 2:
        return parts[-2].capitalize()

    return domain.capitalize()


def clean_company_name(title):
    """
    Clean company name from search result title
    """

    separators = ["|", "-", ":", "–"]

    for sep in separators:
        if sep in title:
            title = title.split(sep)[0]

    title = title.strip()

    return title

def search_company(domain):

    driver = get_driver()

    company = extract_company_from_domain(domain)

    search_context = ""

    try:

        query = f"{domain} company sector what does {domain} do"

        url = f"https://duckduckgo.com/?q={query}"

        driver.get(url)

        time.sleep(0.5)

        results = driver.find_elements(By.CSS_SELECTOR, "article")

        if results:

            title_elem = results[0].find_element(By.CSS_SELECTOR, "h2")
            title = title_elem.text

            company = clean_company_name(title)

        try:
            snippets = driver.find_elements(By.CSS_SELECTOR, ".result__snippet")

            texts = []

            for s in snippets[:5]:
                # t = s.text.strip()
                if s.text:
                    texts.append(s.text)

            search_context = " ".join(texts)

        except:
            search_context = ""

    except Exception:
        pass

    return company, search_context