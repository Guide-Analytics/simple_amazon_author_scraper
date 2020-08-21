# author_amazon_scrape
Install the following packages: <br>
- selenium: To automate scraping. You can download using pip through command line as:
<br><pre><em>pip install selenium</em></pre><br>
- webdriver-manager: Install the chrome driver inplace so no need to download explicitly.
You can download it through command line as:
<br><pre><em> pip install webdriver_manager</em></pre><br>
- pandas: For file manipulation (saving date to csv). You can download using:
<br><pre><em> pip install pandas</em></pre><br>
Currently this script works on Chrome browser.<br>
File structure:<br>
--AuthorProfileConfigConfig.py: Contains user-defined functions to retrieve data.<br>
--DriverSetup.py: Defines and initiate webdriver object of selenium.<br>
--main.py: Run this file to start scraping.<br><br>

To run:
- run <em>main.py<em> and provide the path for CSVs that contain profile information.<br>
  For example: \data_scraping_v2\
