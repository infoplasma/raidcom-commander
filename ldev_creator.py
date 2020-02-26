#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import npyscreen as nps
from writers import write_output, write_yaml
from helper_funcs import  reset_ldev_provisioner_form


# TODO: ADD PORT MAPPING COMMANDS
# TODO: MANUALLY ENTER THE LUN ID
# TODO: GET NAA IDENTIFIER AND ADD TO EMAIL MESSAGE


class LdevCreatorLogic:
    def __init__(self, form):
        self._form = form

    def validate_and_transform_data(self):
        data = dict(LDEVS=self._form.LDEVS.value.upper().split(","),
                    GB=self._form.GB.value.split(","),
                    POOL_ID=self._form.POOL_ID_SEL.values[self._form.POOL_ID_SEL.value[0]].split(":")[0],
                    LDEV_PREFIX=self._form.LDEV_PREFIX_SEL.values[self._form.LDEV_PREFIX_SEL.value[0]].rstrip("_"),
                    IS_GAD=True if self._form.GAD_SEL.values[self._form.GAD_SEL.value[0]] == 'YES' else False,
                    GAD_RES_NAME=self._form.GAD_RES_NAME.value,
                    GAD_DEV_GRP=self._form.GAD_DEV_GRP_SEL.values[self._form.GAD_DEV_GRP_SEL.value[0]],
                    SER_PRI=self._form.SER_PRI_SEL.values[self._form.SER_PRI_SEL.value[0]],)

        if len(data['LDEVS']) != len(data['GB']):
            nps.notify_wait("PLEASE, DOUBLE CHECK LDEVS VS THEIR SIZE", title='WARNING')
        elif not all([len(i) == 4 for i in data['LDEVS']]):
            nps.notify_wait("LDEV ID MUST BE OF EXACTLY _4 DIGITS_, HEX (ex: 012F)", title='WARNING')
        elif not all([j for i in [[k in '0123456789abcdefABCDEF' for k in j] for j in data['LDEVS']] for j in i]):
            nps.notify_wait("LDEV ID MUST BE _HEXADECIMAL_, 4-DIGITS (ex: 012F)", title='WARNING')
        elif not len(data['LDEVS']) == len(set(data['LDEVS'])):
            nps.notify_wait("THERE ARE _REPEATED_ LDEV IDs IN YOUR LIST", title='WARNING')
        else:
            # ldevs = [i.replace(":", "") for i in ldevs]
            ldev_dict = dict(zip(data['LDEVS'], data['GB']))
            clean_data = {'ldevs': [{"ldev_id": i, "ldev_gb": j} for i, j in ldev_dict.items()],
                          'ldevs_prefix': data['LDEV_PREFIX'],
                          'gad': {'gad_grp': data['GAD_DEV_GRP'],
                                  'gad_res_name': data['GAD_RES_NAME'],
                                  'is_gad': data['IS_GAD']},
                          'plural': '' if len(ldev_dict) == 1 else 's',
                          'pool': {'pool_id': data['POOL_ID']},
                          'ser_pri': data['SER_PRI'],}
            write_yaml(clean_data)
            write_output('create')


class LdevCreatorForm(nps.ActionForm):

    def create(self):

        self.Logic = LdevCreatorLogic(self)

        self.LDEVS           = self.add(nps.TitleText, name="Ldev ID's:" )
        self.GB              = self.add(nps.TitleText, name="CAPACITY, GB:")
        self.GAD_RES_NAME    = self.add(nps.TitleFixedText, name="GAD_RES_NAME:")
        self.GAD_SEL         = self.add(nps.TitleSelectOne, max_height=2, name="REPLICATED:",
                                        values=["YES", "NO"], scroll_exit=True)
        self.POOL_ID_SEL     = self.add(nps.TitleSelectOne, max_height=3, name="POOL ID:", scroll_exit=True)
        self.LDEV_PREFIX_SEL = self.add(nps.TitleSelectOne, max_height=6,name="LDEV_PREFIX:", scroll_exit=True)
        self.GAD_DEV_GRP_SEL = self.add(nps.TitleSelectOne, max_height=6, name="GAD GROUP:", scroll_exit=True)
        self.SER_PRI_SEL     = self.add(nps.TitleSelectOne, name="PRIMARY:")
        reset_ldev_provisioner_form(self)

    def on_ok(self):
        self.Logic.validate_and_transform_data()
        self.parentApp.switchForm('MAIN')
        nps.notify_wait("INFO: CONFIGURATION FILE CREATED.")

    def on_cancel(self):
        self.parentApp.setNextForm('MAIN')