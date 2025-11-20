import base64
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote
import os
from src.config.config import USERNAME_FILENET, PASSWORD_FILENET, FILENET_URL_OBJ_STORE
import logging

class FileNetChecker:
    def __init__(self, username_filenet=USERNAME_FILENET, password_filenet=PASSWORD_FILENET, url=FILENET_URL_OBJ_STORE):
        self.username_filenet = username_filenet
        self.password_filenet = password_filenet
        if not self.username_filenet or not self.password_filenet:            
            self.username_filenet = os.getenv("USERNAME_FILENET")
            self.password_filenet = os.getenv("PASSWORD_FILENET")
        self.url = url

    def get_folder_id(self, year, month, headers):
        path = f"/Operações/Aceitação-Atendimento/Alfandega/Fotos Objetos EPA/{year}/{month}"
        encoded_path = quote(path, safe="/")
        url = f"{self.url}Content?path={encoded_path}&filter="
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code != 200:
            logging.error(f"Failed to get folder info ({response.status_code}): {url}")
            return None
        else:
            print(f"[DEBUG] Successfully retrieved folder info for {encoded_path}")
            logging.info(f"Successfully retrieved folder info for {encoded_path}")
        root = ET.fromstring(response.content)
        ns = {"cmis": "http://docs.oasis-open.org/ns/cmis/core/200908/"}
        for prop in root.findall(".//cmis:propertyId", ns):
            if prop.attrib.get("propertyDefinitionId") == "cmis:objectId":
                value_elem = prop.find("cmis:value", ns)
                if value_elem is not None:
                    # print(f"[DEBUG] Found folder ID: {value_elem.text}")
                    return value_elem.text
        print("[ERROR] Folder ID not found in response.")
        logging.error("Folder ID not found in response.")
        return None

    def file_exists_in_filenet(self, file_name):
        try:
            parts = file_name.split("_")
            if len(parts) < 3:
                return False

            year = parts[2][:4]
            month = parts[2][4:6]

            # Basic Auth
            credentials = f"{self.username_filenet}:{self.password_filenet}"
            encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
            headers_basic = {"Authorization": f"Basic {encoded_credentials}"}
            folder_id = self.get_folder_id(year, month, headers_basic)
            print(f"[DEBUG] Folder ID for {year}/{month}: {folder_id}")

            if folder_id:
                query = (
                    f"Query?q=SELECT%20*%20FROM%20cmis:document%20where%20in_folder('{folder_id}')"
                    f"%20AND%20cmis:name='{file_name}'&maxItems=1"
                )
                # print(f"[DEBUG] Constructed query: {query}")
                url = f"{self.url}{query}"
                # print(f"[DEBUG] Checking FileNet URL: {url}")
                response = requests.get(url, headers=headers_basic, verify=False)
                if response.status_code == 200:
                    if file_name in response.text:
                        return True
                else:
                    print(f"[ERROR] Basic Auth query failed ({response.status_code}): {url}")
                    logging.error(f"Basic Auth query failed ({response.status_code}): {url}")

            return False

        except Exception as e:
            print(f"[ERROR] Exception in file_exists_in_filenet: {e}")
            logging.error(f"Exception in file_exists_in_filenet: {e}")
            return False