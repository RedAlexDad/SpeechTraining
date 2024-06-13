import sys
from PyQt5.QtWidgets import QApplication

from AudioRecorderWithDB import AudioRecorderWithDB

if __name__ == "__main__":
    FOLDER_ID = "b1gko9u515ceceiibap6"
    IAM_TOKEN = 't1.9euelZrIlImZzJvGjZrHjMeZkZKUie3rnpWaxo-bkJWWzcnPj5SSkIzNjYrl8_dYNlRM-e9rBgky_d3z9xhlUUz572sGCTL9zef1656VmsqMi86Xy5mNjonMk5eMkYvH7_zF656VmsqMi86Xy5mNjonMk5eMkYvH.FLI4D0KxlIykVE8QCTRN7b_KMuLKvb5OBUZj0i0ZNTVAOyrCSxiwH-6wvesNUBt4xMM_lxTnQ445hr7sQ_jhBg'

    app = QApplication(sys.argv)
    recorder = AudioRecorderWithDB(FOLDER_ID=FOLDER_ID, IAM_TOKEN=IAM_TOKEN)
    recorder.show()
    sys.exit(app.exec_())