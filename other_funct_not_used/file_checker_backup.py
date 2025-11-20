import base64
import requests
import xml.etree.ElementTree as ET
from src.config.config import USERNAME, PASSWORD, FILENET_BASE_URL

def file_in_entries(root, file_name):
    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        for value in entry.findall('.//{http://docs.oasis-open.org/ns/cmis/core/200908/}value'):
            if value.text == file_name:
                return True
    return False

def get_next_link(root):
    next_link = root.find(".//{http://www.w3.org/2005/Atom}link[@rel='next']")
    if next_link is not None and 'href' in next_link.attrib:
        return next_link.attrib['href']
    return None

def file_exists_in_filenet(file_name):
    try:
        parts = file_name.split("_")
        if len(parts) < 3:
            return False

        year = parts[2][:4]
        month = parts[2][4:6]
        url = f"{FILENET_BASE_URL}/{year}/{month}"

        credentials = f"{USERNAME}:{PASSWORD}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        headers = {
            "Authorization": f"Basic {encoded_credentials}"
        }

        while url:
            print(f"[DEBUG] Checking FileNet URL: {url}")
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"[ERROR] Failed to access FileNet ({response.status_code}): {url}")
                return False

            root = ET.fromstring(response.content)
            if file_in_entries(root, file_name):
                return True

            url = get_next_link(root)

        return False

    except Exception as e:
        print(f"[ERROR] Exception in file_exists_in_filenet: {e}")
        return False