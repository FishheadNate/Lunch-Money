#!/usr/bin/env python3
############################################################
# Uses an external yaml file to log into MySchoolBucks.com
# via the SMS message 2-Step Verification option. Then
# navigates to the transaction history page for all linked
# accounts and exports a CSV of the transaction history.
############################################################
import argparse
import csv
import logging
import yaml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def run(args):
    user_creds = yaml.safe_load(open('login_creds.yml'))

    msb_url = user_creds["MySchoolBucks"]["url"]
    msb_email = user_creds["MySchoolBucks"]["email"]
    msb_password = user_creds["MySchoolBucks"]["password"]

    msb_login(msb_url, msb_email, msb_password)

    csv_export(meal_history())

    if input('To log out of MySchoolBucks enter "y": ').lower() == 'y':
        msb_log_out(msb_url)
        driver.quit()


def msb_login(msb_url, msb_email, msb_password):
    driver.get(msb_url)
    login_request = driver.find_element(by=By.ID, value='loginTopLink')
    login_request.click()

    email_field = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(by=By.ID, value='username'))
    password_field = driver.find_element(by=By.ID, value='password')

    email_field.send_keys(msb_email)
    password_field.send_keys(msb_password)
    password_field.send_keys(Keys.ENTER)

    two_step_verification = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(by=By.ID, value='sms'))
    two_step_verification.click()

    login_verification = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(by=By.ID, value='otpCode'))
    login_verification.send_keys(input('MySchoolBucks single-use code: '))
    login_verification.send_keys(Keys.ENTER)


def meal_history():
    driver.get('https://www.myschoolbucks.com/ver2/purchases/getpurchasehistory?requestAction=View&view=all&householdKey=#')
    soup = BeautifulSoup(driver.page_source, 'lxml')
    history = {}

    for i in soup.find_all('div', role='region'):
        student = i.div.h3.get_text()
        logger.info('Gathering meal history for {}'.format(student))
        history[student] = []

        for r in i.find_all('div', class_='row alternate purchase-row'):
            transactions = r.find_all('span', class_='colNormal')
            transaction = {
                "date": transactions[0].get_text().strip(),
                "vendor": transactions[1].get_text().strip(),
                "item": transactions[3].get_text().strip(),
                "payment_method": transactions[4].get_text().strip(),
                "amount": transactions[5].get_text().strip(),
                "balance": transactions[6].get_text().strip()
            }
            history[student].append(transaction)

    return history


def csv_export(meal_history):
    with open('meal_history.csv', 'w', newline='') as dst_file:
        fieldnames = [
            'Student',
            'Date',
            'Vendor',
            'Item',
            'Payment Method',
            'Amount',
            'Balance'
        ]
        writer = csv.DictWriter(dst_file, fieldnames=fieldnames)
        writer.writeheader()
        for student in list(meal_history.keys()):
            for i in meal_history[student]:
                writer.writerow({
                    "Student": student,
                    "Date": i["date"],
                    "Vendor": i["vendor"],
                    "Item": i["item"],
                    "Payment Method": i["payment_method"],
                    "Amount": float(i["amount"].replace('$', '')),
                    "Balance": float(i["balance"].replace('$', ''))
                })


def msb_log_out(msb_url):
    driver.get(msb_url)
    user_menu = driver.find_element(by=By.ID, value='userDropDownMenu')
    user_menu.click()
    log_out = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(by=By.ID, value='userDropDownMenuLogoutMenuItem'))
    log_out.click()


def main():
    parser = argparse.ArgumentParser(description='Opens a new Chrome browser and accesses MySchoolBucks account transactions')
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
