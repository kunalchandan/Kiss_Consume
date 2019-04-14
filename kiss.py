from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import argparse
import os

from typing import List

Keywords = List[str]


def define_driver(title: str) -> webdriver:
    base_url = 'https://readcomiconline.to/Comic/'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(base_url + title)
    return driver


def get_links(driver: webdriver) -> Keywords:
    tag = driver.find_element_by_tag_name('table')

    issue_links = []
    links = tag.find_elements_by_tag_name('a')
    for link in links:
        issue_links.append([link.get_attribute('href'), link.text])
    return issue_links


def main():
    title = 'Chew'
    driver = define_driver(title)
    time.sleep(6)
    issue_links = get_links(driver)
    for issue in issue_links:
        # TODO:: go to page
        # TODO:: Gather images
        # TODO:: Save Images
        # TODO:: Zip images into cbz or cbr
        print(issue)
    driver.close()


if __name__ == "__main__":
    main()
