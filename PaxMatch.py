from __future__ import division
__author__ = 'Callum'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Python 2.7.12
#PaxMatch.py - Match 2 Library items
#Version: 0.1
#Date: June 15th 2019
################ USAGE OF THE  PROGRAM #####################################
# Short Description:
# Allow users to take a config file and apply weights to an existing project

import requests, os, json, copy
from requests.auth import HTTPBasicAuth
from collections import OrderedDict

# the below two lines supress the warning ignoring the "Unverified HTTPS request is being made" warning
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# (23) Get All columns names for a library item
def get_library_item_metadata(authorization_token,paxata_url,dataFileId):
    dataFileId_version= dataFileId.split("_")
    dataFileId = dataFileId_version[0]
    version = dataFileId_version[1]
    url_request = (paxata_url + "/rest/library/data/"+ dataFileId + "/" + version)
    my_response = requests.get(url_request, auth=authorization_token, verify=False)
    if(my_response.ok):
        json_of_library_items = json.loads(my_response.content)
    else:
        json_of_library_items = 0
        my_response.raise_for_status()
    list_of_library_columns = []

#    this would avoid a second call to get the datatypes, but makes things more complex
    for item in json_of_library_items['schema']:
        temp_list = []
        temp_list.append(str(item.get('name')))
        temp_list.append(item.get('type'))
        list_of_library_columns.append(temp_list)
            
    return list_of_library_columns

# (1) Get All Library items for a specific user
def get_library_items_for_user_return_dict(authorization_token,paxata_url,user_email):
    dict_of_library_items = {}
    url_user_request = (paxata_url + "/rest/users?email=" + user_email)
    my_user_response = requests.get(url_user_request, auth=authorization_token, verify=False)

    json_of_user_info = json.loads(my_user_response.content)

    if not json_of_user_info:
        print "No login found for user " + user_email
    else:
        user_id = json_of_user_info[0].get('userId')
        user_name = json_of_user_info[0].get('name')

        url_request = (paxata_url + "/rest/library/data/")
        my_response = requests.get(url_request, auth=authorization_token, verify=False)
        if(my_response.ok):
            json_of_library_items = json.loads(my_response.content)
        else:
            json_of_library_items = 0
            my_response.raise_for_status()
        for item in json_of_library_items:
            if item.get('userId') == user_id:
                id_of_dict = (str(item.get('dataFileId'))+"_"+str(item.get('version')))
                dict_of_library_items[id_of_dict] = item.get('name')
    return OrderedDict(sorted(dict_of_library_items.items(), key=lambda kv:(kv[0].lower(),kv[1])))

# (1) Get Library Name and schema from LibraryID
def get_library_items_for_user(authorization_token,paxata_url):
    user_email = "callum@paxata.com"
    url_user_request = (paxata_url + "/rest/users?email="+user_email)
    my_user_response = requests.get(url_user_request, auth=authorization_token, verify=False)

    json_of_user_info = json.loads(my_user_response.content)

    if not json_of_user_info:
        print "No login found for user " + user_email
    else:
        user_id = json_of_user_info[0].get('userId')
        user_name = json_of_user_info[0].get('name')

        url_request = (paxata_url + "/rest/library/data/")
        my_response = requests.get(url_request, auth=authorization_token, verify=False)
        if(my_response.ok):
            json_of_library_items = json.loads(my_response.content)
        else:
            json_of_library_items = 0
            my_response.raise_for_status()
        list_of_library_items = []
        for item in json_of_library_items:
            if item.get('userId') == user_id:
                temp_list = []
                temp_list.append(str(item.get('dataFileId'))+"_"+str(item.get('version')))
                temp_list.append(str(item.get('name')))
                list_of_library_items.append(temp_list)
    return list_of_library_items


# Get all the data sources for a tennant
def get_datasource_configs(authorization_token,paxata_url):
    url_request = (paxata_url + "/rest/datasource/configs")
    try:
        myResponse = requests.get(url_request, auth=authorization_token, verify=False)
        if (myResponse.ok):
            json_of_datasource_configs = json.loads(myResponse.content)
        else:
            json_of_datasource_configs = 0
            myResponse.raise_for_status()
        dict_of_datasources = {}
        for item in json_of_datasource_configs:
            dict_of_datasources[item.get('dataSourceId')] = item.get('name')
        dict_of_datasources['0'] = ' - No Connector - Data already exists in Paxata - '
        #returning a sorted dictionary
        return(OrderedDict(sorted(dict_of_datasources.items(), key=lambda kv:(kv[1].lower(),kv[0]))))

    except Exception:
        print "Couldn't access Paxata"
        exit



# Get an existing Project's script file
def get_new_project_script(authorization_token,paxata_url,projectId):
    #url_request = (paxata_url + "/rest/scripts?projectId=" + projectId + "&version=" + "95")
    url_request = (paxata_url + "/rest/scripts?projectId=" + str(projectId))
    myResponse = requests.get(url_request, auth=authorization_token, verify=False)
    if (myResponse.ok):
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        json_of_project = json.loads(myResponse.content)
    else:
        json_of_project = 0
        myResponse.raise_for_status()
    return(json_of_project)


    myResponse = requests.get(url_request, auth=authorization_token, verify=False)
    if (myResponse.ok):
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        json_of_project = json.loads(myResponse.content)
    else:
        json_of_project = 0
        myResponse.raise_for_status()
    return(json_of_project)

# Check if a Project Name exists and return it's ID
def check_if_a_project_exists(auth_token,paxata_url,project_name):
    projectId = ""
    url_request = (paxata_url + "/rest/projects?name=" + project_name)
    my_response = requests.get(url_request,auth=auth_token , verify=False)
    if(my_response.ok):
        jdata_new_project_response = json.loads(my_response.content)
        if (not jdata_new_project_response):
            projectId = 0
        else:
            projectId = jdata_new_project_response[0]['projectId']
    else:
        my_response.raise_for_status()
    return projectId

def update_project_with_new_script(working_path,authorization_token,paxata_url,main_project_json_script,projectId):
    url_request = (paxata_url + "/rest/scripts?update=script&force=true&projectId=" + str(projectId))
    s = {'script': json.dumps(main_project_json_script)}
    myResponse = requests.put(url_request, data=s, auth=authorization_token, verify=False)
    if (myResponse.ok):
        json_of_new_project = json.loads(myResponse.content)
    else:
        #if there is a problem in updating the project, it would indicate a problem with the script, so lets output it
        with open(working_path + 'invalid_script_dump.json', 'w') as f:
            json.dump(main_project_json_script, f)
        myResponse.raise_for_status()

def get_name_of_datasource(auth_token,paxata_url,libraryId,version):
    url_request = (paxata_url + "/rest/library/data/"+str(libraryId) + "/" + version)

    my_response = requests.get(url_request, auth=auth_token, verify=False)
    if(my_response.ok):
        jdata_datasources = json.loads(my_response.content)
        library_name = jdata_datasources.get('name')
    return library_name

# (9) Run a Project and publish the answerset to the library
def run_a_project(auth_token,paxata_url,projectId):
    post_request = (paxata_url + "/rest/project/publish?projectId=" + projectId)
    postResponse = requests.post(post_request, auth=auth_token, verify=False)
    if (postResponse.ok):
        print "Project Run - " + str(projectId)
    else:
        print "Something went wrong with POST call " + str(postResponse)
    json_response = json.loads(postResponse.content)
    AnswersetId = json_response[0].get('dataFileId')
    return AnswersetId

def update_the_project(json_config,project_script,matching_step_name):
    name_company_name = json_config["MATCHING_CONFIG"]["name_company_name"]
    name_address_part1 = json_config["MATCHING_CONFIG"]["name_address_part1"]
    name_address_part2 = json_config["MATCHING_CONFIG"]["name_address_part2"]
    name_zip = json_config["MATCHING_CONFIG"]["name_zip"]
    weight_company_name = str(json_config["MATCHING_CONFIG"]["weight_company_name"])
    weight_address_part1 = str(json_config["MATCHING_CONFIG"]["weight_address_part1"])
    weight_address_part2 = str(json_config["MATCHING_CONFIG"]["weight_address_part2"])
    weight_zip = str(json_config["MATCHING_CONFIG"]["weight_zip"])
    i=0
    for item in project_script['steps']:
        try:
            if project_script['steps'][i]['newColumnName'] == matching_step_name:
                project_script['steps'][i]['expression'] = "((@" + name_company_name + "@ * " + weight_company_name +") + (@"+ name_address_part1 +"@  *"+ weight_address_part1 +") + (@"+ name_address_part2 +"@ *"+ weight_address_part2 +")) / ("+ weight_company_name +"+ "+ weight_address_part1 +"+ "+ weight_address_part2 +" )"
            i += 1
        except KeyError:
            #print "Trying next element"
            i += 1
            continue

    # append this onto the initial project script
    return(project_script)

def update_the_project_master_matching_step(project_script,matching_step_name,weight_company_name,weight_address_part1,weight_address_part2):
    name_company_name = "Matching - Company Name"
    name_address_part1 = "Matching - Address Part1"
    name_address_part2 = "Matching - Address Part2"
    #name_zip = "Matching - Zip"
    i=0
    for item in project_script['steps']:
        try:
            if project_script['steps'][i]['newColumnName'] == matching_step_name:
                project_script['steps'][i]['expression'] = "((@" + name_company_name + "@ * " + weight_company_name +") + (@"+ name_address_part1 +"@  *"+ weight_address_part1 +") + (@"+ name_address_part2 +"@ *"+ weight_address_part2 +"))  / ("+ weight_company_name +"+ "+ weight_address_part1 +"+ "+ weight_address_part2 +")"
            i += 1

        except KeyError:
            #print "Trying next element"
            i += 1
            continue

    # append this onto the initial project script
    return(project_script)

# Get an existing Project's script file
def load_project_script_json(json_file_name):
    if json_file_name:
        with open(json_file_name, 'r') as f:
            project_script = json.load(f)
    return project_script

def delete_library_item(auth_token,paxata_url,libraryId):
    url_request = (paxata_url + "/rest/library/data/"+str(libraryId))
    my_response = requests.delete(url_request, auth=auth_token, verify=False)
    if(my_response.ok):
        jdata_datasources = json.loads(my_response.content, object_pairs_hook=OrderedDict)
        library_name = jdata_datasources.get('name')
    return library_name

# Get Library data from Paxata and load it into a file
def get_paxata_library_data(auth_token,paxata_url,library_dataset_id):
    # This first "IF" statement is checking if it is the FIRST dataset, if it is, then download the column headers
    post_request = (paxata_url + "/rest/datasource/exports/local/" + library_dataset_id)
    payload = {'format': 'separator', 'quoteValues': 'True'}
    post_response = requests.post(post_request, auth=auth_token, params=payload)
    if (post_response.ok):
        TextData = post_response.content
    else:
        TextData = "Didn't load the datasset export. Status code " + str(post_response.status_code)
    return TextData

# (12) Create a new (empty) Paxata project. Will return the projectId
def create_a_new_project(auth_token,paxata_url,project_name):
    projectId = ""
    url_request = (paxata_url + "/rest/projects?name=" + project_name)
    my_response = requests.post(url_request,auth=auth_token , verify=False)
    if(my_response.ok):
        print "Project \"" + project_name + "\" created."
        jdata_new_project_response = json.loads(my_response.content)
        projectId = jdata_new_project_response['projectId']
    else:
        if my_response.status_code == 409:
            print("Project Already Exists")
        else:
            my_response.raise_for_status()
    return projectId


# (7) Check if a Project Name exists and return it's ID
def check_if_a_project_exists(auth_token,paxata_url,project_name):
    projectId = ""
    url_request = (paxata_url + "/rest/projects?name=" + project_name)
    my_response = requests.get(url_request,auth=auth_token , verify=False)
    if(my_response.ok):
        jdata_new_project_response = json.loads(my_response.content)
        if (not jdata_new_project_response):
            projectId = 0
        else:
            projectId = jdata_new_project_response[0]['projectId']
    else:
        my_response.raise_for_status()
    return projectId

# (8) Delete a project based on ID (TEST THIS), not sure if i can access the content directly
def delete_a_project_if_it_exists(auth_token,paxata_url,projectId):
    url_request = (paxata_url + "/rest/projects/" + str(projectId))
    my_response = requests.delete(url_request,auth=auth_token , verify=False)
    if(my_response.ok):
        print "Project \"" + json.loads(my_response.content).get("name") + "\" deleted."
    else:
        my_response.raise_for_status()

def insert_initial_data_into_empty_project(authorization_token, paxata_url,json_of_new_project,datasource1,datasource1_version):
    #update the script... take the existing script and manipulate it.
    updated_json_script = copy.deepcopy(json_of_new_project[0])
    updated_json_script['steps'][0]['importStep']['libraryId'] = str(datasource1)
    updated_json_script['steps'][0]['importStep']['libraryVersion'] = 1
    updated_json_script['steps'][0]['importStep']['libraryIdWithVersion'] = str(datasource1) + "_" + str(datasource1_version)
    #function to get the metadata
    json_of_datasource_schema = get_library_data_to_insert_into_project(paxata_url, authorization_token,datasource1,str(datasource1_version))
    i=0
    for schema_item in json_of_datasource_schema:
        temp_name = schema_item.get('name')
        temp_type = schema_item.get('type')
        updated_json_script['steps'][0]['importStep']['columns'].insert(i,{'hidden': False})
        updated_json_script['steps'][0]['importStep']['columns'][i]['columnDisplayName'] = temp_name
        updated_json_script['steps'][0]['importStep']['columns'][i]['columnType'] = temp_type
        updated_json_script['steps'][0]['importStep']['columns'][i]['columnName'] = temp_name
        #go to the next element
        i+=1

    return(updated_json_script)

def get_library_data_to_insert_into_project(paxata_url, authorization_token,libraryId, libraryId_version):
    url_request = (paxata_url + "/rest/library/data/" + libraryId + "/" + libraryId_version)
    myResponse = requests.get(url_request, auth=authorization_token, verify=True)
    if (myResponse.ok):
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        json_of_datasource_schema = json.loads(myResponse.content)['schema']
        print "Library metadata read to update the project"
    else:
        myResponse.raise_for_status()
    return (json_of_datasource_schema)

def update_column_names(authorization_token,paxata_url,project_script, datasource1_id_schema_list, datasource2_id_schema_list, column_weights):
    matching_step_name = "Master Weighted Score"
    datasource1, datasource1_name_column, datasource1_address_column, datasource1_city_column = datasource1_id_schema_list
    datasource2, datasource2_name_column, datasource2_address_column, datasource2_city_column = datasource2_id_schema_list
    cut_off_threshold,weight_company_name,weight_address_part1,weight_address_part2 = column_weights

    ds2_library_id = datasource2_id_schema_list[0].split("_")[0]
    ds2_library_version = datasource2_id_schema_list[0].split("_")[1]
    
    json_of_datasource_schema = get_library_data_to_insert_into_project(paxata_url, authorization_token,ds2_library_id,ds2_library_version)
    counter_main_project=0
    for step in project_script['steps']:
        if (step.get("expression") == "HASHVALUE(@Company Name - DS1@ ,\"orgcleansing\")"):
            project_script['steps'][counter_main_project]['expression'] = "HASHVALUE(@" + datasource1_name_column + "@ ,\"orgcleansing\")"
        
        if (step.get("steps")):
            counter_for_ds2_expand_steps = 0
            for substep in step.get("steps"):
                project_script['steps'][counter_main_project]['steps'][0]['libraryId'] = ds2_library_id
                project_script['steps'][counter_main_project]['steps'][0]['libraryVersion'] = ds2_library_version
                project_script['steps'][counter_main_project]['steps'][0]['libraryIdWithVersion'] = datasource2_id_schema_list[0]
                counter_ds2_schema=0
                # skipping the first element of the list (because thats the library id)
                for schema_item in json_of_datasource_schema:
                    temp_name = schema_item.get('name')
                    temp_type = schema_item.get('type')
                    project_script['steps'][counter_main_project]['steps'][0]['columns'].insert(counter_ds2_schema,{'hidden': False})
                    project_script['steps'][counter_main_project]['steps'][0]['columns'][counter_ds2_schema]['columnDisplayName'] = temp_name
                    project_script['steps'][counter_main_project]['steps'][0]['columns'][counter_ds2_schema]['columnType'] = temp_type
                    project_script['steps'][counter_main_project]['steps'][0]['columns'][counter_ds2_schema]['columnName'] = temp_name
                    #go to the next element
                    counter_ds2_schema+=1
                if (substep.get("expression") == "hashvalue(@Company Name - DS2@ ,\"orgcleansing\")"):
                    project_script['steps'][counter_main_project]['steps'][counter_for_ds2_expand_steps]["expression"] = "HASHVALUE(@" + datasource2_name_column + "@ ,\"orgcleansing\")"
                counter_for_ds2_expand_steps+=1
        #keeping the order of the project script (probably makes more sense to have this at the top...)
        # Currently there is no ZIP in my demo
        #if (step.get("expression")== "HASHVALUE(str(@Zip - DS1@)  ,\"PaxLevenshtein\",str(@Zip - DS2@))"):
        #    project_script['steps'][counter_main_project]['expression'] = "HASHVALUE(str(@Zip - DS1@)  ,\"PaxLevenshtein\",str(@Zip - DS2@))"
        if (step.get("expression")== "HASHVALUE(@Address - DS2@ ,\"orgcleansing\")"):
            project_script['steps'][counter_main_project]['expression'] = "HASHVALUE(@"+ datasource2_address_column +"@ ,\"orgcleansing\")"            
        if (step.get("expression")== "HASHVALUE(@Address - DS1@ ,\"orgcleansing\")"):
            project_script['steps'][counter_main_project]['expression'] = "HASHVALUE(@"+ datasource1_address_column +"@ ,\"orgcleansing\")"
        if (step.get("expression")== "int(HASHVALUE(str(@City - DS1@ )  ,\"PaxLevenshtein\",str(@City - DS2@ )))"):
            project_script['steps'][counter_main_project]['expression'] = "int(HASHVALUE(str(@"+ datasource1_city_column +"@)  ,\"PaxLevenshtein\",str(@"+ datasource2_city_column +"@)))"
        # This isn't a great approach setting variables (because they depend on the project script (which shouldn't change), but still, there is a better way to do it)
        name_company_name_matching = "Name Matching"
        name_address_part1_matching = "Address Matching"
        name_address_part2_matching = "Address Part2 Matching"

        if (step.get("expression") ==  "master_matching_expression"):
            project_script['steps'][counter_main_project]['expression'] = "((@" + str(name_company_name_matching) + "@ * " + str(weight_company_name) +") + (@"+ str(name_address_part1_matching) +"@  *"+ str(weight_address_part1) +") + (@"+ str(name_address_part2_matching) +"@ *"+ str(weight_address_part2) +"))  / ("+ str(weight_company_name) +"+ "+ str(weight_address_part1) +"+ "+ str(weight_address_part2) +")"
            '((@Name Matching@ * 2) + (@Address Matching@  *2) + (@Address Part2 Matching@ *2))  / (2+ 2+ 2)'
            #project_script['steps'][counter_main_project]['expression'] = "((@" + str(name_company_name_matching) + "@ * " + weight_company_name +") + (@"+ str(name_address_part1_matching) +"@  * "+ weight_address_part1 +") + (@"+ str(name_address_part2_matching) +"@ * "+ weight_address_part2 +"))  / ("+ weight_company_name +"+ "+ weight_address_part1 +"+ "+ weight_address_part2 + ")"

        counter_main_project+=1

    return(project_script)

def combine_two_scripts(main_project_json_script,template_project_script):
    i=0
    for schema_item in template_project_script['steps']:
        main_project_json_script['steps'].append(schema_item)

    return main_project_json_script

def update_project_with_filter(working_path, authorization_token, paxata_url, projectId, cut_off_threshold):
    
    project_script = get_new_project_script(authorization_token,paxata_url,projectId)
    
    counter_main_project=0
    for step in project_script[0]['steps']:
        try:
            if project_script[0]['steps'][counter_main_project]['facets'][0]['facetValues'][0]['value']['start']['value']:
                project_script[0]['steps'][counter_main_project]['facets'][0]['facetValues'][0]['value']['start']['value'] = str(cut_off_threshold)
        except:
            counter_main_project += 1
    update_project_with_new_script(working_path,authorization_token,paxata_url,project_script[0],projectId)

def main(paxata_url, datasource1_id_schema_list, datasource2_id_schema_list, column_weights):
    # *****************THESE ARE YO VARIABLES - YOU NEED TO EDIT THESE *******
    # These variables can be changed to whatever you need.
    # These three variables define where to look for the update file and where to move the processed file
    home_dir = os.path.expanduser('~')
    working_path = home_dir + "/Documents/Paxata/development/git_repo_personal/flask/marketing_solution"
    json_file_name = working_path + "/python_files/template_matching_project.json"
    #paxata_url = "http://localhost"
    paxata_restapi_token = "95042539cd3e430c83bf7000a5c9d6c9"
    matching_project_name = "Matching"
    matching_step_name = "Master Weighted Score"

    datasource1, datasource1_name_column, datasource1_address_column, datasource1_city_column = datasource1_id_schema_list
    datasource2, datasource2_name_column, datasource2_address_column, datasource2_city_column = datasource2_id_schema_list
    cut_off_threshold,weight_company_name,weight_address_part1,weight_address_part2 = column_weights

    # set the authorization based on the username and password provided in the user variables section
    authorization_token = HTTPBasicAuth("", paxata_restapi_token)

    # Get the library ID's from the two file's selected
    ds1_temp = datasource1.split("_")
    datasource1 = ds1_temp[0]
    datasource1_version = ds1_temp[1]
    datasource1_name = get_name_of_datasource(authorization_token, paxata_url, datasource1, datasource1_version)

    ds2_temp = datasource2.split("_")
    datasource2 = ds2_temp[0]
    datasource2_version = ds2_temp[1]
    datasource2_name = get_name_of_datasource(authorization_token, paxata_url, datasource2, datasource2_version)


    
    # will probably want these two calls once i make the project update versions
    # Get the ID from the project name
    # projectId = check_if_a_project_exists(authorization_token, paxata_url, matching_project_name)
    
    # Get the JSON script
    # project_script = get_new_project_script(authorization_token, paxata_url, projectId)



    #Create a new project to match the files 
    #Ideally it would be good to make the project_name dynamic
    matching_project_name = "Matching Project"
    matching_project_name = "Match Result - " + datasource1_name + "_and_" + datasource2_name

    #### THIS IS A TEMPORARY LINE (ONCE I START PERFORMING DYNAMIC NAMED PROJECTS)
    projectId = check_if_a_project_exists(authorization_token,paxata_url,matching_project_name)
    if (projectId):
        delete_a_project_if_it_exists(authorization_token,paxata_url,projectId)
    projectId = create_a_new_project(authorization_token,paxata_url,matching_project_name)
    json_of_new_project = get_new_project_script(authorization_token,paxata_url,projectId)
    main_project_json_script = insert_initial_data_into_empty_project(authorization_token,paxata_url,json_of_new_project,datasource1,datasource1_version)
    # The below call might not be necessary, but adding it to make sure all is well until this point.
    update_project_with_new_script(working_path, authorization_token, paxata_url, main_project_json_script, projectId)
    # Load the project steps from the template file
    template_project_script = load_project_script_json(json_file_name)
    # combine the two projects (the one with the data, and the template steps)
    main_project_json_script = combine_two_scripts(main_project_json_script,template_project_script)

    # this is the challenge now.... (change the column names in the JSON)
    main_project_json_script = update_column_names(authorization_token, paxata_url, main_project_json_script, datasource1_id_schema_list, datasource2_id_schema_list,column_weights)
    
    # don't need the below call now I have included it in the previous function    
    #updated_json_script = update_the_project_master_matching_step(main_project_json_script,matching_step_name,str(weight_company_name),str(weight_address_part1),str(weight_address_part2))
    
    # Finally, upload the script to Paxata project
    update_project_with_new_script(working_path, authorization_token, paxata_url, main_project_json_script, projectId)



    # Create the Answersets
    answerset_id = run_a_project(authorization_token, paxata_url, projectId)
    
    matching_only_answerset_id = update_project_with_filter(working_path, authorization_token, paxata_url, projectId, cut_off_threshold)
    
    #non_matching_only_answerset_id = update_project_with_filter(authorization_token, paxata_url, projectId, cut_off_threshold)


    # Lookup what the library item is called
    library_file_name = get_name_of_datasource(authorization_token, paxata_url, answerset_id,"1")
    #library_file_name = get_name_of_datasource(authorization_token, paxata_url, matching_only_answerset_id)






    ## I don't think i will need these, but have left them in case we want to use them.
    # Get the Answerset
    # TextData = get_paxata_library_data(authorization_token, paxata_url, answerset_id)
    # Delete the Library item just created
    # delete_library_item(authorization_token, paxata_url, answerset_id)
    url_for_matching_data = paxata_url + "#/export/" + answerset_id + ":1" 

    return (url_for_matching_data)

# run the main module
if __name__ == "__main__":
    main()

##########################################################################
### End of the program                                                ####
##########################################################################
