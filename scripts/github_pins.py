from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from scripts.utils import CustomLogger


class ScrapeGitHubRepos:
    """Scrape pinned repos for any GitHub username."""

    def __init__(self, username):
        self.logger = CustomLogger("github_scraper")
        self.username = username
        self.selenium_driver = self.setup_selenium_driver()

    def setup_selenium_driver(self):
        """Sets up the Selenium WebDriver for Chrome."""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument('--log-level=1')
        options.add_argument("enable-automation")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

        # driver = webdriver.Chrome(
        #     os.environ.get("CHROMEDRIVER_PATH"), options=options
        # )
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )

        return driver

    def get_website_image(self, owner, repo, link):
        """Scrape the website and image for each repo."""
        self.selenium_driver.get(link)

        # Scraping the website associated with the repo
        web = ""
        try:
            about = self.selenium_driver.find_element(
                By.CLASS_NAME, "BorderGrid-cell")
            web = about.find_element(By.TAG_NAME, "a").get_attribute("href")
            if "Topic" in web:
                web = ""
        except Exception as e:
            self.logger.error("fetching website", e)

        # Scraping the image for the repo
        image = ""
        try:
            image = self.selenium_driver.find_element(
                By.NAME, "twitter:image:src").get_attribute("content")
        except NoSuchElementException:
            image = f"https://opengraph.githubassets.com/1/{owner}/{repo}"

        return web, image

    def get_repo(self, pin):
        """Scrape details for each pinned repo."""
        repo_details = {}

        # Get the repo details with proper error handling
        try:
            try:
                repo_details['owner'] = pin.find_element(
                    By.CLASS_NAME, "owner").text
            except NoSuchElementException:
                repo_details['owner'] = self.username

            try:
                repo_details['description'] = pin.find_element(
                    By.CLASS_NAME, "pinned-item-desc").text
            except NoSuchElementException:
                repo_details['description'] = ""

            try:
                repo_details['language'] = pin.find_element(
                    By.CSS_SELECTOR, "span[itemprop='programmingLanguage']").text
            except NoSuchElementException:
                repo_details['language'] = ""

            try:
                repo_details['languageColor'] = pin.find_element(By.CLASS_NAME, "repo-language-color").get_attribute(
                    "style").replace("background-color: ", "").replace(";", "")
            except NoSuchElementException:
                repo_details['languageColor'] = ""

            repo_details['repo'] = pin.find_element(By.CLASS_NAME, "repo").text
            repo_details['link'] = f"https://github.com/{repo_details['owner']}/{repo_details['repo']}"

            meta = pin.find_elements(By.CLASS_NAME, "pinned-item-meta")
            repo_details['stars'] = int(meta[0].text) if meta else 0
            repo_details['forks'] = int(meta[1].text) if len(meta) > 1 else 0

        except Exception as e:
            self.logger.error(f"fetching repo details for", e)
            return {}

        return repo_details

    def scrape_github(self):
        """Scrape GitHub for pinned repos."""
        data = []
        try:
            path = f"https://www.github.com/{self.username}"
            self.selenium_driver.get(path)
            self.selenium_driver.set_page_load_timeout(5)

            # Get all pinned repos
            pins = self.selenium_driver.find_elements(
                By.CLASS_NAME, "pinned-item-list-item-content"
            )

            # Scraping details for each pinned repo
            for pin in pins:
                data.append(self.get_repo(pin))

            for i in range(len(data)):
                data[i]['website'], data[i]['image'] = self.get_website_image(
                    data[i]['owner'], data[i]['repo'], data[i]['link']
                )

        except Exception as e:
            self.logger.error("scraping GitHub", e)

        finally:
            self.selenium_driver.quit()
        
        self.logger.info(f"Fetched github pinned repos for {self.username} successfully:\n {data}")

        return data
