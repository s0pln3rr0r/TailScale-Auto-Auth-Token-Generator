import requests
import pandas as pd
import os,openpyxl

def api_check(API_KEY, organization_name):
    url = f"https://api.tailscale.com/api/v2/tailnet/{organization_name}/devices"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        if response.status_code==401:
            print("Invalid API Token and credentials")
        else:
            print("Some problem occured")
        print("Exiting tool")
        exit()
    print("API Token verified.")

def acl_get(API_Key, organization_name):
    url = f"https://api.tailscale.com/api/v2/tailnet/{organization_name}/acl"
    headers = {"Authorization": f"Bearer {API_Key}"}
    response = requests.get(url, headers=headers)
    return response.text

def acl_create(API_Key, organization_name):
    tags = {
        "tag:Network-Admin": [f"{organization_name}"],
        "tag:platform": [f"{organization_name}"],
    }
    for num in range(total_team_num):
        tags[f"tag:team-{num+1}"] = [f"{organization_name}"]
    for num in range(total_machines_num):
        tags[f"tag:machine-{num+1}"] = [f"{organization_name}"]

    acls_list = [{
        "action": "accept",
        "src": ["tag:Network-Admin"],
        "dst": ["*:*"],
    }]
    for num in range(total_team_num):
        temp_dict = {
            "action": "accept",
            "src": [f"tag:team-{num+1}"],
            "dst": [f"tag:team-{num+1}:*", "tag:platform:80"]
        }
        acls_list.append(temp_dict)

    Acl_policies = {
        "tagOwners": tags,
        "acls": acls_list,
    }

    previous_acl=acl_get(API_Key,organization_name)

    url = f"https://api.tailscale.com/api/v2/tailnet/{organization_name}/acl"
    headers = {"Authorization": f"Bearer {API_Key}"}

    response = requests.post(url, json=Acl_policies, headers=headers)
    if response.status_code == 200:
        print("ACL Policies replaced. Backup of older ACL list is saved in ACL_Backup.txt in current directory.")
        with open("backup_file.txt", "w") as file:
            file.write(previous_acl)

        print(f"Backup of previous ACL saved to {os.path.abspath("backup_file.txt")}")
    else:
        print("Some error occurred while updating ACL Policies")

def create_auth_tokens(API_Key, organization_name, tags):
    url = f"https://api.tailscale.com/api/v2/tailnet/{organization_name}/keys"
    querystring = {"all": True}
    payload = {
    "capabilities": { "devices": { "create": {
                "reusable": False,
                "ephemeral": False,
                "preauthorized": True,
                "tags": tags
            } } },
    "expirySeconds": 86400,
    "description": ""
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_Key}"
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)

    return response


def create_csv(API,oraganization_name):
    print("Generating Auth Tokens")
    participants_data=[]
    for tnum in range(total_team_num):
        for pnum in range(total_player_num):
            auth_token=create_auth_tokens(API_Key, organization_name, [f"tag:team-{tnum+1}"])
            auth_token = auth_token.json()
            auth_token_id=auth_token["id"]
            auth_token_key=auth_token["key"]
            install_command = f"sudo curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale up --authkey {auth_token_key}"
            temp_dict={"Team Name":f"team-{tnum+1}", "Member Name": f"Member {pnum+1}", "Auth Token id": auth_token_id, "Auth key": auth_token_key, "Installation Command": install_command}
            participants_data.append(temp_dict)
    print("Auth tokens for Participants are generated")
    machines_data=[]
    for tnum in range(total_team_num):
        for mnum in range(total_machines_num):
            auth_token=create_auth_tokens(API_Key, organization_name, [f"tag:team-{tnum+1}", f"tag:machine-{mnum+1}"])
            auth_token = auth_token.json()
            auth_token_id=auth_token["id"]
            auth_token_key=auth_token["key"]
            install_command = f"sudo curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale up --authkey {auth_token_key}"
            temp_dict={"Team Name":f"team-{tnum+1}", "Machine Name": f"machine-{mnum+1}", "Auth Token id": auth_token_id, "Auth key": auth_token_key, "Installation Command": install_command}
            machines_data.append(temp_dict)
    print("Auth tokens for Machines are generated")
    others_data=[]
    auth_token=create_auth_tokens(API_Key, organization_name, [f"tag:Network-Admin"])
    auth_token = auth_token.json()
    auth_token_id=auth_token["id"]
    auth_token_key=auth_token["key"]
    install_command = f"sudo curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale up --authkey {auth_token_key}"
    temp_dict={"Name":"Network Admin", "Auth Token ID": auth_token_id, "Auth key": auth_token_key, "Installation Command": install_command}
    others_data.append(temp_dict)
    print("Auth tokens for Network-Admin is generated")

    auth_token=create_auth_tokens(API_Key, organization_name, [f"tag:platform"])
    auth_token = auth_token.json()
    auth_token_id=auth_token["id"]
    auth_token_key=auth_token["key"]
    install_command = f"sudo curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale up --authkey {auth_token_key}"
    temp_dict={"Name":"Platform", "Auth Token ID": auth_token_id, "Auth key": auth_token_key, "Installation Command": install_command}
    others_data.append(temp_dict)
    print("Auth tokens for CTF-Platform is generated")

    participants_df = pd.DataFrame(participants_data)
    machines_df = pd.DataFrame(machines_data)
    others_df = pd.DataFrame(others_data)
    try:
        with pd.ExcelWriter("Auth_Keys.xlsx", engine="openpyxl") as writer:
            participants_df.to_excel(writer, sheet_name="Participants", index=False)
            machines_df.to_excel(writer, sheet_name="Machines", index=False)
            others_df.to_excel(writer, sheet_name="Others", index=False)
        
        print("Excel file created with 3 sheets containing tokens and commands for each user/machine/role.")
    except Exception as e:
        print(f"Failed to write to Excel: {e}")
        exit()
organization_name=input("Enter your Organization name (can be found at https://login.tailscale.com/admin/settings/general menu): ")
API_Key=input("Enter your API Access token (can be created at https://login.tailscale.com/admin/settings/keys): ")

total_team_num= int(input("Total number of teams invited in your CTF: "))
total_player_num= int(input("Total number of players per team: "))
total_machines_num=int(input("Total Vulnerable machines per team: "))
print()

api_check(API_Key, organization_name)
#acl_get(API_Key, organization_name)
acl_create(API_Key,organization_name)
create_csv(API_Key, organization_name)
