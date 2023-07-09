import time
import scrapy
import gspread
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('', scope)
client = gspread.authorize(credentials)
sheet = ""
spreadsheet = client.open(sheet)

worksheet = spreadsheet.worksheet('test')

date = datetime.now().date().strftime("%d/%m/%Y")
driver = webdriver.Chrome()


def login():
    driver.get("https://tradingv2.most.co.id/Dashboard/Logon")
    username = driver.find_element(By.ID, 'UserName')
    password = driver.find_element(By.ID, 'Password')
    login_button = driver.find_element(By.NAME, 'btn_login')

    username.send_keys('')
    password.send_keys('')
    login_button.click()


def load_pin():
    driver.get('https://tradingv2.most.co.id/Dashboard/Account/Portfolio')
    driver.find_element(By.ID, 'rdportcashPIN').send_keys('')
    driver.find_element(By.ID, 'rdportcashLOAD').click()


login()
time.sleep(10)
load_pin()
time.sleep(5)
source = driver.page_source

driver.quit()

response = scrapy.Selector(text=source)
headers = ["DATE:", "STOCK", "", "AVG COST", "LAST PRICE", "LOT", "SHARES", "STOCK VALUE", "MARKET VALUE", "GAIN/LOSS",
           "%"]

table = response.css("table[class='table table-blueorange tbl-floatthead']")[1]
data = [
    date,
    table.css("tbody > tr > td:nth-child(1)::text").get('').strip(),
    "Owned",
    table.css("tbody > tr > td:nth-child(2)::text").get('').strip(),
    table.css("tbody > tr > td:nth-child(3)::text").get('').strip(),
    table.css("tbody > tr > td:nth-child(4)::text").get('').strip(),
    table.css("tbody > tr > td:nth-child(5)::text").get('').strip(),
    table.css("tbody > tr > td:nth-child(6)::text").get('').strip(),
    table.css("tbody > tr > td:nth-child(7)::text").get('').strip(),
    table.css("tbody > tr > td:nth-child(8)::text").get('').strip(),
    table.css("tbody > tr > td:nth-child(9)::text").get('').strip(),
]

last_row = len(worksheet.get_all_values()) + 2

table_values = [headers] + [data]

worksheet.insert_row(headers, index=2)
worksheet.insert_row(data, index=3)
empty_rows = [[]] * 5
worksheet.insert_rows(empty_rows, row=4)

