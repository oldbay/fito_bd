#!/usr/bin/env python2
#-*- coding: utf-8 -*-

from sqlalchemy.sql import func
from model import \
        Species_area,\
        Species,\
        Genus,\
        Familia,\
        LF_Raunkier,\
        LF_Serebryakov,\
        Relat_at_sal,\
        Phytocenosis,\
        Aqua_regimen,\
        Area,\
        Import_conspect


def connectToDatabase():
    """
    Connect to our SQLite database and return a Session object
    """
    from camelot.core.orm import Session
    session = Session()
    return session


def conspect_query():
    session = connectToDatabase()

    table= []
    string =[]
    for instance in session.query(Import_conspect).all():
        string = [
            instance.id,
            instance.familia,
            instance.familia_loc,
            instance.genus,
            instance.genus_loc,
            instance.species,
            instance.species_loc,
            instance.LF_Raunkier,
            instance.LF_Serebryakov,
            instance.relat_at_sal,
            instance.phytocenosis,
            instance.aqua_regimen,
            instance.area
        ]
        table.append(string)
    session.close()
    return table


def familia_parse():
    session = connectToDatabase()
    for string in conspect_query():
        try:
            SQ = session.query(Familia).filter_by(familia = string[1]).first()
        except:
            SQ = False
        if SQ == None and string[1] != None:
            add_row = Familia()
            add_row.familia = string[1]
            add_row.familia_loc = string[2]

            session.add(add_row)
            session.begin(subtransactions=True).commit()
    session.close()


def genus_parse():
    session = connectToDatabase()
    for string in conspect_query():
        try:
            SQ = session.query(Genus).filter_by(genus = string[3]).first()
        except:
            SQ = False
        if SQ == None and string[3] != None:
            add_row = Genus()
            add_row.genus = string[3]
            add_row.genus_loc = string[4]
            FamiliaID = session.query(Familia.id).filter_by(familia = string[1]).first()[0]
            add_row.familia_id = FamiliaID

            session.add(add_row)
            session.begin(subtransactions=True).commit()
    session.close()


def LF_Raunkier_parse():
    session = connectToDatabase()
    for string in conspect_query():

        try:
            string = string[7].replace(' ','').replace('.','')
        except:
            string = []

        try:
            SQ = session.query(LF_Raunkier).filter_by(LF_Raunkier = string).first()
        except:
            SQ = False
        if SQ == None and string != None:
            add_row = LF_Raunkier()
            add_row.LF_Raunkier = string

            session.add(add_row)
            session.begin(subtransactions=True).commit()
    session.close()


def LF_Serebryakov_parse():
    session = connectToDatabase()
    for string in conspect_query():

        try:
            string = string[8].replace('.','').strip()
        except:
            string = []

        try:
            SQ = session.query(LF_Serebryakov).filter_by(LF_Serebryakov = string).first()
        except:
            SQ = False
        if SQ == None and string != None:
            add_row = LF_Serebryakov()
            add_row.LF_Serebryakov = string

            session.add(add_row)
            session.begin(subtransactions=True).commit()
    session.close()



def Relat_at_sal_parse():
    session = connectToDatabase()
    for string in conspect_query():

        try:
            string = string[9].replace(' ','').replace('.','')
        except:
            string = []

        try:
            SQ = session.query(Relat_at_sal).filter_by(relat_at_sal = string).first()
        except:
            SQ = False
        if SQ == None and string != None:
            add_row = Relat_at_sal()
            add_row.relat_at_sal = string

            session.add(add_row)
            session.begin(subtransactions=True).commit()
    session.close()


def Phytocenosis_parse():
    session = connectToDatabase()
    for string in conspect_query():

        try:
            string = string[10].replace(' ','').replace('.','')
        except:
            string = []

        try:
            SQ = session.query(Phytocenosis).filter_by(phytocenosis = string).first()
        except:
            SQ = False
        if SQ == None and string != None:
            add_row = Phytocenosis()
            add_row.phytocenosis = string

            session.add(add_row)
            session.begin(subtransactions=True).commit()
    session.close()


def Aqua_regimen_parse():
    session = connectToDatabase()
    for string in conspect_query():

        try:
            string = string[11].replace(' ','').replace('.','')
        except:
            string = []

        try:
            SQ = session.query(Aqua_regimen).filter_by(aqua_regimen = string).first()
        except:
            SQ = False
        if SQ == None and string != None:
            add_row = Aqua_regimen()
            add_row.aqua_regimen = string

            session.add(add_row)
            session.begin(subtransactions=True).commit()
    session.close()


def Area_parse():
    session = connectToDatabase()
    for meto_string in conspect_query():
        try:
            split_string = meto_string[12].split(',')
        except:
            split_string = []
        for string in split_string:
            string = string.replace('.','').strip()
            try:
                SQ = session.query(Area).filter_by(area = string).first()
            except:
                SQ = False
            if SQ == None and string != None:
                add_row = Area()
                add_row.area = string

                session.add(add_row)
                session.begin(subtransactions=True).commit()
    session.close()


def species_parse():
    #session = connectToDatabase()
    for string in conspect_query():
        session = connectToDatabase()
        try:
            SQ = session.query(Species).filter_by(species = string[5]).first()
        except:
            SQ = False
        if SQ == None and string[5] != None:
            add_row = Species()
            add_row.species = string[5]
            add_row.species_loc = string[6]
            #Relations:
            #genus
            GenusID = session.query(Genus.id).filter_by(genus = string[3]).first()[0]
            add_row.genus_id = GenusID
            #LF_Raunkier
            try:
                LF_RaunkierID = session.query(LF_Raunkier.id).filter_by(LF_Raunkier = string[7].replace(' ','').replace('.','')).first()[0]
                add_row.LF_Raunkier_id = LF_RaunkierID
            except:
                pass
            #LF_Serebryakov
            try:
                LF_SerebryakovID = session.query(LF_Serebryakov.id).filter_by(LF_Serebryakov = string[8].replace('.','').strip()).first()[0]
                add_row.LF_Serebryakov_id = LF_SerebryakovID
            except:
                pass
            #Relat_at_sal
            try:
                Relat_at_salID =  session.query(Relat_at_sal.id).filter_by(relat_at_sal = string[9].replace(' ','').replace('.','')).first()[0]
                add_row.relat_at_sal_id = Relat_at_salID
            except:
                pass
            #Phytocenosis
            try:
                PhytocenosisID =  session.query(Phytocenosis.id).filter_by(phytocenosis = string[10].replace(' ','').replace('.','')).first()[0]
                add_row.phytocenosis_id = PhytocenosisID
            except:
                pass
            #Aqua_regimen
            try:
                Aqua_regimenID =  session.query(Aqua_regimen.id).filter_by(aqua_regimen = string[11].replace(' ','').replace('.','')).first()[0]
                add_row.aqua_regimen_id = Aqua_regimenID
            except:
                pass

            session.add(add_row)
            session.begin(subtransactions=True).commit()
            session.close()

            #Area
            species_id = session.query(func.max(Species.id)).scalar()

            try:
                split_string = string[12].split(',')
            except:
                split_string = False

            if split_string:
                for one_string in split_string:
                    one_string = one_string.replace('.','').strip()
                    AreaID =  session.query(Area.id).filter_by(area = one_string).first()[0]
                    add_in_row = Species_area()
                    add_in_row.species_id = species_id
                    add_in_row.area_id = AreaID

                    session.add(add_in_row)
                    session.begin(subtransactions=True).commit()
                session.close()
