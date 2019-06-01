from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_brand = Namespace('Brand', description='Brand Operations')

brand_form = ns_brand.model('Brand Details', {
    'first_name' : fields.String(required=True, description='First Name'),
    'last_name' : fields.String(required=True, description='Last Name'),
    'company_name' : fields.String(required=True, description='Company Name'),
    'email' : fields.String(required=True, description='Email'),
    'password' : fields.String(required=True, description='Password')
})

brand_change_password = ns_brand.model('Brand change passoword', {
    # 'old_password' : fields.String(required=True, description='Old Password'),
    'new_password' : fields.String(required=True, description='New Password'),
    # 'con_new_password' : fields.String(required=True, description='Confirm New Password')
})


brand_update_profile_pic = ns_brand.model('Brand update profile pic', {
    'profile_pic' : fields.String(required=True, description='Profile Pic'),
})
brand_create_alert_form = ns_brand.model('Brand create alert form', {
    'channel_id' : fields.String(required=True, description='Channel ID'),
    'alert_followers' : fields.String(required=False, description='Alert Followers'),
    'alert_views' : fields.String(required=False, description='Alert Views'),
    'alert_likes' : fields.String(required=False, description='Alert Likes'),
    'alert_comments' : fields.String(required=False, description='Alert Comments')
})


brand_edit_form = ns_brand.model('Brand Details Update', {
    'first_name' : fields.String(required=True, description='First Name'),
    'last_name' : fields.String(required=True, description='Last Name'),
    'phone': fields.String(required=True, description='Phone'),
    'position': fields.String(required=True, description='Position'),
    'company_name': fields.String(required=True, description='Company Name'),
    'url': fields.String(required=True, description='URL'),
    'country': fields.String(required=True, description='Country'),
    'no_of_employees': fields.String(required=True, description='No Of Employees'),
    'city': fields.String(required=True, description='City'),
    'monthly_budget': fields.String(required=True, description='Monthly Budget'),
    'business_sector': fields.String(required=True, description='Business Sector'),
    'facebook_url': fields.String(required=False, description='Facebook Url'),
    'twitter_url': fields.String(required=False, description='Twitter Url'),
    'insta_url': fields.String(required=False, description='Instegram Url'),
    'youtube_url': fields.String(required=False, description='Youtube Url')
})

@ns_brand.route('/register')
class Brand(Resource):
    @ns_brand.expect(brand_form)
    def post(self):
        '''Registers Brand Details'''
        form_data = request.get_json()
        password_sha = sha256_crypt.encrypt(str(form_data.get('password')))
        pass_dict = {'password':password_sha}
        role = {'role':'Admin'}
        form_data.update(pass_dict)
        form_data.update(role)
        first_name = form_data.get('first_name')
        last_name = form_data.get('last_name')
        company_name = form_data.get('company_name')
        email = form_data.get('email')
        password_sha = form_data.get('password')
        role = form_data.get('role')
        columns = ['first_name', 'last_name', 'email_id', 'company_name', 'password', 'role']
        data = [first_name, last_name, email, company_name, password_sha, role]
        result=0
        try:
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert__(table_name='users_brands',columns=columns,data=data,IGNORE='IGNORE')
            return {'response': result},201
        except: return {'response': result},500

@ns_brand.route('/')
class Brand(Resource):
    def get(self):
        '''List of all Brands'''
        connecsiObj = ConnecsiModel()
        columns = ['user_id','first_name','last_name','company_name','email_id','role']
        data = connecsiObj.get__(table_name='users_brands',columns=columns)
        response_list = []
        for item in data:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        # print(response_list)
        return {'data': response_list},200
        # return {'data':data},200

@ns_brand.route('/influencerList')
class Brand(Resource):
    def get(self):
        '''List of all Influencer'''
        connecsiObj = ConnecsiModel()
        columns = ['channel_id','first_name','last_name','business_email']
        data = connecsiObj.get__(table_name='users_influencers',columns=columns)
        response_list = []
        for item in data:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        return {'data': response_list},200

@ns_brand.route('/<string:user_id>')
class Brand(Resource):
    def get(self,user_id):
        '''Brand details by user_id'''
        connecsiObj = ConnecsiModel()
        columns = ['user_id', 'first_name', 'last_name', 'company_name', 'email_id', 'role','phone','position','url','country'
                   ,'no_of_employees','city','monthly_budget','business_sector','facebook_url','twitter_url',
                   'insta_url','youtube_url','profile_pic','confirmed_email']
        data = connecsiObj.get__(table_name='users_brands',columns=columns,WHERE='WHERE',compare_column='user_id',compare_value=str(user_id))
        response_dict = dict(zip(columns, data[0]))
        print(response_dict)
        return {'data':response_dict},200

    @ns_brand.expect(brand_edit_form)
    def put(self,user_id):
        '''Update Brand Details'''
        form_data = request.get_json()
        first_name = form_data.get('first_name')
        last_name = form_data.get('last_name')
        phone = form_data.get('phone')
        position = form_data.get('position')
        url = form_data.get('url')
        country = form_data.get('country')
        no_of_employees = form_data.get('no_of_employees')
        city = form_data.get('city')
        monthly_budget = form_data.get('monthly_budget')
        business_sector = form_data.get('business_sector')
        company_name = form_data.get('company_name')
        facebook_url= form_data.get('facebook_url')
        twitter_url = form_data.get('twitter_url')
        insta_url = form_data.get('insta_url')
        youtube_url = form_data.get('youtube_url')
        columns = ['first_name', 'last_name', 'company_name', 'phone', 'position', 'url',
                   'country', 'no_of_employees', 'city', 'monthly_budget', 'business_sector','facebook_url','twitter_url',
                   'insta_url','youtube_url']
        data=(first_name,last_name,company_name,phone,position,url,country,no_of_employees,city,monthly_budget,business_sector,
              facebook_url,twitter_url,insta_url,youtube_url)
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.update__(table_name='users_brands',columns=columns,WHERE='WHERE',data=data,compare_column='user_id',compare_value=str(user_id))
            return {"response" : 1},200
        except Exception as e:
            return {"response": e},500


@ns_brand.route('/addToFavList/<string:channel_id>/<string:user_id>/<string:channel_name>')
class Brand(Resource):
    def post(self,channel_id,user_id,channel_name):
        '''add influencer to fav list'''
        columns = ['channel_id', 'user_id', 'alert_followers', 'alert_views', 'alert_likes', 'alert_comments','channel_name']
        data = [channel_id, user_id, '', '', '', '',channel_name]
        result = 0
        try:
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert__(table_name='brands_inf_fav_list', columns=columns, data=data,IGNORE='IGNORE')
            return {'response': result}, 201
        except:
            return {'response': result}, 500

@ns_brand.route('/deleteFromFavList/<string:channel_id>/<string:user_id>')
class Brand(Resource):
    def post(self,channel_id,user_id):
        '''Delete  influencer from fav list'''
        result=0
        try:
            connecsiObj = ConnecsiModel()
            result = connecsiObj.delete_fav_inf(channel_id=channel_id,user_id=user_id)
            return {'response': result}, 201
        except:
            return {'response': result}, 500

@ns_brand.route('/getInfluencerFavList/<string:user_id>')
class Brand(Resource):
    def get(self,user_id):
        '''get all Fav influencer list by user_id'''
        columns = ['channel_id', 'title', 'channel_img', 'desc', 'subscriberCount_gained', 'subscriberCount_lost',
                   'business_email', 'total_100video_views',
                   'total_100video_views_unique', 'total_100video_likes', 'total_100video_dislikes',
                   'total_100video_comments', 'total_100video_shares',
                   'facebook_url', 'insta_url', 'twitter_url','alert_followers','alert_views','alert_likes','alert_comments']
        connecsiObj = ConnecsiModel()
        data = connecsiObj.get_fav_inf_list(user_id=user_id)
        response_list = []
        for item in data:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        # print(response_list)
        return {'data': response_list}


@ns_brand.route('/changePassword/<string:user_id>')
class Brand(Resource):
    @ns_brand.expect(brand_change_password)
    def put(self,user_id):
        '''Update Brands password'''
        form_data = request.get_json()
        new_password = form_data.get('new_password')
        password_sha = sha256_crypt.encrypt(str(new_password))
        columns = ['password']
        data = (password_sha)
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.update__(table_name='users_brands', columns=columns, WHERE='WHERE', data=data,
                                 compare_column='user_id', compare_value=str(user_id))
            return {"response": 1}, 200
        except Exception as e:
            return {"response": e}, 500

@ns_brand.route('/updateProfilePic/<string:user_id>')
class Brand(Resource):
    @ns_brand.expect(brand_update_profile_pic)
    def put(self,user_id):
        '''Update Brands Profile Pic'''
        form_data = request.get_json()
        profile_pic = form_data.get('profile_pic')
        columns = ['profile_pic']
        data = (profile_pic)
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.update__(table_name='users_brands', columns=columns, WHERE='WHERE', data=data,
                                 compare_column='user_id', compare_value=str(user_id))
            return {"response": 1}, 200
        except Exception as e:
            return {"response": e}, 500


@ns_brand.route('/createInfluencerAlerts/<string:user_id>')
class Brand(Resource):
    @ns_brand.expect(brand_create_alert_form)
    def put(self,user_id):
        '''Create alerts for Fav Influencer'''
        form_data = request.get_json()
        channel_id = form_data.get('channel_id')
        alert_followers = form_data.get('alert_followers')
        alert_views = form_data.get('alert_views')
        alert_likes = form_data.get('alert_likes')
        alert_comments = form_data.get('alert_comments')
        channel_name = form_data.get('channel_name')
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.create_alert_for_fav_influencer(user_id=user_id,channel_id=channel_id,alert_followers=alert_followers
                                                        ,alert_views=alert_views,alert_likes=alert_likes,alert_comments=alert_comments,channel_name=channel_name)
            return {"response": 1}, 200
        except Exception as e:
            return {"response": e}, 500


@ns_brand.route('/addInfToCampaignList/<string:channel_id>/<string:campaign_id>/<string:channel_name>')
class Brand(Resource):
    def post(self,channel_id,campaign_id,channel_name):
        '''add Any influencer to Campaign list'''
        columns = ['channel_id', 'campaign_id','status','channel_name']
        data = [channel_id, campaign_id,'Added',channel_name]
        result = 0
        try:
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert__(table_name='channel_campaign_message', columns=columns, data=data)
            return {'response': result}, 201
        except:
            return {'response': result}, 500


@ns_brand.route('/getYoutubeInfList/<string:campaign_id>')
class Brand(Resource):
    def get(self,campaign_id):
        '''get all Youtube influencer list by campaign_id'''
        columns = ['channel_id', 'title', 'channel_img','business_email','ref_link','proposal_channels','proposal_price','channel_name']
        connecsiObj = ConnecsiModel()
        data = connecsiObj.get_youtube_inf_list(campaign_id=campaign_id)
        response_list = []
        for item in data:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        # print(response_list)
        return {'data': response_list}


@ns_brand.route('/Proposal/<string:user_id>')
class Brand(Resource):
    def post(self,user_id):
        '''add Proposal '''
        form_data = request.get_json()
        campaign_id = form_data.get('campaign_id')
        message_id = form_data.get('message_id')

        channel_id = form_data.get('channel_id')
        influencer_id = form_data.get('influencer_id')
        proposal_description = form_data.get('proposal_description')
        proposal_from_date = form_data.get('proposal_from_date')
        proposal_to_date = form_data.get('proposal_to_date')
        proposal_channels = form_data.get('proposal_channels')
        proposal_arrangements = form_data.get('proposal_arrangements')
        proposal_kpis = form_data.get('proposal_kpis')
        currency = form_data.get('currency')
        proposal_price = form_data.get('proposal_price')
        target_url=form_data.get('target_url')
        ref_link = form_data.get('ref_link')

        columns = ['campaign_id','message_id','user_id','channel_id','influencer_id','proposal_description',
                   'proposal_from_date','proposal_to_date',
                   'proposal_channels','proposal_arrangements','proposal_kpis','currency','proposal_price','target_url','ref_link']
        data = [campaign_id,message_id,user_id,channel_id,influencer_id,proposal_description,proposal_from_date,
                proposal_to_date,proposal_channels,proposal_arrangements,proposal_kpis,currency,proposal_price,target_url,ref_link]
        result = 0
        try:
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert__(table_name='campaign_proposal', columns=columns, data=data)
            if channel_id and campaign_id:
                connecsiObj.update_channel_status_by_campaign_id(channel_id=str(channel_id),message_id=str(message_id),campaign_id=str(campaign_id),status='Proposal Sent')
            return {'response': result}, 201
        except:
            return {'response': result}, 500


    def get(self,user_id):
        '''get all Proposal by user id of brands'''
        columns = ['proposal_id','campaign_id','campaign_name','message_id','user_id','company_name','email_id','channel_id','title',
                   'business_email','influencer_id','proposal_description',
                   'proposal_from_date','proposal_to_date',
                   'proposal_channels','proposal_arrangements','proposal_kpis','currency','proposal_price','target_url','ref_link']
        connecsiObj = ConnecsiModel()
        data = connecsiObj.get_all_proposal(user_id=user_id)
        response_list = []
        for item in data:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        # print(response_list)
        return {'data': response_list}



@ns_brand.route('/Proposal/get/<string:proposal_id>')
class Brand(Resource):
    def get(self,proposal_id):
        '''get Proposal by proposal id '''
        columns = ['proposal_id', 'campaign_id', 'campaign_name', 'message_id', 'user_id', 'company_name', 'email_id',
                   'channel_id', 'title',
                   'business_email', 'influencer_id', 'proposal_description',
                   'proposal_from_date', 'proposal_to_date',
                   'proposal_channels', 'proposal_arrangements', 'proposal_kpis', 'currency', 'proposal_price','target_url','ref_link']
        connecsiObj = ConnecsiModel()
        data = connecsiObj.get_proposal(proposal_id=proposal_id)
        response_list = []
        for item in data:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        # print(response_list)
        return {'data': response_list}


    def put(self,proposal_id):
        '''Update Proposal '''
        form_data = request.get_json()
        proposal_description = form_data.get('edit_proposal_description')
        proposal_channels = form_data.get('edit_proposal_channels')
        proposal_arrangements = form_data.get('edit_proposal_arrangements')
        proposal_kpis = form_data.get('edit_proposal_kpis')
        currency = form_data.get('currency')
        proposal_price = form_data.get('proposal_price')
        ref_link = form_data.get('edit_proposal_ref_link')
        columns = ['proposal_description','proposal_channels','proposal_arrangements','proposal_kpis','currency','proposal_price',
                   'ref_link']
        data = [proposal_description,proposal_channels,proposal_arrangements,proposal_kpis,currency,proposal_price,ref_link]
        connecsiObj = ConnecsiModel()
        res =  connecsiObj.update__(table_name='campaign_proposal',columns=columns,data=data,WHERE='WHERE',compare_column='proposal_id',
                                    compare_value=str(proposal_id))
        return {'data':res}

@ns_brand.route('/Proposal/get/<string:message_id>/<string:campaign_id>')
class Brand(Resource):
    def get(self,message_id,campaign_id):
        '''get Proposal by message id and campaign id '''
        columns = ['proposal_id', 'campaign_id', 'campaign_name', 'message_id', 'user_id', 'company_name', 'email_id',
                   'channel_id', 'title',
                   'business_email', 'influencer_id', 'proposal_description',
                   'proposal_from_date', 'proposal_to_date',
                   'proposal_channels', 'proposal_arrangements', 'proposal_kpis', 'currency', 'proposal_price','target_url','ref_link']
        connecsiObj = ConnecsiModel()
        data = connecsiObj.get_proposal_by_message_id_and_campaign_id(message_id=message_id,campaign_id=campaign_id)
        response_list = []
        for item in data:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        # print(response_list)
        return {'data': response_list}



@ns_brand.route('/Confirm_email/<string:email_id>')
class Brand(Resource):
    def post(self,email_id):
        '''confirm brands email by email id, this endpoint sets given email id  = confirmed'''
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.confirm_brands_email(email_id=str(email_id),confirmed='confirmed')
            result=1
            return {'response': result}, 201
        except:
            result=0
            return {'response': result}, 500