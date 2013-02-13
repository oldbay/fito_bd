# -*- coding: utf-8 -*-
from sqlalchemy import Unicode, Integer
from sqlalchemy.schema import Column, ForeignKey
import camelot.types
from camelot.core.utils import ugettext_lazy as _

from camelot.admin.entity_admin import EntityAdmin
from camelot.core.orm import Entity

from sqlalchemy.orm import relationship

from camelot.view.forms import Form, TabForm
from camelot.view.filters import ComboBoxFilter

from camelot.view import action_steps
from camelot.admin.action import Action


class Cons2db ( Action ):

    verbose_name = _('Cons to DB')

    def model_run( self, model_context ):
        from cons2db import\
                familia_parse,\
                genus_parse,\
                LF_Raunkier_parse,\
                LF_Serebryakov_parse,\
                Relat_at_sal_parse,\
                Phytocenosis_parse,\
                Aqua_regimen_parse,\
                Area_parse,\
                species_parse

        yield action_steps.UpdateProgress( 0, 9, _('Create hdbk Familia') )
        familia_parse()
        yield action_steps.UpdateProgress( 1, 9, _('Create hdbk Genus') )
        genus_parse()
        yield action_steps.UpdateProgress( 2, 9, _('Create hdbk LF Raunkier') )
        LF_Raunkier_parse()
        yield action_steps.UpdateProgress( 3, 9, _('Create hdbk LF Serebryakov') )
        LF_Serebryakov_parse()
        yield action_steps.UpdateProgress( 4, 9, _('Create hdbk Relat at sal') )
        Relat_at_sal_parse()
        yield action_steps.UpdateProgress( 5, 9, _('Create hdbk Phytocenosis') )
        Phytocenosis_parse()
        yield action_steps.UpdateProgress( 6, 9, _('Create hdbk Aqua regimen') )
        Aqua_regimen_parse()
        yield action_steps.UpdateProgress( 7, 9, _('Create hdbk Area') )
        Area_parse()
        yield action_steps.UpdateProgress( 8, 9, _('Create Species list') )
        species_parse()


class Species(Entity):
    __tablename__ = 'species'

    species = Column( Unicode(512), nullable = False)
    species_loc = Column( Unicode(512))
    genus = relationship( 'Genus' )
    LF_Raunkier = relationship( 'LF_Raunkier')
    LF_Serebryakov = relationship( 'LF_Serebryakov')
    relat_at_sal = relationship( 'Relat_at_sal')
    phytocenosis = relationship( 'Phytocenosis')
    aqua_regimen = relationship( 'Aqua_regimen')
    area = relationship( 'Area', secondary = 'species_area' )
    image = Column( camelot.types.Image( upload_to = 'image' ) )
    description = Column( camelot.types.RichText )

    genus_id = Column( Integer, ForeignKey('genus.id'), nullable = False )
    LF_Raunkier_id = Column( Integer, ForeignKey('LF_Raunkier.id') )
    LF_Serebryakov_id = Column( Integer, ForeignKey('LF_Serebryakov.id') )
    relat_at_sal_id = Column( Integer, ForeignKey('relat_at_sal.id') )
    phytocenosis_id = Column( Integer, ForeignKey('phytocenosis.id') )
    aqua_regimen_id = Column( Integer, ForeignKey('aqua_regimen.id') )


    def __unicode__( self ):
        return self.species or _('unknown')

    class Admin( EntityAdmin ):
        verbose_name_plural = _('Species')
        list_filter = [
			ComboBoxFilter('Genus.genus'),
			ComboBoxFilter('Familia.familia'),
			ComboBoxFilter('LF_Raunkier.LF_Raunkier'),
			ComboBoxFilter('LF_Serebryakov.LF_Serebryakov'),
			ComboBoxFilter('Relat_at_sal.relat_at_sal'),
			ComboBoxFilter('Phytocenosis.phytocenosis'),
			ComboBoxFilter('Aqua_regimen.aqua_regimen'),
			ComboBoxFilter('Area.area')
			]
        list_display = [
			'species',
			'species_loc',
			'genus',
			'genus_loc',
			'familia',
			'familia_loc'
			]
        form_display = TabForm([
			(_('title'), Form([
				'species',
				'species_loc',
				'genus',
				'genus_loc',
				'familia',
				'familia_loc',
				'image',
				'description'
            ],columns = 2)),
			(_('LF'), Form([
					'LF_Raunkier',
					'LF_Serebryakov'
					])),
			(_('Relats'), Form([
					'relat_at_sal',
					'phytocenosis',
					'aqua_regimen'
					])),
			(_('Area'), Form([
					'area',
					])),
				])
        field_attributes = {'species':{'name':_('Species')},
                           'species_loc':{'name':_('Species Loc')},
                           'genus':{'name':_('Genus')},
                           'genus_loc':{'name':_('Genus Loc')},
                           'familia':{'name':_('Familia')},
                           'familia_loc':{'name':_('Familia Loc')},
                           'image':{'name':_('Image')},
                           'description':{'name':_('Description')},
                           'LF_Raunkier':{'name':_('LF Raunkier')},
                           'LF_Serebryakov':{'name':_('LF Serebryakov')},
                           'relat_at_sal':{'name':_('Relat at sal')},
                           'phytocenosis':{'name':_('Phytocenosis')},
                           'aqua_regimen':{'name':_('Aqua regimen')},
                           'area':{'name':_('Area')}}

    #field_attributes = {'my_image':{'delegate' : ImageDelegate}}
	#field_attributes = { 'species':{'minimal_column_width':20},
	#'short_description':{'minimal_column_width':30},}
	#field_attributes = {'area_VS':{'choices':lambda o:[(True, 'Yes'),(Falce, 'No')]}}


class Genus( Entity ):
    __tablename__ = 'genus'

    genus = Column( Unicode(512), nullable = False)
    genus_loc = Column( Unicode(512))
    familia = relationship( 'Familia' )
    description = Column( camelot.types.RichText )

    speciess = relationship( 'Species' )

    familia_id = Column( Integer, ForeignKey('familia.id'), nullable = False )

    class Admin( EntityAdmin ):
        verbose_name_plural = _('Genus')
        list_display = [ 'genus', 'genus_loc', 'familia','familia_loc' ]
        form_display = TabForm([
			(_('title'), Form([
				'genus',
				'genus_loc',
				'familia',
                'familia_loc',
				'description'
                ])),
			(_('Speciess'), Form([
				'speciess'
				])),
				])
        field_attributes = {'speciess':{'name':_('Speciess')},
                           'genus':{'name':_('Genus')},
                           'genus_loc':{'name':_('Genus Loc')},
                           'familia':{'name':_('Familia')},
                           'familia_loc':{'name':_('Familia Loc')},
                           'description':{'name':_('Description')}}

    def __unicode__(self):
        return self.genus or _('unknown')


class Familia( Entity ):
    __tablename__ = 'familia'

    familia = Column( Unicode(512), nullable = False)
    familia_loc = Column( Unicode(512))
    description = Column( camelot.types.RichText )
    genuss = relationship( 'Genus' )

    class Admin( EntityAdmin ):
        verbose_name_plural = _('Familia')
        list_display = [ 'familia','familia_loc' ]
        form_display = TabForm([
			(_('title'), Form([
				'familia',
				'familia_loc',
				'description'
                ])),
			(_('Genuss'), Form([
				'genuss'
				])),
				])
        field_attributes = {'genuss':{'name':_('Genuss')},
                           'familia':{'name':_('Familia')},
                           'familia_loc':{'name':_('Familia Loc')},
                           'description':{'name':_('Description')}}

    def __unicode__(self):
        return self.familia or _('unknown')


class LF_Raunkier( Entity ):
    __tablename__ = 'LF_Raunkier'

    LF_Raunkier = Column( Unicode(512), nullable = False)
    description = Column( camelot.types.RichText )
    speciess = relationship( 'Species' )

    class Admin( EntityAdmin ):
        verbose_name_plural = _('LF Raunkier')
        list_display = [ 'LF_Raunkier' ]
        form_display = TabForm([
			(_('title'), Form([
				'LF_Raunkier',
				'description'
                ])),
			(_('Speciess'), Form([
				'speciess'
				])),
				])
        field_attributes = {'speciess':{'name':_('Speciess')},
                           'description':{'name':_('Description')},
                           'LF_Raunkier':{'name':_('LF Raunkier')}}

    def __unicode__(self):
        return self.LF_Raunkier or _('unknown')


class LF_Serebryakov( Entity ):
    __tablename__ = 'LF_Serebryakov'

    LF_Serebryakov = Column( Unicode(512), nullable = False)
    speciess = relationship( 'Species' )
    description = Column( camelot.types.RichText )

    class Admin( EntityAdmin ):
        verbose_name_plural = _('LF Serebryakov')
        list_display = [ 'LF_Serebryakov' ]
        form_display = TabForm([
			(_('title'), Form([
				'LF_Serebryakov',
				'description'
                ])),
			(_('Speciess'), Form([
				'speciess'
				])),
				])
        field_attributes = {'speciess':{'name':_('Speciess')},
                           'description':{'name':_('Description')},
                           'LF_Serebryakov':{'name':_('LF Serebryakov')}}

    def __unicode__(self):
        return self.LF_Serebryakov or _('unknown')


class Relat_at_sal( Entity ):
    __tablename__ = 'relat_at_sal'

    relat_at_sal = Column( Unicode(512), nullable = False)
    description = Column( camelot.types.RichText )
    speciess = relationship( 'Species' )

    class Admin( EntityAdmin ):
        verbose_name_plural = _('Relat at sal')
        list_display = [ 'relat_at_sal' ]
        form_display = TabForm([
			(_('title'), Form([
				'relat_at_sal',
				'description'
                ])),
			(_('Speciess'), Form([
				'speciess'
				])),
				])
        field_attributes = {'speciess':{'name':_('Speciess')},
                           'description':{'name':_('Description')},
                           'relat_at_sal':{'name':_('Relat at sal')}}

    def __unicode__(self):
        return self.relat_at_sal or _('unknown')


class Phytocenosis( Entity ):
    __tablename__ = 'phytocenosis'

    phytocenosis = Column( Unicode(512), nullable = False)
    description = Column( camelot.types.RichText )
    speciess = relationship( 'Species' )

    class Admin( EntityAdmin ):
        verbose_name_plural = _('Phytocenosis')
        list_display = [ 'phytocenosis' ]
        form_display = TabForm([
			(_('title'), Form([
				'phytocenosis',
				'description'
                ])),
			(_('Speciess'), Form([
				'speciess'
				])),
				])
        field_attributes = {'speciess':{'name':_('Speciess')},
                           'description':{'name':_('Description')},
                           'phytocenosis':{'name':_('Phytocenosis')}}

    def __unicode__(self):
        return self.phytocenosis or _('unknown')


class Aqua_regimen( Entity ):
    __tablename__ = 'aqua_regimen'

    aqua_regimen = Column( Unicode(512), nullable = False)
    description = Column( camelot.types.RichText )
    speciess = relationship( 'Species' )

    class Admin( EntityAdmin ):
        verbose_name_plural = _('Aqua regimen')
        list_display = [ 'aqua_regimen' ]
        form_display = TabForm([
			(_('title'), Form([
				'aqua_regimen',
				'description'
                ])),
			(_('Speciess'), Form([
				'speciess'
				])),
				])
        field_attributes = {'speciess':{'name':_('Speciess')},
                           'description':{'name':_('Description')},
                           'aqua_regimen':{'name':_('Aqua regimen')}}

    def __unicode__(self):
        return self.aqua_regimen or _('unknown')


class Area( Entity ):
    __tablename__ = 'area'

    area = Column( Unicode(512), nullable = False)
    area_loc = Column( Unicode(512))
    geo_map = Column( camelot.types.Image( upload_to = 'image' ) )
    description = Column( camelot.types.RichText )
    speciess = relationship( 'Species', secondary = 'species_area' )

    class Admin( EntityAdmin ):
        verbose_name_plural = _('Area')
        list_display = [ 'area', 'area_loc' ]
        form_display = TabForm([
			(_('title'), Form([
				'area',
				'area_loc',
				'geo_map',
				'description'
                ])),
			(_('Speciess'), Form([
				'speciess'
				])),
				])
        field_attributes = {'speciess':{'name':_('Speciess')},
                           'description':{'name':_('Description')},
                           'geo_map':{'name':_('Geo Map')},
                           'area':{'name':_('Area')},
                           'area_loc':{'name':_('Area Loc')}}

    def __unicode__(self):
        return self.area or _('unknown')


# импортируемые данные

class Import_conspect( Entity ):

    __tablename__ = 'Import conspect'

    familia = Column( Unicode(512))
    familia_loc = Column( Unicode(512))
    genus = Column( Unicode(512))
    genus_loc = Column( Unicode(512))
    species = Column( Unicode(512))
    species_loc = Column( Unicode(512))
    LF_Raunkier = Column( Unicode(512))
    LF_Serebryakov = Column( Unicode(512))
    relat_at_sal = Column( Unicode(512))
    phytocenosis = Column( Unicode(512))
    aqua_regimen = Column( Unicode(512))
    area = Column( Unicode(512))

    def __unicode__( self ):
        return self.species or _('unknown')

    class Admin( EntityAdmin ):
        verbose_name_plural = _('Import Conspect')
        list_actions = [Cons2db()]
        list_display = ['familia',
            'familia_loc',
            'genus',
            'genus_loc',
			'species',
            'species_loc',
			'LF_Raunkier',
			'LF_Serebryakov',
			'relat_at_sal',
			'phytocenosis',
			'aqua_regimen',
			'area']
        field_attributes = {'species':{'name':_('Species')},
                           'species_loc':{'name':_('Species Loc')},
                           'genus':{'name':_('Genus')},
                           'genus_loc':{'name':_('Genus Loc')},
                           'familia':{'name':_('Familia')},
                           'familia_loc':{'name':_('Familia Loc')},
                           'image':{'name':_('Image')},
                           'description':{'name':_('Description')},
                           'LF_Raunkier':{'name':_('LF Raunkier')},
                           'LF_Serebryakov':{'name':_('LF Serebryakov')},
                           'relat_at_sal':{'name':_('Relat at sal')},
                           'phytocenosis':{'name':_('Phytocenosis')},
                           'aqua_regimen':{'name':_('Aqua regimen')},
                           'area':{'name':_('Area')}}


class Species_area( Entity ):
    __tablename__ = 'species_area'

    species_id = Column(Integer, ForeignKey('species.id'))
    area_id = Column(Integer, ForeignKey('area.id'))



# begin column_property

from sqlalchemy.orm import column_property
from sqlalchemy import select


Genus.familia_lat = column_property( select( [( Familia.familia) ],
                                                    Genus.familia_id == Familia.id ) )

Genus.familia_loc = column_property( select( [( Familia.familia_loc) ],
                                                    Genus.familia_id == Familia.id ) )

Species.genus_loc = column_property( select( [( Genus.genus_loc) ],
                                                    Species.genus_id == Genus.id ) )

Species.familia = column_property( select( [( Genus.familia_lat) ],
                                                    Species.genus_id == Genus.id ) )

Species.familia_loc = column_property( select( [( Genus.familia_loc) ],
                                                    Species.genus_id == Genus.id ) )

# end column_property
