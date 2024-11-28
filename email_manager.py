import smtplib
import ssl

from config import email_config


class Email:
    def __init__(self):
        self.smtp_server = email_config.smtp_server
        self.port = email_config.port
        self.sender = email_config.sender
        self.receiver = email_config.receiver
        self.password = email_config.password
        self.subject = 'TOMATO'
        self.body = 'test'

    def send(self, message: str):
        if message is None or message == '':
            return
        context = ssl.create_default_context()
        context.check_hostname = False  # Disable hostname verification
        context.verify_mode = ssl.CERT_NONE  # Disable certificate verification
        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                # print(f'login name:{self.sender}; pass:{self.password};')
                # server.set_debuglevel(1) # shows debug log
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(self.sender, self.password)
                server.sendmail(
                    self.sender,
                    self.receiver,
                    message
                )
                print(f'Message "{message}" is sent to {self.sender}!')
        except Exception as e:
            print(f'An error occurred: {e}')


email= Email()
