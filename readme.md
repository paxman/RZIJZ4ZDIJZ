RZIJZ4ZDIJZ
===================
Nujne informacije iz registra zavezancev informacij javnega značaja (RZIJZ) v odprt(ejš)ih oblikah (CSV, LDIFF) za (masovno) pošiljanje ZDIJZ zahtevkov.

**POZOR!**
V registru ima e-naslov vpisan - četudi nezakonito - manj kot polovica registriranih zavezancev!

Oblike
-------------

 - **CSV**
 Ločitveni znak je vejica. Zgolj najpomembnejše: naziv organa, e-naslov, naslov, tip subjekta.
 Datoteke:
 VSI.csv - seznam vseh zavezancev
 [*].csv - * je oblika subjekta (banka, delniška družba, d.o.o., ,ministrstvo, sklad, zavod, ...) ali [vrsta pravne podlage](http://www.ajpes.si/Registri/Drugi_registri/Zavezanci_za_informacije_javnega_znacaja/Pravne_podlage?print=yes)
 
   **1.** Thunderbird (/csv/tb/*)
  CSV oblika z zaglavjem za uvoz v slovenski Thunderbird. 
  Zaglavje: ["Ime","Prikazano ime","Glavna e-pošta:","Naslov v službi","Organizacija"]

   **2.** Outlook (/csv/ol/*)
  CSV oblika z zaglavjem za uvoz v angleški Outlook. 
  Zaglavje: ["Title","First Name","E-mail Address","Business Street","Company"]
  
 - **LDIF**(/ldif/*)
[LDIF](https://en.wikipedia.org/wiki/LDAP_Data_Interchange_Format) oblika imenika [v Thunderbirdu lastni shemi](https://wiki.mozilla.org/MailNews:Mozilla_LDAP_Address_Book_Schema). 
Iste podatki kot pri CSV obliki.
Vsebuje poštne sezname, ki so ekvivalentni datotekam pri CSV obliki. 

 **POZOR!**
 Thunderbird ima groznega hrošča, ki kontakta ne doda na poštni seznam če ta nima vpisanega e-naslova (v imenik ga uvozi vseeno),
  zato ga boste morali na poštni seznam dodati sami.

Uporaba
-------------
Načeloma so poštni odjemalci dovolj pametni, da uvoz ene izmed CSV oblik ne bi smel biti (prevelik) problem.
 - **Thunderbird**
 Uvozi imenik v LDIF obliki, ustvari sporočilo, za naslovnike izberi enega izmed poštnih seznamov iz imenika, in uporabi [Mail Merge](https://addons.mozilla.org/en-US/thunderbird/addon/mail-merge/). Za naziv in naslov organa v zahtevi po ZDIJZ uporabi spremenljivki {{FirstName}} in {{WorkAddress}}.
 
 - **Outlook**
  Netestirano.
  
Posodobitev
-------------
Za Python 2 >= 2.7.9 ali Python 3 >= 3.4.
> pip install -r requirements.txt
> python rzijz4zdijz.py
