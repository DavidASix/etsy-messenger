import os
import json
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import credential_handler
import settings_handler

def login_to_etsy(username, password, two_factor):
    settings = settings_handler.get_settings()
    if settings['browser'] == 'Chrome':
        browser_options = webdriver.ChromeOptions()
    elif (settings['browser'] == 'Firefox'):
        browser_options = webdriver.FirefoxOptions()
    else:
        print('Browser not found in settings')
        exit()
    browser_options.add_argument('--disable-gpu')
    browser_options.add_argument('--window-size=1280,720')
    if settings['headless']:
        browser_options.add_argument('--headless')
    try:
        if settings['browser'] == 'Chrome':
            print('Initializing Chrome...')
            driver = webdriver.Chrome(options=browser_options)
        elif (settings['browser'] == 'Firefox'):
            print('Initializing Firefox...')
            driver = webdriver.Firefox(options=browser_options)
    except Exception as e:
        print('Error initializing browser: ', e)
        exit()

    # Navigate to Etsy sign-in page
    driver.get('https://www.etsy.com/signin')
    username_field = driver.find_element(By.ID, 'join_neu_email_field')
    password_field = driver.find_element(By.ID, 'join_neu_password_field')
    username_field.clear()
    password_field.clear()
    username_field.send_keys(username)
    password_field.send_keys(password)
    # Find and click login button
    submit = driver.find_element(By.XPATH, "//*[@type='submit'][contains(@value, 'sign-in')]")
    submit.click()
    # Some users will have two factor auth enabled
    # If the two factor auth field is present, enter the code and submit
    try:
        # Wait for up to 15 seconds before throwing a TimeoutException
        two_fa_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, 'twofactor_token'))
        )

        if two_fa_input:
            code = credential_handler.get_two_factor(two_factor)
            two_fa_input.clear()
            two_fa_input.send_keys(code)
            submit_two_fa = driver.find_element(By.NAME, 'submit_attempt')
            submit_two_fa.click()
    except NoSuchElementException:
        print("Two factor auth field not found")
    except TimeoutException:
        print("Two factor auth timeout exception")
    except Exception as e:
        print('Error: ', e)
    
    # Check tha you are logged in on the home screen
    try:
        # Wait for up to 15 seconds before throwing a TimeoutException
        home_indicator_xpath = "//a[starts-with(@href, 'https://www.etsy.com/ca/your/shops/me/dashboard')]"
        home_indicator = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, home_indicator_xpath))
        )

        if home_indicator:
            print('Logged in')
            return driver
    except NoSuchElementException:
        print('Could not find home element')
    except TimeoutException:
        print("Login to home timeout exception")
    except Exception as e:
        print('Error: ', e)

def collect_order_ids(cookies):
    headers = {"Cookie": cookies}
    api_url = "https://www.etsy.com/api/v3/ajax/bespoke/shop/27751468/mission-control/orders?filters[order_state_id]=1029105132393&limit=50&sort_by=ship_date&sort_order=desc"
    response = requests.get(api_url, headers=headers)
    orders = response.json()['order_ids']
    return orders

def find_orders_without_messages(order_ids, cookies):
    headers = {"Cookie": cookies}
    orders_without_messages = []
    for order_id in order_ids:
        url = f"https://www.etsy.com/api/v3/ajax/shop/27751468/mission-control/orders/convos/{order_id}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = json.loads(response.content)
            if not data["messages"]:
                orders_without_messages.append(order_id)
    return orders_without_messages

def find_element(driver, time, by, value):
    try:
        # Wait for up to 15 seconds before throwing a TimeoutException
        elm = WebDriverWait(driver, time).until(
            EC.presence_of_element_located((by, value))
        )

        if elm:
            return elm
    except NoSuchElementException:
        print('Could not find home element')
        exit()
    except TimeoutException:
        print("Login to home timeout exception")
        exit()
    except Exception as e:
        print('Error: ', e)
        exit()

def send_messages(order_ids, driver):
    i = 1
    for order_id in order_ids:
        driver.get(f"https://www.etsy.com/your/orders/sold/completed?order_id={order_id}")
        message_button = find_element(driver, 10, By.XPATH, "//button//span[contains(text(), 'Message buyer')]/..")
        message_button.click()

        # Wait for the message textarea to be visible and focusable
        textarea = find_element(driver, 10, By.NAME, "message")
        # Get message text
        
        if os.path.isfile('message-custom.txt'):
            print('Using custom message')
            with open('message-custom.txt', 'r') as file:
                message = file.read()
        else:
            print('Using default message')
            with open('message-default.txt', 'r') as file:
                message = file.read()
        # Send some text to the message textarea
        textarea.send_keys(f'\n{message}')
        # This text area is not a basic html form, and relies on javascript to dispatch an event
        # Because of this, after entering text, we need to dispatch an event to let the page know that the text has been entered
        driver.execute_script("arguments[0].dispatchEvent(new Event('input'))", textarea)
        time.sleep(3)
        exit()
        # Wait for the Send button to be visible and clickable
        send_button = find_element(driver, 10, By.XPATH, "//button[text()='Send']")
        # Click the Send button
        send_button.click()
        print(f'Message {i} sent!')
        i += 1
        time.sleep(10)
