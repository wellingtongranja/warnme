# warnme_sms.py

from twilio.rest import Client
import logging

class WarnMeSMS:
    def __init__(self, config):
        self.logger = logging.getLogger('WarnMeLogger')
        self.accountSid = config['WARNME_TWILIO_ACCOUNT_SID']
        self.authToken = config['WARNME_TWILIO_AUTH_TOKEN']
        self.fromPhone = config['WARNME_TWILIO_FROM_PHONE_NUMBER']
        self.client = Client(self.accountSid, self.authToken)

    def SendSMS(self, toPhone, message):
        try:
            sms = self.client.messages.create(
                body=message,
                from_=self.fromPhone,
                to=toPhone
            )
            self.logger.info(f"Message sent: {sms.sid}")
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
