import os
import base64
import random
import questionary
import pyotp

def get_two_factor(two_factor_base32):
    def is_base32(s):
        try:
            base64.b32decode(s)
            return True
        except:
            return False

    if (len(two_factor_base32) % 8):
        tfa_missing_len = 8 - (len(two_factor_base32) % 8)
        two_factor_base32 = two_factor_base32 + ('=' * tfa_missing_len)

    if not is_base32(two_factor_base32):
        print("Invalid base32")
        return False
    
    print('Base32 2FA code parsed')    
    totp = pyotp.TOTP(two_factor_base32)
    return totp.now()

def request_credentials():
    try:
        if os.path.exists('./etsy-messenger/.privatedata'):
            return load_credentials()
        
        username = questionary.text("Please enter your username").ask()
        password = questionary.password("Please enter your password").ask()
        use_2fa = questionary.select("Do you use 2FA?", choices=["Yes", "No"]).ask() == 'Yes'
        
        if use_2fa:
            tfa_token = questionary.text("Please enter your TFA Secret Key (Should be a long base32 string)").ask()
        else:
            tfa_token = None
        store_credentials(username, password, tfa_token)
        return username, password, tfa_token
    except Exception as e:
        print('Error requesting credentials:\n', e)
        exit()

# While peppering doesn't add much security, it makes the credentials at rest slightly harder to access.
def add_pepper(string):
    pepper = chr(random.randint(0, 61))  # 0-9, A-Z, a-z
    return string + pepper

def store_credentials(username, password, tfa_code=None):
    try:
        if (not username or not password):
            raise Exception('Username and password are required')
        encoded_username = base64.b64encode(add_pepper(username).encode()).decode()
        encoded_password = base64.b64encode(add_pepper(password).encode()).decode()
        encoded_tfa_code = base64.b64encode(add_pepper(tfa_code).encode()).decode() if tfa_code else None
        # Store the encoded credentials in a plain text file
        with open('./.privatedata', 'w') as f:
            f.write(encoded_username + ',')
            f.write(encoded_password + ',')
            f.write(encoded_tfa_code) if tfa_code else None
    except Exception as e:
        print('Error storing credentials:\n', e)
        exit()

def load_credentials():
    # Check if the file exists
    try:
        if not os.path.exists('./etsy-messenger/.privatedata'):
            raise Exception('No credential file found')
        with open('./etsy-messenger/.privatedata', 'r') as f:
            encoded_username, encoded_password, tfa_code = f.read().split(',')
        username = base64.b64decode(encoded_username).decode()[:-1]
        password = base64.b64decode(encoded_password).decode()[:-1]
        tfa_code = base64.b64decode(tfa_code).decode()[:-1] if tfa_code else None

        return username, password, tfa_code
    except Exception as e:
        print('Error loading credentials:\n', e)
        exit()

