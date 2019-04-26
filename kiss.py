from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request as req
import argparse
import zipfile
import time
import re
import os

import numpy as np
from typing import List, Tuple

Issues_Links = List[Tuple[str, str]]
Links = List[str]


def define_parser() -> argparse.ArgumentParser:
    # Define CLI Parser arguments
    parser = argparse.ArgumentParser(
        description='Kiss Consume (https://github.com/kunalchandan/Kiss_Consume) a webcomic scraper for Kiss Comics the'
                    ' scraper is purely for educational purposes. Specify the title and the skip(from the top) into the'
                    ' arguments and watch it slowly download the comics into the folder down/ISSUE_TITLE .')
    req = parser.add_argument_group('Required Arguments')
    req.add_argument('-s', '--skip',
                     help='Skip number of comics from top, default=0',
                     default=0,
                     type=int,
                     required=True)
    req.add_argument('-t', '--title',
                     help='title of webcomic, get from the actual link of the comic, '
                          'I might implement searching (probably not)',
                     required=True)
    parser.add_argument('-H', '--human',
                        action='store_true',
                        help='Pause to let you take care of the Google Captcha, '
                             'you must type anything to resume once you\'ve resolved it.')
    return parser


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


def generate_output_folder(output_folder):
    if not os.path.isdir('down/' + output_folder):
        os.mkdir('down/' + output_folder)


def save_images(image_links, output_folder):
    for j in range(len(image_links)):
        req.urlretrieve(str(image_links[j]), 'down/{}/{}.jpg'.format(output_folder, str(j).zfill(4)))


def zip_images(path, output_comic):
    for root, dirs, files in os.walk(path):
        for file in files:
            output_comic.write(os.path.join(root, file))


def download_issues(skip: int, title: str, human):
    driver = define_driver(title)
    time.sleep(6)
    issue_links = get_links(driver)
    issue_links = issue_links[skip:]
    if not os.path.isdir('down/'):
        os.mkdir('down/')
    for i in range(len(issue_links)):
        driver.get(issue_links[i][0] + '&quality=hq&readType=1')
        # Gathering image links
        image_links = get_image_links(driver)

        if len(image_links) == 0:
            if not human:
                print('They don\'t like us anymore, pausing and restarting crawler, hold on')
                driver.quit()
                return i + skip
            else:
                input('Pausing to allow you to take care of captcha')
                image_links = get_image_links(driver)

        output_folder = re.sub(r'[\\/*?:"<>|]', "", issue_links[i][1])
        generate_output_folder(output_folder)
        # Saving Images
        save_images(image_links, output_folder)
        # TODO:: Zip images into cbz or cbr
        output_comic = zipfile.ZipFile(os.path.abspath(output_folder.rstrip('/') + '.cbz'), 'w', zipfile.ZIP_DEFLATED)
        zip_images(os.path.abspath(output_folder), output_comic)
        output_comic.close()
        print(issue_links[i])
    driver.quit()
    return -1


def main():
    args = define_parser().parse_args()
    title = args.title
    skip = args.skip
    human = args.human
    incomplete = True
    while incomplete:
        skip = download_issues(skip, title, human)
        if skip == -1:
            incomplete = False
        else:
            time.sleep(30)


if __name__ == "__main__":
    main()
