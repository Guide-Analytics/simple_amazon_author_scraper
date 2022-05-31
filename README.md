# Simple Amazon Author Scraper
Install the following packages: <br>
- selenium: To automate scraping. You can download using pip through command line as:
<br><pre><em>pip install selenium</em></pre><br>
- webdriver-manager: Install the chrome driver inplace so no need to download explicitly.
You can download it through command line as:
<br><pre><em> pip install webdriver_manager</em></pre><br>
- pandas: For file manipulation (saving data to csv). You can download using:
<br><pre><em> pip install pandas</em></pre><br>
- word2number: Convert words to numbers. You can download using pip through command line as:
<br><pre><em>pip install word2number</em></pre><br>
Currently this script works on Chrome browser.<br>

File structure:<br>
--AuthorProfileConfigConfig.py: Contains user-defined functions to retrieve data.<br>
--DriverSetup.py: Defines and initiate webdriver object of selenium.<br>
--main.py: Run this file to scrape data for author profile.<br><br>
--ProductMain.py: Run this file to scrape data for all the subprodcuts related to each author.

To run:
- run <em>main.py<em>. Data will be scraped from <em>main_product</em> folder containing all the main product data.<br>
  Data will be stored in <em>reviewers</em> folder.
- run <em>ProductMain.py</em>. Data will be scraped from <em>reviewers</em> folder containing all the author profile data.
  Data will be store in <em>reviews</em> folder.
  For example: \data_scraping_v2\
