import time
from bs4 import BeautifulSoup
import requests
import hashlib
import re



payload_2 = {
    "Username": "admin",
    "Password": "7a0efd0c9930d0ebdffbbc67f4f54dbe118e28c4f51f234dcd59af48d1d5b2ac",
    "action": "login",
    "_sessionTOKEN": "250159094715731874732429"
}


def get_token_from_xml(session):
    url = "http://192.168.1.1/function_module/login_module/login_page/logintoken_lua.lua"  # Token URL'si
    response = session.get(url)

    if response.status_code == 200:
        # Yanıt içeriğini al
        xml_content = response.text
        
        # <ajax_response_xml_root>...</ajax_response_xml_root> içeriğini çıkar
        token_pattern = r"<ajax_response_xml_root>(\d+)</ajax_response_xml_root>"
        match = re.search(token_pattern, xml_content)
        
        if match:
            token = match.group(1)
            print("Token alındı:", token)
            return token
        else:
            print("Token bulunamadı!")
            return None
    else:
        print("Token alınamadı! Hata kodu:", response.status_code)
        return None
    
def get_site(url):
    return requests.get(url)

def get_session_token(response):
    if response.status_code == 200:
        # Sayfa içeriğini al
        html_content = response.text
        
        # "_sessionTOKEN", "değer" formatında arama
        token_pattern = r'"_sessionTOKEN",\s*"(\d+)"'
        match = re.search(token_pattern, html_content)
        
        if match:
            session_token = match.group(1)
            print("Session Token alındı:", session_token)
            return session_token
        else:
            print("Session Token bulunamadı!")
            return None
    else:
        print("Session Token alınamadı! Hata kodu:", response.status_code)
        return None

def calculate_password(password, token):
    combined = password + token  # Şifre ve token birleştiriliyor
    sha256_hash = hashlib.sha256(combined.encode()).hexdigest()  # SHA256 hash hesaplama
    return sha256_hash


session = requests.session()
login_url = "http://192.168.1.1/"
response = session.get(login_url)

_sessionToken = get_session_token(response)

login_payload = {
   "Username": "admin",
    "Password": calculate_password("INTERFACE_PASSWORD",get_token_from_xml(session)),
    "action": "login",
    "_sessionTOKEN": _sessionToken
}

login_response = session.post("http://192.168.1.1/", data=login_payload)

if login_response.status_code == 200:
    print("Login başarılı!")
    with open("abc.html", "w", encoding="utf-8") as file:
        file.write(login_response.text)
else:
    print("Login başarısız! Hata kodu:", login_response.status_code)
    print("Hata mesajı:", login_response.text)
    
def extract_session_token(response):
    if response.status_code == 200:
        html_content = response.text
        token_pattern = r'_sessionTmpToken = "([^"]+)"'
        match = re.search(token_pattern, html_content)
        
        if match:
            token = match.group(1)
            token = bytes(token, "utf-8").decode("unicode_escape")
            print("Extracted session token:", token)
            return token
        else:
            print("Session token not found!")
            return None
    else:
        print("Failed to extract session token! Status code:", response.status_code)
        return None
    
tmpToken = extract_session_token(login_response)

print("tmp:",tmpToken)


# http://192.168.1.1/getpage.lua?pid=123&nextpage=ManagDiag_DeviceManag_t.lp&Menu3Location=0&_=1735754423590 
# bu linkteki $('#template_RestartManag')'i 
# template = $('#template_RestartManag')
# ÇALIŞTI: dataPost("Restart", "fillDataByRestartResult", "/common_page/deviceManag_lua.lua", template, undefined, false);
# buraya yolla



session.get("http://192.168.1.1/getpage.lua?pid=123&nextpage=ManagDiag_StatusManag_t.lp&Menu3Location=0")


resp = session.get("http://192.168.1.1/getpage.lua?pid=123&nextpage=ManagDiag_DeviceManag_t.lp&Menu3Location=0")


if resp.status_code == 200:
    with open("zeze.html", "w", encoding="utf-8") as file:
        file.write(resp.text)
else:
    print("Failed to retrieve the page! Status code:", resp.status_code)
    print("Error message:", resp.text)



# # Extract the template from the response
# soup = BeautifulSoup(resp.text, 'html.parser')
# template = soup.select_one('#template_RestartManag')

# if template:
#     print("Template found:", template)
# else:
#     print("Template not found!")




tmpToken = extract_session_token(resp)

print("tmp2:",tmpToken)



# template = $('#template_RestartManag')
# ÇALIŞTI: dataPost("Restart", "fillDataByRestartResult", "/common_page/deviceManag_lua.lua", template, undefined, false);

# URL (Server Address)
params = {
    "IF_ACTION": "Restart",
    "Btn_restart": "",
    "_sessionTOKEN": tmpToken
}
url = "http://192.168.1.1/common_page/deviceManag_lua.lua"
params_str = "&".join([f"{key}={value}" for key, value in params.items()])
hashed = hashlib.sha256(params_str.encode())

# 5b375bdf08e10f6e7d5682d2530104213fc87e88232a5fe10b22c2a8494166d2
print(hashed.hexdigest())
headers = {
    "Check": hashed.hexdigest()
}

response = session.post(url, data=params, headers=headers)

if response.status_code == 200:
    print("Restart request successful!")
    print(response.text)
else:
    print("Restart request failed! Status code:", response.status_code)
    print("Error message:", response.text)




