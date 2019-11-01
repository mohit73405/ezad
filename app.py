from flask import Flask,Blueprint
from flask_cors import CORS
from flask_restplus import Api
from apis.payments  import ns_payments
from apis.brand import ns_brand
from apis.user import ns_user
from apis.youtube import ns_youtube
from apis.twitter_api import ns_twitter
from apis.insta_api import ns_insta
from apis.campaign import ns_campaign
from apis.classified import ns_classified
from apis.messages import ns_messages
from apis.influencer import ns_influencer
from apis.offers import ns_offer
from apis.graph_history import ns_graph_history
from apis.notifications import ns_notifications

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
blueprint = Blueprint('api',__name__,url_prefix='/Apis')
api = Api(blueprint,version='1.0', title='Connecsi Api',description='APIS',doc='/Documentation')
app.register_blueprint(blueprint)


# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api.namespaces.pop(0)

api.add_namespace(ns_user)
api.add_namespace(ns_brand)
api.add_namespace(ns_payments)
api.add_namespace(ns_youtube)
api.add_namespace(ns_twitter)
api.add_namespace(ns_insta)
api.add_namespace(ns_campaign)
api.add_namespace(ns_classified)
api.add_namespace(ns_messages)
api.add_namespace(ns_influencer)
api.add_namespace(ns_offer)
api.add_namespace(ns_graph_history)
api.add_namespace(ns_notifications)

if __name__ == '__main__':
    app.secret_key = 'connecsiSecretKey'
    app.run(host='0.0.0.0',debug=True,port=90,use_reloader=False)