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
