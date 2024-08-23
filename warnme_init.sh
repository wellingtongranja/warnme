#!/bin/bash

# Function to prompt for input and mask sensitive information
prompt_input() {
    local prompt="$1"
    local var_name="$2"
    local is_secret="$3"

    if [ "$is_secret" = true ]; then
        read -s -p "$prompt: " input
        echo
    else
        read -p "$prompt: " input
    fi

    export $var_name="$input"
    echo "$var_name=\"$input\"" >> .env
}

# Clear the .env file
> .env

# Prompt for EMAIL configuration
echo "Please enter the EMAIL configuration:"
prompt_input "SMTP Server" "WARNME_EMAIL_SMTP_SERVER" false
prompt_input "SMTP Port" "WARNME_EMAIL_SMTP_PORT" false
prompt_input "Sender Email" "WARNME_EMAIL_SENDER_EMAIL" false
prompt_input "Sender Password" "WARNME_EMAIL_SENDER_PASSWORD" true

# Prompt for DB configuration
echo "Please enter the DB configuration:"
prompt_input "DB User" "WARNME_DB_USER" false
prompt_input "DB Password" "WARNME_DB_PASSWORD" true
prompt_input "DB Account" "WARNME_DB_ACCOUNT" false
prompt_input "DB Warehouse" "WARNME_DB_WAREHOUSE" false
prompt_input "DB Database" "WARNME_DB_DATABASE" false
prompt_input "DB Schema" "WARNME_DB_SCHEMA" false
prompt_input "DB Role Name" "WARNME_DB_ROLENAME" false

# Prompt for TWILIO configuration (optional)
read -p "Do you want to configure Twilio? (y/n): " configure_twilio
if [ "$configure_twilio" = "y" ]; then
    echo "Please enter the TWILIO configuration:"
    prompt_input "Twilio Account SID" "WARNME_TWILIO_ACCOUNT_SID" false
    prompt_input "Twilio Auth Token" "WARNME_TWILIO_AUTH_TOKEN" true
    prompt_input "Twilio From Phone Number" "WARNME_TWILIO_FROM_PHONE_NUMBER" false
fi

echo "Environment variables set and saved to .env file."