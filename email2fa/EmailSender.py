import email.message
import logging
import smtplib

logger = logging.getLogger(__name__)
SENDER = "iris21741@gmail.com"
SUBJECT = "black-jack-21 驗證碼"
SMTP = "smtp.gmail.com"
PASSWORD = "zuuf zxdo kqoz twzs"

def send_code(to_email:str, code: str):
    try:
        msg = email.message.EmailMessage()
        msg["From"] = SENDER
        msg["To"] = to_email
        msg["Subject"] = SUBJECT
        message = f"<h3>black-jack-21 驗證碼</h3><br/>登入驗證碼：[{code}]<br/>有效時間60秒"
        msg.add_alternative(message, subtype="html")

        # 連線到SMTP Server,驗證寄件人身份並發送郵件
        server = smtplib.SMTP_SSL(SMTP, 465)
        server.login(SENDER, PASSWORD)
        server.send_message(msg)
        server.close()
        logger.info("寄件成功")
        return True
    except Exception as e:
        logger.error(f"發送郵件時發生錯誤: {e}")
        return False


if __name__ == '__main__':
    send_code("uhakulailay415@gmail.com","123456")


