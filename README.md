![graphic](./assets/repo-graphic.jpg)

# Etsy Messenger | Thank your customers every time
Message your new customers right away to secure star seller message status, and get more 5-star reviews! 🌟🌟🌟🌟🌟

This script uses Selenium to log into your Etsy (with optional 2FA handling), check your 50 most recent order for messages, and if they don't have a message history, message the user a thank-you!

## Overview
As an Etsy seller, star seller status is very important. To be a star seller you need to reply to your customers messages in a timeline manner, and maintain a high review rating. But what if you could message your customers first to ensure you have always messaged them in time? And what if frustrated customers already had a conversation going with you, so they can resolve their issues before leaving a review? Enter the Etsy Messenger Program.

![Script running](./assets/script-running.gif)


## Usage
To utilize this project, clone the repository, then do the following

```
cd etsy-messenger
python3 etsy-messenger/
ENTER YOUR USERNAME
ENTER YOUR PASSWORD
ENTER YOUR 2FA BASE32 STRING
```
### Please Note
Either Firefox or Chrome **must** be installed to use this program.
#### Security
Your 2FA Base32 string can be found by opening your 2FA app, selecting Etsy, and clicking "View Secret".
Your username, password, and 2FA code are crucial pieces of information to the security of your Etsy account. If they are exposed to the public, your Etsy account is at **severe risk**.
The program stores your credentials in a pickle file, but while they are not stored in plain text, they are easily decrypted if exposed. Use at your own risk.

### Custom Messages
By default, the script runs with the following message sent to new customers:
```
Hi there, thanks for you purchase!

If you have any questions, please reach out to me as I want to make sure you have an awesome experience.

If you like this product, please consider giving me a 5 star review!
```

You can create a custom message by adding a "message-custom.txt" file in the etsy-messenger folder. The contents of that file will be sent to your customers instead of the default message.

### Automation
This project is built to be run at least once manually, then it can be set up as a CRON job to run daily. If running as an automated task, I recommend running saving the setting for headless mode.

## Warning
Utilizing this script too frequently will flag your IP for captcha review. This means Google Captchas will be much longer, and be required on each login of any website. This will resolve in a few days, but while active it breaks this script.
To avoid this issue, run the script only a few times a day at maximum.