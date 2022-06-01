import requests
import json

from .constants import KeycloakConfig


def add_user_to_keycloak(username_, firstname_, lastname_, email_, password_):

    access_token = get_access_token(KeycloakConfig.ADMIN_USERNAME, KeycloakConfig.ADMIN_PASSWORD)


    addUserUrl = "http://auth-service:8080/auth/admin/realms/shooting-app/users"

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
    try:
        response = requests.request("POST", addUserUrl, headers=headers, data=payload)

        if response.status_code == 201:
            print("user added successfully")
        elif response.status_code == 409:
            print("already exist in the Keycloak")

    except requests.exceptions.ConnectionError:
        print("Problem z połączeniem z bazą danych")

    except requests.exceptions.Timeout:
        print("Zbyt długi czas oczekiwania")


def get_access_token(username_, password_):
    accessTokenUrl = "http://auth-service:8080/auth/realms/shooting-app/protocol/openid-connect/token"

    username = username_
    password = password_
    client_secret = KeycloakConfig.CLIENT_SECRET
    payload = (
        f"client_id={KeycloakConfig.ADMIN_ID}&username="
        + username
        + "&password="
        + password
        + "&grant_type=password"
        + "&client_secret="
        + client_secret
    )

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    print("Retrieving Access token from Keycloak")
    try:
        response = requests.request("POST", accessTokenUrl, headers=headers, data=payload)
        access_token = json.loads(response.text)["access_token"]
        return access_token

    except requests.exceptions.ConnectionError:
        print("Problem z połączeniem z bazą danych")

    except requests.exceptions.Timeout:
        print("Zbyt długi czas oczekiwania")


def check_user_id(username_):
    admin_token = get_access_token(KeycloakConfig.ADMIN_USERNAME, KeycloakConfig.ADMIN_PASSWORD)
    url = (
        "http://auth-service:8080/auth/admin/realms/shooting-app/users?username="
        + username_
    )
    headers = {
        "Authorization": "Bearer " + admin_token + "",
        "Content-Type": "application/json",
    }
    try:
        response = requests.request("GET", url, headers=headers)
        response_json = response.json()
        user_id = response_json[0]["id"]

        return user_id

    except requests.exceptions.ConnectionError:
        print("Problem z połączeniem z bazą danych")

    except requests.exceptions.Timeout:
        print("Zbyt długi czas oczekiwania")


def check_role(username_):
    admin_token = get_access_token(KeycloakConfig.ADMIN_USERNAME, KeycloakConfig.ADMIN_PASSWORD)
    user_id = check_user_id(username_)

    check_url = (
        "http://auth-service:8080/auth/admin/realms/shooting-app/users/"
        + user_id
        + "/role-mappings/realm"
    )

    headers = {
        "Authorization": "Bearer " + admin_token + "",
        "Content-Type": "application/json",
    }

    try:
        response = requests.request("GET", check_url, headers=headers)
        response_json = response.json()

        roles = []
        for role in response_json:
            roles.append(role["name"])
        return roles

    except requests.exceptions.ConnectionError:
        print("Problem z połączeniem z bazą danych")

    except requests.exceptions.Timeout:
        print("Zbyt długi czas oczekiwania")