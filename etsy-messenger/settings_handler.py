import questionary
import json
import os.path

settings_file_name = "./etsy-messenger/settings.json"

def save_settings():
    headless_choice = questionary.select(
        "Run in headless mode?",
        choices=[
            "Yes",
            "No",
        ]).ask()
    headless = headless_choice == "Yes"

    browser_choice = questionary.select(
        "Which browser do you want to use?",
        choices=[
            "Chrome",
            "Firefox",
        ]).ask()

    preferences = {
        "headless": headless,
        "browser": browser_choice
    }

    with open(settings_file_name, "w") as f:
        json.dump(preferences, f)
    print('Settings saved')

def get_settings():
    if not os.path.exists(settings_file_name):
        save_settings()

    with open(settings_file_name, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    settings = get_settings()
