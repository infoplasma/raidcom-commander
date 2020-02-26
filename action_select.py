#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import npyscreen as nps
from yaml import safe_load, safe_dump
from helper_funcs import reset_ldev_provisioner_form, reset_ldev_terminator_form, get_email


def to_dev_list(list_gb=None, first_ldev_id ="0x0000"):

    if list_gb is None:
        list_gb = [0]
    first_dev_id_dec = int(first_ldev_id, 16)

    dev_id_list = []
    for i in range(len(list_gb)):
        dev_id = first_dev_id_dec + i
        dev_id_list.append(f"{dev_id:0{4}x}".upper())

    return list(zip(dev_id_list, list_gb))


def read_config(yaml_file):
    with open(yaml_file, "r") as f:
        return safe_load(f)


class ActionSelectLogic:
    
    def __init__(self, form):
        self._form = form

    def update_config(self):
        sub, sen = get_email()
        nps.notify_wait("INFO: SCANNING INBOX FOR THE LAST STORCOM REQUEST.")

        nps.notify_wait(f"DATE: {sen} - SUBJECT: {sub}")
            
        cfg = read_config('config/defaults.yaml')
        data = read_config('./vars/params.yaml')

        values = []
        mode = data['action_type']

        if mode == 'create':
            for i in data['devices']:
                for j in range(int(i['qty'])):
                    values.append(i['size_gb'])
            first_id = self._form.parentApp.getForm('ACTION SELECT').FIRST_ID.value
            nps.notify_wait(f"FIRST ID= {first_id}")
            a, b = (zip(*to_dev_list(values, first_id)))
            nps.notify_wait(f"A: {a} - B: {b}")
            cfg['LDEVS'] = ','.join(map(str, a))
            cfg['GB'] = ','.join(map(str, b))

            cfg['TIER_INDEX'] = data['tier_index']
            cfg['LDEV_PREFIX_INDEX'] = data['prefix_index']
            cfg['REPLICA_INDEX'] = data['replica_index']

            with open('config/defaults.yaml', 'w', encoding='utf-8') as handle:
                safe_dump(cfg, handle)

            reset_ldev_provisioner_form(self._form.parentApp.getForm('LDEV PROVISIONER'))

        elif mode == 'terminate':
            nps.notify_wait(str(data['devices']))
            cfg['LDEVS'] = ','.join([i['lun_id'] for i in data['devices']])
            cfg['GB'] = ','.join([i['size_gb'] for i in data['devices']])
            self._form.parentApp.getForm('LDEV TERMINATOR').LDEVS.value = cfg['LDEVS']
            cfg['TIER_INDEX'] = data['tier_index']
            cfg['REPLICA_INDEX'] = data['replica_index']

            with open('config/defaults.yaml', 'w', encoding='utf-8') as handle:
                safe_dump(cfg, handle)

            reset_ldev_terminator_form(self._form.parentApp.getForm('LDEV TERMINATOR'))
        

class ActionSelectForm(nps.ActionFormV2):

    def create(self):

        self.Logic = ActionSelectLogic(self)

        self.FIRST_ID = self.add(nps.TitleText, name="FIRST LUN ID:", value='0x0000',
                                    color='STANDOUT')

    def on_ok(self):

        self.Logic.update_config()

        self.parentApp.switchForm('LDEV PROVISIONER')

    def on_cancel(self):

        self.parentApp.switchForm('MAIN')
