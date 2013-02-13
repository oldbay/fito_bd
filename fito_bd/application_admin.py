# -*- coding: utf-8 -*-
from camelot.view.art import Icon
from camelot.admin.application_admin import ApplicationAdmin
from camelot.admin.section import Section
from camelot.core.utils import ugettext_lazy as _
from main import SelKey
from camelot.admin.action import Action


class Authors( Action ):

       verbose_name = _('View Authors')

       def model_run(self, model_context):
           from camelot.view.action_steps import PrintHtml
           from html_dok import html_authors
           yield PrintHtml( html_authors )


class MyApplicationAdmin(ApplicationAdmin):

    name = 'fito_bd'
    application_url = 'http://www.python-camelot.com'
    help_url = 'http://www.python-camelot.com/docs.html'
    author = 'AGU'
    domain = 'mydomain.com'
    if SelKey:
        database_selection = True

    def get_sections(self):
        from camelot.model.memento import Memento
        from camelot.model.i18n import Translation
        from model import Species,\
			Genus,\
			Familia,\
			LF_Raunkier,\
			LF_Serebryakov,\
			Relat_at_sal,\
			Phytocenosis,\
			Aqua_regimen,\
			Area,\
			Import_conspect

        return [ Section( _('flora_list'),
                          self,
                          Icon('tango/22x22/apps/system-users.png'),
                          items = [Species] ),
                 Section( _('hdbk'),
                          self,
                          Icon('tango/22x22/apps/system-users.png'),
                          items = [Genus,
                                   Familia,
                                   LF_Raunkier,
                                   LF_Serebryakov,
                                   Relat_at_sal,
                                   Phytocenosis,
                                   Aqua_regimen,
                                   Area] ),
                 Section( _('Imports'),
                          self,
                          Icon('tango/22x22/apps/system-users.png'),
                          items = [Import_conspect] ),
                 Section( _('Configuration'),
                          self,
                          Icon('tango/22x22/categories/preferences-system.png'),
                          items = [Memento, Translation] )
                ]

    def get_actions(self):
        import os
        import fito_bd
        authors_action = Authors()
        p = os.path.join('authors.png')
        authors_action.icon = Icon( p, module = fito_bd )
        return [authors_action]

    def get_translator(self):
        import os
        translators = []
        for qm_file in ['camelot.qm','fito_bd.qm']:
            translator = self._load_translator_from_file('fito_bd', os.path.join('translations', qm_file ))
            translators.append( translator )
        return translators

    def get_splashscreen(self):
        import os
        from camelot.core.resources import resource_string
        from PyQt4.QtGui import QPixmap
        qpm = QPixmap()
        p = os.path.join('art', 'splashscreen.png')
        r = resource_string('fito_bd', p)
        qpm.loadFromData(r)
        return qpm
