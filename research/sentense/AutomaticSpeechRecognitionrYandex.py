import urllib.request
import json
import io
import requests

class AutomaticSpeechRecognitionYandex:
    def __init__(self, folder_id, iam_token):
        self.folder_id = folder_id
        self.iam_token = iam_token

    def recognize_speech_audio_data(self, audio_data, lang='ru-RU', topic='general'):
        params = "&".join([
            "topic=%s" % topic,
            "folderId=%s" % self.folder_id,
            "lang=%s" % lang
        ])

        url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=audio_data)
        url.add_header("Authorization", "Bearer %s" % self.iam_token)
        url.add_header("Content-Type", "audio/ogg")

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
