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
        "config/sender_config.json": """
        {
            "smtp_server": "smtp.example.com",
            "smtp_port": 587,
            "sender_email": "name@example.com",
            "sender_password": "xxx xxx xxx xxx"
        }
        """,
        "config/db_config.json": """
        {
            "user": "your_snowflake_user",
            "password": "your_snowflake_password",
            "account": "your_snowflake_account",
            "warehouse": "your_snowflake_warehouse",
            "database": "your_snowflake_database",
            "schema": "your_snowflake_schema",
            "rolename": " your_snowflake_rolename"
        }
        """,
        "config/twilio_config.json": """
        {
            "account_sid": "your_twilio_account_sid",
            "auth_token": "your_twilio_auth_token",
            "from_phone_number": "your_twilio_from_phone_number"
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
