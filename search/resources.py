# coding: utf-8
from __future__ import absolute_import
import json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, abort
from ong.documents import OngDocument
from task.documents import TaskDocument

search_blueprint = Blueprint('search', __name__)
api = Api(search_blueprint)


@api.resource('/search/')
class SearchResource(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', type=str)
        parser.add_argument('location', type=str)
        parser.add_argument('title', type=str)
        parser.add_argument('tag', type=str)
        parser.add_argument('remote', type=bool)
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        data = args.get('data', None)
        location = args.get('location', None)
        title = args.get('title', None)
        tag = args.get('tag', None)
        remote = args.get('remote', None)
        name= args.get('name', None)

        if data is not None:
            # BUSCA TODAS AS CIDADES CADASTRADAS (ONG)

            if data == 'cities':
                cities = []
                ongs = OngDocument.objects[:]
                for ong in ongs:
                    cities.append(ong.address['localidade'])
                cities = set(cities)
                cities = sorted(cities)
                return json.dumps(cities, default="utf-8")

            # BUSCA TASKS DE ACORDO COM OS PARÂMETROS PASSADOS
            elif data == 'task':
                if all([location]):
                    ongs = OngDocument.objects(address__localidade__icontains=location).all()
                    tasks = []
                    for ong in ongs:
                        tasks.extend(ong.tasks)
                    return [task.to_dict() for task in tasks], 200

                elif all([tag]):
                    tasks = TaskDocument.objects(tags__icontains=tag)
                    for task in tasks:
                        ong = OngDocument.objects.get(id=task.ong_id)
                        task.location = ong.address['localidade']
                    return [task.to_dict_with_address() for task in tasks], 200

                elif all([title]):
                    tasks = TaskDocument.objects(title__icontains=title)
                    for task in tasks:
                        ong = OngDocument.objects.get(id=task.ong_id)
                        task.location = ong.address['localidade']
                    return [task.to_dict_with_address() for task in tasks], 200

                elif all([remote]):
                    tasks = TaskDocument.objects(is_remote__eq=remote)
                    return [task.to_dict_with_address]

            # BUSCA ONGS DE ACORDO COM OS PARÂMETROS PASSADOS
            elif data == 'ong':
                if all([name]):
                    ongs = OngDocument.objects(name__icontains=name)
                    return [ong.to_dict() for ong in ongs], 200

                elif all([location]):
                    ongs = OngDocument.objects(address__localidade__icontains=location)
                    return [ong.to_dict() for ong in ongs], 200

        abort(400, message="You must provide data attribute")
