import os
import base64
import random

def request_credentials():
    if os.path.exists('./.privatedata'):
        return
    
    print("Please enter your username: ")
    username = input()
    
    print("Please enter your password: ")
    password = input()
    
    print("Do you want to use 2FA? (y/n): ")
    use_2fa = input().lower() == 'y'
    
    if use_2fa:
        print("Please enter your 2FA token: ")
        tfa_token = input()
    else:
        tfa_token = None
    
    return username, password, tfa_token

# While peppering doesn't add much security, it makes the credentials at rest slightly harder to access.
def add_pepper(string):
    pepper = chr(random.randint(0, 61))  # 0-9, A-Z, a-z
    return string + pepper

def store_credentials(username, password, tfa_code=None):
    if (not username or not password):
        print("Invalid credentials")
        return
    encoded_username = base64.b64encode(add_pepper(username).encode()).decode()
    encoded_password = base64.b64encode(add_pepper(password).encode()).decode()
    encoded_tfa_code = base64.b64encode(add_pepper(tfa_code).encode()).decode() if tfa_code else None
    # Store the encoded credentials in a plain text file
    with open('./.privatedata', 'w') as f:
        f.write(encoded_username + ',')
        f.write(encoded_password + ',')
        f.write(encoded_tfa_code) if tfa_code else None

def load_credentials():
    # Check if the file exists
    if os.path.exists('./.privatedata'):
        with open('./.privatedata', 'r') as f:
            encoded_username, encoded_password, tfa_code = f.read().split(',')
        username = base64.b64decode(encoded_username).decode()[:-1]
        password = base64.b64decode(encoded_password).decode()[:-1]
        tfa_code = base64.b64decode(tfa_code).decode()[:-1] if tfa_code else None

        return username, password, tfa_code
    else:
        raise Exception('No credential file found')
