from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request
import argparse
import zipfile
import time
import re
import os

import numpy as np
from typing import List, Tuple

Issues_Links = List[Tuple[str, str]]
Links = List[str]

SUPPORTED_SITES = {'comics' : 'https://readcomiconline.to/Comic/',
                   'manga'  : 'https://kissmanga.com/Manga/'}


def define_parser() -> argparse.ArgumentParser:
    # Define CLI Parser arguments
    parser = argparse.ArgumentParser(
        description='Kiss Consume (https://github.com/kunalchandan/Kiss_Consume) a webcomic scraper for Kiss Comics the'
                    ' scraper is purely for educational purposes. Specify the title and the skip(from the top) into the'
                    ' arguments and watch it slowly download the comics into the folder down/ISSUE_TITLE .')
    req = parser.add_argument_group('Required Arguments')
    req.add_argument('-t', '--title',
                     help='title of webcomic, get from the actual link of the comic, '
                          'I might implement searching (probably not)',
                     required=True)
    req.add_argument('--consume',
                     help='The media to scrape, this is one of {}'.format(list(SUPPORTED_SITES.keys())),
                     choices=list(SUPPORTED_SITES.keys()),
                     required=True)

    parser.add_argument('-s', '--skip',
                        help='Skip number of comics from top, default=0',
                        default=0,
                        type=int)
    parser.add_argument('-H', '--human',
                        action='store_true',
                        help='Pause to let you take care of the Google Captcha, '
                             'you must type anything to resume once you\'ve resolved it.')
    return parser


def define_driver(site: str, title: str) -> webdriver:
    base_url = SUPPORTED_SITES[site]
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


def get_image_links(driver: webdriver, site: str) -> Links:

    # On a side note, I am genuinely surprised how they managed to obfuscate the images on each of their sites.
    # On KissComics, they have all the links in some script located in the page, this script holds the image links
    # On KissManga, they have img tags that somehow only load the image links once the page is loaded in a browser
    # viewing the raw HTML leads to the images somehow not being there, I don't know enough WebDev to say how they do it
    image_links = []
    if site == 'comics':
        regex = re.compile('lstImages.push\\("(.*?)"')

        for a in driver.find_elements_by_tag_name('script'):
            img_set = re.findall(regex, a.get_attribute('innerHTML'))
            if not img_set == []:
                image_links.append(img_set)

    elif site == 'manga':
        elements = driver.find_elements_by_xpath('//img[@onerror="onErrorImg(this)"]')

        for elem in elements:
            src = elem.get_attribute('src')
            image_links.append(src)

    print(image_links)
    return np.array(image_links).flatten().tolist()


def generate_output_folder(output_folder):
    if not os.path.isdir('down/' + output_folder):
        os.mkdir('down/' + output_folder)


def save_images(image_links, output_folder):
    for j in range(len(image_links)):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(str(image_links[j]), 'down/{}/{}.jpg'.format(output_folder, str(j).zfill(4)))


def zip_images(path, output_comic):
    for root, dirs, files in os.walk(path):
        for file in files:
            output_comic.write(os.path.join(root, file))


def download_issues(site: str, title: str, skip: int, human):
    driver = define_driver(site, title)
    time.sleep(6)
    issue_links = get_links(driver)
    issue_links = issue_links[skip:]
    if not os.path.isdir('down/'):
        os.mkdir('down/')
    for i in range(len(issue_links)):
        driver.get(issue_links[i][0] + '&quality=hq&readType=1')
        # Gathering image links
        image_links = get_image_links(driver, site)

        if len(image_links) == 0:
            if not human:
                print('They don\'t like us anymore, pausing and restarting crawler, hold on')
                driver.quit()
                return i + skip
            else:
                input('Pausing to allow you to take care of captcha')
                image_links = get_image_links(driver, site)

        # Create output location
        output_folder = re.sub(r'[\\/*?:"<>|]', "", issue_links[i][1]).replace('..', '_').replace(' ', '-')
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
    site = args.consume
    skip = args.skip
    title = args.title
    human = args.human
    incomplete = True
    while incomplete:
        skip = download_issues(site, title, skip, human)
        if skip == -1:
            incomplete = False
        else:
            # This is some sleep value to pause and hope they forget about us
            # (for not dealing with captcha)
            time.sleep(30)


if __name__ == "__main__":
    main()
