import datetime
import smtplib

gmail_user = 'natalia.wojtkowiak@nielsen.com'
gmail_password = 'kgixsmdlhzdntzyn'

def mail():
    sent_from = 'natalia.wojtkowiak@nielsen.com'
    to = ['daten.eingang@nielsen.com', 'natalia.wojtkowiak@nielsen.com']
    subject = 'Sirpair production!'
    body = '''
Hi,

\(^ _ ^)/    Completed REWE split task at:{}.    \(^ _ ^)/'''.format(str(datetime.datetime.now()))

    email_text = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(sent_from, to, subject, body)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

def mail_failure():
    sent_from = 'natalia.wojtkowiak@nielsen.com'
    to = ['natalia.wojtkowiak@nielsen.com', 'marek.milcarz@nielsen.com']
    subject = 'Sirpair production!'
    body = '''
Hi,

( / _ \ )   Somethin went wrong with sending. Better check what happened.  ( / _ \ )'''

    email_text = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(sent_from, to, subject, body)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

def mail_missing(flagA, flagB):
    if flagA:
        file = 'TOIFNI'
    elif flagB:
        file = 'FIIFNI'
    else:
        file = 'FIIFNI and TOIFNI'
    sent_from = 'natalia.wojtkowiak@nielsen.com'
    to = ['natalia.wojtkowiak@nielsen.com', 'marek.milcarz@nielsen.com']
    subject = 'Sirpair production!'
    body = '''
Hi,

\( O . O )\   I couldn\'t find file {file}. /( O . O )/'''.format(file=file)

    email_text = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(sent_from, to, subject, body)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()
