from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException  # Import the exception
import re
from time import sleep

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("headless")
# chrome_options.add_argument("--ignore-certificate-errors")

main_url = "https://www.the-numbers.com/movie/budgets/all"
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
driver.maximize_window()
all_movie = []

# 
for page_number in ["", "/101", "/201", "/301", "/401", "/501", "/601", "/701", "/801", "/901"]:

    url = main_url + page_number
    driver.get(url)
    sleep(2)

    table = driver.find_element(By.CSS_SELECTOR, 'table')
    rows = table.find_elements(By.CSS_SELECTOR, 'table tbody tr')
    del rows[0]
    # no_movies = 0
    # movie_in = []
    for row in rows[:100]:
        re_date = row.find_element(By.CSS_SELECTOR, 'td a').text
        movie = row.find_element(By.CSS_SELECTOR, 'td b').text
        production_budget = row.find_element(By.CSS_SELECTOR, 'td.data:nth-of-type(4)').text
        domestic_gross = row.find_element(By.CSS_SELECTOR, 'td.data:nth-of-type(5)').text
        worldwide_gross = row.find_element(By.CSS_SELECTOR, 'td.data:nth-of-type(6)').text
        link_element = row.find_element(By.CSS_SELECTOR, 'td b a')
        link_url = link_element.get_attribute("href")
        # print(link_url)
        driver.execute_script("window.open(arguments[0]);", link_url)
        windows = driver.window_handles
        driver.switch_to.window(windows[1])
        sleep(1)
        try:
            source = driver.find_element(By.XPATH, "//*[@id='summary']/table[3]/tbody/tr[td[b[contains(text(), 'Source:')]]]/td[2]").text
        except NoSuchElementException:
            source = ""
        try:
            production_company = driver.find_element(By.XPATH,"//*[@id='summary']/table[3]/tbody/tr[td[b[contains(text(), 'Production/Financing Companies:')]]]/td[2]").text
        except NoSuchElementException:
            production_company = ""
        try:
            production_country = driver.find_element(By.XPATH, "//*[@id='summary']/table[3]/tbody/tr[td[b[contains(text(), 'Production Countries:')]]]/td[2]").text
        except NoSuchElementException:
            production_country = ""
        try:
            production_method = driver.find_element(By.XPATH, "//*[@id='summary']/table[3]/tbody/tr[td[b[contains(text(), 'Method:')]]]/td[2]").text
        except NoSuchElementException:
            production_method = ""
        try:
            genre = driver.find_element(By.XPATH, "//*[@id='summary']/table[3]/tbody/tr[td[b[contains(text(), 'Genre:')]]]/td[2]").text
        except NoSuchElementException:
            genre = ""
        try:
            language = driver.find_element(By.XPATH,"//*[@id='summary']/table[3]/tbody/tr[td[b[contains(text(), 'Languages:')]]]/td[2]").text
        except NoSuchElementException:
            language = ""
        driver.find_element(By.XPATH,"//a[normalize-space()='Cast & Crew']").click()
        try:
            director = driver.find_element(By.XPATH, "//*[@id='cast-and-crew']/div[table[tbody[tr[td[contains(text(), 'Director')]]]]]/table/tbody/tr[1]/td[1]").text
        except:
            director = ""
        try:
            driver.find_element(By.XPATH, "//a[@id='a_international']").click()
            # WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")[1]))
            sleep(5)
            frames = driver.find_elements(By.TAG_NAME, "iframe")
            # print(len(frames))
            if len(frames) >= 4:
                driver.switch_to.frame(frames[-1])
                # best_performed = driver.find_element(By.XPATH, "//*[local-name()='svg' and @width='720']/*[name()='g'][2]/*[name()='g'][3]/*[name()='g'][8]").text
                att = driver.find_elements(By.XPATH, "//*[local-name()='svg' and @width='720']/*[name()='g'][2]/*[name()='g'][3]/*[name()='g']")
                pattern = re.compile(r'^\$?\d+(\.\d+)?[mk]?$')
                filtered_att = [g.text for g in att if not pattern.match(g.text)]
                best_performed = filtered_att[0]
                driver.switch_to.default_content()
            else: 
                best_performed = ""
        except:
            best_performed = ""
        driver.close()
        driver.switch_to.window(windows[0])
        windows.clear()
        movie_in = list([re_date,movie,production_budget,domestic_gross,worldwide_gross, source,director, production_company,production_country,production_method,genre,language,best_performed])
        # print(movie_in)
        all_movie.append(movie_in)
 
        # print(re_date,movie,production_budget,domestic_gross,worldwide_gross, source, production_company,production_country,production_method,genre,language,best_performed )





    

