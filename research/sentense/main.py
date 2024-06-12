import sys
from PyQt5.QtWidgets import QApplication

from AudioRecorderWithDB import AudioRecorderWithDB

if __name__ == "__main__":
    FOLDER_ID = "b1gko9u515ceceiibap6"
    IAM_TOKEN = 't1.9euelZqWm8eNmc2PyprHycqcnM6elO3rnpWaxo-bkJWWzcnPj5SSkIzNjYrl9PdNOFhM-e9oCjnb3fT3DWdVTPnvaAo5283n9euelZqRzpLJmpPPks-SnY7MzJedm-_8xeuelZqRzpLJmpPPks-SnY7MzJedmw.TqrhFZXYT6rlgEn-jsZ0WMtrQ_aPMZJwSMJjSo2fzppP3gMPivif8OzKAb-kIjee5G48Z4nj2EwTxsFdPITVDA'

    app = QApplication(sys.argv)
    recorder = AudioRecorderWithDB(FOLDER_ID=FOLDER_ID, IAM_TOKEN=IAM_TOKEN)
    recorder.show()
    sys.exit(app.exec_())