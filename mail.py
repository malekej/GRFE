import datetime
import smtplib

gmail_user = 'natalia.wojtkowiak@nielsen.com'
gmail_password = 'kgixsmdlhzdntzyn'

def mail():
    sent_from = 'natalia.wojtkowiak@nielsen.com'
    to = ['daten.eingang@nielsen.com', 'natalia.wojtkowiak@nielsen.com']
    subject = 'Sirpair production!'
    body = '''
Czesc,

\(^ _ ^)/    Zrobilem {sklep} o: {czas}     \(^ _ ^)/

Skryptor'''.format(sklep=sklep, czas = str(datetime.datetime.now()))

    email_text = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(sent_from, to, subject, body)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()
