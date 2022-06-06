# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
import requests
import json

# from flask import session


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f"Hi, {name}")  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
def add_user_to_keycloak(username_, firstname_, lastname_, email_, password_):
    accessTokenUrl = (
        "http://127.0.0.1:8080/auth/realms/shooting-app/protocol/openid-connect/token"
    )

    username = "admin"
    password = "password"
    payload = (
        "client_id=admin-cli&username="
        + username
        + "&password="
        + password
        + "&grant_type=password"
        + "&client_secret=hm3W9Nr2L4BPhtGmjItHWDaLteTVi8sF"
    )

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    print("Retrieving Access token from Keycloak")
    response = requests.request("POST", accessTokenUrl, headers=headers, data=payload)
    access_token = json.loads(response.text)["access_token"]

    print("Here is the access token" + access_token)

    # addUserUrl = "http://localhost:8080/auth/admin/realms/master/users"
    addUserUrl = "http://127.0.0.1:8080/auth/admin/realms/shooting-app/users"

    username = username_
    firstname = firstname_
    lastname = lastname_
    email = email_
    password = password_

    payload = (
        '{\r\n    "username":"'
        + username
        + '",\r\n    "firstName":"'
        + firstname
        + '",\r\n    "lastName":"'
        + lastname
        + '",\r\n    "enabled":true,\r\n    "emailVerified":true,\r\n    "email":"'
        + email
        + '",    "credentials":[ {\r\n      "type": "password",\r\n      "value": "'
        + password
        + '" \r\n    }]\r\n}'
    )

    headers = {
        "Authorization": "Bearer " + access_token + "",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", addUserUrl, headers=headers, data=payload)
    print(f"response is: {dir(response)}")
    print(f"response is: {response.reason}")
    print(f"response is: {response.json}")
    print(f"response is: {response.text}")
    print(f"response is: {response.request}")
    print(f"response is: {response.iter_content}")
    if response.status_code == 201:
        print("user added successfully")
    elif response.status_code == 409:
        print("already exist in the Keycloak")


def get_access_token(username_, password_):
    accessTokenUrl = (
        "http://127.0.0.1:8080/auth/realms/shooting-app/protocol/openid-connect/token"
    )

    username = username_
    password = password_
    payload = (
        "client_id=admin-cli&username="
        + username
        + "&password="
        + password
        + "&grant_type=password"
    )

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    print("Retrieving Access token from Keycloak")
    response = requests.request("POST", accessTokenUrl, headers=headers, data=payload)
    access_token = json.loads(response.text)["access_token"]
    print(access_token)
    return access_token


def check_user_id(username_):
    admin_token = get_access_token("admin", "password")
    print(f"Admin token = {admin_token}")
    url = (
        "http://127.0.0.1:8080/auth/admin/realms/shooting-app/users?username="
        + username_
    )
    headers = {
        "Authorization": "Bearer " + admin_token + "",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers)
    response_json = response.json()
    user_id = response_json[0]["id"]

    print(f"USer ID: {user_id}")
    return user_id


def check_role(username_):
    admin_token = get_access_token("admin", "password")
    print(f"admin token = {admin_token}")
    user_id = check_user_id(username_)

    check_url = (
        "http://127.0.0.1:8080/auth/admin/realms/shooting-app/users/"
        + user_id
        + "/role-mappings/realm"
    )

    headers = {
        "Authorization": "Bearer " + admin_token + "",
        "Content-Type": "application/json",
    }

    response = requests.request("GET", check_url, headers=headers)
    response_json = response.json()

    # print(response_json['id'])
    roles = []
    for role in response_json:
        roles.append(role["name"])

    print(f"Roles: {roles}")

    return roles


if __name__ == "__main__":
    print_hi("PyCharm")
    add_user_to_keycloak(username_='pppa@aa.pl', firstname_='ppxxaaaa@aa.pl', lastname_='ppaxxaaa@aa.pl',
                         email_='ppxxaaaa@aa.pl', password_='aaxssaa@aa.pl')
    # check_user_id('qapl@op.pl')
    # check_role("qapl@op.pl")
