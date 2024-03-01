import sys
import time
from colorama import init
init(strip=not sys.stdout.isatty())
from termcolor import cprint 
from pyfiglet import figlet_format

import credential_handler
import etsy_handler

def main():
    cprint(figlet_format('ETSY', font='roman'), 'white', 'on_red', attrs=['bold'])
    cprint(figlet_format('Thanks Bot', font='speed'), 'white', 'on_red', attrs=['bold'])
    print('By David A Six')
    print('https://www.github.com/davidsix\n\n')

    # Get and set user credentials
    username, password, two_factor = credential_handler.request_credentials()
    # Call the login function
    print('Attempting to log in to Etsy...')
    driver = etsy_handler.login_to_etsy(username, password, two_factor)
    print('Log in Success')
    # Strip the cookies from the driver
    cookies = driver.get_cookies()
    cookies = "; ".join([f"{c['name']}={c['value']}" for c in cookies])

    # Utilize the cookies to get the 50 most recent orders
    print('Finding recent orders...')
    order_ids = etsy_handler.collect_order_ids(cookies)
    print(f"Found {len(order_ids)} orders")
    print('Checking orders for message history...')
    # Check which orders do not have a message history
    orders_without_messages = etsy_handler.find_orders_without_messages(order_ids, cookies)
    print(f"Found {len(orders_without_messages)} orders without messages")
    # orders_without_messages = orders_without_messages[:1]
    
    # Send a message to the orders without message history
    etsy_handler.send_messages(orders_without_messages, driver)
    print('Script complete, thanks for using the Etsy Message Bot!')
    time.sleep(5)
    driver.quit()
    exit()

if __name__ == "__main__":
    main()