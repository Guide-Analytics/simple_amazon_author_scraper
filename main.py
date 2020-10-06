"""
This file will scrape author profiles.
Required files are read from 'main_product/' folder in 'data_scraper_v2'
Contents are saved as CSV in 'reviewers/'
"""

import time
import datetime
import random
import pandas as pd
import glob
import AuthorProfileConfig as config
import DriverSetup as setup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from platform import system  # to check os

from urllib.request import urlretrieve  # to download image

configuration = None

os = system()  # get the os

amazon_reviews = {}


# dictionary to store fields
def initialize_dict():
    global amazon_reviews
    amazon_reviews = {
        'author_id': [],
        'date_review_posted': [],
        'review_title': [],
        'reviews': [],
        'verified_purchase': [],
        'people_find_helpful': [],
        'ratings': [],
        'product_url': [],
        'start': [],
        'end': []
    }


def add_to_dict(id, date, title, ratings, review, verified_purchase, helpful, url, start, end):
    """
    Store data to dictionary

    Attributes
    ----------
    id: string
        unique id of reviewer
    date: string
        date the review was posted
    title: string
        title related to review
    ratings: strings
        ratings related to reviews
    review: string
        review posted by author
    verified_purchase: string
        whether it's a verified purchased or not
    helpful: string
        number of people found the review helpful
    url: string
        product url of the review
    start: datetime
        start time for extracting a review
    end: datetime
        time extraction process ends for a review
    """

    amazon_reviews['author_id'].append(id)
    amazon_reviews['date_review_posted'].append(date)
    amazon_reviews['review_title'].append(title)
    amazon_reviews['ratings'].append(ratings)
    amazon_reviews['reviews'].append(review)
    amazon_reviews['verified_purchase'].append(verified_purchase)
    amazon_reviews['people_find_helpful'].append(helpful)
    amazon_reviews['product_url'].append(url)
    amazon_reviews['start'].append(start)
    amazon_reviews['end'].append(end)


def extract_author_profile(df):
    """
    extract information (all reviews) about an author

    Parameters
    ----------
    df: pandas data frame
        list containing url of an author profile
    """
    global configuration
    files = glob.glob("reviewers\*.csv")  # contents for author profile
    files = list(map(lambda x: x.split("\\")[1].split('_')[0], files))  # extracts the author_id from the file name
    df = df[~df['author_id'].isin(files)]  # remove the authors that are al ready scraped
    product_category = df['product_category'].dropna().unique()[0]
    product_id = df['product_id'].unique()[0]

    driver = setup.DriverSetup().driver
    # load the url from csv

    for url in df['reviewer_profile_url'].dropna().unique():

        print(url)

        id = df.author_id[df['reviewer_profile_url'].isin([url])].to_list()[0]  # get the author id
        print(id)

        # id = url.split('/')[-2]
        # id = id.split('.')[-1]

        # initialize the dictionary
        initialize_dict()

        # url = 'https://www.amazon.ca/gp/profile/amzn1.account.AE3X4B27XTAPBJLVXZX4YVM6KPBQ/ref=cm_cr_dp_d_gw_tr?ie=UTF8'
        driver.get(url)

        # setup all configurations defined in AmazonConfig file
        configuration = config.AuthorConfiguration()

        # profile picture
        img = configuration.get_profile_image(driver)
        if not img:
            driver.refresh()
            time.sleep(2)
            img = configuration.get_profile_image(driver)
        urlretrieve(img, f'images\profile\{id}.jpg')

        # cover picture
        img = configuration.get_cover_image(driver)
        urlretrieve(img, f'images\cover\{id}.jpg')

        # scroll till the end to load all the reviews
        # idea: scroll till the end, then scroll up a little to load otherwise it won't load
        # all the reviews. Do this recursively till the page height is fixed
        time.sleep(3)
        try:
            SCROLL_PAUSE_TIME = 0.5
            # get the height of the page
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll to bottom
                time.sleep(SCROLL_PAUSE_TIME)
                height = driver.execute_script("return document.body.scrollHeight")  # get the height of page
                driver.execute_script(f"window.scrollTo(0,{height - 10});")  # scroll a little and wait to load reviews
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll to end
                new_height = driver.execute_script("return document.body.scrollHeight")  # get the final page after
                # loading reviews
                if new_height == last_height:  # check if height of pages are similar stop
                    break
                last_height = new_height  # change the old page height to new height
        except Exception as exc:
            print(exc)
            print('not able to load')
            driver.quit()

        # scraping reviews
        driver.execute_script("window.scrollTo(0,0);")
        time.sleep(3)

        # get author name
        author_name = configuration.get_author_name(driver)
        print(author_name)

        path = '//div[@id="profile-at-card-container"]//div[@class="a-row"]'  # review cards for each review
        try:
            reviews = driver.find_elements_by_xpath(path)
        except NoSuchElementException:
            print('No such element found, re-look the path')
            driver.quit()
            return
        for review in reviews:
            time.sleep(random.randint(4, 7))
            # check for more_reviews hyperlink to expand the review
            # without that, the review can not be extracted completely
            path = 'div.a-section.profile-at-content > p > a'
            try:
                more_review = review.find_element_by_css_selector(path)
            except NoSuchElementException:
                print('Unable to locate the element (path can be wrong)')
                break

            # if review is expanded then extract all the required information
            if more_review:
                start = datetime.datetime.now()
                current_window = driver.current_window_handle  # get the current window

                if os == 'Windows' or os == 'Linux':
                    more_review.send_keys(Keys.CONTROL + Keys.ENTER)  # open link in new tab keyboard shortcut
                else:
                    more_review.send_keys(Keys.COMMAND + Keys.ENTER)
                WebDriverWait(driver, 10).until(ec.number_of_windows_to_be(2))
                driver.switch_to.window(driver.window_handles[1])  # new tab is at index 1

                time.sleep(random.randint(4, 7))
                # extract info

                date = configuration.get_posted_date(driver)
                if not date:
                    driver.refresh()
                    time.sleep(2)
                    date = configuration.get_posted_date(driver)
                # extract the information
                title = configuration.get_title(driver)
                ratings = configuration.get_ratings(driver)
                review = configuration.get_reviews(driver)
                verified_purchase = configuration.is_verified_purchase(driver)
                helpful = configuration.get_helpful_count(driver)
                url = configuration.get_product_url(driver)

                end = datetime.datetime.now()
                # store to dictionary
                add_to_dict(id, date, title, ratings, review, verified_purchase, helpful, url, start, end)
                time.sleep(3)
                driver.close()  # closes new tab
                try:
                    WebDriverWait(driver, 10).until(ec.number_of_windows_to_be(1))
                except TimeoutException:
                    print('time out occurred')
                    return
                driver.switch_to.window(current_window)

        # if reviews are present then save to csv file.
        if len(amazon_reviews['reviews']) > 0:
            frame = pd.DataFrame.from_dict(amazon_reviews)
            frame['reviewer_name'] = author_name
            frame['product_category'] = product_category
            frame['product_id'] = product_id

            try:
                frame.to_csv(f"reviewers\{id}_{product_id}.csv")
                print(f'Author{product_id}.csv is saved')
            except Exception as exp:
                print("Permission denied, if the file already exist then delete first")
                print(exp)
                driver.quit()
                return

    driver.quit()


def main():
    """
    Main function
    """

    files = glob.glob(r'F:\GuideAnalytics\data_scraper_v2\main_product\*.csv')

    for file in files:
        df = pd.read_csv(file)
        extract_author_profile(df)  # extract the author_profile

    # extract_author_profile(['https://www.amazon.ca/gp/profile/amzn1.account.AGH7OYWNBYDRL7AN5LTSZ3HIK6LQ/ref=cm_cr_arp_d_gw_btm?ie=UTF8'])


if __name__ == '__main__':
    main()
