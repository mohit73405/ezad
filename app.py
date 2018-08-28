from flask import Flask,Blueprint
from flask_cors import CORS
from flask_restplus import Api
from apis.payments  import ns_payments
from apis.brand import ns_brand
from apis.user import ns_user
from apis.youtube import ns_youtube
from apis.campaign import ns_campaign
from apis.messages import ns_messages

app = Flask(__name__)


blueprint = Blueprint('api',__name__,url_prefix='/api')
api = Api(blueprint,version='1.0', title='Connecsi Api',description='APIS',doc='/documentation')
app.register_blueprint(blueprint)

CORS(app)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api.namespaces.pop(0)

api.add_namespace(ns_user)
api.add_namespace(ns_brand)
api.add_namespace(ns_payments)
api.add_namespace(ns_youtube)
api.add_namespace(ns_campaign)
api.add_namespace(ns_messages)



if __name__ == '__main__':
    app.secret_key = 'connecsiSecretKey'
    app.run(debug=True,port=8080)