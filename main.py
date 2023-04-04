# This is a sample Python script.
from tkinter import *
import openai
from PIL import Image, ImageTk
import PIL
import time
import os
from google.cloud import speech
import pyaudio
import threading
import wave
from tkinter import filedialog
import PyPDF2
import os
import textract
import json

from database_connector import *
from gtts import gTTS
import playsound


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'potent-minutia-381604-89d2d33e5f12.json'
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "voice.wav"

CHUNK_SIZE = 1024
MIN_VOLUME = 2600
white_frame = 3
max_file = 100
BUF_MAX_SIZE = CHUNK_SIZE * 10

openai.api_key = "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"


def text_to_speech(msg):
    output = gTTS(msg,lang="vi", slow=False)
    output.save("coutput.mp3")
    playsound.playsound('coutput.mp3', True)
    os.remove("coutput.mp3")

class AppChatGPT:

    def __init__(self) -> None:
        self.speech_client = speech.SpeechClient()
        self.root = Tk()
        self.root.resizable(False,False)
        self.root.rowconfigure(9, minsize=300)
        self.root.columnconfigure(9, minsize=900)
        self.root.title("Q&A with ChatGPT")
        self.root.geometry('1400x900')
        # self.root.minsize(width=screenWidth, height=screenHeight)
        self.root.state('zoomed')
        self.db = database()
        self.lbl = Label(self.root, text="Question?")
        self.lbl.grid(column=1,row=0)

        self.tk_image =PIL.Image.open("ChatGPT_logo.png")
        # Resize the image to 20x20 pixels
        self.tk_image = self.tk_image.resize((40,40))
        # Convert image to tkinter-compatible format
        self.tk_image = ImageTk.PhotoImage(self.tk_image)
        self.gptIcon = Label(self.root, image=self.tk_image)
        self.gptIcon.grid(column=0,row=0)

        self.txtAnswer=Text(self.root,width=80,font=('Times New Roman', 17))
        self.txtAnswer.grid(column=4, row=5, rowspan=3)
        self.txtQuestion=Text(self.root,width=40,font=('Times New Roman', 17))
        self.txtQuestion.grid(column=1, row=5, rowspan=3)
        self.btnClrQ = Button(self.root, text="Clear Q", fg="black", command=self.clearQ)
        # Set Button Grid
        self.btnClrQ.grid(column=1, row=8)
        self.btn = Button(self.root, text="Answer", fg="red", command=self.clicked)
        # Set Button Grid
        self.btn.grid(column=2, row=6)
        self.recording=False

        self.btnClrA = Button(self.root, text="Clear A", fg="black", command=self.clearA)
        # Set Button Grid
        self.btnClrA.grid(column=4, row=8)

        self.mic_icon =PIL.Image.open("micIcon.jpg")
        self.mic_icon = self.mic_icon.resize((30,30))
        self.mic_icon_tk = ImageTk.PhotoImage(self.mic_icon)

        self.mic_btn = Button(self.root, image=self.mic_icon_tk,command=self.click_recording) 
        self.mic_btn.grid(column=2, row=1)

        self.messages = [
        {"role": "system", "content": "You are a helpful and kind AI Assistant."},
        ]
        # add button to load file
        self.btnLoadFile = Button(self.root, text="Load file", fg="blue", command=self.loadDocFile)
        # Set Button Grid
        self.btnLoadFile.grid(column=0, row=2)
        # add button to load file
        self.btnLoadDataBase = Button(self.root, text="Load database", fg="blue", command=self.click_load_db)
        # Set Button Grid
        self.btnLoadDataBase.grid(column=0, row=3)
        self.root.mainloop()
    def clicked(self):
        res = "Chat GPT in progress...."
        time.sleep(1)
        self.lbl.configure(text=res)
        question = self.txtQuestion.get("1.0", "end-1c")
        msg = self.chatbot(question)

        self.txtAnswer.insert(END,"\n"+ "\n >> "+ msg)
        res = "Chat GPT 3.5"
        self.lbl.configure(text=res)
        self.btn = Button( self.root, text="Answer", fg="red", command=self.clicked)
        self.btn.grid(column=2, row=6)
        threading.Thread(target=text_to_speech, args=(msg,)).start()
        threading.Thread(target=self.execute_sql, args=(msg,)).start()

    def clearQ(self):
        self.txtQuestion.delete(1.0,END)

    def clearA(self):
        self.txtAnswer.delete(1.0,END)

    def chatbot(self, input):
        if input:
            self.messages.append({"role": "user", "content": input})
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=self.messages
            )
            reply = chat.choices[0].message.content
            self.messages.append({"role": "assistant", "content": reply})
            return reply

    def loadDocFile(self):
        # Open a file dialog box
        file_path = filedialog.askopenfilename()
        # Read the file
        extension = os.path.splitext(file_path)[1]
        # print(extension)
        if extension == '.pdf':
            self.txtQuestion.delete(1.0, END)
            self.readPDF(file_path)
        elif extension == '.docx':
            text = textract.process(file_path)
            self.txtQuestion.delete(1.0, END)
            self.txtQuestion.insert(END, text)
            # doc = docx.Document(file_path)
            # all_paragraphs = doc.paragraphs
            # for paragraph in all_paragraphs:
            # txtQuestion.insert(END,paragraph.text)
        else:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                # Print the file contents
                self.txtQuestion.delete(1.0, END)
                self.txtQuestion.insert(END, file_contents)

    def readPDF(self,filePath):
        with open(filePath, 'rb') as f:
            # Create a PDF reader object
            pdfReader = PyPDF2.PdfReader(f)
            # Get the total number of pages
            numPages = len(pdfReader.pages)
            # Loop over each page and extract the text
            for i in range(numPages):
                print(pdfReader.pages[0].extract_text())
                self.txtQuestion.insert(END, pdfReader.pages[i].extract_text())

    def click_load_db(self):

        sample=self.db.get_sample()
        self.txtQuestion.delete(1.0,END)
        self.txtQuestion.insert(END,"cusomers database has been loaded. Beside are 5 sample rows")
        self.txtAnswer.insert(END,sample)
        msg=self.chatbot(input=sample)
        print(msg)
        self.txtAnswer.insert(END, msg)

    def execute_sql(self,msg):
        sql = get_sql_from_msg(msg)
        print(sql)
        # try:
        sql_response = self.db.execute_sql(sql)
        self.txtAnswer.insert(END, '\n')
        self.txtAnswer.insert(END, sql_response_analyze(sql,sql_response))
        # except:
        #     print('sql syntax error')


    
    def click_recording(self):
        if self.recording:
            time.sleep(3)
            self.recording=False
            self.txtAnswer.insert(END," \n >>Processing......")
        
        else:
            self.recording=True
            self.txtQuestion.delete(1.0,END)
            self.txtQuestion.insert(END,"Listening......")
            threading.Thread(target=self.record).start()
    
    def record(self):
        audio = pyaudio.PyAudio()
        stream=audio.open(format=FORMAT,channels=CHANNELS,rate=RATE,
                        input=True,frames_per_buffer=CHUNK_SIZE)
        frames=[]
        while self.recording:
            data=stream.read(1024)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        questions=self.File_to_text(WAVE_OUTPUT_FILENAME,self.speech_client)
        self.txtQuestion.delete(1.0,END)
        self.txtQuestion.insert(END,questions)
        msg = self.chatbot(questions)
        self.txtAnswer.insert(END,"\n"+ "\n >> "+ msg)
        
        output = gTTS(msg,lang="vi", slow=False)
        output.save("coutput.mp3")
        playsound.playsound('coutput.mp3', True)
        os.remove("coutput.mp3")

    def File_to_text(self,file_name,speech_client):
        with open(file_name, 'rb') as f2:
            byte_data_wav = f2.read()
        audio_wav = speech.RecognitionAudio(content=byte_data_wav)

        config_wav = speech.RecognitionConfig(
            sample_rate_hertz=44100,
            enable_automatic_punctuation=True,
            language_code='vi-VN',
            audio_channel_count=2
        )


        response_standard_wav = speech_client.recognize(
            config=config_wav,
            audio=audio_wav
        )
        return response_standard_wav.results[0].alternatives[0].transcript


if __name__=="__main__":
    AppChatGPT()




