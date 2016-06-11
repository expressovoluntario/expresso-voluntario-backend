# coding: utf-8
from __future__ import absolute_import

from flask import Blueprint
from flask_restful import Api, Resource, reqparse, abort
from .documents import OngDocument

ong_blueprint = Blueprint('ong', __name__)
api = Api(ong_blueprint)


@api.resource('/ong/', '/ong/<string:id>')
class OngResource(Resource):

    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int)
        args = parser.parse_args(strict=True)
        limit = args.get('limit')
        if limit is not None:
            ongs = OngDocument.objects[:limit]
            return [ong.to_dict() for ong in ongs]
        elif id is not None:
            ong = OngDocument.objects.get_or_404(id=id)
            return ong.to_dict()

        abort(400, message="You must provide limit or id")

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='You must provide name')
        args = parser.parse_args(strict=True)
        name = args.get('name')
        if name is None:
            abort(400, message="You must provide name")

        ong = OngDocument(name=name).save()
        return ong.to_dict(), 201

    def delete(self, id=None):
        if id is not None:
            ong_document = OngDocument.objects.get_or_404(id=id)
            ong_document.delete()
            return None, 204
        abort(400, message="You must provide an id")

    def put(self, id=None):
        if id is None:
            abort(400, message="You must provide an id")

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('purpose', type=str)
        parser.add_argument('phone1', type=str)
        parser.add_argument('phone2', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('site', type=str)
        parser.add_argument('address', type=dict)
        parser.add_argument('addressNumber', type=str)
        parser.add_argument('logoUrl', type=str)
        args = parser.parse_args()

        name = args.get("name", None)
        description = args.get("description", None)
        purpose = args.get("purpose", None)
        phone1 = args.get("phone1", None)
        phone2 = args.get("phone2", None)
        email = args.get("email", None)
        site = args.get("site", None)
        address = args.get("address", None)
        addressNumber = args.get("addressNumber", None)
        logoUrl = args.get("logoUrl", None)

        ong_document = OngDocument.objects.get_or_404(id=id)

        if name is not None:
            ong_document.name = name

        if description is not None:
            ong_document.description = description

        if purpose is not None:
            ong_document.purpose = purpose

        if phone1 is not None:
            ong_document.phone1 = phone1

        if phone2 is not None:
            ong_document.phone2 = phone2

        if email is not None:
            ong_document.email = email

        if site is not None:
            ong_document.site = site

        if address is not None:
            ong_document.address = address

        if addressNumber is not None:
            ong_document.addressNumber = addressNumber

        if logoUrl is not None:
            ong_document.logoUrl = logoUrl

        ong_document.save()
        return ong_document.to_dict(), 201
