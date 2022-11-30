from flask import Flask, request, send_from_directory
from flask_restful import Resource, Api
from db import Tasker

app = Flask(__name__)
api = Api(app)


class Task(Resource):

    def get(self, task_id):
        return Tasker().get_one(task_id), 200

    def delete(self, task_id):
        Tasker().delete(task_id)
        return {'status': 'ok'}, 202

    def put(self, task_id):
        payload = request.get_json()

        if 'title' in payload and 'description' in payload:
            Tasker().edit(task_id, payload.get('title'), payload.get('description'))
        else:
            # this is a move request
            to_status = payload.get('status')
            after_id = payload.get('after')
            Tasker().move(task_id, to_status, after_id)
        return {'status': 'ok'}, 202


class TaskList(Resource):

    def get(self):
        return Tasker().get(), 200

    def post(self):
        payload = request.get_json()
        return Tasker().create(payload.get('title'), payload.get('description')), 202


api.add_resource(TaskList, '/api/tasks')
api.add_resource(Task, '/api/tasks/<task_id>')


@app.route('/<path:path>')
def send_report(path):
    return send_from_directory('taskBoard', path)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
