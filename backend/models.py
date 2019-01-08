#!/usr/bin/python3
# -*- coding: utf-8 -*-

from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import UUID, JSONB

from gncitizen.core.commons.models import (
    ProgramsModel, TimestampMixinModel, MediaModel)
from gncitizen.core.users.models import ObserverMixinModel
from gncitizen.utils.utilssqlalchemy import serializable, geoserializable
from gncitizen.core.observations.models import ObservationModel
from server import db


def create_schema(db):
    db.session.execute('CREATE SCHEMA IF NOT EXISTS gnc_sites')
    db.session.commit()


@serializable
class TypeSiteModel(TimestampMixinModel, db.Model):
    """Table des types de sites"""
    __tablename__ = 't_typesite'
    __table_args__ = {'schema': 'gnc_sites'}
    id_typesite = db.Column(db.Integer, primary_key=True, unique=True)
    category = db.Column(db.String(200))
    type = db.Column(db.String(200))
    json_schema_form = db.Column(JSONB, nullable=True)


@serializable
@geoserializable
class SiteModel(TimestampMixinModel, ObserverMixinModel, db.Model):
    """Table des sites"""
    __tablename__ = 't_sites'
    __table_args__ = {'schema': 'gnc_sites'}
    id_site = db.Column(db.Integer, primary_key=True, unique=True)
    uuid_sinp = db.Column(UUID(as_uuid=True), nullable=False, unique=True)
    id_program = db.Column(db.Integer, db.ForeignKey(
        ProgramsModel.id_program), nullable=False)
    name = db.Column(db.String(250))
    id_type = db.Column(db.Integer, db.ForeignKey(
        TypeSiteModel.id_typesite), nullable=False)
    geom = db.Column(Geometry('POINT', 4326))


class VisitModel(TimestampMixinModel, ObserverMixinModel, db.Model):
    """Table des sessions de suivis des sites"""
    __tablename__ = 't_visit'
    __table_args__ = {'schema': 'gnc_sites'}
    id_visit = db.Column(db.Integer, primary_key=True, unique=True)
    id_site = db.Column(db.Integer, db.ForeignKey(
        SiteModel.id_site, ondelete='CASCADE'))
    date = db.Column(db.Date)
    id_media = db.Column(db.Integer, db.ForeignKey(
        MediaModel.id_media, ondelete='SET NULL'))


class ObservationsOnSiteModel(TimestampMixinModel, db.Model):
    """Table de correspondance des observations avec les sites"""
    __tablename__ = 'cor_sites_obstax'
    __table_args__ = {'schema': 'gnc_sites'}
    id_cor_site_obstax = db.Column(db.Integer, primary_key=True, unique=True)
    id_site = db.Column(db.Integer, db.ForeignKey(
        SiteModel.id_site, ondelete='SET NULL'), nullable=False)
    id_obstax = db.Column(db.Integer, db.ForeignKey(
        ObservationModel.id_observation, ondelete='SET NULL'), nullable=False)


@serializable
class BibAttributeCategoryModel(db.Model):
    """Catégories d'attributs (pour la structuration des formulaires"""
    __tablename__ = 'bib_themes'
    __table_args__ = {'schema': 'gnc_sites'}
    id_attr_cat = db.Column(db.Integer, primary_key=True)
    id_type = db.Column(db.Integer, db.ForeignKey(
        TypeSiteModel.id_typesite), nullable=False)
    name = db.Column(db.Unicode)
    desc = db.Column(db.Unicode)
    order = db.Column(db.Integer)
    type = db.relationship("TypeSiteModel", lazy='select')


@serializable
class BibAttributsModel(db.Model):
    """Table descriptive des attributs pour une création automatique des formulaires"""
    __tablename__ = 'bib_attributs'
    __table_args__ = {'schema': 'gnc_sites'}
    id_attribut = db.Column(db.Integer, primary_key=True)
    nom_attribut = db.Column(db.Unicode)
    label_attribut = db.Column(db.Unicode)
    liste_valeur_attribut = db.Column(db.Text)
    obligatoire = db.Column(db.BOOLEAN)
    desc_attribut = db.Column(db.Text)
    type_attribut = db.Column(db.Unicode)
    type_widget = db.Column(db.Unicode)
    regne = db.Column(db.Unicode)
    group2_inpn = db.Column(db.Unicode)
    id_attr_cat = db.Column(
        db.Integer,
        db.ForeignKey(BibAttributeCategoryModel.id_attr_cat),
        nullable=False,
        primary_key=False
    )
    ordre = db.Column(db.Integer)
    attr_cat = db.relationship("BibAttributeCategoryModel", lazy='select')


@serializable
class CorAttributeVisite(TimestampMixinModel, db.Model):
    """Table des attributs descriptifs des visites de sites"""
    __tablename__ = 'cor_attr_visit'
    __table_args__ = {'schema': 'gnc_sites'}
    id_attr_visit = db.Column(db.Integer, primary_key=True)
    attr_value = db.Column(db.Text, nullable=False)
    id_visit = db.Column(db.Integer, db.ForeignKey(
        VisitModel.id_visit), nullable=False)
    visit = db.relationship("VisitModel", lazy='select')
