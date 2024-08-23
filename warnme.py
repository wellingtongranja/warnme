import argparse
import json
import logging
import os
import warnings
from datetime import datetime
import pytz
from warnme_db import SnowflakeConnector
from warnme_sender import WarnMeSender
from warnme_sms import WarnMeSMS

warnings.filterwarnings("ignore", category=UserWarning, message="pandas only supports SQLAlchemy connectable")

def GetCurrentDateTime():
    local_tz = pytz.timezone('US/Central')
    return datetime.now(local_tz).strftime("%Y%m%d_%H%M%S")

CURRENT_DATETIME = GetCurrentDateTime()

def ConfigureLogger():
    logger = logging.getLogger('WarnMeLogger')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('./logs/warnme.log')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def LoadConfig(file_path, env_prefix):
    config = {}
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                config = json.load(file)
        except Exception as e:
            logging.getLogger('WarnMeLogger').error(f"Error loading config file {file_path}: {e}")
    else:
        for key, value in os.environ.items():
            if key.startswith(env_prefix):
                config_key = key[len(env_prefix):].lower()
                config[config_key] = value
    return config

def LoadFile(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        logging.getLogger('WarnMeLogger').error(f"Error loading file {file_path}: {e}")
        return None

def Main(recipient_emails, subject, query, css_file, template_file, output_folder=None, phone_number=None):
    logger = ConfigureLogger()

    email_config = LoadConfig('./config/sender_config.json', 'EMAIL_')
    db_config = LoadConfig('./config/db_config.json', 'DB_')
    twilio_config = LoadConfig('./config/twilio_config.json', 'TWILIO_')

    if not email_config or not db_config or not twilio_config:
        logger.error("Configuration files are missing or invalid.")
        return

    snowflake_connector = SnowflakeConnector(db_config)
    warnme_sender = WarnMeSender(email_config)
    warnme_sms = WarnMeSMS(twilio_config)

    query_content = LoadFile(query)
    if query_content is None:
        logger.error("Query failed, email will not be sent.")
        return

    df = snowflake_connector.Query(query_content)
    if df is None:
        logger.error("Query execution failed, email will not be sent.")
        return

    if df.empty:
        logger.info("Query result is empty, email will not be sent.")
        return

    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
        query_name = os.path.splitext(os.path.basename(query))[0]
        csv_file_name = f"{query_name}_{CURRENT_DATETIME}.csv"
        csv_file_path = os.path.join(output_folder, csv_file_name)
        df.to_csv(csv_file_path, index=False)
        logger.info(f"Query result saved as CSV to {csv_file_path}")
        attachments = [csv_file_path]
    else:
        attachments = []

    table_html = df.to_html(index=False, escape=False)
    css_styles = LoadFile(css_file)
    email_template = LoadFile(template_file)

    if not css_styles or not email_template:
        logger.error("CSS or template files are missing or invalid.")
        return

    email_body = email_template.replace("{{subject}}", subject).replace("{{table_content}}", table_html)
    email_body = email_body.replace("{{CURRENT_DATETIME}}", CURRENT_DATETIME)
    email_body = email_body.replace('<link rel="stylesheet" href="../css/table_styles.css">', f'<style>{css_styles}</style>')

    for recipient_email in recipient_emails:
        warnme_sender.SendEmail(
            recipient_email, 
            subject, 
            email_body, 
            isHtml=True, 
            attachments=attachments, 
            inlineImages={
                'Header_image': 'template/img/header.png',
                'Footer_image': 'template/img/footer.png'
            }
        )
    
    if phone_number:
        warnme_sms.SendSMS(phone_number, f"You received your {subject} in your e-mail.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send an email using WarnMeSender.")
    parser.add_argument("recipientEmails", help="Comma-separated list of recipient email addresses")
    parser.add_argument("subject", help="The subject of the email")
    parser.add_argument("query", help="The SQL query to execute and include in the email body")
    parser.add_argument("cssFile", help="The CSS file to style the email")
    parser.add_argument("templateFile", help="The HTML template file for the email")
    parser.add_argument("--outputFolder", help="The folder to save the query result as a CSV file", default=None)
    parser.add_argument("--phoneNumber", help="The phone number to send SMS to", default=None)

    args = parser.parse_args()
    recipient_emails = args.recipientEmails.split(',')
    
    Main(recipient_emails, args.subject, args.query, args.cssFile, args.templateFile, args.outputFolder, args.phoneNumber)