from selenium import webdriver
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request as req
import time
import re
import argparse
import os

import numpy as np
from typing import List, Tuple

Issues_Links = List[Tuple[str, str]]
Links = List[str]


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


def get_image_links(driver: webdriver) -> Links:
    image_links = []
    regex = re.compile('lstImages.push\\("(.*?)"')

    for a in driver.find_elements_by_tag_name('script'):
        img_set = re.findall(regex, a.get_attribute('innerHTML'))
        if not img_set == []:
            image_links.append(img_set)
    print(image_links)
    return np.array(image_links).flatten().tolist()


def download_issues(skip: int, title: str):
    driver = define_driver(title)
    time.sleep(6)
    issue_links = get_links(driver)
    issue_links = issue_links[skip:]
    if not os.path.isdir('down/'):
        os.mkdir('down/')
    for i in range(len(issue_links)):
        driver.get(issue_links[i][0] + '&quality=hq&readType=1')
        # TODO:: Gather image links
        image_links = get_image_links(driver)

        if len(image_links) == 0:
            print('They don\'t like us anymore, pausing and restarting crawler, hold on')
            return i + skip

        if not os.path.isdir('down/' + issue_links[i][1]):
            os.mkdir('down/' + issue_links[i][1])

        # TODO:: Save Images
        for j in range(len(image_links)):
            req.urlretrieve(str(image_links[j]), 'down/{}/{}.jpg'.format(issue_links[i][1], str(j).zfill(4)))

        # TODO:: Zip images into cbz or cbr
        print(issue_links[i])
    driver.quit()
    return -1


def main():
    title = 'Chew'
    skip = 60
    incomplete = True
    while incomplete:
        skip = download_issues(skip, title)
        if skip == -1:
            incomplete = False
        else:
            time.sleep(30)


if __name__ == "__main__":
    main()
