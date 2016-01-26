# coding: utf-8
from __future__ import absolute_import

from flask import Blueprint
from flask_restful import Api, Resource, reqparse, abort
from .documents import TaskDocument

task_blueprint = Blueprint('task', __name__)
api = Api(task_blueprint)


@api.resource('/task/', '/task/<string:id_>')
class TaskResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, type=str)
        parser.add_argument('description', required=True, type=str)
        args = parser.parse_args(strict=True)

        title = args.get('title')
        description = args.get("description")

        task = TaskDocument(title=title, description=description).save()

        return task.to_dict(), 201

    def delete(self, id_=None):
        if id_ is None:
            abort(400, message="You must provide an id")
        TaskDocument.objects.get_or_404(id=id_).delete()
        return None, 204

    def get(self, id_=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int)
        limit = parser.parse_args(strict=True).get("limit", None)

        if id_ is None and limit is None:
            abort(400, message="You must provide an id or limit")

        elif limit is not None:
            tasks = TaskDocument.objects[:limit]
            return [task.to_dict() for task in tasks], 200

        task = TaskDocument.objects.get_or_404(id=id_)
        return task.to_dict(), 200

    def put(self, id_=None):
        if id_ is None:
            abort(400, message="You must provide an id")

        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str)
        parser.add_argument("description", type=str)
        args = parser.parse_args(strict=True)
        title = args.get("title", None)
        description = args.get("description", None)

        task = TaskDocument.objects.get_or_404(id=id_)
        task.title = title
        task.description = description
        task.save()
        return 200
