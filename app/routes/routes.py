from flask import request, jsonify, make_response
from flask_restful import Resource
from sqlalchemy import func, select
from flask_jwt_extended import jwt_required
from datetime import datetime, date, timedelta
from app.extensions import cache, db, ma
from app.models.models import Kunde, Auftrag, Bestellposition
from app.schemas.schemas import KundeSchema, AuftragSchema, BestellpositionSchema, NeuerAuftragSchema
from sqlalchemy.orm import selectinload

                

               # https://flask.palletsprojects.com/en/stable/api/#flask.Response

from pprint import pprint

class Service_A(Resource):         
    @jwt_required()
    def post(self):
        data = request.get_json()

        kunde_input = data.get("kunde")
        auftrag_input = data.get("auftrag")
        bestellpos_input = data.get("bestellpositionen")  

        kunde_schema = KundeSchema()
        auftrag_schema = AuftragSchema()
        bestellposition_schema = BestellpositionSchema(many=True)

        # 1. Prüfen ob Kunde existiert
        kunde_query = db.session.query(Kunde).filter(
            (Kunde.vorname == kunde_input["vorname"]) &
            (Kunde.nachname == kunde_input["nachname"]) &
            (Kunde.geburtsdatum == kunde_input["geburtsdatum"])
        )

        kunde = kunde_query.first()

        if not kunde:
            # Kunde existiert nicht → neu anlegen
            kunde = kunde_schema.load(kunde_input, session=db.session)
            kunde.letzter_zugriff = datetime.utcnow()
            db.session.add(kunde)
            db.session.commit()  # Jetzt hat Kunde eine kd_nr

        # 2. Auftrag anlegen
        auftrag = Auftrag(
            fk_kunde=kunde.kd_nr,
            fk_shop=auftrag_input["fk_shop"]
        )
        db.session.add(auftrag)
        db.session.commit()  # Jetzt hat Auftrag eine auft_nr

        # 3. Bestellpositionen anlegen
        for pos_data in bestellpos_input:
            pos = Bestellposition(
                fk_auftrag=auftrag.auft_nr,
                fk_artikel=pos_data["fk_artikel"],
                position=pos_data["position"],
                anzahl=pos_data["anzahl"]
            )
            db.session.add(pos)

        db.session.commit()

        return {
            "message": "Bestellung erfolgreich erstellt.",
            "kunde_id": kunde.kd_nr,
            "auftrag_id": auftrag.auft_nr
        }, 201



class Service_B(Resource):      
    #@cache.cached(timeout=60)                                               # Cache Service B - 60 Sekunden
    @jwt_required()                                                         # JWT-Authorization

    def get(self, id):
        stmt = select(Auftrag).options(selectinload(Auftrag.bestellpositionen)).where(Auftrag.fk_kunde == id)
        result = db.session.execute(stmt).scalars().all()
        
        result_body = {}
        for auft in result:
            str1 = f"Auftrag {auft.auft_nr}"
            result_body[str1] = {
                'datum': auft.bestelldat,
                'fk_shop': auft.fk_shop,
                'auft_daten': f"/auftrag/get/{auft.auft_nr}",
            }
            for bp in auft.bestellpositionen:
                str2 = f"position {bp.position}"
                result_body[str1][str2] = [{
                    "Artikel Nr.": bp.fk_artikel,
                    "Anzahl": bp.anzahl
                }]
        result_body["kunde_daten"] = f"/kunde/get/{id}"
        
        resp = make_response(result_body)                       # Wichtig - Response objekt für die Doku
        resp.headers['Cache-Control'] = "public, max-age=60"  # cache_control Header
        return resp



