#!/usr/bin/python3
# -*- coding: utf-8 -*-

from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import UUID

from gncitizen.core.commons.models import (
    ProgramsModel, TimestampMixinModel, MediaModel)
from gncitizen.core.users.models import ObserverMixinModel
from gncitizen.utils.utilssqlalchemy import serializable, geoserializable
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


class VisitAttributeModel(TimestampMixinModel, db.Model):
    """Table des sessions de suivis des sites"""
    __tablename__ = 't_visit_attributes'
    __table_args__ = {'schema': 'gnc_sites'}
    id_attribute = db.Column(db.Integer, primary_key=True, unique=True)
    id_visit = db.Column(db.Integer, db.ForeignKey(
        VisitModel.id_visit, ondelete='CASCADE'))
    key = db.Column(db.String(200), nullable=False)
    value = db.Column(db.Text)
