import os
import getpass

def DisplayHeader():
    header = """
    ===============================================
    |                                             |
    |                WarnMe                       |
    |                                             |
    |  https://github.com/wellingtongranja/warnme |
    |                                             |
    |  For more details, see README.md            |
    |  License: GNU General Public License v3.0   |
    |  By using this application, you agree to    |
    |  the terms in LICENSE.txt                   |
    |                                             |
    |  Credits:                                   |
    |  Developed with the support of VSCode       |
    |  and GitHub Copilot                         |
    ===============================================
    """
    print(header)

def DeleteConfigFiles():
    config_files = [
        './config/sender_config.json',
        './config/db_config.json',
        './config/twilio_config.json'
    ]
    for file_path in config_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted config file: {file_path}")
        except Exception as e:
            print(f"Error deleting config file {file_path}: {e}")

def masked_input(prompt):
    return getpass.getpass(prompt)

def PromptForEmailConfig():
    print("Please enter the EMAIL configuration:")
    os.environ['WARNME_EMAIL_SMTP_SERVER'] = input("SMTP Server: ")
    os.environ['WARNME_EMAIL_SMTP_PORT'] = input("SMTP Port: ")
    os.environ['WARNME_EMAIL_SENDER_EMAIL'] = input("Sender Email: ")
    os.environ['WARNME_EMAIL_SENDER_PASSWORD'] = masked_input("Sender Password: ")

def PromptForDbConfig():
    print("Please enter the DB configuration:")
    os.environ['WARNME_DB_USER'] = input("DB User: ")
    os.environ['WARNME_DB_PASSWORD'] = masked_input("DB Password: ")
    os.environ['WARNME_DB_ACCOUNT'] = input("DB Account: ")
    os.environ['WARNME_DB_WAREHOUSE'] = input("DB Warehouse: ")
    os.environ['WARNME_DB_DATABASE'] = input("DB Database: ")
    os.environ['WARNME_DB_SCHEMA'] = input("DB Schema: ")
    os.environ['WARNME_DB_ROLENAME'] = input("DB Role Name: ")

def PromptForTwilioConfig():
    print("Please enter the TWILIO configuration (optional, press Enter to skip):")
    os.environ['WARNME_TWILIO_ACCOUNT_SID'] = input("Twilio Account SID: ")
    os.environ['WARNME_TWILIO_AUTH_TOKEN'] = masked_input("Twilio Auth Token: ")
    os.environ['WARNME_TWILIO_FROM_PHONE_NUMBER'] = input("Twilio From Phone Number: ")

def InitializeEnvironmentVariables():
    try:
        PromptForEmailConfig()
        PromptForDbConfig()
        if input("Do you want to configure Twilio? (y/n): ").lower() == 'y':
            PromptForTwilioConfig()
    except KeyboardInterrupt:
        print("\nProcess aborted by user.")
        return

def ReadEnvironmentVariables():
    print("Current environment variables:")
    for key, value in os.environ.items():
        if key.startswith('WARNME_'):
            if 'PASSWORD' in key or 'TOKEN' in key:
                print(f"{key}: {'#' * 8}")
            else:
                print(f"{key}: {value}")

def ClearEnvironmentVariables():
    keys_to_clear = [
        'WARNME_EMAIL_SMTP_SERVER', 'WARNME_EMAIL_SMTP_PORT', 'WARNME_EMAIL_SENDER_EMAIL', 'WARNME_EMAIL_SENDER_PASSWORD',
        'WARNME_DB_USER', 'WARNME_DB_PASSWORD', 'WARNME_DB_ACCOUNT', 'WARNME_DB_WAREHOUSE', 'WARNME_DB_DATABASE', 'WARNME_DB_SCHEMA', 'WARNME_DB_ROLENAME',
        'WARNME_TWILIO_ACCOUNT_SID', 'WARNME_TWILIO_AUTH_TOKEN', 'WARNME_TWILIO_FROM_PHONE_NUMBER'
    ]
    for key in keys_to_clear:
        if key in os.environ:
            del os.environ[key]
    print("Environment variables cleared.")

if __name__ == "__main__":
    DisplayHeader()
    if input("Do you agree with the terms in LICENSE.txt? (y/n): ").lower() != 'y':
        print("You must agree with the terms to use this application.")
        exit(1)
    
    while True:
        print("\nOptions:")
        print("1. Initialize environment variables")
        print("2. Read environment variables")
        print("3. Clear environment variables")
        print("4. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            DeleteConfigFiles()
            InitializeEnvironmentVariables()
            print("Environment variables initialized and local config files deleted for serverless deployments.")
        elif choice == '2':
            ReadEnvironmentVariables()
        elif choice == '3':
            ClearEnvironmentVariables()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")