import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from pizza_hub_app.utils.logger.logger import AppLogger
from pydantic import EmailStr
from pizza_hub.settings import BASE_DIR
import pybars


logger = AppLogger(__name__)

email_username = os.getenv("EMAIL_SENDER", "mysmtp@email.com")
email_password = os.getenv("EMAIL_PASSWORD", "")
email_host = os.getenv("EMAIL_HOST", "localhost")
email_port = os.getenv("EMAIL_PORT", "1025")
fronted_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
reset_link_frontend_url = os.getenv("FRONTEND_RESET_PASSWORD_LINK", "/reset-password")

class EmailSender:

    def __init__(self):
        try:
            self.__emailConfig : smtplib.SMTP = smtplib.SMTP(email_host, email_port)
            self.__emailConfig.set_debuglevel(1)
            #self.__emailConfig.starttls()
            self.__emailConfig.ehlo()
            self.__emailConfig.login(email_username, email_password)
            logger.info('SMTP connection initialized successfully.')
        except Exception as e:
            logger.error('An error occured during SMTP initilization. DETAIL-----> ' + str(e))
            self.__emailConfig = None  # Imposta a None se la connessione fallisce
    

    

    async def send_welcome_email(self, name : str, lastname : str, email : EmailStr, token : str) -> bool:
        try:
            emailServer =  smtplib.SMTP(email_host, email_port)
            # emailServer.set_debuglevel(1)
            message = MIMEMultipart()
            message["Subject"] = "Pizza Hub"
            message["From"] = email_username
            message["To"] = email
            template_path = os.path.join(BASE_DIR, "template", "email", "reset-email-link.hbs")
            with open(template_path, 'r', encoding='utf-8') as file:
                template_content = file.read()
            handlebars = pybars.Compiler()
            template = handlebars.compile(str(template_content))
            reset_password_link : str = fronted_url + reset_link_frontend_url + '&token=' + token
            body_email = template({"name": name, "lastname": lastname, "reset_password_link" : reset_password_link})
            message.attach(MIMEText(body_email, 'html'))
            #emailServer.login(email_username, email_password)
            emailServer.set_debuglevel(1)
            #emailServer.starttls()
            emailServer.ehlo()
            emailServer.sendmail(email_username, email, message.as_string())
            logger.info('Reset password link sended successfully to email ' + email)
            emailServer.close()
            return True

        except Exception as e:
            logger.error('An error occured while sending welcome email. DETAIL-----> ' + str(e))
            return False