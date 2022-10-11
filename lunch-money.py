#!/usr/bin/env python3
###########################################################
# Uses an external yaml file to log into MySchoolBucks.com
# via the SMS message option for 2-Step Verification and
# then navigates to the transaction history page for all
# linked accounts.
###########################################################
import argparse
import logging
import yaml
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

    view_accounts()

    if input('To log out of MySchoolBucks enter "y": ').lower() == 'y':
        msb_log_out()
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


def view_accounts():
    meal_account_menu = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(by=By.ID, value='mealAccountsMenu'))
    meal_account_menu.click()
    meal_history = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(by=By.ID, value='cafeteriaMealHistoryMenuItem'))
    meal_history.click()


def msb_log_out():
    user_menu = driver.find_element(by=By.ID, value='userDropDownMenu')
    user_menu.click()
    log_out = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(by=By.ID, value='userDropDownMenuLogoutMenuItem'))
    log_out.click()


def main():
    parser = argparse.ArgumentParser(description='Opens a new Chrome browser and logs into MySchoolBucks account')
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
