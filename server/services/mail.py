import smtplib
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from email.mime.text import MIMEText
from email.header import Header
import json
import logging


# my exceptions
class Error(Exception):
    """Base class for exceptions in this module."""


class InputError(Error):
    """Exception raised for errors in the input.
        not used yet
    """

    def __init__(self, message):
        self.message = message


class MailSender(object):
    @staticmethod
    def __contains_nonascii_characters(string):
        """ check if the body contain nonascii characters"""
        for c in string:
            if not ord(c) < 128:
                return True
        return False

    def __addheader(self, msg, headername, headervalue):
        """ judge the message's charset and set header with "utf-8" when there is nonascii characters """
        if self.__contains_nonascii_characters(headervalue):
            h = Header(headervalue, 'utf-8')
            msg[headername] = h
        else:
            msg[headername] = headervalue
        return msg

    def __init__(self, smtp_host=None, smtp_port=None, smtp_user=None, smtp_password=None, tls=False):

        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.tls = tls

    def send_mail(self, mail_from, mail_to_list, mail_subject, mail_body, mime_type="html"):
        if not mail_to_list:
            return

        msg = MIMEMultipart()

        if self.__contains_nonascii_characters(mail_body):
            plaintext = MIMEText(unicode(mail_body), mime_type, 'utf-8')
        else:
            plaintext = MIMEText(mail_body, mime_type)
        msg.attach(plaintext)

        msg["From"] = mail_from
        for recipient in mail_to_list:
            msg.add_header('To', recipient)
        msg["Subject"] = mail_subject
        msg['Date'] = formatdate(localtime=True)

        # login to smtp server
        if self.smtp_user is None:
            raise Error("no smpt user provided ")
        if self.smtp_host is None:
            raise Error("no smpt password provider")
        server = smtplib.SMTP(self.smtp_host)
        if self.tls:
            server.starttls()
        server.login(self.smtp_user, self.smtp_password)  # optional
        # server.set_debuglevel(1)

        server.sendmail(msg['from'], mail_to_list, msg.as_string())
        server.close()


class MailQueuePusher(object):
    rds_queue_key = "mail_queue"

    def __init__(self, rds_conn, enabled=False):
        self.rds_conn = rds_conn
        self.enabled = enabled

    def push_data_to_queue(self, data):
        if self.enabled is True:
            self.rds_conn.lpush(self.rds_queue_key, data)

    def push_single_mail(self, mail):
        mail_data = json.dumps(mail)
        self.push_data_to_queue(mail_data)
        return True


class MailQueueWatcher(object):
    rds_queue_key = "mail_queue"

    def __init__(self, rds_conn):
        self.rds_conn = rds_conn
        return

    def watch(self):
        print "watching"
        while True:
            queue_name, mail_data = self.rds_conn.brpop(self.rds_queue_key, 0)
            print "get mail: %s" % (mail_data,)
            try:
                mail = json.loads(mail_data)
                mail_from = mail["from"]
                mail_to = mail["to"]
                mail_subject = mail["subject"]
                host = mail["host"]
                port = mail["port"]
                username = mail["username"]
                passwd = mail["passwd"]
                use_tls = mail["use_tls"]
                assert isinstance(mail_to, list)
                mail_body = mail["body"]
            except Exception as e:
                logging.error("parse mail error %r" % (e,))
                continue
            mailer = MailSender(smtp_host=host, smtp_port=port, smtp_user=username, smtp_password=passwd, tls=use_tls)
            try:
                mailer.send_mail(mail_from, mail_to, mail_subject, mail_body)
            except Exception as e:
                print "Sending Error: ", e


if __name__ == "__main__":
    from application import create_app
    app = create_app()
    with app.app_context():
        rds_conn = app.redis
        watcher = MailQueueWatcher(rds_conn)
        watcher.watch()