# coding: utf-8
from __future__ import absolute_import

from flask import Blueprint
from flask_restful import Api, Resource, reqparse, abort
from .documents import TaskDocument
from ong.documents import OngDocument

task_blueprint = Blueprint('task', __name__)
api = Api(task_blueprint)


@api.resource('/task/', '/task/<string:id_>')
class TaskResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, type=str)
        parser.add_argument('description', required=True, type=str)
        parser.add_argument('status', type=str)
        parser.add_argument('ong_id', required=True, type=str)
        args = parser.parse_args(strict=True)

        title = args.get('title')
        description = args.get("description")
        status = args.get("status")
        ong_id = args.get('ong_id')

        task = TaskDocument(title=title, description=description, status=status).save()

        ong = OngDocument.objects.get_or_404(id=ong_id)
        ong.tasks.append(task)
        ong.save()

        return task.to_dict(), 201

    def delete(self, id_=None):
        if id_ is None:
            abort(400, message="You must provide an id")
        TaskDocument.objects.get_or_404(id=id_).delete()
        return None, 204

    def get(self, id_=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int)
        parser.add_argument('tag', type=str)
        args = parser.parse_args(strict=True)
        limit = args.get("limit", None)
        tag = args.get('tag', None)

        if not any([id_, limit, tag]):
            abort(400, message="You must provide an id, limit or tag")

        elif limit is not None:
            tasks = TaskDocument.objects[:limit]
            return [task.to_dict() for task in tasks], 200
        elif tag is not None:
            tasks = TaskDocument.objects(tags__in=[tag])
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
