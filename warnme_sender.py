# wanrme_sender.py

import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage

class WarnMeSender:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('WarnMeLogger')

    def SendEmail(self, recipientEmail, subject, body, isHtml=False, attachments=None, inlineImages=None):
        message = MIMEMultipart('related')
        message['From'] = self.config["sender_email"]
        message['To'] = recipientEmail
        message['Subject'] = subject

        msgAlternative = MIMEMultipart('alternative')
        message.attach(msgAlternative)

        if isHtml:
            msgAlternative.attach(MIMEText(body, 'html'))
        else:
            msgAlternative.attach(MIMEText(body, 'plain'))

        # Attach inline images
        if inlineImages:
            self._AttachInlineImages(message, inlineImages)

        # Attach other files
        if attachments:
            self._AttachFiles(message, attachments)

        self._SendSMTPMail(message, recipientEmail)

    def _AttachInlineImages(self, message, inlineImages):
        for cid, filePath in inlineImages.items():
            try:
                with open(filePath, 'rb') as img:
                    mimeImage = MIMEImage(img.read())
                    mimeImage.add_header('Content-ID', f'<{cid}>')
                    mimeImage.add_header('Content-Disposition', 'inline', filename=os.path.basename(filePath))
                    message.attach(mimeImage)
            except Exception as e:
                self.logger.error(f"Failed to attach image {filePath}: {e}")

    def _AttachFiles(self, message, attachments):
        for filePath in attachments:
            try:
                part = MIMEBase('application', 'octet-stream')
                with open(filePath, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filePath)}')
                message.attach(part)
            except Exception as e:
                self.logger.error(f"Failed to attach file {filePath}: {e}")

    def _SendSMTPMail(self, message, recipientEmail):
        try:
            with smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"]) as server:
                server.starttls()
                server.login(self.config["sender_email"], self.config["sender_password"])
                server.sendmail(self.config["sender_email"], recipientEmail, message.as_string())
                self.logger.info(f"Email sent to {recipientEmail}")
        except Exception as e:
            self.logger.error(f"Failed to send email to {recipientEmail}: {e}")
