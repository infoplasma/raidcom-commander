#!/usr/bin/env python3

print("*** INFO: LOADING PROGRAM, PLEASE BE PATIENT. ***")
 
import npyscreen as nps
from ldev_creator import LdevCreatorForm
from ldev_terminator import LdevTerminatorForm


class myEntryForm(nps.FormBaseNewWithMenus):
    def create(self):
        self.pager = self.add(nps.Pager, values=["WELCOME TO RAIDCOMMANDER", "PRESS CTRL-X TO START. THANK YOU."])
        self.menu = self.new_menu(name='OPTION MENU', shortcut=None)
        self.menu.addItem(text='LDEV PROVISIONER..............', onSelect=self.ldev_creator, shortcut='1')
        self.menu.addItem(text="LDEV TERMINATOR...............", onSelect=self.ldev_terminator, shortcut='2')
        self.menu.addItem(text='CONFIGURATOR PARAMETRI........', onSelect=self.configurator_parametri, shortcut='3')
        self.menu.addItem(text='EXODUS........................', onSelect=self.exit_func, shortcut='0')

    def configurator_parametri(self):
        self.parentApp.switchForm("CONFIGURATOR PARAMETRI")

    def ldev_creator(self):
        self.parentApp.switchForm("LDEV PROVISIONER")


    def ldev_terminator(self):
        self.parentApp.switchForm("LDEV TERMINATOR")

    def exit_func(self):
        nps.notify_wait("*** INFO: EXITING PROGRAM: >>> GOODBYE! <<< ***")
        self.parentApp.switchForm(None)


class configuratorForm(nps.ActionForm):
    def activate(self):
        nps.notify_wait("to change configuration settings you must manually edit config/defaults.yaml", title='WARNING')
        self.parentApp.setNextForm("MAIN")
    
    def create(self):
        pass

    def on_ok(self):
        self.parentApp.setNextForm("MAIN")


class MyApplication(nps.NPSAppManaged):
    def onStart(self):
        nps.setTheme(nps.Themes.ElegantTheme)
        self.addForm('MAIN', myEntryForm, name='RAIDCOMMANDER')
        self.addForm('LDEV PROVISIONER', LdevCreatorForm, name="LDEV PROVISIONER")
        self.addForm('LDEV TERMINATOR', LdevTerminatorForm, name="LDEV TERMINATOR")
        self.addForm("CONFIGURATOR PARAMETRI", configuratorForm, name="CONFIGURATOR PARAMETRI")
        

if __name__ == "__main__":
    MyApplication().run()
    print('*** INFO: PROGRAM ENDED, GOODBYE. ***')
