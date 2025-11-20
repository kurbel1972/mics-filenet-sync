import base64
import http.client

username = "FileNetDSPService"
password = "Vedu5wY)IgkB6nNvGoNR"
credentials = f"{username}:{password}"
encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

host = "svxrecordmp01.internal.ctt.pt"
port = 9081
resource_path = "/fncmis/resources/CTT_DSP_OBJ/query"

headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/cmisquery+xml"
}

file_name = "UV086773132DE_01_2025052616541988_01.tif"
payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<cmis:query xmlns:cmis="http://docs.oasis-open.org/ns/cmis/core/200908/">
    <cmis:statement>
        SELECT * FROM cmis:document WHERE cmis:objectTypeId = 'dcFotosObjetosEPA' AND DocumentTitle = '{file_name}'
    </cmis:statement>
    <cmis:searchAllVersions>false</cmis:searchAllVersions>
</cmis:query>
"""

print(f"Headers: {headers}")
print(f"Payload: {payload}")

try:
    print(f"Connecting to http://{host}:{port}{resource_path}")
    
    conn = http.client.HTTPConnection(host, port)
    conn.request("POST", resource_path, body=payload.encode("utf-8"), headers=headers)
    res = conn.getresponse()
    print(f"Status: {res.status} {res.reason}")
    data = res.read()
    print("Response body:")
    print(data.decode("utf-8"))
except Exception as e:
    print(f"Erro: {e}")