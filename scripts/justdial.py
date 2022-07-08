import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")


def strings_to_num(argument):
    switcher = {
        'dc': '+',
        'fe': '(',
        'hg': ')',
        'ba': '-',
        'acb': '0',
        'yz': '1',
        'wx': '2',
        'vu': '3',
        'ts': '4',
        'rq': '5',
        'po': '6',
        'nm': '7',
        'lk': '8',
        'ji': '9'
    }
    return switcher.get(argument, "nothing")


def scrape_justdial(topic, cities):
    driver = webdriver.Chrome(
        os.environ.get("CHROMEDRIVER_PATH"), options=options
    )
    doc_name = []
    doc_contact = []
    doc_rating = []
    doc_tags = []
    for city in cities:
        for page in range(1, 5):
            try:
                path = f"https://www.justdial.com/{city}/{topic}/page-{page}"
                driver.get(path)
                driver.set_page_load_timeout(5)

                # getting all details
                Details = driver.find_elements_by_class_name('store-details')

                for i in range(len(Details)):
                    # name of doctor or clinic
                    name = Details[i].find_element_by_class_name(
                        'lng_cont_name').text
                    # rating
                    rating = Details[i].find_elements_by_class_name(
                        'green-box')[0].text
                    # tags
                    tags = Details[i].find_elements_by_class_name('addrinftxt')
                    tags = ", ".join([i.text for i in tags if not ".." in i.text])
                    # contact
                    contact = Details[i].find_elements_by_class_name('mobilesv')

                    number = []
                    for j in range(len(contact)):
                        myString = contact[j].get_attribute('class').split("-")[1]
                        number.append(strings_to_num(myString))

                    doc_name.append(name)
                    doc_contact.append("".join(number))
                    doc_rating.append(rating)
                    doc_tags.append(tags)

            except:
                pass
    driver.quit()

    data = {
        'Doctor/Clinic': doc_name,
        'Phone': doc_contact,
        'Rating': doc_rating,
        'Tags': doc_tags
    }

    return data
