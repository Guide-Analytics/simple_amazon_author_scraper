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

configuration = None

# dictionary to store fields
author_analysis = {
    'date_review_posted': [],
    'review_title': [],
    'review': [],
    'verified_purchase': [],
    'people_find_helpful': [],
    'ratings': [],
    'start': [],
    'end': []

}


def add_to_dict(date, title, ratings, review, verified_purchase, helpful, start, end):
    """
    Store data to dictionary

    Attributes
    ----------
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
    start: datetime
        start time for extracting a review
    end: datetime
        time extraction process ends for a review
    """

    author_analysis['date_review_posted'].append(date)
    author_analysis['review_title'].append(title)
    author_analysis['ratings'].append(ratings)
    author_analysis['review'].append(review)
    author_analysis['verified_purchase'].append(verified_purchase)
    author_analysis['people_find_helpful'].append(helpful)
    author_analysis['start'].append(start)
    author_analysis['end'].append(end)


def extract_author_profile(urls):
    """
    extract information (all reviews) about an author

    Parameters
    ----------
    urls: list
        list containing url of an author profile
    """
    global configuration
    driver = setup.DriverSetup().driver
    # load the url from csv
    for url in urls:
        # url = 'https://www.amazon.ca/gp/profile/amzn1.account.AE3X4B27XTAPBJLVXZX4YVM6KPBQ/ref=cm_cr_dp_d_gw_tr?ie=UTF8'
        driver.get(url)

        # setup all configurations defined in AmazonConfig file
        configuration = config.AuthorConfiguration()

        # scroll till the end to load all the reviews
        # idea: scroll till the end, then scroll up a little to load otherwise it won't load
        # all the reviews. Do this recursively till the page height is fixed

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
        except:
            print('not able to load')
            driver.quit()

        # scraping reviews
        driver.execute_script("window.scrollTo(0,0);")
        time.sleep(3)

        # get author name
        author_name = configuration.get_author_name(driver)

        path = '//div[@id="profile-at-card-container"]//div[@class="a-row"]'  # review cards for each review
        reviews = driver.find_elements_by_xpath(path)
        for review in reviews:
            time.sleep(random.randint(3, 7))
            path = 'div.a-section.profile-at-content > p > a'
            try:
                more_review = review.find_element_by_css_selector(path)
                if more_review:
                    start = datetime.datetime.now()
                    current_window = driver.current_window_handle
                    more_review.send_keys(Keys.CONTROL + Keys.ENTER)  # open link in new tab keyboard shortcut
                    WebDriverWait(driver, 10).until(ec.number_of_windows_to_be(2))
                    driver.switch_to.window(driver.window_handles[1])  # new tab is at index 1

                    # extract info
                    date = configuration.get_posted_date(driver)
                    title = configuration.get_title(driver)
                    ratings = configuration.get_ratings(driver)
                    review = configuration.get_reviews(driver)
                    verified_purchase = configuration.is_verified_purchase(driver)
                    helpful = configuration.get_helpful_count(driver)
                    end = datetime.datetime.now()
                    # store to dictionary
                    add_to_dict(date, title, ratings, review, verified_purchase, helpful, start, end)
                    time.sleep(3)
                    driver.close()  # closes new tab
                    WebDriverWait(driver, 10).until(ec.number_of_windows_to_be(1))
                    driver.switch_to.window(current_window)
            except:
                print('exception occurred')
                driver.quit()
                return

        df = pd.DataFrame.from_dict(author_analysis)
        df['author'] = author_name
        df.to_csv(f'{author_name}.csv')
        print(f'Contents are saved in: {author_name}.csv')

    driver.quit()


def main():
    """
    Main function
    """
    print("Enter the folder path for CSV files:")
    path = input()
    files = glob.glob(path + '*.csv')
    for file in files:
        df = pd.read_csv(file)
        urls = df['author_profile'].dropna().tolist()
        extract_author_profile(urls)


if __name__ == '__main__':
    main()
