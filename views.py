from run import app,db,api
from flask import jsonify
from flask_restplus import Resource

@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})


class WorkesFeedback(Resource):
    def get(self):
        result = db.engine.execute('select * from v_workers_feedback')
        return jsonify({'workers_feedback' : [dict(r) for r in result]})

# class UserModel(db):
#     view = Table('v_users', MetaData())
#     definition = 'SELECT * FROM t_users'
#     create_view = CreateView(view, definition, or_replace=True)
#     print(str(create_view.compile()).strip())