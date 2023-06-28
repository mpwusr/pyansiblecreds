import hvac
import requests
import json


def get_vault_client(vault_url, vault_token):
    vault_client = hvac.Client(url=vault_url, token=vault_token)
    return vault_client


def get_app_role_secret_id(vault_client):
    app_role_secret_id = vault_client.secrets.approle.create_secret()['data']['secret_id']
    return app_role_secret_id


def vault_auth(awx_username, app_role_secret_id):
    headers = {'Content-Type': 'application/json'}
    data = {'name': awx_username, 'password': app_role_secret_id}
    auth_url = 'https://<awx_server>/api/v2/auth/token/'
    auth_response = requests.post(auth_url, headers=headers, data=json.dumps(data))
    auth_token = auth_response.json()['token']
    return auth_token


def vault_response(auth_token):
    headers = {'Content-Type': 'application/json', 'Authorization': f'Token{auth_token}'}
    response = requests.get('https://<awx_server>/api/v2/job-templates/', headers=headers)
    return response.json()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
