import requests
import uuid
import base64
from datetime import datetime

import urllib3
# Отключение предупреждений о самоподписанных сертификатах
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_access_token(client_id, client_secret, scope):
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    auth_string = f"{client_id}:{client_secret}"
    auth_header = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "RqUID": str(uuid.uuid4()),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "scope": scope
    }

    try:
        response = requests.post(url, headers=headers, data=data, verify=False)
        response.raise_for_status()
        token_info = response.json()
        return token_info["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса токена: {e}")
        return None


def recognize_speech(audio_path, access_token):
    url = "https://smartspeech.sber.ru/rest/v1/speech:recognize"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "audio/ogg;codecs=opus"
    }
    params = {
        "language": "ru-RU",
        "sample_rate": 16000,
        "enable_profanity_filter": False,
        "channels_count": 1
    }

    try:
        with open(audio_path, "rb") as audio_file:
            audio_data = audio_file.read()
            response = requests.post(url, headers=headers, params=params, data=audio_data, verify=False)
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None


if __name__ == '__main__':
    client_id = "8259c3ae-f7e2-42a1-8e9f-74fe65ad071d"  # Укажите ваш Client ID
    client_secret = "0817aa25-bbd8-4448-940b-c8bf7422e8e0"  # Укажите ваш Client Secret
    scope = "SALUTE_SPEECH_PERS"  # Укажите ваш scope (SALUTE_SPEECH_PERS, SALUTE_SPEECH_CORP или SBER_SPEECH)

    access_token = get_access_token(client_id, client_secret, scope)

    if access_token:
        audio_file_path = '../voice/test.ogg'  # Укажите путь к вашему аудиофайлу
        transcript = recognize_speech(audio_file_path, access_token)
        if transcript:
            print("Распознанный текст:", transcript)
        else:
            print("Не удалось распознать текст")
    else:
        print("Не удалось получить токен доступа")
