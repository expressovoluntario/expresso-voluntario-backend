# coding: utf-8
from __future__ import absolute_import

from flask import Blueprint
from flask_restful import Api, Resource, reqparse, abort
from flask.ext.login import login_user
from mongoengine import DoesNotExist
from .documents import UserDocument
from ong.documents import OngDocument

user_blueprint = Blueprint('user', __name__)
api = Api(user_blueprint)


class UserLoginResource(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, type=str)
        parser.add_argument('password', required=True, type=str)
        args = parser.parse_args()
        email = args.get("email")
        password = args.get("password")

        try:
            user = UserDocument.objects.get(email=email)
            if user.check_password(password):
                login_user(user)
                return 200
            else:
                abort(401)
        except DoesNotExist:
            abort(401)


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

        user = UserDocument(name=name, email=email, _password=password, ong_id=ong_id).save()

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

api.add_resource(
    UserLoginResource,
    '/user/login/'
)
