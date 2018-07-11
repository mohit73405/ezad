from functools import wraps

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from model.ConnecsiModel import ConnecsiModel
from wtforms import Form, StringField, TextAreaField, PasswordField, validators,TextField
from passlib.hash import sha256_crypt


connecsiApp = Flask(__name__)


@connecsiApp.route('/')
def index():
    title='Connesi App Login Panel'
    data=[]
    data.append(title)
    return render_template('user/login.html',data=data)



@connecsiApp.route('/registerBrand')
def registerBrand():
    return render_template('user/registerFormBrand.html')

@connecsiApp.route('/saveBrand',methods=['GET','POST'])
def saveBrand():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        company_name = request.form.get('company_name')
        password = request.form.get('password')
        password_sha = sha256_crypt.encrypt(str(password))
        data = [first_name,last_name,email,company_name,password_sha]
        # print(data)

        columns = ['first_name','last_name','email_id','company_name','password']
        connecsiObj = ConnecsiModel()
        connecsiObj.insert__(data=data,columns=columns,table_name='users_brands',IGNORE='IGNORE')


        flash("Brand Details Successfully Registered", 'success')
        title = 'Connesi App Login Panel'
        return render_template('login.html', title=title)


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, Please login','danger')
            return redirect(url_for('index'))
    return wrap


#Logout
@connecsiApp.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('index'))


# User login
@connecsiApp.route('/login',methods=['POST'])
def login():
    if request.method=='POST':
        if 'brand' in request.form:
            email_id = request.form.get('brand_email')
            password = request.form.get('brand_password')
            print(email_id)
            print(password)
            # password_sha = sha256_crypt.encrypt(str(password))
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_user_by_email_id(table_name='users_brands',email_id=email_id)
            print(data)

            if data!=None:
                if sha256_crypt.verify(password,data[4]):
                    session['logged_in']=True
                    session['email_id']=email_id
                    session['first_name'] = data[1]
                    session['last_name'] = data[2]
                    session['type'] = 'brand'
                    session['company_name'] = data[5]
                    session['user_id']=data[0]
                    print(session['user_id'])
                    flash('You are now logged in', 'success')
                    return redirect(url_for('admin'))
                else:
                    error = 'Invalid login'
                    flash(error,'danger')
            else:
                return render_template('login.html')

        elif 'influencer' in request.form:
            email_id = request.form.get('inf_username')
            password = request.form.get('inf_password')
            print(email_id)
            print(password)



@connecsiApp.route('/admin')
@is_logged_in
def admin():
    title='Dashboard'
    return render_template('index.html',title=title)


@connecsiApp.route('/profileView')
@is_logged_in
def profileView():
    title='Profile View'
    type = session['type']
    user_id = session['user_id']
    if type == 'brand':
        table_name = 'users_brands'
    else:
        table_name = 'users_inf'
    connecsiObj = ConnecsiModel()
    data = connecsiObj.get_user_by_user_id(table_name=table_name,user_id=str(user_id))
    # print(data)
    return render_template('user/user-profile-page.html',data=data,title=title)



if __name__ == '__main__':
    connecsiApp.secret_key = 'connecsiSecretKey'
    connecsiApp.run(debug=True,host='localhost',port=8080)