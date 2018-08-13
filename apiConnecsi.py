from flask import Flask, request, session, Blueprint
from flask_restplus import Resource, Api, fields
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime


# app = Flask(__name__)

# blueprint = Blueprint('api',__name__,url_prefix='/api')
# api = Api(blueprint,version='1.0', title='Connecsi Api',description='APIS',doc='/documentation')
# app.register_blueprint(blueprint)
# api.namespaces.pop(0)
# app.config['SWAGGER_UI_JSON_EDITOR'] = True
################# NAME SPACE #######################################################

# ns_brands = api.namespace('Brand', description='Brand Operations')
# ns_user = api.namespace('User', description='User Operations')
# ns_youtube_region_codes = api.namespace('YoutubeRegionsCodes', description='Youtube Region Codes')
# ns_youtube_video_categories = api.namespace('YoutubeVideoCategories', description='Youtube Video Categories')
# ns_payments = api.namespace('Payments', description='Brand Payments')
# ns_campaign = api.namespace('Campaign', description='Brands Campaign')

#############################################################################################################################################
########################## MODEL FORM VALIDATIONS ###################################################################

# login_form = api.model('Login', {
#     'email' : fields.String(required=True, description='Email'),
#     'password' : fields.String(required=True, description='Password')
# })

# brand_form = api.model('Brand Details', {
#     'first_name' : fields.String(required=True, description='First Name'),
#     'last_name' : fields.String(required=True, description='Last Name'),
#     'company_name' : fields.String(required=True, description='Company Name'),
#     'email' : fields.String(required=True, description='Email'),
#     'password' : fields.String(required=True, description='Password')
# })
#
# brand_payment_form = api.model('Brand Payments', {
#     'amount' : fields.Integer(required=True, description='Amount'),
#     'description' : fields.String(required=True, description='Description')
# })

# brand_campaign_form = api.model('Brand Campaign', {
#     'amount' : fields.Integer(required=True, description='Amount'),
#     'description' : fields.String(required=True, description='Description')
# })

###########################################################################################################################################

########################## LOGIN MODULE ##################################################################
# @ns_user.route('/login')
# class Login(Resource):
#     @api.expect(login_form)
#     # @api.param('password')
#     # @api.param('username')
#     def post(self):
#         # languages.append(api.payload)
#         '''checks the login details and sets session variables'''
#         data = request.get_json()
#         email = data.get('email')
#         password = data.get('password')
#         # username=flask.request.args.get("username")
#         connecsiObj = ConnecsiModel()
#         data = connecsiObj.get_user_by_email_id(table_name='users_brands', email_id=email)
#         # print(data)
#         if data != None:
#             if sha256_crypt.verify(password, data[4]):
#                 session['logged_in'] = True
#                 session['email_id'] = email
#                 session['first_name'] = data[1]
#                 session['last_name'] = data[2]
#                 session['type'] = 'brand'
#                 session['company_name'] = data[5]
#                 session['user_id'] = data[0]
#                 print(session['user_id'])
#                 return {'user_id': session['user_id']},200
#             else:
#                 error = 'Invalid login'
#                 return {'error': error},404
#         else:
#             return {'error':'No such Username'},404
#
# @ns_user.route('/logout/<string:user_id>')
# class Logout(Resource):
#     def post(self,user_id):
#         '''clear all session of user_id'''
#         session.clear()
#         return {'Logged out':'Success'},200
#
###########################################################################################################

############################################## BRANDS MODULE #############################################
# @ns_brands.route('/register')
# class Brand(Resource):
#     @api.expect(brand_form)
#     def post(self):
#         '''Registers Brand Details'''
#         form_data = request.get_json()
#         password_sha = sha256_crypt.encrypt(str(form_data.get('password')))
#         pass_dict = {'password':password_sha}
#         role = {'role':'Admin'}
#         form_data.update(pass_dict)
#         form_data.update(role)
#         first_name = form_data.get('first_name')
#         last_name = form_data.get('last_name')
#         company_name = form_data.get('company_name')
#         email = form_data.get('email')
#         password_sha = form_data.get('password')
#         role = form_data.get('role')
#         columns = ['first_name', 'last_name', 'email_id', 'company_name', 'password', 'role']
#         data = [first_name, last_name, email, company_name, password_sha, role]
#         result=0
#         try:
#             connecsiObj = ConnecsiModel()
#             result = connecsiObj.insert__(table_name='users_brands',columns=columns,data=data,IGNORE='IGNORE')
#             return {'response': result},201
#         except: return {'response': result},500
#
# @ns_brands.route('/')
# class Brand(Resource):
#     def get(self):
#         '''List of all Brands'''
#         connecsiObj = ConnecsiModel()
#         columns = ['user_id','first_name','last_name','company_name','email_id','role']
#         data = connecsiObj.get__(table_name='users_brands',columns=columns)
#         return {'data':data},200
#
# @ns_brands.route('/<string:user_id>')
# class Brand(Resource):
#     def get(self,user_id):
#         '''Brand details by user_id'''
#         connecsiObj = ConnecsiModel()
#         columns = ['user_id', 'first_name', 'last_name', 'company_name', 'email_id', 'role']
#         data = connecsiObj.get__(table_name='users_brands',columns=columns,WHERE='WHERE',compare_column='user_id',compare_value=str(user_id))
#         return {'data':data},200
##############################################################################################################################

######################################## PAYMENTS BRANDS ################################################
# @ns_payments.route('/<string:user_id>')
# class BrandPayments(Resource):
#     @api.expect(brand_payment_form)
#     def post(self,user_id):
#         form_data = request.get_json()
#         amount = form_data.get('amount')
#         description = form_data.get('description')
#         connecsiObj = ConnecsiModel()
#         columns = ['user_id','email_id']
#         data_tuple = connecsiObj.get__(table_name='users_brands',columns=columns,WHERE='WHERE',compare_column='user_id',compare_value=str(user_id))
#         date = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
#         email_id = data_tuple[0][1]
#         data = [user_id, date, email_id, amount, description]
#         res = connecsiObj.insert__(table_name='users_brands_payments',
#                              columns=['user_id', 'date', 'email_id', 'amount', 'description'], data=data)
#         return {'response': res },201
#
#     def get(self,user_id):
#         connecsiObj = ConnecsiModel()
#         data_tuple = connecsiObj.get__(table_name='users_brands_payments',STAR='*',WHERE='WHERE',compare_column='user_id',compare_value=str(user_id))
#         return {'data' : data_tuple},200

###############################################################################################################################

# @ns_youtube_region_codes.route('/')
# class RegionCodesList(Resource):
#     def get(self):
#         '''get all youtube region codes'''
#         connecsiObj = ConnecsiModel()
#         region_codes = connecsiObj.get__(table_name='youtube_region_codes', STAR='*')
#         return {'data' : region_codes}
#
# @ns_youtube_region_codes.route('<string:regionCode>')
# class RegionCode(Resource):
#     def get(self,regionCode):
#         '''get country name by region code'''
#         connecsiObj = ConnecsiModel()
#         data = connecsiObj.get__(table_name='youtube_region_codes',STAR='*',WHERE='WHERE',compare_column='regionCode',compare_value=str(regionCode))
#         return {'data' : data}
#

############################ CAMPAIGN MODULE ###################################################################################





# if __name__ == '__main__':
#     app.secret_key = 'connecsiSecretKey'
#     app.run(debug=True,port=8090)