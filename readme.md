# WarnMe Readme.md

- License: GNU General Public License v3.0
- By using this application, you agree to the terms in LICENSE.txt
- Credits: Developed with the support of VSCode and GitHub Copilot

Necessary environment for the WarnMe application: required libraries, necessary directories, template configuration files, and environment variables.

## Prerequisites

- Ensure you have Python 3.x installed on your machine.
- Ensure you have `pip` installed.

## Installation

**Clone the repository or download the script.**
- Clone from Github repository https://github.com/wellingtongranja/warnme.git
- Or visit and download most recent release package at https://github.com/wellingtongranja/warnme/releases

## Usage

### Use Case 1: Local Configuration Setup

To run the setup script and generate local configuration files, execute the following command in your terminal:

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

### Use Case 2:  Environment Variables Setup (Recommended for Serverless Deployments)
To initialize environment variables, execute the following command in your terminal:

```sh
python warnme_init.py
```

This will prompt you to enter the necessary configuration values, which will be stored as environment variables with the WARNME_ prefix.

**Environment Variables**

When using warnme_init.py, the following environment variables will be set:

```
WARNME_EMAIL_SMTP_SERVER
WARNME_EMAIL_SMTP_PORT
WARNME_EMAIL_SENDER_EMAIL
WARNME_EMAIL_SENDER_PASSWORD
WARNME_DB_USER
WARNME_DB_PASSWORD
WARNME_DB_ACCOUNT
WARNME_DB_WAREHOUSE
WARNME_DB_DATABASE
WARNME_DB_SCHEMA
WARNME_DB_ROLENAME
WARNME_TWILIO_ACCOUNT_SID
WARNME_TWILIO_AUTH_TOKEN
WARNME_TWILIO_FROM_PHONE_NUMBER
```

## Notes
Ensure that you have the necessary permissions to create directories and files in the script's directory. If any step fails, the script will print an error message indicating the failure.