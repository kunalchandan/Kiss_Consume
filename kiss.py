from selenium import webdriver
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import argparse
import os

from typing import List, Tuple

Issues_Links = List[Tuple[str, str]]


def define_driver(title: str) -> webdriver:
    base_url = 'https://readcomiconline.to/Comic/'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(base_url + title)
    return driver


def get_links(driver: webdriver) -> Issues_Links:
    tag = driver.find_element_by_tag_name('table')

    issue_links: list = []
    links = tag.find_elements_by_tag_name('a')
    for link in links:
        issue_links.append(list([link.get_attribute('href'), link.text]))
    return issue_links


def set_settings(driver: webdriver):
    # Could do this
    select = Select(driver.find_element_by_id('selectQuality'))
    select.select_by_value('hq')
    time.sleep(1)
    select = Select(driver.find_element_by_id('selectReadType'))
    select.select_by_value('1')
    time.sleep(2)
    # Or use REST API


def main():
    title = 'Chew'
    driver = define_driver(title)
    time.sleep(6)
    issue_links = get_links(driver)

    for issue in issue_links:
        # TODO:: go to page
        driver.get(issue[0])
        # TODO:: Set Settings on page
        set_settings(driver)
        # TODO:: Gather images

        # TODO:: Save Images
        # TODO:: Zip images into cbz or cbr
        print(issue)
    driver.close()


if __name__ == "__main__":
    main()
