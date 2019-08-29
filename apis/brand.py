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
    'channel_name' : fields.String(required=False, description='Channel Name'),
    'alert_followers' : fields.Integer(required=False, description='Alert Followers'),
    'alert_views' : fields.Integer(required=False, description='Alert Views'),
    'alert_likes' : fields.Integer(required=False, description='Alert Likes'),
    'alert_comments' : fields.Integer(required=False, description='Alert Comments')
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
        # data = connecsiObj.get__(table_name='users_influencers',columns=columns)
        data = connecsiObj.get_influencer_list()
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


@ns_brand.route('/getDetailsByEmailId/<string:email_id>')
class Brand(Resource):
    def get(self,email_id):
        '''Brand details by email_id'''
        connecsiObj = ConnecsiModel()
        columns = ['user_id', 'first_name', 'last_name', 'company_name', 'email_id', 'role','phone','position','url','country'
                   ,'no_of_employees','city','monthly_budget','business_sector','facebook_url','twitter_url',
                   'insta_url','youtube_url','profile_pic','confirmed_email']
        data = connecsiObj.get__(table_name='users_brands',columns=columns,WHERE='WHERE',compare_column='email_id',compare_value=str(email_id))
        response_dict = dict(zip(columns, data[0]))
        print(response_dict)
        return {'data':response_dict},200


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
        columns = ['channel_id','alert_followers','alert_views','alert_likes','alert_comments','channel_name']
        connecsiObj = ConnecsiModel()
        data = connecsiObj.get_fav_inf_list(user_id=user_id)
        response_list = []
        for item in data:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        # print(response_list)
        return {'data': response_list}

@ns_brand.route('/getInfluencerFavList_with_details/<string:user_id>/<string:channel_name>')
class Brand(Resource):
    def get(self,user_id,channel_name):
        '''get all Fav influencer list by user_id and channel name'''
        if channel_name == 'youtube':
            columns = ['channel_id', 'title', 'channel_img', 'desc', 'subscriberCount_gained', 'subscriberCount_lost',
                       'business_email', 'total_100video_views',
                       'total_100video_views_unique', 'total_100video_likes', 'total_100video_dislikes',
                       'total_100video_comments', 'total_100video_shares',
                       'facebook_url', 'insta_url', 'twitter_url', 'country',
                       'alert_followers','alert_views','alert_likes','alert_comments','channel_name']
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_fav_inf_list_by_channel_name(user_id=user_id,channel_name=channel_name)
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            # print(response_list)
            return {'data': response_list}
        if channel_name == 'twitter':
            columns = ['channel_id', 'screen_name', 'title', 'channel_img', 'desc', 'subscriberCount_gained',
                       'business_email', 'total_100video_views',
                       'total_100video_likes',
                       'total_100video_comments', 'total_100video_shares',
                       'facebook_url', 'insta_url', 'youtube_url', 'twitter_url', 'country',
                       'alert_followers','alert_views','alert_likes','alert_comments','channel_name']
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_fav_inf_list_by_channel_name(user_id=user_id,channel_name=channel_name)
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            # print(response_list)
            return {'data': response_list}
        if channel_name == 'instagram':
            columns = ['channel_id', 'username','title', 'channel_img', 'desc', 'subscriberCount_gained',
                            'business_email', 'total_100video_views',
                            'total_100video_likes',
                           'total_100video_comments', 'total_100video_shares',
                           'facebook_url', 'insta_url','youtube_url', 'twitter_url', 'country',
                       'alert_followers','alert_views','alert_likes','alert_comments','channel_name']
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_fav_inf_list_by_channel_name(user_id=user_id,channel_name=channel_name)
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
    # @ns_brand.expect(brand_create_alert_form)
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
                                                        ,alert_views=alert_views,alert_likes=alert_likes,
                                                        alert_comments=alert_comments,channel_name=channel_name)
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
        columns = ['channel_id', 'title', 'channel_img','business_email','ref_link','proposal_channels','proposal_price','channel_name','proposal_id']
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
            proposal_id = connecsiObj.insert__(table_name='campaign_proposal', columns=columns, data=data)
            if channel_id and campaign_id:
                connecsiObj.update_channel_status_by_campaign_id(channel_id=str(channel_id),message_id=str(message_id),campaign_id=str(campaign_id),status='Proposal Sent')
            return {'response': 1,'proposal_id':proposal_id}, 201
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


@ns_brand.route('/brandsGoogleAnalyticsCredentials/<string:user_id>')
class BrandsGoogleAnalyticsCredentials(Resource):
    def post(self,user_id):
        '''Add or update google analytics credentials for brands'''
        post_data = request.get_json()
        access_token = post_data.get('access_token')
        refresh_token = post_data.get('refresh_token')
        expires_in = post_data.get('expires_in')
        scope = post_data.get('scope')
        token_type = post_data.get('token_type')

        data = [int(user_id),access_token, refresh_token,expires_in,scope,token_type]
        result = 0
        try:
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert_update_users_brands_google_analytics_credentials(data=data)
            return {'response': result}, 201
        except:
            return {'response': result}, 500

    def get(self,user_id):
        '''GET Brands-google analytics credentials by user_id'''
        connecsiObj = ConnecsiModel()
        columns = ['user_id', 'access_token', 'refresh_token', 'expires_in', 'scope', 'token_type']
        data = connecsiObj.get_users_brands_google_analytics_credentials(user_id=user_id)
        response_dict = dict(zip(columns, data[0]))
        print(response_dict)
        return {'data':response_dict},200


package_form = ns_brand.model('Package Details', {
    'package_name' : fields.String(required=True, description='Package Name'),
    'p_created_date' : fields.String(required=True, description='created date in timestamp format'),
    'p_expiry_date' : fields.String(required=True, description='expiry date'),
    'base_package' : fields.String(required=True, description='base package')
})

@ns_brand.route('/updatePackageDetails/<string:user_id>')
class updatePackageDetails(Resource):
    @ns_brand.expect(package_form)
    def post(self,user_id):
        '''Add or update subscription package details for brands
           required parameter : package name (string) example(Free/Basic/Professional/Enterprise)
           required parameter : created date (string) example(date in timestamp in seconds)
           required parameter : expiry date (string) example(date in timestamp in seconds)
           required parameter : base_package (string) example(Free/Basic/Professional/Enterprise)
        '''
        post_data = request.get_json()
        package_name = post_data.get('package_name')

        p_created_date_timestamp = post_data.get('p_created_date')
        p_created_date_object = datetime.datetime.fromtimestamp(int(p_created_date_timestamp))
        p_expiry_date_timestamp = post_data.get('p_expiry_date')
        p_expiry_date_object = datetime.datetime.fromtimestamp(int(p_expiry_date_timestamp))

        base_package = post_data.get('base_package')

        data = [int(user_id),package_name, p_created_date_object,p_expiry_date_object,base_package]
        result = 0
        try:
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert_update_users_brands_subscription_package_details(data=data)
            return {'response': result}, 201
        except:
            return {'response': result}, 500



sub_feature_form = ns_brand.model('sub feature Details', {
    'feature_name' : fields.String(required=True, description='Feature Name'),
    'units' : fields.Integer(required=True, description='Units'),
    'price' : fields.Integer(required=True, description='price'),
    'customized_feature' : fields.String(required=True, description='customized feature'),
    'added_units' : fields.Integer(required=True, description='Added Units'),
    'base_units' : fields.Integer(required=True, description='Base Units')
})

@ns_brand.route('/subscriptionFeatureDetails/<string:user_id>')
class subscriptionFeatureDetails(Resource):
    @ns_brand.expect(sub_feature_form)
    def post(self,user_id):
        '''Add or update subscription feature details for brands
           required parameter : feature name (string) example(create campaign) must be unique
           required parameter : units (integer) example(integer)
           required parameter : price (integer) example(integer)
           required parameter : customized feature (string) example(Yes/No)
           required parameter : added_units (integer) example(integer)
           required parameter : base_units (integer) example(integer)
        '''
        post_data = request.get_json()
        feature_name = post_data.get('feature_name')
        units = post_data.get('units')
        price = post_data.get('price')
        customized_feature = post_data.get('customized_feature')
        added_units = post_data.get('added_units')
        base_units = post_data.get('base_units')


        data = [str(user_id),feature_name, str(units),str(price),customized_feature,added_units,base_units]
        result = 0
        try:
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert_update_subscription_feature_details(data=data)
            return {'response': result}, 200
        except:
            return {'response': result}, 500

    # @ns_brand.expect(sub_feature_form)
    # def put(self,user_id):
    #     post_data = request.get_json()
    #     feature_name = post_data.get('feature_name')
    #     units = post_data.get('units')
    #     price = post_data.get('price')
    #     customized_feature = post_data.get('customized_feature')
    #     result=0
    #     try:
    #         connecsiObj = ConnecsiModel()
    #         result = connecsiObj.update_subscription_feature_details(user_id=user_id,feature_name=feature_name,units=units,price=price,customized_feature=customized_feature)
    #         return {'response': result}, 201
    #     except:
    #         return {'response': result}, 500



@ns_brand.route('/subscriptionPackageDetails/<string:user_id>')
class subscriptionPackageDetails(Resource):
    def get(self,user_id):
        '''GET Brands-subcription package details by user_id'''
        connecsiObj = ConnecsiModel()
        columns = ['user_id', 'package_name', 'p_created_date', 'p_expiry_date','feature_name',
                   'units','price','customized_feature','base_package','added_units','base_units']
        data = connecsiObj.get_users_brands_subscription_package_with_feature_details(user_id=user_id)
        data_list = []
        for item in data:
            temp_list = []
            temp_list.append(item[0])
            temp_list.append(item[1])
            created_date_timestamp = datetime.datetime.timestamp(item[2])
            temp_list.append(created_date_timestamp)
            expiry_date_timestamp = datetime.datetime.timestamp(item[3])
            temp_list.append(expiry_date_timestamp)
            temp_list.append(item[4])
            temp_list.append(item[5])
            temp_list.append(item[6])
            temp_list.append(item[7])
            temp_list.append(item[8])
            temp_list.append(item[9])
            data_list.append(temp_list)
        response_list=[]
        for item1 in data_list:
            dict_temp = dict(zip(columns, item1))
            response_list.append(dict_temp)
        return {'data': response_list}




auto_fill_proposal_form = ns_brand.model('autofill proposal feature Details', {
    'auto_or_manual' : fields.String(required=True, description='Auto or manual')
})
@ns_brand.route('/subscriptionAutoFillProposal/<string:user_id>/<string:proposal_id>')
class subscriptionAutoFillProposal(Resource):
    @ns_brand.expect(auto_fill_proposal_form)
    def post(self,user_id,proposal_id):
        '''Add autofill proposal subscription feature details for brands
        required parameter : auto_or_manual (string) example:(auto/manual)
        '''
        post_data = request.get_json()
        auto_or_manual = post_data.get('auto_or_manual')
        data = [user_id,proposal_id, auto_or_manual]
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.insert_autofill_proposal_subscription_feature(data=data)
            result=1
            return {'response': result}, 200
        except:
            result=0
            return {'response': result}, 500

    def get(self,user_id,proposal_id):
        connecsiObj = ConnecsiModel()
        columns = ['user_id', 'proposal_id', 'auto_or_manual']
        data = connecsiObj.get_subscription_feature_autofill_proposal_details(user_id=user_id,proposal_id=proposal_id)
        print(data)
        response_list = []
        for item in data:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        return {'data': response_list}

