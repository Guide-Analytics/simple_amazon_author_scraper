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

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from platform import system # to check os

configuration = None

os = system() # get the os

author_analysis = {}

# dictionary to store fields
def initialize_dict():
    global author_analysis
    author_analysis = {
        'date_review_posted': [],
        'review_title': [],
        'review': [],
        'verified_purchase': [],
        'people_find_helpful': [],
        'ratings': [],
        'product_url': [],
        'start': [],
        'end': []
    }


def add_to_dict(date, title, ratings, review, verified_purchase, helpful, url, start, end):
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
    url: string
        product url of the review
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
    author_analysis['product_url'].append(url)
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
        #initialize the dictionary
        print(url)
        initialize_dict()
        
        # url = 'https://www.amazon.ca/gp/profile/amzn1.account.AE3X4B27XTAPBJLVXZX4YVM6KPBQ/ref=cm_cr_dp_d_gw_tr?ie=UTF8'
        driver.get(url)

        # setup all configurations defined in AmazonConfig file
        configuration = config.AuthorConfiguration()

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
            path = 'div.a-section.profile-at-content > p > a'
            try:
                more_review = review.find_element_by_css_selector(path)
            except NoSuchElementException:
                print('Unable to locate the element (path can be wrong)')
                driver.quit()
                return
            if more_review:
                start = datetime.datetime.now()
                current_window = driver.current_window_handle
                
                if os == 'Windows' or os == 'Linux':
                    more_review.send_keys(Keys.CONTROL + Keys.ENTER)  # open link in new tab keyboard shortcut
                else:
                    more_review.send_keys(Keys.COMMAND + Keys.ENTER)
                WebDriverWait(driver, 10).until(ec.number_of_windows_to_be(2))
                driver.switch_to.window(driver.window_handles[1])  # new tab is at index 1

                time.sleep(random.randint(4, 7))
                # extract info
                url = configuration.get_product_url(driver)
                date = configuration.get_posted_date(driver)
                title = configuration.get_title(driver)
                ratings = configuration.get_ratings(driver)
                review = configuration.get_reviews(driver)
                verified_purchase = configuration.is_verified_purchase(driver)
                helpful = configuration.get_helpful_count(driver)
                end = datetime.datetime.now()
                # store to dictionary
                add_to_dict(date, title, ratings, review, verified_purchase, helpful, url, start, end)
                time.sleep(3)
                driver.close()  # closes new tab
                try:
                    WebDriverWait(driver, 10).until(ec.number_of_windows_to_be(1))
                except TimeoutException:
                    print('time out occurred')
                    return
                driver.switch_to.window(current_window)

        if len(author_analysis['review']) > 0:
            df = pd.DataFrame.from_dict(author_analysis)
            df['author'] = author_name
            try:
                df.to_csv(f'{author_name}.csv')
            except Exception as exp:
                print("Permission denied, if the file already exist then delete first")
                print(exp)
                driver.quit()
                return
            print(f'Contents are saved in: {author_name}.csv')
    driver.quit()


def main():
    """
    Main function
    """
    urls = ['https://www.amazon.ca/gp/profile/amzn1.account.AFRS5KMWWN72ZEJE5Y5UL6NVFFXA/ref=cm_cr_arp_d_gw_btm?ie=UTF8']
    extract_author_profile(urls)
    print("Enter the folder path for CSV files:")
    path = input()

    files = glob.glob(r'C:\Users\Raj\Desktop\test\*.csv')
    print(len(files))
    for file in files:
       df = pd.read_csv(file)
       urls = df['author_profile'].dropna().tolist()
       extract_author_profile(urls)

    # extract_author_profile(['https://www.amazon.ca/gp/profile/amzn1.account.AGH7OYWNBYDRL7AN5LTSZ3HIK6LQ/ref=cm_cr_arp_d_gw_btm?ie=UTF8'])

if __name__ == '__main__':
    main()
