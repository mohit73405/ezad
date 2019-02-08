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


brand_campaign_report_form = ns_campaign.model('Brand Campaign report form', {
    'revenue_generated' : fields.Integer(required=True, description='Revenue generated'),
    'currency' : fields.String(required=True, description='Currency'),
    'target_url' : fields.String(required=True, description='Target URL'),
    'new_users' : fields.Integer(required=True, description='New Users')
})


inf_campaign_report_form = ns_campaign.model('Influencer Campaign report form', {
    'channel_name' : fields.String(required=True, description='Channel Name'),
    'date_posted' : fields.String(required=True, description='Date Posted'),
    'link_posted' : fields.String(required=True, description='Link Posted'),
    'content_type' : fields.String(required=True, description='Content Type'),
    'post_views' : fields.Integer(required=False, description='Views'),
    'post_clicks' : fields.Integer(required=False, description='Clicks'),
    'post_likes' : fields.Integer(required=False, description='Likes'),
    'post_dislikes' : fields.Integer(required=False, description='Dislikes'),
    'post_comments' : fields.Integer(required=False, description='Comments'),
    'post_retweets' : fields.Integer(required=False, description='Retweets'),
    'post_remarks' : fields.String(required=False, description='Remarks'),
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
        campaign_status = 'New'
        data = [campaign_name, from_date, to_date, budget, currency, channels,
                regions, min_lower, max_upper, video_cat, target_url, campaign_description, arrangements,
                kpis, user_id,is_classified_post,files,campaign_status]
        columns = ['campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                   'min_lower_followers', 'max_upper_followers', 'video_cat_id', 'target_url', 'campaign_description',
                   'arrangements', 'kpis', 'user_id','is_classified_post','files','campaign_status']
        connecsiObj = ConnecsiModel()
        res=''
        try:
            res=connecsiObj.insert__(table_name='brands_campaigns', columns=columns, data=data)
            return {'response' : res}
        except Exception as e:
            print(e)
            return {'response':res}

    def get(self,user_id):
        ''' get all campaings by user id'''
        try:
            connecsiObj = ConnecsiModel()
            all_campaigns_data = connecsiObj.get__(table_name='brands_campaigns', STAR='*', WHERE='WHERE', compare_column='user_id',compare_value=str(user_id))
            columns = ['campaign_id','user_id','campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                       'min_lower_followers', 'max_upper_followers','files', 'video_cat_id', 'target_url',
                       'campaign_description',
                       'arrangements', 'kpis', 'is_classified_post','deleted','campaign_status']
            response_list = []
            for item in all_campaigns_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)







@ns_campaign.route('/<string:campaign_id>/<string:user_id>')
class Campaign(Resource):
    def get(self,campaign_id,user_id):
        ''' get Campaign details by campaign id'''
        try:
            connecsiObj = ConnecsiModel()
            campaign_data = connecsiObj.get_campaign_details_by_campaign_id_and_user_id(campaign_id=campaign_id,user_id=user_id)
            columns = ['campaign_id','user_id','campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                       'min_lower_followers', 'max_upper_followers','files', 'video_cat_id', 'target_url',
                       'campaign_description',
                       'arrangements', 'kpis', 'is_classified_post','deleted','campaign_status']
            response_list = []
            for item in campaign_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)

    @ns_campaign.expect(brand_campaign_form)
    def put(self,campaign_id, user_id):
        ''' Edit Campaign'''
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
                kpis, user_id, is_classified_post, files]
        columns = ['campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                   'min_lower_followers', 'max_upper_followers', 'video_cat_id', 'target_url', 'campaign_description',
                   'arrangements', 'kpis', 'user_id', 'is_classified_post', 'files']
        connecsiObj = ConnecsiModel()
        res=''
        try:
            connecsiObj.update__(table_name='brands_campaigns', columns=columns, data=data,WHERE='WHERE',compare_column='campaign_id',compare_value=campaign_id)
            res = 1
            return {'response': res},201
        except Exception as e:
            print(e)
            res = 0
            return {'response': res},500

    def delete(self,campaign_id,user_id):
        '''Delete Campaign'''
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.delete_campaign(campaign_id=campaign_id,user_id=user_id)
            res = 1
            return {'response': res}, 201
        except Exception as e:
            print(e)
            res = 0
            return {'response': res}, 500


@ns_campaign.route('/channel_status_for_campaign/<string:channel_id>')
class Campaign(Resource):
    def get(self,channel_id):
        ''' get Channel details and status for campaigns by channel id'''
        try:
            connecsiObj = ConnecsiModel()
            channel_campaign_message_status_data=connecsiObj.get_channel_campaign_message_status(channel_id=channel_id)
            columns = ['campaign_id', 'campaign_name','message_id','status']
            response_list = []
            for item in channel_campaign_message_status_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)


@ns_campaign.route('/channel_status_for_campaign_by_campaign_id/<string:campaign_id>')
class Campaign(Resource):
    def get(self,campaign_id):
        ''' get Channel details and status for campaigns by campaign id'''
        try:
            connecsiObj = ConnecsiModel()
            channel_campaign_message_status_data=connecsiObj.get_channel_campaign_message_status_by_campaign_id(campaign_id=campaign_id)
            columns = ['campaign_id','campaign_name','message_id','status','channel_id','user_id']
            response_list = []
            for item in channel_campaign_message_status_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)


@ns_campaign.route('/update_channel_status_for_campaign/<string:message_id>/<string:campaign_id>/<string:status>')
class Campaign(Resource):
    def put(self,message_id,campaign_id,status):
        ''' update Channel status campaigns by message id and campaign id'''
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.update_channel_campaign_message_status_by_message_id_campaign_id(message_id=message_id,campaign_id=campaign_id,status=status)

            return {'response': 1},201

        except Exception as e:
            print(e)


@ns_campaign.route('/update_campaign_status/<string:campaign_id>/<string:campaign_status>')
class Campaign(Resource):
    def put(self,campaign_id,campaign_status):
        ''' update campaign status by campaign id'''
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.update_campaign_status(campaign_id=campaign_id,campaign_status=campaign_status)

            return {'response': 1},201

        except Exception as e:
            print(e)

@ns_campaign.route('/BrandCampaignReport/<string:user_id>/<string:campaign_id>')
class Campaign(Resource):
    @ns_campaign.expect(brand_campaign_report_form)
    def post(self,user_id,campaign_id):
        ''' Add New Brand Campaign report'''
        data_json = request.get_json()
        revenue_generated = data_json.get('revenue_generated')
        currency = data_json.get('currency')

        new_users = data_json.get('new_users')
        channel_id = data_json.get('channel_id')
        channel = data_json.get('channel')
        data = [user_id, campaign_id, revenue_generated, currency,new_users,channel_id,channel]

        columns = ['user_id', 'campaign_id', 'revenue_generated', 'currency', 'new_users','channel_id','channel']
        connecsiObj = ConnecsiModel()

        try:
            connecsiObj.insert__(table_name='brand_campaign_report', columns=columns, data=data)
            res=1
            return {'response': res},200
        except Exception as e:
            res=0
            print(e)
            return {'response': res},500

    def get(self, user_id,campaign_id):
        ''' get Brand Campaign Report details  by user id and campaign id'''
        try:
            connecsiObj = ConnecsiModel()
            brand_campaign_report_data = connecsiObj.get_brand_campaign_report(user_id=user_id,campaign_id=campaign_id)
            columns = ['brand_campaign_report_id', 'user_id', 'campaign_id', 'revenue_generated','currency','new_users','channel_id','channel']
            response_list = []
            for item in brand_campaign_report_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)


@ns_campaign.route('/BrandCampaignReport/<string:user_id>/<string:campaign_id>/<string:channel_id>')
class Campaign(Resource):
    def get(self, user_id,campaign_id,channel_id):
        ''' get Brand Campaign Report details  by user id and campaign id and channel_id'''
        try:
            connecsiObj = ConnecsiModel()
            brand_campaign_report_data = connecsiObj.get_brand_campaign_report_by_channel_id(user_id=user_id,campaign_id=campaign_id,channel_id=channel_id)
            columns = ['brand_campaign_report_id', 'user_id', 'campaign_id', 'revenue_generated','currency','new_users','channel_id','channel']
            response_list = []
            for item in brand_campaign_report_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)


@ns_campaign.route('/BrandCampaignReport/Update/<string:campaign_id>/<string:channel_id>')
class Campaign(Resource):
    def put(self,campaign_id,channel_id):
        ''' Edit Brand Campaign report by campaign_id and channel_id'''
        data_json = request.get_json()
        revenue_generated = data_json.get('revenue_generated')
        currency = data_json.get('currency')
        new_users = data_json.get('new_users')
        data = [revenue_generated, currency,new_users]
        connecsiObj = ConnecsiModel()
        try:
            connecsiObj.update_brand_campaign_report(campaign_id=campaign_id,channel_id=channel_id,data=data)
            res=1
            return {'response': res},200
        except Exception as e:
            res=0
            print(e)
            return {'response': res},500



@ns_campaign.route('/BrandCampaignReport/Delete/<string:campaign_id>/<string:channel_id>')
class Campaign(Resource):
    def delete(self,campaign_id,channel_id):
        ''' Delete Brand Campaign report by campaign_id and channel_id'''
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.delete_brand_campaign_report(campaign_id=campaign_id,channel_id=channel_id)
            res = 1
            return {'response': res}, 200
        except Exception as  e:
            res = 0
            print(e)
            return {'response': res}, 500




@ns_campaign.route('/InfluencerCampaignReport/<string:campaign_id>/<string:proposal_id>/<string:user_id>')
class Campaign(Resource):
    @ns_campaign.expect(inf_campaign_report_form)
    def post(self,campaign_id,proposal_id,user_id):
        ''' Add New Influencer Campaign report'''
        data_json = request.get_json()
        channel_name = data_json.get('channel_name')
        date_posted = data_json.get('date_posted')
        link_posted = data_json.get('link_posted')
        content_type = data_json.get('content_type')
        post_views = data_json.get('post_views')
        post_clicks = data_json.get('post_clicks')
        post_likes = data_json.get('post_likes')
        post_dislikes = data_json.get('post_dislikes')
        post_comments = data_json.get('post_comments')
        post_retweets = data_json.get('post_retweets')
        post_remarks = data_json.get('post_remarks')
        post_shares = data_json.get('post_shares')

        data = [campaign_id,proposal_id,user_id,channel_name, date_posted, link_posted,content_type,
                post_views,post_clicks,post_likes,post_dislikes,post_comments,post_retweets,post_remarks,post_shares]

        columns = ['campaign_id','proposal_id','channel_id','channel_name', 'date_posted', 'link_posted', 'content_type',
                   'post_views','post_clicks','post_likes','post_dislikes','post_comments','post_retweets','post_remarks','post_shares']
        connecsiObj = ConnecsiModel()

        try:
            connecsiObj.insert__(table_name='inf_campaign_report', columns=columns, data=data)
            res=1
            return {'response': res},200
        except Exception as e:
            res=0
            print(e)
            return {'response': res},500

    def get(self,campaign_id,proposal_id, user_id):
        ''' get All Influencer Campaign Report details  by campaign id ,proposal id and user id'''
        try:
            connecsiObj = ConnecsiModel()
            inf_campaign_report_data = connecsiObj.get_inf_campaign_report(campaign_id=campaign_id,proposal_id=proposal_id,channel_id=str(user_id))
            columns = ['inf_campaign_report_id','campaign_id', 'proposal_id', 'channel_id', 'channel_name',
                       'date_posted', 'link_posted','content_type',
                       'post_views', 'post_likes', 'post_dislikes', 'post_comments', 'post_retweets', 'post_remarks',
                       'post_clicks','post_shares']
            response_list = []
            for item in inf_campaign_report_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)




@ns_campaign.route('/getInfluencerCampaignReportByReportId/<string:inf_campaign_report_id>')
class Campaign(Resource):
    def get(self,inf_campaign_report_id):
        ''' get  Influencer Campaign Report details  by report id'''
        try:
            connecsiObj = ConnecsiModel()
            inf_campaign_report_data = connecsiObj.get__(table_name='inf_campaign_report',STAR='*',WHERE='WHERE',
                                                         compare_column='inf_campaign_report_id',compare_value=str(inf_campaign_report_id))
            columns = ['inf_campaign_report_id','campaign_id', 'proposal_id', 'channel_id', 'channel_name',
                       'date_posted', 'link_posted','content_type',
                       'post_views', 'post_likes', 'post_dislikes',
                       'post_comments', 'post_retweets', 'post_remarks',
                       'post_clicks','post_shares']
            response_list = []
            for item in inf_campaign_report_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)

    @ns_campaign.expect(inf_campaign_report_form)
    def put(self,inf_campaign_report_id):
        ''' Edit Influencer Campaign report'''
        data_json = request.get_json()
        # channel_name = data_json.get('channel_name')
        date_posted = data_json.get('date_posted')
        link_posted = data_json.get('link_posted')
        content_type = data_json.get('content_type')
        post_views = data_json.get('post_views')
        post_likes = data_json.get('post_likes')
        post_dislikes = data_json.get('post_dislikes')
        post_comments = data_json.get('post_comments')
        post_retweets = data_json.get('post_retweets')
        post_remarks = data_json.get('post_remarks')
        post_clicks = data_json.get('post_clicks')
        post_shares = data_json.get('post_shares')

        data = [ date_posted, link_posted, content_type,
                post_views, post_likes, post_dislikes, post_comments, post_retweets, post_remarks,post_clicks,post_shares]

        columns = [ 'date_posted', 'link_posted',
                   'content_type',
                   'post_views', 'post_likes', 'post_dislikes', 'post_comments', 'post_retweets', 'post_remarks',
                   'post_clicks','post_shares']
        connecsiObj = ConnecsiModel()

        try:
            connecsiObj.update__(table_name='inf_campaign_report',WHERE='WHERE', columns=columns, data=data,compare_column='inf_campaign_report_id'
                                 ,compare_value=str(inf_campaign_report_id))
            res = 1
            return {'response': res}, 200
        except Exception as e:
            res = 0
            print(e)
            return {'response': res}, 500

    def delete(self,inf_campaign_report_id):
        ''' Delete  Influencer Campaign Report details  by report id'''
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.delete_inf_campaign_report(inf_campaign_report_id=str(inf_campaign_report_id))
            return {'response': 'deleted'},200
        except Exception as e:
            print(e)
            return {'response':e},500



@ns_campaign.route('/postAsClassified/<string:campaign_id>/<string:user_id>/')
class Campaign(Resource):
    def put(self,campaign_id,user_id):
        try:
            connecsiObj=ConnecsiModel()
            connecsiObj.post_as_classified(campaign_id=campaign_id,user_id=user_id)
            res = 1
            return {'response': res},201
        except Exception as e:
            print(e)
            res = 0
            return {'response': res},500
