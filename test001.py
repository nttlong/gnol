import requests
url_token_request="https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=24584627-4f3d-40f8-a606-619b0e007fc6&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%2Fmyapp%2F&response_mode=query&scope=offline_access%20user.read%20mail.read&state=12345"

r = requests.post(url_token_request)
print(r.status_code, r.reason)