import http.client
import base64
import time

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

file_name = "AN103896346GB_01_2025050510150973_01.tif"
payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<cmis:query xmlns:cmis="http://docs.oasis-open.org/ns/cmis/core/200908/">
    <cmis:statement>
        SELECT * FROM cmis:document WHERE cmis:objectTypeId = 'dcFotosObjetosEPA' AND DocumentTitle = '{file_name}'
    </cmis:statement>
    <cmis:searchAllVersions>false</cmis:searchAllVersions>
</cmis:query>
"""

print(f"Headers: {headers}")

try:
    print(f"Connecting to http://{host}:{port}{resource_path}")
    t0 = time.time()
    conn = http.client.HTTPConnection(host, port, timeout=30)
    t1 = time.time()
    print(f"Tempo a criar conexão: {t1-t0:.3f} segundos")

    conn.request("POST", resource_path, body=payload.encode("utf-8"), headers=headers)
    t2 = time.time()
    print(f"Tempo a enviar request: {t2-t1:.3f} segundos")

    res = conn.getresponse()
    t3 = time.time()
    print(f"Tempo a obter resposta: {t3-t2:.3f} segundos")

    data = res.read()
    t4 = time.time()
    print(f"Tempo a ler resposta: {t4-t3:.3f} segundos")

    print(f"Status: {res.status} {res.reason}")
    print("Response body:")
    print(data.decode("utf-8"))
    print(f"Tempo total: {t4-t0:.3f} segundos")
except Exception as e:
    print(f"Erro: {e}")