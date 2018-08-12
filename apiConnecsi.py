from flask import Flask, request, session, Blueprint
from flask_restplus import Resource, Api, fields
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt

app = Flask(__name__)

blueprint = Blueprint('api',__name__,url_prefix='/api')
api = Api(blueprint,version='1.0', title='Connecsi Api',description='APIS',doc='/documentation')
app.register_blueprint(blueprint)
api.namespaces.pop(0)
# app.config['SWAGGER_UI_JSON_EDITOR'] = True
################# NAME SPACE #######################################################

ns_brands = api.namespace('Brand', description='Brand operations')
ns_user = api.namespace('User', description='User Operations')

#############################################################################################################################################

login_form = api.model('Login', {
    'email' : fields.String(required=True, description='Email'),
    'password' : fields.String(required=True, description='Password')
})

brand_form = api.model('Brand Details', {
    'first_name' : fields.String(required=True, description='First Name'),
    'last_name' : fields.String(required=True, description='Last Name'),
    'company_name' : fields.String(required=True, description='Company Name'),
    'email' : fields.String(required=True, description='Email'),
    'password' : fields.String(required=True, description='Password')
})

@ns_user.route('/login')
class Login(Resource):
    @api.expect(login_form)
    # @api.param('password')
    # @api.param('username')
    def post(self):
        # languages.append(api.payload)
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        # username=flask.request.args.get("username")
        connecsiObj = ConnecsiModel()
        data = connecsiObj.get_user_by_email_id(table_name='users_brands', email_id=email)
        # print(data)
        if data != None:
            if sha256_crypt.verify(password, data[4]):
                session['logged_in'] = True
                session['email_id'] = email
                session['first_name'] = data[1]
                session['last_name'] = data[2]
                session['type'] = 'brand'
                session['company_name'] = data[5]
                session['user_id'] = data[0]
                print(session['user_id'])
                return {'user_id': session['user_id']},200
            else:
                error = 'Invalid login'
                return {'error': error},404
        else:
            return {'error':'No such Username'},404

@ns_user.route('/logout/<string:user_id>')
class Logout(Resource):
    def post(self,user_id):
        session.clear()
        return {'Logged out':'Success'},200


@ns_brands.route('/register')
class Brand(Resource):
    @api.expect(brand_form)
    def post(self):
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

@ns_brands.route('/getAll')
# @ns_brands.doc('list_brand')
class Brand(Resource):
    def get(self):
        connecsiObj = ConnecsiModel()
        data = connecsiObj.get__(table_name='users_brands',STAR='*')
        return {'data':data}




if __name__ == '__main__':
    app.secret_key = 'connecsiSecretKey'
    app.run(debug=True,port=8090)