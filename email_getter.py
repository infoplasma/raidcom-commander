import win32com.client
import os


def get_email():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

    messages = outlook.Folders["lamante@dxc.com"].Folders["Inbox"].Items

    found = False
    msg = messages.GetLast()

    print("*** INFO: SCANNING INBOX FOR THE LAST STORCOM REQUEST.")

    while not found:
        if "[STORCOM]" in str(msg):

            print(f"Subject: {msg.Subject}")
            print(f"SentOn: {msg.SentOn}")
            found = True
            attachments = msg.Attachments
            attachment = attachments.Item(1)
            #print(os.path.join(os.getcwd(), "vars"))
            attachment.SaveASFile(os.path.join(os.getcwd(), "vars", str(attachment)))

            #print(attachment)

        msg = messages.GetPrevious()

