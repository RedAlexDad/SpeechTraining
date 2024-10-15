import sys
from PyQt5.QtWidgets import QApplication

from AudioRecorderWithDB import AudioRecorderWithDB
from tokens import FOLDER_ID, OAUTH, CLIENT_ID, CLIENT_SECRET

if __name__ == "__main__":
    app = QApplication(sys.argv)
    recorder = AudioRecorderWithDB(FOLDER_ID_Y=FOLDER_ID, OAUTH=OAUTH, CLINET_ID_S=CLIENT_ID, CLIENT_SECRET_S=CLIENT_SECRET)
    recorder.show()
    sys.exit(app.exec_())