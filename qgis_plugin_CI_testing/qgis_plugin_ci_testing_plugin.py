#!/usr/bin/env python
"""
/***************************************************************************

 QGIS Plugin CI Testing
 Copyright (C) 2019 Denis Rouzaud

 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.gui import QgisInterface
from qgis.PyQt.QtCore import QCoreApplication, QLocale, QSettings, QTranslator


DEBUG = False


class QgisPluginCiTesting:
    def __init__(self, iface: QgisInterface):
        self.iface = iface

        # initialize translation
        qgis_locale = QLocale(QSettings().value("locale/userLocale"))
        locale_path = os.path.join(os.path.dirname(__file__), "i18n")
        self.translator = QTranslator()
        self.translator.load(qgis_locale, "swiss_locator", "_", locale_path)
        QCoreApplication.installTranslator(self.translator)

        self.tr("some UTF-8 translation: un épilogue où l'on marche sur des œufs")

    def tr(self, message: str) -> str:
        """Translate a string, using the class name as context."""
        return QCoreApplication.translate(self.__class__.__name__, message)

    def initGui(self):
        pass

    def unload(self):
        pass
