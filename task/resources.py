# coding: utf-8
from __future__ import absolute_import

from flask import Blueprint
from flask_restful import Api, Resource, reqparse, abort
from .documents import TaskDocument

task_blueprint = Blueprint('task', __name__)
api = Api(task_blueprint)


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

api.add_resource(
    TaskResource,
    '/task/',
    '/task/<string:id>')
