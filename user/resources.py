# coding: utf-8
from __future__ import absolute_import

from flask import Blueprint
from flask_restful import Api, Resource, reqparse, abort
from .documents import UserDocument

user_blueprint = Blueprint('user', __name__)
api = Api(user_blueprint)


class UserResource(Resource):

    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int)
        args = parser.parse_args(strict=True)
        limit = args.get('limit')

        if limit is not None:
            users = UserDocument.objects[:limit]
            return [user.to_dict() for user in users]
        elif id is not None:
            user = UserDocument.objects.get_or_404(id=id)
            return user.to_dict()

        abort(400, message="You must provide limit or id")

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str)
        parser.add_argument('email', required=True, type=str)
        parser.add_argument('password', required=True, type=str)
        parser.add_argument('ong_id', required=True, type=str)
        args = parser.parse_args(strict=True)

        name = args.get('name')
        email = args.get('email')
        password = args.get('password')
        ong_id = args.get('ong_id')

        user = UserDocument(name=name, email=email, password=password, ong_id=ong_id).save()

        return user.to_dict(), 201

    def delete(self, id=None):
        if id is not None:
            user_document = UserDocument.objects.get_or_404(id=id)
            user_document.delete()
            return None, 204

        abort(400, message="You must provide an id")

    def put(self, id=None):
        if id is None:
            abort(400, message="You must provide an id")

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args(strict=True)

        name = args.get('name')
        email = args.get('email')

        to_update = {key: value for key, value in args.items()if value is not None}
        ong_document = OngDocument.objects.get_or_404(id=id)

        if to_update:
            ong_document.update(**to_update)
            return ong_document.to_dict(), 201

        return ong_document.to_dict(), 201

api.add_resource(
    UserResource,
    '/user/',
    '/user/<string:id>')
