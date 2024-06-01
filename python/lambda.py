import json
import requests
import sys

passwd = "Secret@123"

def get_internalusers(url,username,password):
    print("Diaplay internal users present in the domain")
    header = {
        "Authorization": "Basic",
    }
    user_list = requests.get(url+"/_plugins/_security/api/internalusers/",auth=(username,password),headers=header)
    users = (user_list.json()).keys()
    for user in users:
        return user

def create_roles(url,username,password,role):
    print("Creating new role: {}".format(role))
    payload = {
	"description": "Provide access to the user",
	"cluster_permissions": ["cluster_composite_ops"],
	"index_permissions": [{
			"index_patterns": [".opensearch_dashboards", ".opensearch_dashboards-6", ".opensearch_dashboards_*"],
			"fls": [],
			"masked_fields": [],
			"allowed_actions": ["read", "delete", "manage", "index"]
		},
		{
			"index_patterns": [".tasks", ".management-beats"],
			"fls": [],
			"masked_fields": [],
			"allowed_actions": ["indices_all"]
		}
	],
	"tenant_permissions": [{
		"tenant_patterns": ["global_tenant"],
		"allowed_actions": ["kibana_all_write"]
	}]
    }
    header = {
        "Authorization": "Basic",
        "Content-Type": "application/json"
    }
    role_create = requests.put(url+"/_plugins/_security/api/roles/"+role,auth=(username,password),data=json.dumps(payload),headers=header)
    if role_create.status_code == 201:
        return {
            "status": "success",
            "response": role_create.status_code,
            "message": role_create.json(),
            "status": "Role has been created successfully"
        }
    elif role_create.status_code == 200:
        return {
            "status": "success",
            "response": role_create.status_code,
            "message": role_create.json(),
            "status": "Role has been modified successfully"
        }
    else:
        return {
            "status": "failure",
            "response": role_create.status_code,
            "message": role_create.json(),
            "status": "role creation failed"
        }

def create_user(url,username,password,user):
    print("Creating user {}".format(user))
    user_payload = {
        "password": passwd,
        "opendistro_security_roles": ["readall_and_monitor", "opensearch_dashboards_read_only"],
        "backend_roles": [],
        "attributes": {
            "aexp-app-carid": "600001519",
            "aexp-app-env": "eng",
            "aexp-app-name": "Opensearch App"
        }
    }
    header = {
        "Authorization": "Basic",
        "Content-Type": "application/json"
    }
    user_creation = requests.put(url+"/_plugins/_security/api/user/"+user,auth=(username,password),data=json.dumps(user_payload),headers=header)
    if user_creation.status_code == 201:
        return {
            "status": "success",
            "response": user_creation.status_code,
            "message": user_creation.json(),
            "status": "User has been created successfully"
        }
    elif user_creation.status_code == 200:
        return {
            "status": "success",
            "response": user_creation.status_code,
            "message": user_creation.json(),
            "status": "User has been modified successfully"
        }
    else:
        return {
            "status": "failure",
            "response": user_creation.status_code,
            "message": user_creation.json(),
            "status": "User creation failed"
        }

def get_userslist(url,username,password,role):
    print("Geting users inside the role {}".format(role))
    header = {
        "Authorization": "Basic",
        "Content-Type": "application/json"
    }
    users_list = []
    users_in_role = requests.get(url+"/_plugins/_security/api/rolesmapping/"+role,auth=(username,password),headers=header)

    return users_in_role.json()


def map_users(url,username,password,user,role):
    print("Mapping user {} to role {}".format(user,role))
    #users =[].append(user)
    #print(users)
    #users_listuser)
    rolemap_payload = {
        "users": [user],
        "backend_roles": [],
        "hosts": []
    }
    header = {
        "Authorization": "Basic",
        "Content-Type": "application/json"
    }
    user_mapping = requests.put(url+"/_plugins/_security/api/rolesmapping/"+role,auth=(username,password),data=json.dumps(rolemap_payload),headers=header)
    if user_mapping.status_code == 201:
        return {
            "status": "success",
            "response": user_mapping.status_code,
            "mapped_user": user,
            "mapped_to_role": role,
            "message": "User successfully mapped to role"
        }
    elif user_mapping.status_code == 200:
        return {
            "status": "success",
            "response": user_mapping.status_code,
            "mapped_user": user,
            "mapped_to_role": role,
            "message": "Role has been modified"
        }
    else:
        return {
            "status": "failure",
            "response": user_mapping.status_code,
            "response": user_mapping.json(),
            "message": "User not mapped to role"
        }
    
if __name__ =="__main__":
    url="https://search-domain1-jra4uodezy2er3gfujfnt5csxi.us-east-1.es.amazonaws.com"
    username = "admin"
    password = "Password@123"
    user = "xpaas_user"
    role = "xpaas_role"
    internalusers = get_internalusers(url,username,password)
    print (internalusers)
    createroles=create_roles(url,username,password,role)
    print(createroles)
    usercreate = create_user(url,username,password,user)
    print(usercreate)
    user_list=get_userslist(url,username,password,role)
    print(user_list)
    useradd = map_users(url,username,password,user,role)
    print(useradd)