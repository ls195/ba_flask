from marshmallow import Schema, fields
from datetime import datetime, date, timedelta
from app.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.models import Kunde, Auftrag, Bestellposition


aktuelle_zeit=datetime.utcnow().isoformat()                                 #aktuelle_zeit
aktuelles_datum=date.today()


# class BestellpositionSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Bestellposition
#         include_fk = True

# class AuftragSchema(SQLAlchemyAutoSchema):
#     positionen = fields.Nested(BestellpositionSchema, many=True)

#     class Meta:
#         model = Auftrag
#         include_fk = True

# class KundeSchema(SQLAlchemyAutoSchema):
#     auftraege = fields.Nested(AuftragSchema, many=True)

#     class Meta:
#         model = Kunde


class KundeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Kunde
        load_instance = True
        include_fk = True



class AuftragSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Auftrag
        load_instance = True
        include_fk = True

class BestellpositionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Bestellposition
        load_instance = True
        include_fk = True



class NeuerAuftragSchema(Schema):
    kunde = fields.Nested(KundeSchema)
    auftrag = fields.Nested(AuftragSchema)
    bestellposition = fields.Nested(BestellpositionSchema, many=True)






# class KundeSchema(ma.Schema):
#     kd_nr=fields.Int(dump_only=True)
#     vorname= fields.Str(required=True)
#     nachname= fields.Str(required=True)
#     strasse= fields.Str(required=True)
#     plz= fields.Str(required=True)
#     ort= fields.Str(required=True)
#     vorwahl= fields.Str(required=True) 
#     telefon= fields.Str(required=True)
#     geburtsdatum= fields.Date(required=True)
#     ledig= fields.Int(required=True)
#     rabatt= fields.Float(required=True)
#     letzter_zugriff = fields.DateTime(dump_only=True)
    
#     class Meta:
#         include_fk=True
#         load_instance=True
    


# class AuftragSchema():
#     # auft_nr=fields.Int(dump_only=True)
#     # bestelldat = fields.Date(dump_only=True)
#     # lieferdat= aktuelles_datum+timedelta(days=21),
#     # zahlungsziel=aktuelles_datum+timedelta(days=21),
#     # zahlungseingang=aktuelles_datum,
#     #mahnung=0
#     #fk_kunde= fields.Nested(KundeSchema, load_only=True)                     #Foreign key auf kunde.kd_nr  
#     #fk_shop=  fields.Int(required=True)                                        #  =mapped_column(ForeignKey("shop.shop_nr"))   Foreign key auf shop.shop_nr
    
#     auft_nr = fields.Int(dump_only=True)
#     bestelldat = fields.Date(dump_only=True)
#     lieferdat = fields.Date(dump_only=True)
#     zahlungsziel = fields.Date(dump_only=True)
#     zahlungseingang = fields.Date(dump_only=True)
#     mahnung = fields.Int(dump_only=True)
#     fk_kunde = fields.Int(dump_only=True)
#     fk_shop = fields.Int(required=True)
    
#     class Meta:
        
#         #fields =("fk_shop", "bestelldat","lieferdat","zahlungsziel", "zahlungseingang", "mahnung")
#         exclude =("auft_nr", "fk_kunde")
#         include_fk = True


# class BestellpositionSchema(Schema):
#     fk_auftrag=fields.Nested(AuftragSchema, dump_only=True)
#     position=fields.Int(dump_only=True)
#     fk_artikel=fields.Int(dump_only=True)                                                        # =mapped_column(ForeignKey("artikel.art_nr"))
#     anzahl=fields.Int(required=True)
    
#     class Meta:
#         many=True
#         include_fk = True

# class NeuerAuftragSchema(Schema):
#     kunde = KundeSchema()
#     auftrag=AuftragSchema()
#     bestellposition = BestellpositionSchema()    