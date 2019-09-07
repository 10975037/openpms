from flask_restplus import Resource
from app.api import ns
from app.marshalling import gma
from app.utils import authenticate


@ns.route('/test/', endpoint='test', methods=['GET'])
class Test(Resource):
    method_decorators = [authenticate]
    def get(self):
        res = {
            'code': 20000
        }
        return gma.dump(res)