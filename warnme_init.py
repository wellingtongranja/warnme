import os

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

def InitializeEnvironmentVariables():
    os.environ['EMAIL_SMTP_SERVER'] = 'smtp.example.com'
    os.environ['EMAIL_SMTP_PORT'] = '587'
    os.environ['EMAIL_SENDER_EMAIL'] = 'name@example.com'
    os.environ['EMAIL_SENDER_PASSWORD'] = 'xxx xxx xxx xxx'
    os.environ['DB_USER'] = 'your_snowflake_user'
    os.environ['DB_PASSWORD'] = 'your_snowflake_password'
    os.environ['DB_ACCOUNT'] = 'your_snowflake_account'
    os.environ['DB_WAREHOUSE'] = 'your_snowflake_warehouse'
    os.environ['DB_DATABASE'] = 'your_snowflake_database'
    os.environ['DB_SCHEMA'] = 'your_snowflake_schema'
    os.environ['DB_ROLENAME'] = 'your_snowflake_rolename'
    os.environ['TWILIO_ACCOUNT_SID'] = 'your_twilio_account_sid'
    os.environ['TWILIO_AUTH_TOKEN'] = 'your_twilio_auth_token'
    os.environ['TWILIO_FROM_PHONE_NUMBER'] = 'your_twilio_from_phone_number'

if __name__ == "__main__":
    DeleteConfigFiles()
    InitializeEnvironmentVariables()
    print("Environment variables initialized and local config files deleted for serverless deployments")