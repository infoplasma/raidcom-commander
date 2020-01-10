import imaplib


EMAIL = "lorenzoamante@infoplasma.com"
PWD = input("PWD:")

IMAP_SERVER = "pop.securemail.pro"
IMAP_PORT = 993

def read_mail():

    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PWD)

    mail.select('Posta in arrivo')

    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()

    print(data)
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    for i in range(latest_email_id, first_email_id, -1):
        typ, data = mail.fetch(i, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1])
                email_subject = msg['subject']
                email_from = msg['from']
                print('From : ' + email_from + '\n')
                print('Subject : ' + email_subject + '\n')


if __name__ == '__main__':
    read_mail()