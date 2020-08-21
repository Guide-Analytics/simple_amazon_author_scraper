from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class DriverSetup:
    """
    Selenium web driver setup.

    Attributes
    ----------
    driver : selenium web driver object
        object of webdriver.

    """
    driver = None

    def __init__(self):
        """
        Constructor for webdriver initialisation
        """
        opt = Options()
        # opt.headless = True  # set headless mode to True
        opt.add_argument('--incognito')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=opt)
