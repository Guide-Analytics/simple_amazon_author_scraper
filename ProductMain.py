"""
This file will scrape each reviews of the sub-product reviewed
by an author.
Contents are read from 'reviewers/'
Contents are saved as CSV to 'reviews/'
"""



import time
import datetime
import random
import pandas as pd

import AuthorProfileConfig as config
import DriverSetup as setup
from selenium.common.exceptions import NoSuchElementException

from platform import system  # to check os

configuration = None  # AuthorProfileConfig variable declaration

os = system()  # get the os

amazon_reviews = {}  # dict to store reviews

flag = True  # to collect reviews within canada only


# dictionary to store fields
def initialize_dict():
    global amazon_reviews
    amazon_reviews = {
        'subproduct_author_id': [],
        'verified_purchase': [],
        'review_title': [],
        'reviews': [],
        'date': [],
        'reviewer_name': [],
        'ratings': [],
        'people_find_helpful': [],
        'reviewer_profile_url': [],
        'start_time': [],
        'end_time': []
    }


def add_to_dict(id, reviewer, review, review_title, ratings, author_profile, date, verified_purchase, number, start,
                end):
    """
    Store data to dictionary

    Attributes
    ----------
    id: string
        unique id of reviewer
    review: string
        review posted by author
    start: datetime
        start time for extracting a review
    end: datetime
        time extraction process ends for a review
    """

    amazon_reviews['subproduct_author_id'].append(id)
    amazon_reviews['reviewer_profile_url'].append(author_profile)
    amazon_reviews['reviewer_name'].append(reviewer)
    amazon_reviews['date'].append(date)
    amazon_reviews['ratings'].append(ratings)
    amazon_reviews['reviews'].append(review)
    amazon_reviews['people_find_helpful'].append(number)
    amazon_reviews['review_title'].append(review_title)
    amazon_reviews['verified_purchase'].append(verified_purchase)
    amazon_reviews['start_time'].append(start)
    amazon_reviews['end_time'].append(end)


# check if all reviews are not loaded, them load them first
def checkMoreReviews(driver):
    """
    This function checks if main page contains more reviews to load before scraping

    Parameters
    ----------
    driver : selenium webdriver object
        web driver of selenium

    Returns
    -------
    bool
        True if contains more reviews else False
    """

    try:
        isMoreReviews = driver.find_element_by_partial_link_text('See all reviews')
        if isMoreReviews:
            isMoreReviews.click()
            time.sleep(3)
            return True
    except:
        print('no link to see more reviews')
        return False


# fetch reviews and store in a dictionary
def getReviews(driver):
    """
    This function collects all reviews and stores in dictionary

    Parameters
    ----------
    driver : selenium webdriver object
        web driver of selenium

    """
    global flag

    all_reviews = configuration.getPageContent(driver)
    for rev in all_reviews:
        #     print(rev.text)
        id = rev.find_elements_by_xpath('//div[@data-hook="review"]')
        for i in id:
            unique_id = i.get_attribute('id')
            start = datetime.datetime.now()
            reviewer = configuration.getReviewer(i, unique_id)
            if reviewer:

                date, flag = configuration.getDate(i, unique_id)
                if not flag:
                    return
                ratings = configuration.getRatings(i, unique_id)
                review = configuration.getReview(i, unique_id)
                number = configuration.peopleFindHelpful(i, unique_id)
                verified_purchase = configuration.isVerifiedPurchase(i, unique_id)
                review_title = configuration.getReviewTitle(i, unique_id)
                author_profile = configuration.getAuthorProfile(i, unique_id)
                id = author_profile.split('/')[-2]
                id = id.split('.')[-1]
                end = datetime.datetime.now()
                add_to_dict(id, reviewer, review, review_title, ratings, author_profile, date, verified_purchase,
                            number, start, end)

            else:
                print('no reviews to collect')
                flag = False
                return


def totalReviews(driver):
    """
    Get total reviews in Canada

    Parameters
    ----------
    driver : selenium webdriver object
        web driver of selenium

    Returns
    -------
    reviews : string
        Total reviews in Canada if reviews are found or False
    """
    path = '#filter-info-section > span';
    try:
        reviews = driver.find_element_by_css_selector(path).text
        print(reviews)
        reviews = reviews.split()[-2]
        reviews = reviews.replace(',', '')
        print(reviews)
        return reviews
    except:
        return False


# reinitiate driver if all reviews are not fetched and an error occurs
def reinitiate(driver, url):
    """
    This function reinitiates web driver object if some error occurs while
    scraping reviews

    Parameters
    ----------
    driver : selenium webdriver object
        web driver of selenium
    url : string
        url of the page from where to begin with

    Returns
    -------
    driver : selenium webdriver object
        web driver of selenium
    """

    driver.quit()
    driver = setup.SetupDriver().driver
    driver.get(url)
    return driver


# refresh when an error occurs and all reviews are not extracted
def extractReviews(driver):
    """
    This function made necessary calls to collect all the reviews

    Parameters
    ----------
    driver : selenium webdriver object
        web driver of selenium

    """

    global flag
    # if no reviews are collected, then expand all the reviews
    # and extract each page.
    if len(amazon_reviews['reviewer_name']) == 0:
        checkMoreReviews(driver)  # this will expand all the reviews
        getReviews(driver)
        if len(amazon_reviews['reviewer_name']) == 0:
            return

    else:
        # random refresh if gets blocked while scraping
        try:
            print("--------refreshing page to load ---------------------")
            driver.refresh()
            time.sleep(random.randint(2, 6))
            getReviews(driver)
        except:
            driver.refresh()
            time.sleep(random.randint(2, 6))
            getReviews(driver)

    while True:
        try:
            # if reviews are outside of Canada, then discontinue
            if not flag:
                print('other countries reviews')
                return
            # check if reviews are present on next page, by clicking button
            next_button = driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a')
            next_button.click()
            time.sleep(random.randint(2, 6))
            getReviews(driver)
        except:
            return
    # extractReviews(driver)


def extract_product(df):
    """
    extract information (all reviews) about an author

    Parameters
    ----------
    df: pandas data frame
        dataframe related to an author profile
    """
    # remove the main product
    df = df[~(df['subproduct_id'] == df['product_id'])]
    try:
        product_category = df['product_category'].dropna().unique()[0]  # if product category is null then return
        # empty string
    except IndexError:
        product_category = ""
    try:
        product_id = df.product_id.dropna().unique()[0] # if product category is null then return
        # empty string
    except IndexError:
        product_id = ""
    # pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\Raj\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

    global configuration
    driver = setup.DriverSetup().driver  # initialize the web driver instance

    # setup all configurations defined in AmazonConfig file
    configuration = config.AuthorConfiguration()  # initialize the config file object
    # load the url from csv
    initialize_dict()  # initialize the dictionary to store the data
    print(df.shape)
    dataframe = None  # this will contain the result of all sub-products related to an author
    for data in df.itertuples():
        url = data.product_url  # get the url of sub-product

        # initialize the dictionary
        initialize_dict()
        print('-----------------------------')
        print('take new url')
        print('-----------------------------')
        driver.get(url)
        time.sleep(4)
        k = 0
        prod_name = configuration.getProductName(driver)  # retrieves product name
        # if page is not loaded properly, try to refresh for
        # at most 3 times. If page is not loaded, then extract other url
        # 'cause may be the given url is not working or broken
        while not prod_name:
            if k > 3:
                break
            driver.refresh()
            time.sleep(4)
            prod_name = configuration.getProductName(driver)
            k += 1

        product_info = configuration.get_summary_table(driver)  # table where brand and rank are specified

        brand = []
        # brand name can be found in one of the two different tables.
        # if not found in 1st scenario below, then check for other table
        for i in product_info:
            row = i.find_element_by_xpath('th').text.lower().strip()
            if (row is not None) and (row == "brand"):
                brand.append(i.find_element_by_xpath('td').text)
        # 2nd scenario to get brand name
        if len(brand) == 0:
            rows = configuration.get_brand(driver)
            if rows is not None:
                for row in rows:
                    try:
                        bname = row.find_element_by_xpath('span/span[1]').text.lower()
                    except NoSuchElementException:
                        continue
                    if (bname is not None) and (
                            (('manufacturer' in bname) and len(bname.split()) > 1) or ('brand' in bname)):
                        print(bname)
                        try:
                            bname = row.find_element_by_xpath('span/span[2]').text
                            brand.append(bname)
                            print(brand)
                        except NoSuchElementException:
                            brand = []

        # get the rank of the product
        # rank can be found in one of the two tables:
        # check in 1st table
        extra_info = configuration.get_extra_info(driver)
        rank = []
        for i in extra_info:
            row = i.find_element_by_xpath('th').text.lower().strip()
            if "rank" in row:
                rank.append(i.find_element_by_xpath('td').text)
        # if 1st table is not found, check for 2nd table
        if len(rank) == 0:
            row = configuration.get_rank(driver)
            if row is not None:
                row = row.split('#')[1].split()[0]
                rank.append(row)

        categories = configuration.get_category(driver)
        # check if category belongs to main product category then only scrape
        if categories:
            category = categories[0].text
            if product_category in category:
                sub_name = str(data.subproduct_id)
                extractReviews(driver)  # extract the data
                print('all reviews are collected')
                # if data is collected then save in a pandas data frame
                if len(amazon_reviews['reviews']) > 0:
                    # create data frame
                    frame = pd.DataFrame.from_dict(amazon_reviews)
                    # create extra columns for product name, avg rating and total reviews
                    frame['product_name'] = prod_name  # product name
                    frame['brand_name'] = brand[0] if len(brand) > 0 else ""
                    frame['rank'] = rank[0] if len(rank) > 0 else ""
                    frame['product_id'] = product_id
                    try:
                        frame['author_id'] = df['author_id'].dropna().unique()[0] # if author id is null then
                        # return empty string
                    except IndexError:
                        frame['author_id'] = ""
                    frame['subproduct_id'] = sub_name

                    dataframe = frame if dataframe is None else pd.concat([dataframe, frame])

    driver.quit()
    print(dataframe is None)
    return dataframe


def filter_files():
    """
    This function filter the files that are already processed
    Returns
    -------
    files: list
        list of files not read yet
    """
    import os
    author_files = os.listdir('reviewers')  # author_profile data
    print((author_files[0]))
    prod_files = os.listdir('reviews')  # subproduct data
    print(len(author_files))
    files = list(set(author_files) - set(prod_files))
    print(len(files))
    return files


def save_data(frame, name):
    """
    This function save the content to given file.
    Parameters
    ----------
    frame : pandas data frame
    name : file name to save the content (dataframe)
    """
    print(name)
    if frame is not None:
        frame.to_csv(f"reviews\{name}.csv")


def main():
    """
    Main function
    """
    urls = ""
    # extract_product(['https://www.amazon.ca/Maxpower-Planet-Traffic-Greater-Training/dp/B0749K8SMT?ref=pf_vv_at_pdctrvw_dp&th=1'])

    files = filter_files() # filter the files that are already processed
    # fl = files[0]
    # print(fl)
    path = r"reviewers/"
    for file in files:
        file = file.strip()
        df = pd.read_csv(path+file)
        frame = extract_product(df)
        save_data(frame, file)


if __name__ == '__main__':
    main()
