import npyscreen as nps
from writers import write_output, write_yaml
from yaml import safe_load


# TODO: ADD PORT MAPPING COMMANDS
# TODO: MANUALLY ENTER THE LUN ID
# TODO: GET NAA IDENTIFIER AND ADD TO EMAIL MESSAGE


def get_default_form_data(form):
    return [
            form.LDEVS.value,
            form.LDEVS_GB.value,
            form.GAD_RES_NAME.value,
            form.SER_PRI.value,
            form.SER_SEC.value,
            form.GAD_SEL.values,
            form.POOL_ID_SEL.values,
            form.LDEV_PREFIX_SEL.values,
            form.GAD_DEV_GRP_SEL.values, ]


def validate_and_transform_data(form):
    LDEVS = form.LDEVS.value.upper().split(",")
    LDEVS_GB = form.LDEVS_GB.value.split(",")
    POOL_ID_SEL = form.POOL_ID_SEL
    POOL_ID = POOL_ID_SEL.values[POOL_ID_SEL.value[0]].split(":")[0]
    LDEV_PREFIX_SEL = form.LDEV_PREFIX_SEL
    LDEV_PREFIX = LDEV_PREFIX_SEL.values[LDEV_PREFIX_SEL.value[0]]
    LDEV_PREFIX = LDEV_PREFIX.rstrip("_")
    GAD_SEL = form.GAD_SEL
    GAD = GAD_SEL.values[GAD_SEL.value[0]]
    IS_GAD = True if GAD == 'YES' else False
    GAD_RES_NAME = form.GAD_RES_NAME.value
    GAD_DEV_GRP_SEL = form.GAD_DEV_GRP_SEL
    GAD_DEV_GRP = GAD_DEV_GRP_SEL.values[GAD_DEV_GRP_SEL.value[0]]
    SER_PRI = form.SER_PRI.value
    SER_SEC = form.SER_SEC.value

    if len(LDEVS) != len(LDEVS_GB):
        nps.notify_wait("PLEASE, DOUBLE CHECK LDEVS VS THEIR SIZE", title='WARNING')
    elif not all([len(i) == 4 for i in LDEVS]):
        nps.notify_wait("LDEV ID MUST BE OF EXACTLY _4 DIGITS_, HEX (ex: 012F)", title='WARNING')
    elif not all([j for i in [[k in '0123456789abcdefABCDEF' for k in j] for j in LDEVS] for j in i]):
        nps.notify_wait("LDEV ID MUST BE _HEXADECIMAL_, 4-DIGITS (ex: 012F)", title='WARNING')
    elif not len(LDEVS) == len(set(LDEVS)):
        nps.notify_wait("THERE ARE _REPEATED_ LDEV IDs IN YOUR LIST", title='WARNING')
    else:
        write_yaml(ldev_prefix=LDEV_PREFIX,
                   ldevs_gb=LDEVS_GB,
                   is_gad=IS_GAD,
                   gad_res_name=GAD_RES_NAME,
                   gad_dev_grp=GAD_DEV_GRP,
                   pool_id=POOL_ID,
                   ser_pri=SER_PRI,
                   ser_sec=SER_SEC,
                   ldevs=LDEVS)
        write_output('create')

    import pprint as pp
    import sys
    pp.pprint(get_default_form_data(form))
    sys.exit(0)
    nps.notify_wait("CONFIGURATION FILE CREATED.")


class LdevCreatorForm(nps.ActionForm):

    @staticmethod
    def _load_defaults():
        with open('config/defaults.yaml') as yaml_data:
            return safe_load(yaml_data)


    def create(self):
        self._cfg = self._load_defaults()

        self.LDEVS           = self.add(nps.TitleText, name="Ldev ID's:", value=self._cfg['LDEVS'])
        self.LDEVS_GB        = self.add(nps.TitleText, name="CAPACITY, GB:", value=self._cfg['LDEVS_GB'])
        self.GAD_RES_NAME    = self.add(nps.TitleFixedText, name="GAD_RES_NAME:", value=self._cfg['GAD_RES_NAME'])
        self.SER_PRI         = self.add(nps.TitleFixedText, name="SER_PRI:", value=self._cfg['SER_PRI'])
        self.SER_SEC         = self.add(nps.TitleFixedText, name="SER_SEC:", value=self._cfg['SER_SEC'])
        self.GAD_SEL         = self.add(nps.TitleSelectOne, max_height=2, name="REPLICATED:",
                                        values=["YES", "NO"], value=0, scroll_exit=True)
        self.POOL_ID_SEL     = self.add(nps.TitleSelectOne, max_height=3, name="POOL ID:",
                                        values=self._cfg['POOL_ID'], value=0, scroll_exit=True)
        self.LDEV_PREFIX_SEL = self.add(nps.TitleSelectOne, max_height=6, name="LDEV_PREFIX:",
                                        values=self._cfg['LDEV_PREFIX'], value=0, scroll_exit=True)
        self.GAD_DEV_GRP_SEL = self.add(nps.TitleSelectOne, max_height=6, name="GAD GROUP:",
                                        values=self._cfg['DEFAULT_GROUPS'], value=0, scroll_exit=True)

    def on_ok(self):
        validate_and_transform_data(self)

        self.parentApp.switchForm("MAIN")


    def on_cancel(self):
        self.parentApp.setNextForm("MAIN")


class App(nps.NPSAppManaged):
    def onStart(self):
        nps.setTheme(nps.Themes.ElegantTheme)
        self.addForm("MAIN", LdevCreatorForm, name="RAIDCOM COMMANDER")
        main()

def main():
    form = LdevCreatorForm()
    nps.notify_wait(str(get_default_form_data(form)))


if __name__ == "__main__":
    App().run()
    print(" *** I WANT PIZZA ***")

