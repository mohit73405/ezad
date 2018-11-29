from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_offer = Namespace('Offer', description='Offer')

inf_offer_form = ns_offer.model('Offer', {
    'offer_name' : fields.String(required=True, description='Offer Name'),
    'from_date' : fields.String(required=True, description='From Date'),
    'to_date' : fields.String(required=True, description='To Date'),
    'budget' : fields.Integer(required=True, description='Budget'),
    'currency' : fields.String(required=True, description='Currency'),
    # 'channels' : fields.List(required=True, description='Channels',cls_or_instance=fields.String),
    'channels' : fields.String(required=True, description='Channels'),
    'regions' : fields.String(required=True, description='Regions'),
    'min_lower': fields.Integer(required=True, description='Min Followers'),
    'max_upper': fields.Integer(required=True, description='Max Followers'),
    'files': fields.String(required=False, description='Files'),
    'video_cat': fields.String(required=True, description='Video Category'),
    'offer_description': fields.String(required=True, description='Classified description'),
    'arrangements': fields.String(required=True, description='Arrangements'),
    'kpis': fields.String(required=True, description='KPIs'),
})

@ns_offer.route('/<string:user_id>')
class Offers(Resource):
    @ns_offer.expect(inf_offer_form)
    def post(self,user_id):
        ''' Add New offer'''
        data_json = request.get_json()
        offer_name = data_json.get('offer_name')
        from_date = data_json.get('from_date')
        to_date = data_json.get('to_date')
        budget = data_json.get('budget')
        currency = data_json.get('currency')
        channels = data_json.get('channels')
        regions = data_json.get('regions')
        min_lower = data_json.get('min_lower')
        max_upper = data_json.get('max_upper')
        files = data_json.get('files')
        video_cat = data_json.get('video_cat')
        offer_description = data_json.get('offer_description')
        arrangements = data_json.get('arrangements')
        kpis = data_json.get('kpis')

        data = [offer_name, from_date, to_date, budget, currency, channels,
                regions, min_lower, max_upper, video_cat, offer_description, arrangements,
                kpis, user_id,files]
        columns = ['offer_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                   'min_lower_followers', 'max_upper_followers', 'video_cat_id', 'offer_description',
                   'arrangements', 'kpis', 'channel_id','files']
        connecsiObj = ConnecsiModel()
        try:
            connecsiObj.insert__(table_name='inf_offers', columns=columns, data=data)
            res = 1
            return {'response':res}
        except Exception as e:
            print(e)
            res = 0
            return {'response':res}

    def get(self,user_id):
        ''' get all Offers by user id'''
        try:
            connecsiObj = ConnecsiModel()
            all_classifieds_data = connecsiObj.get__(table_name='inf_offers', STAR='*', WHERE='WHERE', compare_column='user_id',compare_value=str(user_id))
            columns = ['offer_id','user_id','offer_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                       'min_lower_followers', 'max_upper_followers','files', 'video_cat_id', 'target_url',
                       'offer_description',
                       'arrangements', 'kpis','no_of_views','no_of_replies']
            response_list = []
            for item in all_classifieds_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)


@ns_offer.route('/<string:offer_id>/<string:user_id>')
class Offers(Resource):
    def get(self,offer_id,user_id):
        ''' get Offer details by offer id'''
        try:
            connecsiObj = ConnecsiModel()
            offer_data = connecsiObj.get_inf_offer_details_by_offer_id_and_user_id(offer_id=offer_id,user_id=user_id)
            columns = ['offer_id', 'user_id', 'offer_name', 'from_date', 'to_date', 'budget', 'currency', 'channels',
                       'regions',
                       'min_lower_followers', 'max_upper_followers', 'files', 'video_cat_id', 'target_url',
                       'offer_description',
                       'arrangements', 'kpis', 'no_of_views', 'no_of_replies']
            response_list = []
            for item in offer_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)

    @ns_offer.expect(inf_offer_form)
    def put(self, offer_id,user_id):
        ''' Edit offer'''
        data_json = request.get_json()
        offer_name = data_json.get('offer_name')
        from_date = data_json.get('from_date')
        to_date = data_json.get('to_date')
        budget = data_json.get('budget')
        currency = data_json.get('currency')
        channels = data_json.get('channels')
        regions = data_json.get('regions')
        min_lower = data_json.get('min_lower')
        max_upper = data_json.get('max_upper')
        files = data_json.get('files')
        video_cat = data_json.get('video_cat')
        target_url = data_json.get('target_url')
        offer_description = data_json.get('offer_description')
        arrangements = data_json.get('arrangements')
        kpis = data_json.get('kpis')

        data = [offer_name, from_date, to_date, budget, currency, channels,
                regions, min_lower, max_upper, video_cat, target_url, offer_description, arrangements,
                kpis, user_id, files]
        columns = ['classified_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                   'min_lower_followers', 'max_upper_followers', 'video_cat_id', 'target_url', 'classified_description',
                   'arrangements', 'kpis', 'user_id', 'convert_to_campaign', 'files']
        connecsiObj = ConnecsiModel()
        try:
            connecsiObj.update__(table_name='inf_offers', columns=columns, data=data, WHERE='WHERE',
                                 compare_column='offer_id', compare_value=offer_id)
            res = 1
            return {'response': res}
        except Exception as e:
            print(e)
            res = 0
            return {'response': res}


@ns_offer.route('/NumberOfViews/<string:classified_id>/<string:user_id>/<string:no_of_views>')
class Offers(Resource):
    def put(self,offer_id,user_id,no_of_views):
        try:
            connecsiObj=ConnecsiModel()
            connecsiObj.update_offer_no_of_views(offer_id=offer_id,user_id=user_id,no_of_views=no_of_views)
            res = 1
            return {'response': res},201
        except Exception as e:
            print(e)
            res = 0
            return {'response': res},500


@ns_offer.route('/NumberOfReplies/<string:offer_id>/<string:user_id>/<string:no_of_replies>')
class Offers(Resource):
    def put(self,offer_id,user_id,no_of_replies):
        try:
            connecsiObj=ConnecsiModel()
            connecsiObj.update_offer_no_of_replies(offer_id=offer_id,user_id=user_id,no_of_replies=no_of_replies)
            res = 1
            return {'response': res},201
        except Exception as e:
            print(e)
            res = 0
            return {'response': res},500
