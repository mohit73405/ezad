from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_classified = Namespace('Classified', description='Classified')

brand_classified_form = ns_classified.model('Classified', {
    'classified_name' : fields.String(required=True, description='Classified Name'),
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
    'target_url': fields.Url(required=True, description='Target URL'),
    'classified_description': fields.String(required=True, description='Classified description'),
    'arrangements': fields.String(required=True, description='Arrangements'),
    'kpis': fields.String(required=True, description='KPIs'),
    'convert_to_campaign': fields.String(required=False, description='Convert to Campaign',default='false')

})

@ns_classified.route('/<string:user_id>')
class Classified(Resource):
    @ns_classified.expect(brand_classified_form)
    def post(self,user_id):
        ''' Add New Classified'''
        data_json = request.get_json()
        classified_name = data_json.get('classified_name')
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
        classified_description = data_json.get('classified_description')
        arrangements = data_json.get('arrangements')
        kpis = data_json.get('kpis')
        convert_to_campaign = data_json.get('convert_to_campaign')
        data = [classified_name, from_date, to_date, budget, currency, channels,
                regions, min_lower, max_upper, video_cat, target_url, classified_description, arrangements,
                kpis, user_id,convert_to_campaign]
        columns = ['classified_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                   'min_lower_followers', 'max_upper_followers', 'video_cat_id', 'target_url', 'classified_description',
                   'arrangements', 'kpis', 'user_id','convert_to_campaign']
        connecsiObj = ConnecsiModel()
        res=connecsiObj.insert__(table_name='brands_classifieds', columns=columns, data=data)
        return {'response':res}

    def get(self,user_id):
        ''' get all Classifieds by user id'''
        try:
            connecsiObj = ConnecsiModel()
            all_classifieds_data = connecsiObj.get__(table_name='brands_classifieds', STAR='*', WHERE='WHERE', compare_column='user_id',compare_value=str(user_id))
            columns = ['classified_id','user_id','classified_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                       'min_lower_followers', 'max_upper_followers','files', 'video_cat_id', 'target_url',
                       'classified_description',
                       'arrangements', 'kpis', 'convert_to_campaign']
            response_list = []
            for item in all_classifieds_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)


@ns_classified.route('/<string:clasified_id>/<string:user_id>')
class Classified(Resource):
    def get(self,clasified_id,user_id):
        ''' get Classified details by classified id'''
        try:
            connecsiObj = ConnecsiModel()
            classified_data = connecsiObj.get_brand_classified_details_by_classified_id_and_user_id(classified_id=clasified_id,user_id=user_id)
            columns = ['classified_id','user_id','classified_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                       'min_lower_followers', 'max_upper_followers','files', 'video_cat_id', 'target_url',
                       'classified_description',
                       'arrangements', 'kpis','convert_to_campaign']
            response_list = []
            for item in classified_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)
