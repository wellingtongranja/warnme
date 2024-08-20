import argparse
import json
import logging
import os
from datetime import datetime
import pytz
from warnme_db import SnowflakeConnector
from warnme_sender import WarnMeSender
from warnme_sms import WarnMeSMS

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

def LoadConfig(filePath):
    try:
        with open(filePath, 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.getLogger('WarnMeLogger').error(f"Error loading config file {filePath}: {e}")
        return None

def LoadFile(filePath):
    try:
        with open(filePath, 'r') as file:
            return file.read()
    except Exception as e:
        logging.getLogger('WarnMeLogger').error(f"Error loading file {filePath}: {e}")
        return None

def Main(recipientEmail, subject, query, cssFile, templateFile, outputFolder, phoneNumber):
    logger = ConfigureLogger()

    emailConfigFile = './config/sender_config.json'
    dbConfigFile = './config/db_config.json'
    twilioConfigFile = './config/twilio_config.json'

    emailConfig = LoadConfig(emailConfigFile)
    dbConfig = LoadConfig(dbConfigFile)
    twilioConfig = LoadConfig(twilioConfigFile)

    if not emailConfig or not dbConfig or not twilioConfig:
        logger.error("Configuration files are missing or invalid.")
        return

    snowflakeConnector = SnowflakeConnector(dbConfig)
    warnmeSender = WarnMeSender(emailConfig)
    warnmeSms = WarnMeSMS(twilioConfig)

    queryContent = LoadFile(query)
    if queryContent is None:
        logger.error("Query failed, email will not be sent.")
        return

    df = snowflakeConnector.Query(queryContent)
    if df is None:
        logger.error("Query execution failed, email will not be sent.")
        return

    if df.empty:
        logger.info("Query result is empty, email will not be sent.")
        return

    if outputFolder:
        os.makedirs(outputFolder, exist_ok=True)
        queryName = os.path.splitext(os.path.basename(query))[0]
        csvFileName = f"{queryName}_{CURRENT_DATETIME}.csv"
        csvFilePath = os.path.join(outputFolder, csvFileName)
        df.to_csv(csvFilePath, index=False)
        logger.info(f"Query result saved as CSV to {csvFilePath}")

    tableHtml = df.to_html(index=False, escape=False)
    cssStyles = LoadFile(cssFile)
    emailTemplate = LoadFile(templateFile)

    if not cssStyles or not emailTemplate:
        logger.error("CSS or template files are missing or invalid.")
        return

    emailBody = emailTemplate.replace("{{subject}}", subject).replace("{{table_content}}", tableHtml)
    emailBody = emailBody.replace("{{CURRENT_DATETIME}}", CURRENT_DATETIME)
    emailBody = emailBody.replace('<link rel="stylesheet" href="../css/table_styles.css">', f'<style>{cssStyles}</style>')

    warnmeSender.SendEmail(
        recipientEmail, 
        subject, 
        emailBody, 
        isHtml=True, 
        attachments=[csvFilePath], 
        inlineImages={'header_image': 'template/img/iNFX-APP-Microservices-Icon--EPS.png'}
    )
    
    if phoneNumber:
        warnmeSms.SendSMS(phoneNumber, f"You received your {subject} in your e-mail.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send an email using WarnMeSender.")
    parser.add_argument("recipientEmail", help="The recipient's email address")
    parser.add_argument("subject", help="The subject of the email")
    parser.add_argument("query", help="The SQL query to execute and include in the email body")
    parser.add_argument("cssFile", help="The CSS file to style the email")
    parser.add_argument("templateFile", help="The HTML template file for the email")
    parser.add_argument("outputFolder", help="The folder to save the query result as a CSV file", default=None)
    parser.add_argument("phoneNumber", help="The phone number to send SMS to", default=None)

    args = parser.parse_args()
    
    Main(args.recipientEmail, args.subject, args.query, args.cssFile, args.templateFile, args.outputFolder, args.phoneNumber)
