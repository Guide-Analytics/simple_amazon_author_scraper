from selenium.common.exceptions import NoSuchElementException


class AuthorConfiguration:
    """
    get_author_name():
        Get the name of author
    get_posted_date():
        Get the date a review was posted
    get_title():
        Get the title of review
    get_ratings():
        Get ratings for a review
    get_reviews():
        Get review text
    get_helpful_count():
        Get the count of helpful votes for a review
    is_verified_purchase():
        Check whether review is described verified_purchased or not
    get_product_url():
        Get the url of the sub product.
    get_profile_image():
        Get the profile image of the author.
    get_cover_image():
        Get the cover image of the author.
    get_category():
        Get category of the product.
    getPageContent():
        Retrieve the info about brand and rank.
    getReviewer():
        Gives the name of the reviewer.
    getRatings():
        Gives the ratings associated with the review.
    getDate():
        Gives the date of review posted.
    isVerifiedPurchase():
        Check if the product is verified_purchased or not.
    getReview():
        Get the reviews.
    peopleFindHelpful():
        Get count of people find the review helpful.
    getReviewTitle():
        Get the title of the review.
    getProductName():
        Get the name of the product.
    getAuthorProfile():
        Get the url of the author to scrape.
    get_summary_table():
        Gives table with brand name.
    get_brand():
        If brand is not present in get_summary_table(), then this function will check.
    get_extra_info():
        Gives table with rank of the product.
    get_rank():
        If rank is not present in get_extra_info(), then this function will check.
    """

    def get_author_name(self, driver):
        """
        Get the name of the author.

        Parameters
        ----------
        driver : selenium web driver object
            object of webdriver.
        Returns
        -------
        name: string
            name of the author
        """
        path = '#customer-profile-name-header > div.a-row.a-spacing-none.name-container > span'
        try:
            name = driver.find_element_by_css_selector(path).text

            return name
        except NoSuchElementException:
            return ""

    def get_posted_date(self, driver):
        """
        Get the date the review was posted.

        Parameters
        ----------
        driver : selenium web driver object
            object of webdriver.
        Returns
        -------
        date: string
            date the review was posted
        """
        # path = 'div.a-profile-content > span.a-profile-descriptor' # if no more reviews
        path = '//span[@data-hook="review-date"]'
        try:
            # date = driver.find_element_by_css_selector(path).text
            date = driver.find_element_by_xpath(path).text
            date = date.split()[-3:]
            date = ' '.join(map(str, date))

            return date
        except NoSuchElementException:
            print("No date found...")
            return ""

    def get_title(self, driver):
        """
        Title of the review.

        Parameters
        ----------
        driver : selenium web driver object
            object of webdriver.
        Returns
        -------
        title: string
            title related to a review
        """

        # path = '#profile-at-card-container div.a-section.a-spacing-none span '
        path = '//a[@data-hook="review-title"]'
        try:
            # title = driver.find_element_by_css_selector(path).text
            title = driver.find_element_by_xpath(path).text

            return title
        except NoSuchElementException:
            print("No title found...")
            return ""

    def get_ratings(self, driver):
        """
        Ratings for a review.

        Parameters
        ----------
        driver : selenium web driver object
            object of webdriver.
        Returns
        -------
        rating: string
            ratings related to a review
        """
        path = '.a-link-normal'
        try:
            rating = driver.find_element_by_css_selector(path).get_attribute('title')
            rating = rating.split()[0]

            return rating
        except NoSuchElementException:
            return ""

    def get_reviews(self, driver):
        """
        Get the review.

        Parameters
        ----------
        driver : selenium web driver object
            object of webdriver.
        Returns
        -------
        review: string
            review posted
        """
        path = '//span[@data-hook="review-body"]'
        try:
            review = driver.find_element_by_xpath(path).text
            return review
        except NoSuchElementException:
            return ""

    def get_helpful_count(self, driver):
        """
        Number of people found a review helpful.

        Parameters
        ----------
        driver : selenium web driver object
            object of webdriver.
        Returns
        -------
        count: string
            number of people found helpful
        """
        path = 'span.cr-vote > div.a-row.a-spacing-small > span'
        try:
            text = driver.find_element_by_css_selector(path).get_attribute('textContent')
            count = text.split()[0]
            return count
        except NoSuchElementException:
            return 0

    def is_verified_purchase(self, driver):
        """
        Check review is verified_purchased or not
        Parameters
        ----------
        driver : selenium web driver object
            object of webdriver.
        Returns
        -------
        check: string
            whether review is labeled Verified_purchased or not
        """
        path = '//span[@data-hook="avp-badge"]'
        try:
            check = driver.find_element_by_xpath(path).text

            return "yes"
        except NoSuchElementException:
            return "no"

    def get_product_url(self, driver):
        """
        get product url
        Parameters
        ----------
        driver : selenium web driver object
            object of webdriver.
        Returns
        -------
        url: string
            url of the product
        """
        path = '//a[@data-hook="product-link"]'
        try:
            url = driver.find_element_by_xpath(path).get_attribute('href')
            return url
        except NoSuchElementException:
            return ""

    def get_profile_image(self, driver):
        """
        retrieve path of profile picture of the reviewer
        Parameters
        ----------
        driver : selenium web driver object
            object of webdriver.
        Returns
        -------
        img: string
            source path of image
        """
        path = '//*[@id="avatar-image"]'
        try:
            img = driver.find_element_by_xpath(path).get_attribute('src')
            return img
        except NoSuchElementException:
            return ""

    def get_cover_image(self, driver):
        """
        retrieve path of cover picture of the reviewer
        Parameters
        ----------
        driver : selenium web driver object
            object of webdriver.
        Returns
        -------
        img: string
            source path of image
        """
        path = '//*[@id="cover-image-with-cropping"]'
        try:
            img = driver.find_element_by_xpath(path).get_attribute('src')
            return img
        except NoSuchElementException:
            return ""

    def get_category(self, driver):
        path = '//*[@id="wayfinding-breadcrumbs_feature_div"]/ul'
        try:
            li_list = driver.find_elements_by_xpath(path)
            return li_list
        except NoSuchElementException:
            return False

    """
    *******************************************************************************
    Functions for product scraping (level 3)
    *******************************************************************************
    """

    def getPageContent(self, driver):

        """
        This function finds and return the content of page where all reviews are located.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium

        Returns
        -------
        list
            list of elements attached to the given page
            includes inforation associated with reviews, hyperlinks - See more reviews (from Canada), Next page button
        """
        path = '//div[@id="cm_cr-review_list"]'
        page_content = driver.find_elements_by_xpath(path)
        return page_content

    def getReviewer(self, driver, id):
        """
        This function returns name of a reviewer.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        id : int
            unique id that corresponds to each unique review

        Returns
        -------
        string
            name of reviewer
        """
        path = '#customer_review-' + id + ' div.a-profile-content > span'
        try:
            reviewer = driver.find_element_by_css_selector(path).get_attribute('textContent').split('\n')
            return reviewer[0]
        except NoSuchElementException:
            return False

    def getRatings(self, driver, id):
        """
        This function returns ratings given by a reviewer.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        id : int
            unique id that corresponds to each unique review

        Returns
        -------
        float(or empty if not found)
            ratings given by reviewer
        """
        path = '//*[@id="customer_review-' + id + '"]/div[2]/a[1]'
        try:
            ratings = driver.find_element_by_xpath(path).get_attribute('title')
            ratings = float(ratings[0])
        except NoSuchElementException:
            return ""
        return ratings

    def getDate(self, driver, id):

        """
        This function returns date at which a review was posted by a reviewer

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        id : int
            unique id that corresponds to each unique review

        Returns
        -------
        string
            date a review was posted
        """

        path = '//*[@id="customer_review-' + id + '"]//span[@data-hook="review-date"]'
        message = str(driver.find_element_by_xpath(path).get_attribute('textContent'))
        country = message.split()[2]

        if country.lower() == 'canada':
            message = message.split()[-3:]
            date = ' '.join(map(str, message))
            return date, True
        else:
            print('not canada')
            return message, False

    def isVerifiedPurchase(self, driver, id):

        """
        This function checks whether a product is labeled as Verified Purchase or not.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        id : int
            unique id that corresponds to each unique review

        Returns
        -------
        bool
            True if product is labeled Verified Purchase else False
        """

        path = '//*[@id="customer_review-' + id + '"]/div[3]/span/a/span'
        try:
            isverified = driver.find_element_by_xpath(path).text
            return True
        except NoSuchElementException:
            return False

    def getReview(self, driver, id):

        """
        This function collects the review posted by a reviewer.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        id : int
            unique id that corresponds to each unique review

        Returns
        -------
        string
            review given by a reviewer
        """

        path = '//*[@id="customer_review-' + id + '"]/div[4]/span'
        return driver.find_element_by_xpath(path).text

    def peopleFindHelpful(self, driver, id):

        """
        This function checks the count for number of people who found the review helpful.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        id : int
            unique id that corresponds to each unique review

        Returns
        -------
        string
            number of people found helpful, if none returns empty string
        """

        path = '#customer_review-' + id + ' span.cr-vote > div.a-row.a-spacing-small > span'

        try:
            text = driver.find_element_by_css_selector(path).get_attribute('textContent')
            number = text.split()[0]
            return number
        except NoSuchElementException:
            return 0

    def getReviewTitle(self, driver, id):

        """
        This function gets the review title given by reviewer.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        id : int
            unique id that corresponds to each unique review

        Returns
        -------
        string
            review title given by reviewer
        """

        path = '//*[@id="customer_review-' + id + '"]/div[2]/a[2]/span'
        try:
            review = driver.find_element_by_xpath(path).text
            return review
        except NoSuchElementException:
            return ""

    def getProductName(self, driver):

        """
        This function gets the name of the product.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium

        Returns
        -------
        string
            review name of product
        """

        path = '//*[@id="productTitle"]'
        try:
            name = driver.find_element_by_xpath(path).text
            return name
        except NoSuchElementException:
            return None

    def getAuthorProfile(self, driver, id):

        """
        This function gets the author url.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        id : int
            unique id that corresponds to each unique review

        Returns
        -------
        profile: string
            author profile url
        """
        path = '//*[@id="customer_review-' + id + '"]//div[@data-hook="genome-widget"]/a'
        try:
            profile = driver.find_element_by_xpath(path).get_attribute('href')
            return profile
        except NoSuchElementException:
            return ""

    def get_summary_table(self, driver):
        """
        This function gets the brand of the product.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        Returns
        -------
        table: list of web elements if present or None
            It will return all the content of table
        """
        path = '//*[@id="productDetails_techSpec_section_1"]//tbody/tr'
        try:
            table = driver.find_elements_by_xpath(path)

            return table
        except NoSuchElementException:
            return None

    def get_brand(self, driver):
        """
        This function get the brand name
        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium

        Returns
        -------
        table: list of web elements if present or None
            It will return all the content of table

        """
        path = '//*[@id="detailBullets_feature_div"]//ul/li'
        try:
            table = driver.find_elements_by_xpath(path)
            return table
        except NoSuchElementException:
            return None

    def get_extra_info(self, driver):
        """
        This function gets the table containing rank of the product
        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium

        Returns
        -------
        table: list of web elements if present or None
            It will return all the content of table

        """
        path = '//*[@id="productDetails_detailBullets_sections1"]//tbody/tr'
        try:
            table = driver.find_elements_by_xpath(path)
            return table
        except NoSuchElementException:
            return None

    def get_rank(self, driver):
        """

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium

        Returns
        -------
        rank: string if present or None
            It will return the rank of a product

        """
        path = '//*[@id="SalesRank"]'
        try:
            rank = driver.find_element_by_xpath(path).text
            return rank
        except NoSuchElementException:
            return None