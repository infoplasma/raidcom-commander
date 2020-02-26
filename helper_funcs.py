#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import win32com.client
from yaml import safe_load


def load_defaults():
    with open('config/defaults.yaml') as yaml_data:
        return safe_load(yaml_data)


def reset_ldev_provisioner_form(form):
    _cfg = load_defaults()

    form.LDEVS.value = _cfg['LDEVS']
    form.GB.value = _cfg['GB']
    form.GAD_RES_NAME.value = _cfg['GAD_RES_NAME']
    form.GAD_SEL.value = _cfg['REPLICA_INDEX']
    form.POOL_ID_SEL.value = _cfg['TIER_INDEX']
    form.POOL_ID_SEL.values = _cfg['POOL_ID']
    form.LDEV_PREFIX_SEL.value = _cfg['LDEV_PREFIX_INDEX']
    form.LDEV_PREFIX_SEL.values = _cfg['LDEV_PREFIX']
    form.GAD_DEV_GRP_SEL.value = 0
    form.GAD_DEV_GRP_SEL.values = _cfg['DEFAULT_GROUPS']
    form.SER_PRI_SEL.value = _cfg['SERIAL_INDEX']
    form.SER_PRI_SEL.values = _cfg['SERIALS']


def reset_ldev_terminator_form(form):
    _cfg = load_defaults()

    form.LDEVS.value = _cfg['LDEVS']
    form.GB.value = _cfg['GB']
    form.GAD_RES_NAME.value = _cfg['GAD_RES_NAME']
    form.GAD_SEL.value = _cfg['REPLICA_INDEX']
    form.GAD_DEV_GRP_SEL.value = 0
    form.GAD_DEV_GRP_SEL.values = _cfg['DEFAULT_GROUPS']
    form.SER_PRI_SEL.value = _cfg['SERIAL_INDEX']
    form.SER_PRI_SEL.values = _cfg['SERIALS']


def get_email():

    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    messages = outlook.Folders["lamante@dxc.com"].Folders["Inbox"].Items
    found = False
    msg = messages.GetLast()
    print("*** INFO: SCANNING INBOX FOR THE LAST STORCOM REQUEST.")

    while not found:
        if '[STORCOM]' in str(msg):

            print(f"Subject: {msg.Subject}")
            print(f"SentOn: {msg.SentOn}")
            found = True
            attachments = msg.Attachments
            attachment = attachments.Item(1)
            attachment.SaveASFile(os.path.join(os.getcwd(), 'vars', str(attachment)))
            return msg.Subject, msg.SentOn

        msg = messages.GetPrevious()