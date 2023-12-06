from PyQt6.QtCore import QCoreApplication, QDir, qDebug
from PyQt6.QtWidgets import QMessageBox
import mobase

class LootPreventifier(mobase.IPlugin):

    def __init__(self):
        super().__init__()
        self._organizer = None
        self._parent = None

    def __tr(self, str_):
        return QCoreApplication.translate("LootPreventifier", str_)

    # IPlugin
    def init(self, organizer):
        self._organizer = organizer
        if not self._organizer.onAboutToRun(lambda appName: self._preventLoot(appName)):
            qDebug("Failed to register onAboutToRun callback!")
            return False
        return True

    def name(self):
        return "LOOT Preventifier"

    def author(self):
        return "LostDragonist & Miss Corruption"

    def description(self):
        return self.__tr("Prevents the user from running LOOT")

    def version(self):
        return mobase.VersionInfo(1, 0, 0, 0)

    def settings(self):
        return [
            mobase.PluginSetting("dialog", self.__tr("String displayed when LOOT is ran"),
                                 "This load order was created by hand and is carefully curated. "
                                 "Running LOOT is disabled."
                                 ""
                                 "You can disable this plugin by:"
                                 " 1. Opening Settings."
                                 " 2. Going to the plugins tab."
                                 " 3. Selecting the LOOT Preventifier plugin."
                                 " 4. Unchecking the enabled box on the right.")
        ]

    def _preventLoot(self, appName):
        if appName.lower().endswith("loot.exe") or appName.lower().endswith("lootcli.exe"):
            dialog = self._organizer.pluginSetting(self.name(), "dialog")
            if dialog != '':
                QMessageBox.information(self._parent, self.name(), dialog)
            return False
        return True

def createPlugin():
    return LootPreventifier()
