import os
import subprocess
import sys

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Successfully installed required libraries.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install required libraries: {e}")

def create_directories():
    directories = ["logs", "config", "script", "css", "template", "output"]
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
        except OSError as e:
            print(f"Failed to create directory {directory}: {e}")

def create_template_config():
    config_templates = {
        "config/email_config.json": """
        {
            "WARNME_EMAIL_SMTP_SERVER": "smtp.example.com",
            "WARNME_EMAIL_SMTP_PORT": 587,
            "WARNME_EMAIL_SENDER_EMAIL": "name@example.com",
            "WARNME_EMAIL_SENDER_PASSWORD": "xxx xxx xxx xxx"
        }
        """,
        "config/db_config.json": """
        {
            "WARNME_DB_USER": "your_snowflake_user",
            "WARNME_DB_PASSWORD": "your_snowflake_password",
            "WARNME_DB_ACCOUNT": "your_snowflake_account",
            "WARNME_DB_WAREHOUSE": "your_snowflake_warehouse",
            "WARNME_DB_DATABASE": "your_snowflake_database",
            "WARNME_DB_SCHEMA": "your_snowflake_schema",
            "WARNME_DB_ROLENAME": "your_snowflake_rolename"
        }
        """,
        "config/twilio_config.json": """
        {
            "WARNME_TWILIO_ACCOUNT_SID": "your_twilio_account_sid",
            "WARNME_TWILIO_AUTH_TOKEN": "your_twilio_auth_token",
            "WARNME_TWILIO_FROM_PHONE_NUMBER": "your_twilio_from_phone_number"
        }
        """
    }

    for path, template in config_templates.items():
        try:
            with open(path, "w") as config_file:
                config_file.write(template.strip())
            print(f"Created template configuration file at {path}")
        except IOError as e:
            print(f"Failed to create configuration file {path}: {e}")

def main():
    install_requirements()
    create_directories()
    create_template_config()

if __name__ == "__main__":
    main()