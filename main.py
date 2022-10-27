
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt,QCoreApplication
from GUI import *
import sys
import os
import wave
import pyaudio
from aip import AipSpeech
import pandas as pd
from dialogue import UNIT
from qt_material import apply_stylesheet
from urllib.parse import urlencode
from playsound import playsound
APP_ID='28110954'
API_KEY = 'tuXGzyBMMu0O0PSWzT4G395B'
API_SECRET='ueWt6T0XHZ8saSH4glFcwGtr6nTchG1j'
SERVICE_ID = 'S76849'
CHUNK = 1024 
FORMAT = pyaudio.paInt16 # 16位深
CHANNELS = 1 #1是单声道，2是双声道。
RATE = 16000 # 采样率，调用API一般为8000或16000
RECORD_SECONDS = 5 # 录制时间4s

FilePath = "test.wav"

def save_wave_file(pa, filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(data))
    wf.close()

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

class GUI(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(GUI,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("人机对话")
        self.move(0,0)
        self.ui.listWidget.setWordWrap(True)
        self.setWindowIcon(QtGui.QIcon('R-C.jfif'))
        
        self.client = AipSpeech(APP_ID, API_KEY, API_SECRET)

        self.ui.pushButton_2.clicked.connect(self.begin_recognize)

        self.ui.pushButton.clicked.connect(self.button_1_send)


        self.dialogue = UNIT(API_KEY,API_SECRET,SERVICE_ID)

        self.count=0
        audio_list = os.listdir(os.getcwd())
        for audio_ in audio_list:
            n = audio_.find('audio')
            if n!=-1:
                os.remove(audio_)

        

        
    def send_message(self,text:str,user:bool=True):
        messageItem=QtWidgets.QListWidgetItem()
        time = QtCore.QDateTime.currentDateTime().time().toString("hh:mm:ss")
        messageItem.setText(time + "  "+text)
        hint = self.ui.listWidget.sizeHint()
        hint.setWidth(-1)
        messageItem.setSizeHint(hint)
        if user ==True:
            messageItem.setIcon(QtGui.QIcon('R-C2.jfif'))
        else:
            messageItem.setIcon(QtGui.QIcon('R-C.jfif'))
        return messageItem

    def button_1_send(self):
        try:
            input_text = self.ui.lineEdit.text()
            self.ui.listWidget.addItem(self.send_message(input_text))
            self.ui.listWidget.scrollToBottom()
            QCoreApplication.processEvents()

            result = self.dialogue.query(input_text)

            self.ui.listWidget.addItem(self.send_message(result,user=False))

            self.ui.listWidget.scrollToBottom()
            QCoreApplication.processEvents()

            self.text_2_audio(result)
        except:
            pass

       
            
        

                
        

            
            

            

    def get_audio(self,filepath):
        pa = pyaudio.PyAudio()
        stream = pa.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)
        
        print("*" * 10, f"开始录音：请在{RECORD_SECONDS}秒内输入语音")

        self.ui.pushButton_2.setText("正在录音")
        QCoreApplication.processEvents()
        frames = []  
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):  
            data = stream.read(CHUNK)  # 读取chunk个字节 保存到data中
            frames.append(data)  # 向列表frames中添加数据data
        
        print("*" * 10, "录音结束\n")

        stream.stop_stream()
        stream.close()  # 停止数据流
        pa.terminate()  # 关闭PyAudio
        
        self.ui.pushButton_2.setText("语音输入")
        
        #写入录音文件
        save_wave_file(pa, filepath, frames)

    def begin_recognize(self):
        self.get_audio(FilePath)

        result = self.client.asr(get_file_content(FilePath), 'wav',16000,{'dev_pid': 1537,})

        self.ui.lineEdit.setText(result['result'][0])

    def text_2_audio(self,text:str):
        """
        语音参数网址 https://ai.baidu.com/ai-doc/SPEECH/Qk38y8lrl
        vol 音量
        aue 输出文件格式 3为mp3格式(默认),
         4为pcm-16k,
         5为pcm-8k,
         6为wav内容同pcm-16k;
         注意aue=4或者6是语音识别要求的格式,但是音频内容不是语音识别要求的自然人发音，所以识别效果会受影响。
        """
        result  = self.client.synthesis(text=text, lang='zh', ctp=1, options={'vol': 5,'aue':6})
        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if not isinstance(result, dict):
            with open(f'audio{self.count}.wav', 'wb') as f:
                f.write(result)

        #树莓派上 请使用 os.system(f"aplay audio{self.count}.wav") 播放语音
        playsound(f'audio{self.count}.wav')

        self.count=self.count+1

        

                
                



        







if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    #MainWindow = QtWidgets.QMainWindow()
    window = GUI()
    #window.showFullScreen()
    apply_stylesheet(app, theme='dark_teal.xml')
    window.show()
    sys.exit(app.exec_())