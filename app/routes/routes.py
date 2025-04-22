from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy import func, select
from flask_jwt_extended import jwt_required
from datetime import datetime, date, timedelta
from app.extensions import cache, db
from app.models.models import Kunde, Auftrag, Bestellposition


class Kunde_list(Resource):
    @cache.cached(timeout=60)                                       #routenspezifisches Caching --> Erneuerung des Cache alle 60 Sekunden
    @jwt_required()
    def get(self):                              #Service Initialisierung   
        now = datetime.utcnow().isoformat()
        print(f"Uhrzeit der Generierung des Cache: {now}")
#        current_user = get_jwt_identity()

        #eigentlicher Service startet hier
        kunden=Kunde.query.all() 
        return [{'kd_nr':kunde.kd_nr, 'vorname':kunde.vorname}for kunde in kunden]



class Kunde_add(Resource):  
    #@cache.cached(timeout=60)
    @jwt_required()
    
    def post(self):
        data=request.get_json()     #hier wird die gesamte im URL-Body mitgeteilte JSOn entgegengenommen
                                            #Welche Daten benötigt die Datenbank für einen vollständigen Eintrag ? --> Wie soll die JSON-Datenstruktur aussehen ? 
        neue_kd_nr=db.session.query(func.max(Kunde.kd_nr)).scalar()+1 
        letzter_zugriff_aktuell=datetime.utcnow().isoformat()
      
        kunde_neu=Kunde(
                kd_nr=neue_kd_nr,
                vorname=data['vorname'],
                nachname=data['nachname'],
                strasse=data['strasse'],
                plz=data['plz'],
                ort=data['ort'],
                vorwahl=data['vorwahl'],
                telefon=data['telefon'],
                geburtsdatum=data['geburtsdatum'],
                ledig=data['ledig'],
                rabatt=data['rabatt'],
                letzter_zugriff=letzter_zugriff_aktuell)
        db.session.add(kunde_neu)
        db.session.commit()
        print(f"Kunde -{neue_kd_nr}- angelegt")
        return {"message": "Alles erstellt."}, 201

class Get_max_kd_nr(Resource):                                          #Service: Get_max_kd_nr
    def get(self):
        max_kd_nr = db.session.query(db.func.max(Kunde.kd_nr)).scalar()
        return {"kd_nr_max":max_kd_nr or 0}, 200





                                                                #SERVICE_A

class Service_A(Resource):         
    def post(self):

        data=request.get_json()                 #daten aus JSON-Body auslesen
        
        
        neue_kd_nr=db.session.query(func.max(Kunde.kd_nr)).scalar()+1               #neue kd_nr -> 1 höher als die aktuell höchste
        neue_auft_nr=db.session.query(func.max(Auftrag.auft_nr)).scalar()+1         #neue auft_nr -> 1 höher als die aktuell höchste
        aktuelle_zeit=datetime.utcnow().isoformat()                                 #aktuelle_zeit
        aktuelles_datum=date.today()
       
        kunde_data=data.get("kunde")
        auftrag_data=data.get("auftrag")
        bestellpositionen_data=data.get("bestellpositionen")
        
        #Folgendes ist für die Prüfung, ob ein Kunde mit gleichem vor-, nachnamen sowie geburtsdatum existiert.
        kunde_exist=db.session.query(Kunde).filter((Kunde.vorname==kunde_data['vorname']) & (Kunde.nachname==kunde_data['nachname']) & (Kunde.geburtsdatum==kunde_data['geburtsdatum']))  #Statement zur Überprüfung, ob vorname existiert
        k_exist=db.session.query(kunde_exist.exists()).scalar() #hier werden drei unterabfragen abgrafragt. Sollte in allen reihen etwas gefunden wrden, so wird mittels scalar() True zurückgegeben

        #Der Auftrag wird erstellt und einer neuen kd_nr zugewiesen- Was falsch ist. 
        kd_nr_aktu=db.session.query(Kunde.kd_nr).filter((Kunde.vorname==kunde_data['vorname']) & (Kunde.nachname==kunde_data['nachname']) &(Kunde.geburtsdatum==kunde_data['geburtsdatum'])).scalar()
        
        if k_exist:         #==True
            print(f"Kunde with {kunde_data['vorname']}, {kunde_data['nachname']}, born in {kunde_data['geburtsdatum']} DOES already EXIST with kd_nr: {kd_nr_aktu}.")
            auftrag_neu=Auftrag(
                auft_nr=neue_auft_nr,
                bestelldat=aktuelles_datum,
                lieferdat=aktuelles_datum+timedelta(days=1),
                zahlungsziel=aktuelles_datum+timedelta(days=21),
                zahlungseingang=aktuelles_datum,
                mahnung=0,
                fk_kunde=kd_nr_aktu,
                fk_shop=auftrag_data['fk_shop']                      
                )
            db.session.add(auftrag_neu)
            print(f"New Auftrag with auft_nr. {neue_auft_nr} was created") 
            
            for best_position in bestellpositionen_data:
                bestellposition_neu = Bestellposition(
                fk_auftrag=neue_auft_nr,
                fk_artikel=best_position['fk_artikel'],
                position=best_position['position'],
                anzahl=best_position['anzahl']
                )
                db.session.add(bestellposition_neu)
            

            db.session.commit()
            print(f"New Bestellpositionen were created.")
            
            return {"message": "Alles erstellt außer Kunde."}, 201
 

        else:
            print(f"Kunde with {kunde_data['vorname']}, {kunde_data['nachname']}, born in {kunde_data['geburtsdatum']} DOES NOT EXIST.")
            kunde_neu=Kunde(
                kd_nr=neue_kd_nr,
                vorname=kunde_data['vorname'],
                nachname=kunde_data['nachname'],
                strasse=kunde_data['strasse'],
                plz=kunde_data['plz'],
                ort=kunde_data['ort'],
                vorwahl=kunde_data['vorwahl'],
                telefon=kunde_data['telefon'],
                geburtsdatum=kunde_data['geburtsdatum'],
                ledig=kunde_data['ledig'],
                rabatt=kunde_data['rabatt'],
                letzter_zugriff=aktuelle_zeit)
            db.session.add(kunde_neu)
            print(f"Kunde with kd_nr: {neue_kd_nr} was created.")
            
            auftrag_neu=Auftrag(
                auft_nr=neue_auft_nr,
                bestelldat=aktuelles_datum,
                lieferdat=aktuelles_datum+timedelta(days=1),
                zahlungsziel=aktuelles_datum+timedelta(days=21),
                zahlungseingang=aktuelles_datum,
                mahnung=0,
                fk_kunde=neue_kd_nr,
                fk_shop=auftrag_data['fk_shop']                      
                )
            db.session.add(auftrag_neu)
            print(f"New Auftrag with auft_nr. {neue_auft_nr} was created.")
            for best_position in bestellpositionen_data:
                bestellposition_neu = Bestellposition(
                fk_auftrag=neue_auft_nr,
                fk_artikel=best_position['fk_artikel'],
                position=best_position['position'],
                anzahl=best_position['anzahl']
                )
                db.session.add(bestellposition_neu)
            print(f"Bestellpositionen were created.") 
        

            db.session.commit()
            return {"message": "Alles erstellt mit Kunde."}, 201

class Service_B(Resource):
    @cache.cached(timeout=60)
    @jwt_required()
    def get(self, id):
        stmt = select(Auftrag).where(Auftrag.fk_kunde==id)
        result=db.session.execute(stmt)
        result_json=dict()
        auftrag=dict()
        for auft in result.scalars():
           # print(f"Auftragsnummer: {auft.auft_nr}")
            str1="Auftrag "+str(auft.auft_nr)
            auftrag[str1]={
                     'datum':auft.bestelldat,
                     'fk_shop':auft.fk_shop
                        }
            stmt2 = select(Bestellposition).where(Bestellposition.fk_auftrag==auft.auft_nr)
            result2 =db.session.execute(stmt2)
            
            for bp in result2.scalars():
               # print(f"Bestellposition: {bp.position}, Artikelnr.: {bp.fk_artikel}, Anzahl: {bp.anzahl}")
                str2="position "+str(bp.position)
                auftrag[str1][str2]=[]
                auftrag[str1][str2].append({
                    "Artikel Nr.":bp.fk_artikel, 
                    "Anzahl":bp.anzahl
                                   })

            result_json.update(auftrag)
        return jsonify(result_json)
                
                #return jsonify({'Auftragsnummer':auft.auft_nr,'Bestellposition':bp.fk_artikel,'Anzahl':bp.anzahl}), 200


