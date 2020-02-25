import pytest
import requests
import json
import jsonpath

def test_create_user(supply_url,create_user_json):
	#API url
	url  = supply_url+"/users"
	#Read Input Json file
	file = open(create_user_json)
	json_input = file.read()
	request_json = json.loads(json_input)
	#Make post request
	response = requests.post(url,request_json)
	#Validating Responce Code
	assert response.status_code == 201,"user Created"

	result = json.loads(response.text)
	id = jsonpath.jsonpath(result,'id')
	print("userid => ",id[0])

@pytest.mark.parametrize("userid, firstname",[(1,"George")])
def test_list_valid_user(supply_url,userid,firstname):
	#API url
	url = supply_url + "/users/" + str(userid)
	#Make get request to fetch user
	resp = requests.get(url)
	result = json.loads(resp.text)
	#Validating Responce Code
	assert resp.status_code == 200, resp.text
	#Validating existing userid 
	assert result['data']['id'] == userid, resp.text
	#Validating existing username
	assert result['data']['first_name'] == firstname, resp.text

def test_register_no_password(supply_url):
	#API url
	url = supply_url + "/register/"
	#Pass only email id
	data = {'email':'jira.merahkee@gmail.com'}
	#Make post request
	response = requests.post(url,data)
	result = json.loads(response.content)
	#Validating Responce Code
	assert response.status_code == 400,response.text
	#what went wrong
	assert result['error'] == 'Missing password',response.text

#remove user using userid
@pytest.mark.parametrize("userid",[1])
def test_delete_user(supply_url,userid):
	#API url
	url = supply_url+"/users/"+str(userid)
	response = requests.delete(url)
	#Validating Responce Code
	assert response.status_code == 204,response.content
	#Validating successful deletion
	assert response.text == '',"Successfully, user deleted"

@pytest.mark.parametrize("userid",[19])
def test_user_not_exist(supply_url,userid):
	#API url
	url = supply_url +"/unknown/"+str(userid)
	response = requests.get(url)
	#Validating Responce Code
	assert response.status_code == 404,response.text
	#Validating return response
	assert response.text == '{}',"User not found"

#validating existing users information
@pytest.mark.parametrize("userid,username,dofb",[(19,"Sumana",2000),(1,"George",1987),(2,"fuchsia rose",2001)])
def test_get_user_info(supply_url,userid,username,dofb):
	#API url
	url = supply_url +"/unknown/"+str(userid)
	#Make get request to fetch user
	response = requests.get(url)

	#User not found
	if response.status_code == 404:
		#Validating Responce Code
		assert response.text == '',response.content
	#Existing user	
	if response.status_code == 200:
		#Json info of user
		result = json.loads(response.content)
		#Validating username
		assert result['data']['name'] == username,response.content
		#Validating user date of birth
		assert result['data']['year'] == dofb,response.content