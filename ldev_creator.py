import npyscreen as nps
from writers import write_output, write_yaml
from yaml import safe_load


# TODO: ADD PORT MAPPING COMMANDS
# TODO: MANUALLY ENTER THE LUN ID
# TODO: GET NAA IDENTIFIER AND ADD TO EMAIL MESSAGE


def validate_and_transform_data(form):
    data = dict(LDEVS=form.LDEVS.value.upper().split(","),
                GB=form.GB.value.split(","),
                POOL_ID=form.POOL_ID_SEL.values[form.POOL_ID_SEL.value[0]].split(":")[0],
                LDEV_PREFIX=form.LDEV_PREFIX_SEL.values[form.LDEV_PREFIX_SEL.value[0]].rstrip("_"),
                IS_GAD=True if form.GAD_SEL.values[form.GAD_SEL.value[0]] == 'YES' else False,
                GAD_RES_NAME=form.GAD_RES_NAME.value,
                GAD_DEV_GRP=form.GAD_DEV_GRP_SEL.values[form.GAD_DEV_GRP_SEL.value[0]],
                SER_PRI=form.SER_PRI_SEL.values[form.SER_PRI_SEL.value[0]],)

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

    nps.notify_wait("CONFIGURATION FILE CREATED.")


class LdevCreatorForm(nps.ActionForm):

    @staticmethod
    def _load_defaults():
        with open('config/defaults.yaml') as yaml_data:
            return safe_load(yaml_data)

    def create(self):
        self._cfg = self._load_defaults()

        self.LDEVS           = self.add(nps.TitleText, name="Ldev ID's:", value=self._cfg['LDEVS'])
        self.GB              = self.add(nps.TitleText, name="CAPACITY, GB:", value=self._cfg['GB'])
        self.GAD_RES_NAME    = self.add(nps.TitleFixedText, name="GAD_RES_NAME:", value=self._cfg['GAD_RES_NAME'])

        self.GAD_SEL         = self.add(nps.TitleSelectOne, max_height=2, name="REPLICATED:",
                                        values=["YES", "NO"], value=self._cfg['REPLICA_INDEX'], scroll_exit=True)
        self.POOL_ID_SEL     = self.add(nps.TitleSelectOne, max_height=3, name="POOL ID:",
                                        values=self._cfg['POOL_ID'], value=self._cfg['TIER_INDEX'], scroll_exit=True)
        self.LDEV_PREFIX_SEL = self.add(nps.TitleSelectOne, max_height=6, name="LDEV_PREFIX:",
                                        values=self._cfg['LDEV_PREFIX'], value=self._cfg['LDEV_PREFIX_INDEX'],
                                        scroll_exit=True)
        self.GAD_DEV_GRP_SEL = self.add(nps.TitleSelectOne, max_height=6, name="GAD GROUP:",
                                        values=self._cfg['DEFAULT_GROUPS'], value=0, scroll_exit=True)
        self.SER_PRI_SEL         = self.add(nps.TitleSelectOne, name="PRIMARY:", values=self._cfg['SERIALS'],
                                        value=self._cfg['SERIAL_INDEX'])

    def on_ok(self):
        validate_and_transform_data(self)
        self.parentApp.switchForm("MAIN")

    def on_cancel(self):
        self.parentApp.setNextForm("MAIN")

"""
class App(nps.NPSAppManaged):
    def onStart(self):
        # main()
        nps.setTheme(nps.Themes.ElegantTheme)
        self.addForm("MAIN", LdevCreatorForm, name="RAIDCOM COMMANDER")


if __name__ == "__main__":
    App().run()
    print(" *** I WANT PIZZA ***")

"""