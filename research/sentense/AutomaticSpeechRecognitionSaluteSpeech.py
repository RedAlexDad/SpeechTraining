import requests
import uuid
import base64
import urllib3

# Отключение предупреждений о самоподписанных сертификатах
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from tokens import CLIENT_ID, CLIENT_SECRET


class AutomaticSpeechRecognitionSaluteSpeech:
    def __init__(self, client_id, client_secret, scope='SALUTE_SPEECH_PERS'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope  # Укажите ваш scope (SALUTE_SPEECH_PERS, SALUTE_SPEECH_CORP или SBER_SPEECH)
        self.access_token = self.get_access_token()

    def get_access_token(self):
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_header = base64.b64encode(auth_string.encode()).decode()

        headers = {
            "Authorization": f"Basic {auth_header}",
            "RqUID": str(uuid.uuid4()),
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "scope": self.scope
        }

        try:
            response = requests.post(url, headers=headers, data=data, verify=False)
            response.raise_for_status()
            token_info = response.json()
            return token_info["access_token"]
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса токена: {e}")
            return ""

    def recognize_speech_salute(self, audio_data):
        url = "https://smartspeech.sber.ru/rest/v1/speech:recognize"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "audio/ogg;codecs=opus"
        }
        params = {
            "language": "ru-RU",
            "sample_rate": 16000,
            "enable_profanity_filter": False,
            "channels_count": 1
        }

        try:
            response = requests.post(url, headers=headers, params=params, data=audio_data, verify=False)
            response.raise_for_status()
            # print('response:', response.json(), end='\n\n')
            # Соединяем тексты из массива в один текст
            combined_text = " ".join(response.json()['result'])
            print('[SALUTE SPEECH] Распознанный текст:', combined_text)
            return combined_text
        except requests.exceptions.RequestException as error:
            print(f"Ошибка запроса: {error}")
            return f"Ошибка: {str(error)}"

    def recognize_speech_audio_path(self, audio_file_path):
        url = "https://smartspeech.sber.ru/rest/v1/speech:recognize"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "audio/ogg;codecs=opus"
        }
        params = {
            "language": "ru-RU",
            "sample_rate": 16000,
            "enable_profanity_filter": False,
            "channels_count": 1
        }

        try:
            with open(audio_file_path, "rb") as audio_file:
                audio_data = audio_file.read()
                response = requests.post(url, headers=headers, params=params, data=audio_data, verify=False)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return None

# if __name__ == '__main__':
#     audio_file_path = "../voice/output.ogg"
#
#     ASR_SaluteSpeech = AutomaticSpeechRecognitionSaluteSpeech(CLIENT_ID, CLIENT_SECRET)
#
#     transcript = ASR_SaluteSpeech.recognize_speech_audio_path(audio_file_path)
#
#     if transcript:
#         print("Распознанный текст:", transcript)
#     else:
#         print("Не удалось распознать текст")
