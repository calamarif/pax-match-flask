from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, make_response, current_app
from flask_session.__init__ import Session
from wtforms import Form, BooleanField, SubmitField, StringField, TextAreaField, IntegerField, PasswordField, validators, SelectField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
import PaxMatch
from requests.auth import HTTPBasicAuth
import re

app = Flask(__name__)
app.secret_key = 'secret123'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

#paxata_url = "https://dataprep.paxata.com"
#paxata_restapi_token = "567e0af0e62f4e5d92b8279809f8b014"
#user_email = "callum@paxata.com"

#paxata_url = "https://internal.paxata.com"
#paxata_restapi_token = "c350fb6f0ca541dd9984313c62b99eac"
#user_email = "cfinlayson@paxata.com"

# docker 2.22
# paxata_url = "http://localhost"
# paxata_restapi_token = "7ROnmdrNaXYpmagiS34KAgUhnzHRxcZ7H8dwU/Qndpo="
# user_email = "callum@paxata.com"

# docker 2019.1 # localhost
paxata_url = "http://localhost:8080"
paxata_restapi_token = "12d0335f0ed94adf83d80c570d2eeba5"
user_email = "callum@datarobot.com"

# set the authorization based on the username and password provided in the user variables section
authorization_token = HTTPBasicAuth("", paxata_restapi_token)
#drop down list  (call Paxata to get a list of projects)
dict_of_datasources = PaxMatch.get_datasource_configs(authorization_token,paxata_url)
if dict_of_datasources:
    print "got dict of datasources"
dict_of_library_items = PaxMatch.get_library_items_for_user_return_dict(authorization_token,paxata_url,user_email)
if dict_of_datasources:
    print "got dict of library names"

@app.route('/dynamic_form')
def login():
    
    form = LoginForm()
    return render_template('dynamic_form.html', title='Sign In', form=form)

@app.route("/hello/<name>")
def hello_there(name):

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + "monday"
    return content

@app.route('/')
def index():
    #print dict_of_datasources
    return render_template('index.html', datasources1=dict_of_library_items, datasources2=dict_of_library_items)

@app.route('/step1')
def step1():
    #print dict_of_library_items
    return render_template('step1.html', datasources1=dict_of_library_items, datasources2=dict_of_library_items)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/fileselect', methods=['GET','POST'])
def fileselect():
    #drop down list  (call Paxata to get a list of projects)
    colours = ['SFDC', 'Marketo','Sugar CRM']
    return render_template('fileselect.html', colours=colours)


@app.route('/about')
def about():
    return render_template('about.html')

class DataSources(Form):
    companyNameWeight = IntegerField('Company Name Weight' , validators=[validators.input_required()])
    addressPart1Weight = IntegerField('Address Part1 Weight' , validators=[validators.input_required()])
    addressPart2Weight = IntegerField('Address Part2 Weight' , validators=[validators.input_required()])
    zipWeight = IntegerField('Zip Weight' , validators=[validators.input_required()])

@app.route('/step2_old', methods = ['GET','POST'])
def step2_old():
    if request.method == 'POST':
        datasource1 = request.form.get('datasource1')
        my_description1 = dict_of_datasources.get(datasource1)

        datasource2 = request.form['datasource2']
        my_description2 = dict_of_datasources.get(datasource2)

        # make a cookie (for later)
        cookie_response = current_app.make_response(redirect('/step2') )
        cookie_response.set_cookie('datasource1',datasource1)
        cookie_response.set_cookie('datasource2',datasource2)
        cookie_response.set_cookie('my_description1',my_description1)
        cookie_response.set_cookie('my_description2',my_description2)

        return render_template('step2_old.html', datasource1=my_description1, datasource2=my_description2)

@app.route('/step2', methods = ['GET','POST'])
def step2():
    if request.method == 'POST':
        datasource1 = request.form.get('datasource1')
        my_description1 = dict_of_library_items.get(datasource1)
        session['datasource1'] = datasource1

        datasource2 = request.form['datasource2']
        my_description2 = dict_of_library_items.get(datasource2)
        session['datasource2'] = datasource2

        datasource1_schema = PaxMatch.get_library_item_metadata(authorization_token,paxata_url,datasource1)
        datasource2_schema = PaxMatch.get_library_item_metadata(authorization_token,paxata_url,datasource2)

        # make a cookie (for later)
        #cookie_response = current_app.make_response(redirect('/step2') )
        #cookie_response.set_cookie('datasource1',datasource1)
        #cookie_response.set_cookie('datasource2',datasource2)
        #cookie_response.set_cookie('my_description1',my_description1)
        #cookie_response.set_cookie('my_description2',my_description2)
        

        return render_template('step2.html', datasource1=my_description1, datasource2=my_description2, datasource1_schema=datasource1_schema, datasource2_schema=datasource2_schema)

class ExternalMatchForm(Form):
    companyNameWeight = IntegerField('Name Weight' , validators=[validators.input_required()])
    addressPart1Weight = IntegerField('Address Weight' , validators=[validators.input_required()])
    addressPart2Weight = IntegerField('City Weight' , validators=[validators.input_required()])


@app.route('/step3', methods = ['GET','POST'])
def step3():
    #if request.method == 'POST' and form.validate():
    datasource1_id_schema_list = []
    datasource2_id_schema_list = []
    column_weights = []

    datasource1_name_column = request.form.get('datasource1_name_column')
    datasource2_name_column = request.form.get('datasource2_name_column')
    
    datasource1_address_column = request.form.get('datasource1_address_column')
    datasource2_address_column = request.form.get('datasource2_address_column')
    
    datasource1_city_column = request.form.get('datasource1_city_column')
    datasource2_city_column = request.form.get('datasource2_city_column')
    
    datasource1 = session.get('datasource1', None)
    datasource2 = session.get('datasource2', None)

    datasource1_id_schema_list.extend((datasource1,datasource1_name_column,datasource1_address_column,datasource1_city_column))
    datasource2_id_schema_list.extend((datasource2,datasource2_name_column,datasource2_address_column,datasource2_city_column))

    form = ExternalMatchForm(request.form)
    if request.method == 'POST' and form.validate():

        form = ExternalMatchForm(request.form)

        weight_company_name = form.companyNameWeight.data
        weight_address_part1 = form.addressPart1Weight.data
        weight_address_part2 = form.addressPart2Weight.data
        cutoff_threshold = request.form["cutoff_threshold"]
        column_weights.extend((cutoff_threshold,weight_company_name,weight_address_part1,weight_address_part2))
        
        url_for_matching_data = PaxMatch.main(paxata_url, paxata_restapi_token, datasource1_id_schema_list, datasource2_id_schema_list, column_weights)

        flash("Matching Run, check Paxata or the SFTP location for the results","success")
        return render_template('step5.html', url_for_matching_data= url_for_matching_data)
    return render_template('step3.html', form=form, datasource1_name_column=datasource1_name_column, datasource2_name_column = datasource2_name_column, datasource1_address_column=datasource1_address_column,datasource2_address_column=datasource2_address_column, datasource1_city_column=datasource1_city_column,datasource2_city_column=datasource2_city_column,datasource1=datasource1,datasource2=datasource2)

@app.route('/step4', methods = ['GET','POST'])
def step4():
    return render_template('step4.html')

@app.route('/step5', methods = ['GET','POST'])
def step5():
    return render_template('step5.html')

@app.route('/index_multislider')
def index_multislider():
    return render_template('index_multislider.html')

@app.route('/externalmatch', methods=['GET','POST'])
def externalmatch():
    form = ExternalMatchForm(request.form)
    if request.method == 'POST' and form.validate():
        companyNameWeight = form.companyNameWeight.data
        addressPart1Weight = form.addressPart1Weight.data
        addressPart2Weight = form.addressPart2Weight.data
        zipWeight = form.zipWeight.data
        PaxMatch.main(paxata_url, paxata_restapi_token, companyNameWeight,addressPart1Weight,addressPart2Weight,zipWeight)

        flash("Matching Run, check Paxata or the SFTP location for the results","success")

        redirect(url_for('index'))


    return render_template('externalmatch.html', form=form)

if __name__ == '__main__':
    #app.secret_key = "secret123"
    #app.run(debug=True)
    sess = Session()
    sess.init_app(app)
    app.secret_key = 'secret123'
    app.config['SESSION_TYPE'] = 'filesystem'
    
    app.debug = True
    app.run()