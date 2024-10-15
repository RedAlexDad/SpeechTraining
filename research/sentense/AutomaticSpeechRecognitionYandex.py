import urllib.request
import json
import io
import requests

class AutomaticSpeechRecognitionYandex:
    def __init__(self, folder_id, oauth_token):
        self.folder_id = folder_id
        self.oauth_token = oauth_token
        self.iam_token = self.get_iam_token()

    def get_iam_token(self):
        url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "yandexPassportOauthToken": self.oauth_token
        })

        try:
            response = requests.post(url, headers=headers, data=data)
            response_data = response.json()

            if "iamToken" in response_data:
                return response_data["iamToken"]
            else:
                raise Exception(
                    f"Ошибка при получении IAM-токена: {response_data.get('message', 'Неизвестная ошибка')}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка запроса: {str(e)}")

    def recognize_speech_audio_data(self, audio_data, lang='ru-RU', topic='general', print_result=True):
        params = "&".join([
            "topic=%s" % topic,
            "folderId=%s" % self.folder_id,
            "lang=%s" % lang
        ])

        # Проверка формата аудиоданных
        if not audio_data or len(audio_data) == 0:
            print("Ошибка: Аудиоданные пустые или некорректные.")
            return "Ошибка: Аудиоданные пустые."

        url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=audio_data)
        url.add_header("Authorization", "Bearer %s" % self.iam_token)
        url.add_header("Content-Type", "audio/ogg")
                
        print(f"Отправка аудиоданных длиной: {len(audio_data)} байт с параметрами: {params}")  # Отладочная информация

        try:
            responseData = urllib.request.urlopen(url).read().decode('UTF-8')
            decodedData = json.loads(responseData)

            if decodedData.get("error_code") is None:
                if print_result: print('[SPEECH KIT] Распознанный текст:', decodedData.get('result'))
                return decodedData.get("result")
            else:
                # print(f"Ошибка Yandex: {decodedData.get('error_code')} - {decodedData.get('error_message')}")
                return f"Ошибка: {decodedData.get('error_code')} - {decodedData.get('error_message')}"
        except urllib.error.HTTPError as error:
            return f"HTTP Error: {error.code} - {error.reason}"
        except Exception as error:
            return f"Ошибка: {str(error)}"


    def recognize_speech_audio_path(self, audio_file_path, lang='ru-RU', topic='general'):
        with open(audio_file_path, "rb") as f:
            data = f.read()

        params = "&".join([
            "topic=%s" % topic,
            "folderId=%s" % self.folder_id,
            "lang=%s" % lang
        ])

        url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data)
        url.add_header("Authorization", "Bearer %s" % self.iam_token)

        try:
            responseData = urllib.request.urlopen(url).read().decode('UTF-8')
            decodedData = json.loads(responseData)

            if decodedData.get("error_code") is None:
                return decodedData.get("result")
            else:
                return f"Ошибка: {decodedData.get('error_code')} - {decodedData.get('error_message')}"
        except urllib.error.HTTPError as e:
            return f"HTTP Error: {e.code} - {e.reason}"
        except Exception as e:
            return f"Ошибка: {str(e)}"
