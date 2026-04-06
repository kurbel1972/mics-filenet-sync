"""
Script para pesquisar um documento específico no FileNet via API MuleSoft
e devolver informações do processo, nomeadamente o OBJECT_ID.

Uso:
    python search_filenet.py <nome_ficheiro>

Exemplo:
    python search_filenet.py LE555301278GB_01_2026031707053339_03.tif
"""

import sys
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Configuração via .env ou valores directos
MULESOFT_URL = os.getenv(
    "MULESOFT_SEARCH_URL",
    "https://ctt-prc-documents-ksbqtw.internal-6baq1j.irl-e1.eu1.cloudhub.io/api/v1/documents/search"
)
CLIENT_ID = os.getenv("MULESOFT_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("MULESOFT_CLIENT_SECRET", "")


def search_filenet(file_name: str) -> dict | None:
    """Pesquisa um documento no FileNet via API MuleSoft e devolve a resposta."""
    if not CLIENT_ID or not CLIENT_SECRET:
        print("[ERRO] MULESOFT_CLIENT_ID e MULESOFT_CLIENT_SECRET devem estar definidos no .env")
        return None

    headers = {
        "Content-Type": "application/json",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    payload = {"fileUrl": file_name}

    print(f"[INFO] A pesquisar no FileNet: {file_name}")
    print(f"[INFO] URL: {MULESOFT_URL}")

    response = requests.post(MULESOFT_URL, headers=headers, json=payload, timeout=60)

    if response.status_code != 200:
        print(f"[ERRO] Resposta HTTP {response.status_code}")
        print(f"[ERRO] Body: {response.text[:500]}")
        return None

    # Tentar interpretar como JSON
    try:
        data = response.json()
    except json.JSONDecodeError:
        print("[AVISO] Resposta não é JSON. A mostrar conteúdo raw (primeiros 1000 chars):")
        print(response.text[:1000])
        return None

    return data


def extract_info(data):
    """Extrai e imprime informações relevantes da resposta, incluindo OBJECT_ID."""
    if isinstance(data, list):
        if len(data) == 0:
            print("[INFO] Nenhum documento encontrado.")
            return
        for i, doc in enumerate(data):
            print(f"\n--- Documento {i + 1} ---")
            print_doc_info(doc)
    elif isinstance(data, dict):
        # Pode ser um objecto único ou ter uma chave com a lista de resultados
        # Tentar chaves comuns
        for key in ("documents", "results", "items", "entries", "data"):
            if key in data and isinstance(data[key], list):
                if len(data[key]) == 0:
                    print("[INFO] Nenhum documento encontrado.")
                    return
                for i, doc in enumerate(data[key]):
                    print(f"\n--- Documento {i + 1} ---")
                    print_doc_info(doc)
                return
        # Se não encontrou lista, tratar o dict como documento único
        print("\n--- Documento ---")
        print_doc_info(data)
    else:
        print("[INFO] Resposta inesperada:")
        print(data)


def print_doc_info(doc):
    """Imprime os campos de um documento, destacando OBJECT_ID."""
    if not isinstance(doc, dict):
        print(doc)
        return

    # Procurar variantes comuns de OBJECT_ID
    object_id_keys = [
        "OBJECT_ID", "objectId", "object_id", "ObjectId",
        "cmis:objectId", "Id", "id", "ID",
        "documentId", "DocumentId", "document_id",
    ]

    found_object_id = False
    for key in object_id_keys:
        if key in doc:
            print(f"  ** {key}: {doc[key]} **")
            found_object_id = True

    # Imprimir todos os campos
    for key, value in doc.items():
        if key not in object_id_keys:
            print(f"  {key}: {value}")

    if not found_object_id:
        print("  [AVISO] OBJECT_ID não encontrado nos campos do documento.")


def main():
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]
    else:
        file_name = input("Introduz o nome do ficheiro (ex: idd_509EFA9C-0000-CA13-A00E-7EB0420C09D2): ").strip()
        if not file_name:
            print("[ERRO] Nome do ficheiro não pode estar vazio.")
            sys.exit(1)
    data = search_filenet(file_name)

    if data is not None:
        print("\n========== RESULTADO DA PESQUISA ==========")
        extract_info(data)
        print("\n========== JSON COMPLETO ==========")
        print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
