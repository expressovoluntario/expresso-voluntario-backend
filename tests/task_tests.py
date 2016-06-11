import json
import unittest
import mongoengine
from app import app
from task.documents import TaskDocument


class TaskTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.client = app.test_client()
        self.task = TaskDocument(title='A title', description='A description', tags=['tag']).save()
        TaskDocument(title='Another title', description='Another description', tags=['tag']).save()
        TaskDocument(title='yet Another title', description='yet Another description').save()

    def tearDown(self):
        TaskDocument.drop_collection()

    def test_search_by_tag(self):

        response = self.client.get('/task/?tag={tag}'.format(tag='tag'))
        content = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertDictContainsSubset(
                                      {
                                          'description': 'A description',
                                          'tags': ['tag'],
                                          'title': 'A title'
                                      }, content[0])
        self.assertDictContainsSubset({
                                          'description': 'Another description',
                                          'tags': ['tag'],
                                          'title': 'Another title'
                                      }, content[1])

    def test_add_task(self):
        data = {'title': 'A cool task', 'description': 'Hasta la vista baby!'}
        response = self.client.post('/task/', data=data)
        task = TaskDocument.objects.get(**data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(task.title, data['title'])
        self.assertEqual(task.description, data['description'])

    def test_add_task_without_params(self):
        response = self.client.post('/task/')
        decoded_response_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(decoded_response_data,
                             {'message': {'title': 'Missing required parameter in the JSON body or the '
                                                   'post body or the query string'}})

    def test_delete_task(self):
        id_ = self.task.id
        response = self.client.delete("/task/{id}".format(id=id_))

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(mongoengine.DoesNotExist):
            TaskDocument.objects.get(id=id_)

    def test_delete_inexistent_task(self):
        id_ = '43422423432'  # task that does not exist
        response = self.client.delete("/task/{id}".format(id=id_))

        self.assertEqual(response.status_code, 404)

    def test_delete_task_without_id(self):
        response = self.client.delete('/task/')
        decoded_response_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(decoded_response_data, {"message": "You must provide an id"})

    def test_get_task_by_id(self):
        response = self.client.get("/task/{id}".format(id=self.task.id))
        decoded_response_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(decoded_response_data, self.task.to_dict())

    def test_get_inexistent_task(self):
        response = self.client.get("/task/{id}".format(id='123456'))

        self.assertEqual(response.status_code, 404)

    def test_get_task_without_pass_id(self):
        response = self.client.get("/task/")

        self.assertEqual(response.status_code, 400)

    def test_list_tasks(self):
        another_task = TaskDocument(title="Another task", description="Another Description").save()
        response = self.client.get("/task/?limit=2")
        response_data_decoded = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data_decoded, [
            self.task.to_dict(), another_task.to_dict()
        ])

    def test_put_task(self):
        data = {"title": "New title", "description": "New Description"}
        id_ = self.task.id
        response = self.client.put('/task/{id}'.format(id=id_), data=data)
        updated_task = TaskDocument.objects.get(id=id_)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_task.title, data['title'])
        self.assertEqual(updated_task.description, data['description'])

    def test_put_nonexistent_task(self):
        id_ = '12345'
        response = self.client.put("/task/{id}".format(id=id_))

        self.assertEqual(response.status_code, 404)

    def test_put_task_without_pass_id(self):
        response = self.client.put("/task/")
        decoded_response_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(decoded_response_data, {"message": "You must provide an id"})


if __name__ == '__main__':
    unittest.main()