import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")


def get_website_image(owner, repo, link):
    DRIVER.get(link)

    try:
        about = DRIVER.find_element(By.CLASS_NAME, "BorderGrid-cell")
        web = about.find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        web = ""

    try:
        image = DRIVER.find_element(
            By.NAME, "twitter:image:src"
        ).get_attribute("content")
    except:
        image = f"https://opengraph.githubassets.com/1/{owner}/{repo}"

    return web, image


def get_repo(username, pin):
    try:
        owner = pin.find_element(By.CLASS_NAME, "owner").text
    except:
        owner = username

    try:
        repo = pin.find_element(By.CLASS_NAME, "repo").text
    except:
        return {}

    try:
        link = f"https://github.com/{owner}/{repo}"
    except:
        link = ""

    try:
        description = pin.find_element(By.CLASS_NAME, "pinned-item-desc").text
    except:
        description = ""

    try:
        language = pin.find_element(By.CLASS_NAME, "pinned-item-desc").text
    except:
        language = ""

    try:
        languageColor = pin.find_element(
            By.CLASS_NAME, "repo-language-color"
        ).get_attribute("style")
        languageColor = languageColor.replace("background-color: ", "")
        languageColor = languageColor.replace(";", "")
    except:
        languageColor = ""

    try:
        stars = pin.find_element(By.PARTIAL_LINK_TEXT, '/stargazers').text
    except:
        stars = "0"

    try:
        forks = pin.find_element(By.PARTIAL_LINK_TEXT, '/network/members').text
    except:
        forks = "0"

    result = {
        'owner': owner,
        'repo': repo,
        'link': link,
        'description': description,
        'image': '',
        'website': '',
        'language': language,
        'languageColor': languageColor,
        'stars': stars,
        'forks': forks,
    }

    return result


def scrape_github(username):
    global DRIVER

    data = []
    DRIVER = webdriver.Chrome(
        os.environ.get("CHROMEDRIVER_PATH"), options=options
    )

    try:
        path = f"https://www.github.com/{username}"
        DRIVER.get(path)
        DRIVER.set_page_load_timeout(5)

        # getting all details
        pins = DRIVER.find_elements(
            By.CLASS_NAME, "pinned-item-list-item-content"
        )

        for pin in pins:
            data.append(get_repo(username, pin))

        for i in range(len(data)):
            data[i]['website'], data[i]['image'] = get_website_image(
                data[i]['owner'], data[i]['repo'], data[i]['link']
            )

    except:
        pass

    DRIVER.quit()

    return data
