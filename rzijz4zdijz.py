# -*- coding: utf-8 -*-
import os
#from pprint import pprint

from lxml import etree
from ldif3 import LDIFWriter

#...
from pip._vendor.distlib.util import CSVWriter

objclasses = {'objectclass': [u'top', u'person',u'organizationalPerson',u'inetOrgPerson',u'mozillaAbPersonAlpha']}

def get_rzijz_root():
    root = etree.parse("http://www.ajpes.si/RZIJZ/Vpogled/XML", parser=None, base_url=None)
    return root

#from parsel/selector
def remove_namespaces(root):
    
    #remove namespaces
    for el in root.iter('*'):
        if el.tag.startswith('{'):
            el.tag = el.tag.split('}', 1)[1]
        # loop on element attributes also
        for an in el.attrib.keys():
            if an.startswith('{'):
                el.attrib[an.split('}', 1)[1]] = el.attrib.pop(an)

def clean_folders():
    
    import shutil
    shutil.rmtree('./csv')
    shutil.rmtree('./ldif')
    
    try:
        os.makedirs("./csv/tb")
        os.makedirs("./csv/ol")
        os.makedirs("./ldif")
    except (IOError, OSError) as exception:
        pass
    
    
def parse_zavezance(root):            
    zav_by_type = {}
    zavezanci = []
    e = 0
    z = 0
    #fields = []
    
    for zavezanec in root.xpath("//Zavezanec"):
        
        item = {'name':"",
                'mail':"",
                'street':"",
                'company':"",
                }
        
        #oblika zavezanca in pravne podlage zavezanca
        item_types = []
        
        z+=1
        
        for field in zavezanec.xpath("./*"):
            sub_fields = field.xpath("./*")
            
            tag = field.tag

            if tag == "Naslov":
                fieldr = {}
                #need subfields
                for sub_field in sub_fields:
                    fieldr[sub_field.tag] = sub_field.xpath("./text()")#.extract_first("")
                    
                naslov = " ".join([
                    fieldr.get('Ulica',[""]).pop(),
                    fieldr.get('HisnaStevilka',[""]).pop(),
                    fieldr.get('HisnaStevilkaDodatek',[""]).pop()
                ]).strip()
                
                posta = " ".join([
                    fieldr.get('PostnaSt',[""]).pop(),
                    fieldr.get('Posta',[""]).pop()
                ]).strip()
                
                naslov = ", ".join([naslov,posta])
                item['street'] = naslov.encode("utf-8")
                
            elif tag == "Naziv":
                naziv = field.xpath("./text()")
                if naziv:
                    naziv = naziv.pop()
                    item['name'] = naziv.encode("utf-8")
                    
            elif tag == "OblikaNaziv":    
                naziv_oblika = field.xpath("./text()")
                if naziv_oblika:
                    naziv_oblika = naziv_oblika.pop()
                    item['company'] = ", ".join([item.get('company',""), naziv.encode("utf-8")])
                    item_types.append(naziv_oblika.lower())
                    
            elif tag == "PravnaPodlaga":                    
                for sub_field in sub_fields:
                    if sub_field.tag == 'VrstaPravnePodlageNaziv':
                        field = sub_field.xpath("./text()").pop().split(" - ").pop()
                        item_types.append(field.lower())
                        break;
    
            elif tag == "ENaslov":
                enaslov = field.xpath("./text()")
                
                if enaslov:
                    e+=1
                    enaslov = enaslov.pop()
                    item['mail'] = enaslov.encode("utf-8")
                    #print enaslov
        
        #item['types'] = list(set(item_types))
        for item_type in list(set(item_types)):
            temptype = zav_by_type.get(item_type,[])
            temptype.append(item)
            zav_by_type[item_type]=temptype
            
        zavezanci.append(item)
        
        #pprint (item)
        #pprint (list(set(item_types)))
    return zavezanci, zav_by_type

def item_to_ldif(item):
    ldif_item = item.copy()
    ldif_item['cn'] = item['name']
    ldif_item['givenName'] = item['name']
    
    del ldif_item['name']
    
    for key,value in ldif_item.iteritems():
        ldif_item[key] = [value]
        
    return ldif_item

def get_item_dn(item):
    dn = "cn={0}".format(item.get('name',''),)
    if item.get('mail',None):
        dn += ",mail="+item.get('mail','')
    return dn

def item_to_csv(item):
    csv_item = [item.get('name',''),
                                 item.get('name',''),
                                 item.get('mail',''),
                                 item.get('street',''),
                                 item.get('company','')
                                ]        
    return csv_item

def export_csv_all(items):
    #thunderbird csv
    #thunderbird SI(!)
    thunderbird_csv_writer = CSVWriter('./csv/tb/VSI.csv')
    #thun @ 45.3.0, SL_SI
    #all_tb_headers = ["Ime","Priimek","Prikazano ime","Vzdevek","Glavna e-pošta:","Dodatna e-pošta:","Zaslonsko ime","Telefon v službi","Telefon doma","Številka faksa","Številka pozivnika","Številka mobilnika","DomaÄŤi naslov","DomaÄŤi naslov 2","Mesto (doma)","Zv. država (doma)","Poštna številka (doma)","Država (doma)","Naslov v službi","Naslov v službi 2","Mesto (služba)","Zv. država (služba)","Poštna številka (služba)","Država (služba)","Službeni naziv","Oddelek","Organizacija","Spletna stran 1","Spletna stran 2","Rojstno leto","Rojstni mesec","Rojstni dan","Po meri 1","Po meri 2","Po meri 3","Po meri 4","Beležke"] 
    thunderbird_csv_writer.writerow(["Ime","Prikazano ime","Glavna e-pošta:","Naslov v službi","Organizacija"])
    
    #outlook csv
    #http://stackoverflow.com/questions/4847596/what-are-the-csv-headers-in-outlook-contact-export
    outlook_csv_writer = CSVWriter('./csv/ol/VSI.csv')
    #all_outlook_csvheaders = ["Title","First Name","Middle Name","Last Name","Suffix","Company","Department","Job Title","Business Street","Business Street 2","Business Street 3","Business City","Business State","Business Postal Code","Business Country/Region","Home Street","Home Street 2","Home Street 3","Home City","Home State","Home Postal Code","Home Country/Region","Other Street","Other Street 2","Other Street 3","Other City","Other State","Other Postal Code","Other Country/Region","Assistant's Phone","Business Fax","Business Phone","Business Phone 2","Callback","Car Phone","Company Main Phone","Home Fax","Home Phone","Home Phone 2","ISDN","Mobile Phone","Other Fax","Other Phone","Pager","Primary Phone","Radio Phone","TTY/TDD Phone","Telex","Account","Anniversary","Assistant's Name","Billing Information","Birthday","Business Address PO Box","Categories","Children","Directory Server","E-mail Address","E-mail Type","E-mail Display Name","E-mail 2 Address","E-mail 2 Type","E-mail 2 Display Name","E-mail 3 Address","E-mail 3 Type","E-mail 3 Display Name","Gender","Government ID Number","Hobby","Home Address PO Box","Initials","Internet Free Busy","Keywords","Language","Location","Manager's Name","Mileage","Notes","Office Location","Organizational ID Number","Other Address PO Box","Priority","Private","Profession","Referred By","Sensitivity","Spouse","User 1","User 2","User 3","User 4","Web Page"] 
    outlook_csv_writer.writerow(["Title","First Name","E-mail Address","Business Street","Company"])
    
    
    for item in items:
        csv_item = item_to_csv(item)
        thunderbird_csv_writer.writerow(csv_item)
        outlook_csv_writer.writerow(csv_item)

def export_csv_by_type(zav_by_type):
    
    for key, zav_by_type in zav_by_type.items():
        tb_csv_writer = CSVWriter("./csv/tb/"+key+'.csv')
        tb_csv_writer.writerow(["Ime","Prikazano ime","Glavna e-pošta:","Naslov v službi","Organizacija"])
        
        outlook_csv_writer = CSVWriter("./csv/ol/"+key+'.csv')
        #all_outlook_csvheaders = ["Title","First Name","Middle Name","Last Name","Suffix","Company","Department","Job Title","Business Street","Business Street 2","Business Street 3","Business City","Business State","Business Postal Code","Business Country/Region","Home Street","Home Street 2","Home Street 3","Home City","Home State","Home Postal Code","Home Country/Region","Other Street","Other Street 2","Other Street 3","Other City","Other State","Other Postal Code","Other Country/Region","Assistant's Phone","Business Fax","Business Phone","Business Phone 2","Callback","Car Phone","Company Main Phone","Home Fax","Home Phone","Home Phone 2","ISDN","Mobile Phone","Other Fax","Other Phone","Pager","Primary Phone","Radio Phone","TTY/TDD Phone","Telex","Account","Anniversary","Assistant's Name","Billing Information","Birthday","Business Address PO Box","Categories","Children","Directory Server","E-mail Address","E-mail Type","E-mail Display Name","E-mail 2 Address","E-mail 2 Type","E-mail 2 Display Name","E-mail 3 Address","E-mail 3 Type","E-mail 3 Display Name","Gender","Government ID Number","Hobby","Home Address PO Box","Initials","Internet Free Busy","Keywords","Language","Location","Manager's Name","Mileage","Notes","Office Location","Organizational ID Number","Other Address PO Box","Priority","Private","Profession","Referred By","Sensitivity","Spouse","User 1","User 2","User 3","User 4","Web Page"] 
        outlook_csv_writer.writerow(["Title","First Name","E-mail Address","Business Street","Company"])

        #write mailing list  members
        for item in zav_by_type:
            
            csv_item = item_to_csv(item)
            tb_csv_writer.writerow(csv_item)
            outlook_csv_writer.writerow(csv_item)
            
def export_csv(items,zav_by_type):
    export_csv_all(items)
    export_csv_by_type(zav_by_type)

def export_ldif(items,zav_by_type):
    ldifwriter = LDIFWriter(open('./ldif/rzijz.ldif', 'wb'))
    all_members = []
    
    for item in items:

        dn = get_item_dn(item)
        all_members.append(dn)
        
        ldif_item =  item_to_ldif(item)
        ldif_item.update(objclasses)
            
        ldifwriter.unparse(dn, ldif_item)
    
    #write "mailing lists"
    for key, zavezanci in zav_by_type.items():

        #mailing list title and members
        group_item = {'objectclass': [u'top', u'groupOfNames'],
                      'cn': [key.encode("utf-8")],
                      'member': [get_item_dn(item) for item in zavezanci]}   
        
        ldifwriter.unparse("cn={0}".format(key.encode("utf-8")), group_item)
    
    #write all mailing list
    group_item = {'objectclass': [u'top', u'groupOfNames'],
                      'cn': ["Vsi".encode("utf-8")],
                      'member': all_members}   
         
    ldifwriter.unparse("cn={0}".format("Vsi".encode("utf-8")), group_item)
    
"""----- main ------"""   
clean_folders()          
root = get_rzijz_root()
remove_namespaces(root)
zavezanci, zav_by_type = parse_zavezance(root)
export_csv(zavezanci, zav_by_type)
export_ldif(zavezanci, zav_by_type)