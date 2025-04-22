from typing import List
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from app.extensions import db

 
class Kunde(db.Model):
    __tablename__ = 'kunde'
    kd_nr:Mapped[int]=mapped_column(primary_key = True)
    vorname:Mapped[str]
    nachname:Mapped[str]
    strasse:Mapped[str]
    plz:Mapped[int]
    ort:Mapped[str]
    vorwahl:Mapped[str]
    telefon:Mapped[str]
    geburtsdatum:Mapped[date]
    ledig:Mapped[int]
    rabatt:Mapped[float]
    letzter_zugriff:Mapped[datetime]
    k_a:Mapped[List["Auftrag"]]=relationship()

class Auftrag(db.Model):
    __tablename__ = 'auftrag'
    auft_nr:Mapped[int]=mapped_column(primary_key = True)
    bestelldat:Mapped[date]
    lieferdat:Mapped[date]
    zahlungsziel:Mapped[date]
    zahlungseingang:Mapped[date]
    mahnung:Mapped[int]
    fk_kunde:Mapped[int]=mapped_column(ForeignKey("kunde.kd_nr"))                   #Foreign key auf kunde.kd_nr  
    fk_shop:Mapped[int]=mapped_column(ForeignKey("shop.shop_nr"))                   #Foreign key auf shop.shop_nr
    


class Bestellposition(db.Model):
    __tableame__='bestellposition'
    fk_auftrag:Mapped[int]=mapped_column(ForeignKey("auftrag.auft_nr"))
    position:Mapped[int]
    fk_artikel:Mapped[int]=mapped_column(ForeignKey("artikel.art_nr"))
    anzahl:Mapped[int]

    __table_args__=(
            PrimaryKeyConstraint('fk_auftrag', 'fk_artikel'),
            )

class Artikel(db.Model):
    __tablename__='artikel'
    art_nr:Mapped[int]=mapped_column(primary_key=True)
    artikelbezeichnung:Mapped[str]
    einzelpreis:Mapped[float]
    gewicht:Mapped[float]
    fk_hersteller:Mapped[float]=mapped_column(ForeignKey("hersteller.herst_nr"))
    

class Hersteller(db.Model):
    __tablename__='hersteller'
    herst_nr:Mapped[int]=mapped_column(primary_key=True)
    herstellerbezeichnung:Mapped[str]

class Stadt(db.Model):
    __tablename__='stadt'
    stadt_nr:Mapped[int]=mapped_column(primary_key=True)
    stadt:Mapped[str]
    lat:Mapped[float]
    lot:Mapped[float]

class Shop(db.Model):
    __tablename__='shop'
    shop_nr:Mapped[int]=mapped_column(primary_key=True)
    fk_shoptyp:Mapped[int]
    strasse:Mapped[str]
    plz:Mapped[str]
    fk_stadt:Mapped[int]=mapped_column(ForeignKey("stadt.stadt_nr"))
    s_a:Mapped[List["Auftrag"]]=relationship()                                         
