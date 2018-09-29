from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_campaign = Namespace('Campaign', description='Brand Campaign')

brand_campaign_form = ns_campaign.model('Brand Campaign', {
    'campaign_name' : fields.String(required=True, description='Campaign Name'),
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
    'campaign_description': fields.String(required=True, description='Campaign description'),
    'arrangements': fields.String(required=True, description='Arrangements'),
    'kpis': fields.String(required=True, description='KPIs'),
    'is_classified_post': fields.String(required=False, description='Classified Post',default='false')

})

@ns_campaign.route('/<string:user_id>')
class Campaign(Resource):
    @ns_campaign.expect(brand_campaign_form)
    def post(self,user_id):
        ''' Add New Campaign'''
        data_json = request.get_json()
        campaign_name = data_json.get('campaign_name')
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
        campaign_description = data_json.get('campaign_description')
        arrangements = data_json.get('arrangements')
        kpis = data_json.get('kpis')
        is_classified_post = data_json.get('is_classified_post')
        data = [campaign_name, from_date, to_date, budget, currency, channels,
                regions, min_lower, max_upper, video_cat, target_url, campaign_description, arrangements,
                kpis, user_id,is_classified_post]
        columns = ['campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                   'min_lower_followers', 'max_upper_followers', 'video_cat_id', 'target_url', 'campaign_description',
                   'arrangements', 'kpis', 'user_id','is_classified_post']
        connecsiObj = ConnecsiModel()
        res=connecsiObj.insert__(table_name='brands_campaigns', columns=columns, data=data)

        return {'response':res}

