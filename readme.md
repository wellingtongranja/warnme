# WarnMe Setup Script

This script sets up the necessary environment for the WarnMe application by installing required libraries, creating necessary directories, and generating template configuration files.

## Prerequisites

- Python 3.x
- `pip` (Python package installer)

## Installation

1. Clone the repository or download the script.

- Clone from Github repository https://github.com/wellingtongranja/warnme.git
- Or visit and download most recent release package at https://github.com/wellingtongranja/warnme/releases

2. Ensure you have Python 3.x installed on your machine.
3. Ensure you have `pip` installed.

## Usage

To run the setup script, execute the following command in your terminal:

```sh
python warnme_setup.py
```

This will perform the following actions:

1. Install the required libraries specified in requirements.txt.
2. Create the following directories if they do not already exist:
- logs
- config
- script
- css
- template
- output
3. Generate template configuration files in the config directory:
- config/sender_config.json
- config/db_config.json
- config/twilio_config.json

## Configuration
The script generates the following template configuration files:

- config/sender_config.json:
```
{
    "smtp_server": "smtp.example.com",
    "smtp_port": 587,
    "sender_email": "name@example.com",
    "sender_password": "xxx xxx xxx xxx"
}
```
- config/db_config.json:
```
{
    "user": "your_snowflake_user",
    "password": "your_snowflake_password",
    "account": "your_snowflake_account",
    "warehouse": "your_snowflake_warehouse",
    "database": "your_snowflake_database",
    "schema": "your_snowflake_schema",
    "rolename": " your_snowflake_rolename"
}
```
- config/twilio_config.json:
```
{
    "account_sid": "your_twilio_account_sid",
    "auth_token": "your_twilio_auth_token",
    "from_phone_number": "your_twilio_from_phone_number"
}
```
You will need to update these configuration files with your actual credentials and settings.

## Notes
Ensure that you have the necessary permissions to create directories and files in the script's directory.
If any step fails, the script will print an error message indicating the failure.