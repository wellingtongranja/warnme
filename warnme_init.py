import os
import json
import logging
import subprocess

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

def LoadConfig(file_path):
    """Load configuration from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading config file {file_path}: {e}")
        return None

def SetEnvVariables(config, env_prefix):
    """Set environment variables from the config dictionary."""
    for key, value in config.items():
        env_var = f"{env_prefix}{key.upper()}"
        os.environ[env_var] = str(value)

def SetHerokuEnvVariables(config, env_prefix, app_name):
    """Set Heroku environment variables using the Heroku CLI."""
    heroku_path = "C:\\Program Files\\Heroku\\bin\\heroku.cmd"  # Update this path based on the output of `where heroku`
    for key, value in config.items():
        env_var = f"{env_prefix}{key.upper()}={value}"
        try:
            result = subprocess.run([heroku_path, "config:set", env_var, "--app", app_name], check=True, capture_output=True, text=True)
            logging.info(f"Set Heroku env variable: {env_var}")
            logging.info(f"Heroku CLI output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error setting Heroku env variable: {env_var}")
            logging.error(f"Heroku CLI error output: {e.stderr}")
        except FileNotFoundError:
            logging.error("Heroku CLI not found. Please ensure it is installed and added to your PATH.")
            print("Heroku CLI not found. Please ensure it is installed and added to your PATH.")
            return

def ReadHerokuEnvVariables(app_name):
    """Read Heroku environment variables using the Heroku CLI."""
    heroku_path = "C:\\Program Files\\Heroku\\bin\\heroku.cmd"  # Update this path based on the output of `where heroku`
    try:
        result = subprocess.run([heroku_path, "config", "--app", app_name], check=True, capture_output=True, text=True)
        logging.info(f"Heroku env variables for app {app_name}:")
        logging.info(result.stdout)
        print(f"Heroku env variables for app {app_name}:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error reading Heroku env variables for app {app_name}")
        logging.error(f"Heroku CLI error output: {e.stderr}")
    except FileNotFoundError:
        logging.error("Heroku CLI not found. Please ensure it is installed and added to your PATH.")
        print("Heroku CLI not found. Please ensure it is installed and added to your PATH.")

def ClearHerokuEnvVariables(config, env_prefix, app_name):
    """Clear Heroku environment variables using the Heroku CLI."""
    heroku_path = "C:\\Program Files\\Heroku\\bin\\heroku.cmd"  # Update this path based on the output of `where heroku`
    for key in config.keys():
        env_var = f"{env_prefix}{key.upper()}"
        try:
            result = subprocess.run([heroku_path, "config:unset", env_var, "--app", app_name], check=True, capture_output=True, text=True)
            logging.info(f"Cleared Heroku env variable: {env_var}")
            logging.info(f"Heroku CLI output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error clearing Heroku env variable: {env_var}")
            logging.error(f"Heroku CLI error output: {e.stderr}")
        except FileNotFoundError:
            logging.error("Heroku CLI not found. Please ensure it is installed and added to your PATH.")
            print("Heroku CLI not found. Please ensure it is installed and added to your PATH.")
            return

def PrintEnvVariables():
    """Print initialized environment variables."""
    print("Initialized Environment Variables:")
    for key, value in os.environ.items():
        if key.startswith('WARNME_'):
            print(f"{key}: {value}")

def ClearEnvVariables():
    """Clear environment variables that start with 'WARNME_'."""
    keys_to_clear = [key for key in os.environ if key.startswith('WARNME_')]
    for key in keys_to_clear:
        del os.environ[key]
    print("Cleared all WARNME_ environment variables.")

def Main():
    logging.basicConfig(level=logging.DEBUG)
    
    DisplayHeader()
    agree = input("Do you agree to the terms in LICENSE.txt? (yes/no): ")
    if agree.lower() != 'yes':
        print("You must agree to the terms to use this application.")
        return
    
    while True:
        DisplayHeader()
        print("\n= MENU =================================")
        print("1. LOCAL MACHINE: Initialize env. variables (config content)")
        print("2. LOCAL MACHINE: Read env. variables")
        print("3. LOCAL MACHINE: Clear env. variables")
        print("4. HEROKU: Initialize env. variables (config content)")
        print("5. HEROKU: Read env. variables")
        print("6. HEROKU: Clear env. variables")
        print("------------------------------------------------------------------")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Load and set environment variables for email config
            email_config = LoadConfig('./config/email_config.json')
            if email_config:
                SetEnvVariables(email_config, 'WARNME_EMAIL_')
            
            # Load and set environment variables for database config
            db_config = LoadConfig('./config/db_config.json')
            if db_config:
                SetEnvVariables(db_config, 'WARNME_DB_')
            
            # Load and set environment variables for Twilio config
            twilio_config = LoadConfig('./config/twilio_config.json')
            if twilio_config:
                SetEnvVariables(twilio_config, 'WARNME_TWILIO_')
            print("Environment variables initialized.")
        
        elif choice == '2':
            PrintEnvVariables()
        
        elif choice == '3':
            ClearEnvVariables()
        
        elif choice == '4':
            heroku_app_name = input("Enter your Heroku app name: ")
            # Load and set Heroku environment variables for email config
            email_config = LoadConfig('./config/email_config.json')
            if email_config:
                SetHerokuEnvVariables(email_config, 'WARNME_EMAIL_', heroku_app_name)
            
            # Load and set Heroku environment variables for database config
            db_config = LoadConfig('./config/db_config.json')
            if db_config:
                SetHerokuEnvVariables(db_config, 'WARNME_DB_', heroku_app_name)
            
            # Load and set Heroku environment variables for Twilio config
            twilio_config = LoadConfig('./config/twilio_config.json')
            if twilio_config:
                SetHerokuEnvVariables(twilio_config, 'WARNME_TWILIO_', heroku_app_name)
            print("Heroku environment variables initialized.")
        
        elif choice == '5':
            heroku_app_name = input("Enter your Heroku app name: ")
            ReadHerokuEnvVariables(heroku_app_name)
        
        elif choice == '6':
            heroku_app_name = input("Enter your Heroku app name: ")
            # Load and clear Heroku environment variables for email config
            email_config = LoadConfig('./config/email_config.json')
            if email_config:
                ClearHerokuEnvVariables(email_config, 'WARNME_EMAIL_', heroku_app_name)
            
            # Load and clear Heroku environment variables for database config
            db_config = LoadConfig('./config/db_config.json')
            if db_config:
                ClearHerokuEnvVariables(db_config, 'WARNME_DB_', heroku_app_name)
            
            # Load and clear Heroku environment variables for Twilio config
            twilio_config = LoadConfig('./config/twilio_config.json')
            if twilio_config:
                ClearHerokuEnvVariables(twilio_config, 'WARNME_TWILIO_', heroku_app_name)
            print("Heroku environment variables cleared.")
        
        elif choice == '0':
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    Main()