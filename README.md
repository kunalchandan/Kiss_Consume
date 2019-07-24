# Kiss Consume
This is a basic KissComics crawler.

The crawler will:
* Gather issue links based on a given title
* Collect all issue links
* Save all pages of the issue in sequential order
* zip/rar into a .cbr or .cbz format

Although not all features have been tested, this crawler is officially complete.
## Usage

```
usage: kiss.py [-h] -t TITLE --consume {comics,manga} [-s SKIP] [-H]

Kiss Consume (https://github.com/kunalchandan/Kiss_Consume) a webcomic scraper
for Kiss Comics the scraper is purely for educational purposes. Specify the
title and the skip(from the top) into the arguments and watch it slowly
download the comics into the folder down/ISSUE_TITLE .

optional arguments:
  -h, --help            show this help message and exit
  -s SKIP, --skip SKIP  Skip number of comics from top, default=0
  -H, --human           Pause to let you take care of the Google Captcha, you
                        must type anything to resume once you've resolved it.

Required Arguments:
  -t TITLE, --title TITLE
                        title of webcomic, get from the actual link of the
                        comic, I might implement searching (probably not)
  --consume {comics,manga}
                        The media to scrape, this is one of ['comics',
                        'manga']
```

## Example

```
python3 kiss.py --consume comics -t Chew
python3 kiss.py --consume manga  -t 'Tenkuu-Shinpan' -s 24
```

## Dependancies
```
selenium
beautifulsoup4
webdriver-manager
```
You should be able to install all of these with pip or conda, whatever you prefer.

## Reasoning
I was far far too lazy to actually download each and every one of these images one at a time and I don't really like the ads on the site, so yeah...

# Disclaimer
This is purely an educational tool for helping students learn `Selenium` for `Python`.

Use at your own discretion, I do not support piracy.
