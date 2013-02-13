# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath(os.curdir))
try:
    SelKey = sys.argv[1]
except:
    SelKey = False
else:
    if SelKey != "-s":
        SelKey = False


import logging
from camelot.core.conf import settings, SimpleSettings

FORMAT = '[%(levelname)-7s] [%(name)-35s] - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger( 'main' )

# begin custom settings
class MySettings( SimpleSettings ):

    # add an ENGINE or a CAMELOT_MEDIA_ROOT method here to connect
    # to another database or change the location where files are stored
    #
    # def ENGINE( self ):
    #     from sqlalchemy import create_engine
    #     return create_engine( 'postgresql://user:passwd@127.0.0.1/database' )

    def setup_model( self ):
        """This function will be called at application startup, it is used to
        setup the model"""
        from camelot.core.sql import metadata
        from sqlalchemy.orm import configure_mappers
        metadata.bind = self.ENGINE()
        import camelot.model.authentication
        import camelot.model.i18n
        import camelot.model.memento
        import fito_bd.model
        configure_mappers()
        metadata.create_all()

    def CAMELOT_MEDIA_ROOT( self ):
        import fito_bd
        MediaPath = os.path.dirname(fito_bd.__file__) + '/media'
        return MediaPath

    def ENGINE( self ):
        if SelKey:
            from camelot.core.dbprofiles import engine_from_profile
            return engine_from_profile()
        else:
            from sqlalchemy import create_engine
            import fito_bd
            DBPath =  'sqlite:///' + os.path.dirname(fito_bd.__file__) + '/media/data.sqlite'
            return create_engine( DBPath )


my_settings = MySettings( 'AGU', 'fito_bd' )
settings.append( my_settings )
# end custom settings

def start_application():
    from camelot.view.main import main
    from fito_bd.application_admin import MyApplicationAdmin
    main(MyApplicationAdmin())

if __name__ == '__main__':
    start_application()
