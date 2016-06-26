# coding: utf-8
from __future__ import absolute_import
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, abort
from .documents import TaskDocument
from ong.documents import OngDocument

task_blueprint = Blueprint('task', __name__)
api = Api(task_blueprint)


@api.resource('/task/', '/task/<string:id>')
class TaskResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, type=str)
        parser.add_argument('description', required=True, type=str)
        parser.add_argument('status', type=str)
        parser.add_argument('tags', type=list, location='json')
        parser.add_argument('is_remote', type=bool)
        parser.add_argument('ong_id', required=True, type=str)
        args = parser.parse_args(strict=True)

        title = args.get('title')
        description = args.get("description")
        status = args.get("status")
        tags = args.get("tags")
        is_remote = args.get("is_remote")
        ong_id = args.get('ong_id')

        task = TaskDocument(
            title=title,
            description=description,
            status=status,
            tags=tags,
            ong_id=ong_id,
            is_remote=is_remote).save()

        ong = OngDocument.objects.get_or_404(id=ong_id)
        ong.tasks.append(task)
        ong.save()

        return task.to_dict(), 201

    def delete(self, id=None):
        if id is None:
            abort(400, message="You must provide an id")
        TaskDocument.objects.get_or_404(id=id).delete()
        return None, 204

    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int)
        parser.add_argument('title', type=str)
        parser.add_argument('tag', type=str)
        parser.add_argument('location', type=str)
        args = parser.parse_args(strict=True)
        limit = args.get("limit", None)
        title = args.get("title", None)
        tag = args.get('tag', None)
        location = args.get('location', None)

        if not any([id, limit, tag, location, title]):
            abort(400, message="You must provide an id, limit, location, title or tag")

        elif limit is not None:
            tasks = TaskDocument.objects[:limit]
            return [task.to_dict() for task in tasks], 200

        elif tag is not None:
            tasks = TaskDocument.objects(tags__in=[tag])
            return [task.to_dict() for task in tasks], 200

        elif location is not None:
            ongs = OngDocument.objects(address__localidade__in=[location]).all()

            tasks = []
            for ong in ongs:
                tasks.extend(ong.tasks)

            return [task.to_dict() for task in tasks], 200

        elif title is not None:
            tasks = TaskDocument.objects(title__icontains=title)
            return [task.to_dict() for task in tasks], 200

        task = TaskDocument.objects.get_or_404(id=id)
        return task.to_dict(), 200

    def put(self, id=None):
        if id is None:
            abort(400, message="You must provide an id")

        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str)
        parser.add_argument("description", type=str)
        parser.add_argument("status", type=str)
        parser.add_argument("tags", type=list, location='json')
        parser.add_argument("is_remote", type=bool)
        args = parser.parse_args()
        title = args.get("title", None)
        description = args.get("description", None)
        status = args.get("status", None)
        tags = args.get("tags", None)
        is_remote = args.get("is_remote", None)

        task = TaskDocument.objects.get_or_404(id=id)

        if title and title is not None:
            task.title = title
        if description and description is not None:
            task.description = description
        if status and status is not None:
            task.status = status
        if tags is not None:
            task.tags = tags
        if is_remote is not None:
            task.is_remote = is_remote

        task.save()
        return task.to_dict(), 200
