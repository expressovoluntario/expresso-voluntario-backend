# coding: utf-8
from __future__ import absolute_import

from flask import Blueprint
from flask_restful import Api, Resource, reqparse, abort
from .documents import OngDocument

ong_blueprint = Blueprint('ong', __name__)
api = Api(ong_blueprint)


class OngResource(Resource):

    def put(self, id=None):
        if id is None:
            abort(400, message="You must provide an id")
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
        args = parser.parse_args(strict=True)

        to_update = {key: value for key, value in args.items()if value is not None}
        ong_document = OngDocument.objects.get_or_404(id=id)

        if to_update:
            ong_document.update(**to_update)
            return ong_document.to_dict(), 201
        return ong_document.to_dict(), 201

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str)
        parser.add_argument('description', type=str)
        args = parser.parse_args(strict=True)

        name = args.get('name')
        description = args.get("description", None)

        ong = OngDocument(name=name, description=description).save()

        return ong.to_dict(), 201

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

    def delete(self, id=None):
        if id is not None:
            ong_document = OngDocument.objects.get_or_404(id=id)
            ong_document.delete()
            return None, 204
        abort(400, message="You must provide an id")

api.add_resource(
    OngResource,
    '/ong/',
    '/ong/<string:id>')
