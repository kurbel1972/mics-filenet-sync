import http.client
import base64

# Dados de autenticação
username = "FileNetDSPService"
password = "Vedu5wY)IgkB6nNvGoNR"

# Codifica as credenciais em base64
credentials = f"{username}:{password}"
encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
print(f"Encoded credentials: {encoded_credentials}")

# Host e porta
host = "svxrecordmp01.internal.ctt.pt"
port = 9081

# Caminho do recurso (codificado como no Postman)
resource_path = "/fncmis/resources/CTT_DSP_OBJ/query"

#"/fncmis/resources/CTT_DSP_OBJ/ContentFlat/Opera%C3%A7%C3%B5es/Aceita%C3%A7%C3%A3o-Atendimento/Alfandega/Fotos%20Objetos%20EPA/2025/05"

headers = {
    "Authorization": f"Basic {encoded_credentials}"
}

print(f"Headers: {headers}")

try:
    print(f"Connecting to http://{host}:{port}{resource_path}")
    conn = http.client.HTTPConnection(host, port)  # <-- Troque para HTTPConnection
    conn.request("GET", resource_path, headers=headers)
    res = conn.getresponse()
    print(f"Status: {res.status} {res.reason}")
    data = res.read()
    print("Response body:")
    print(data.decode("utf-8"))
except Exception as e:
    print(f"Erro: {e}")