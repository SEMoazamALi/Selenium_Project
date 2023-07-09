from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("http://books.toscrape.com")

book_links = driver.find_elements(By.XPATH, "//h3/a")

for link in book_links:
    book_url = link.get_attribute("href")

    driver.get(book_url)

    title = driver.find_element(By.XPATH, "//h1").text
    description = driver.find_element(By.XPATH, "//article/p").text

    print("Title:", title)
    print("Description:", description)
    print("------------------")

driver.quit()
