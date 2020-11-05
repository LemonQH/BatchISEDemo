import pyaudio
import threading
import wave
import os

from isebynetease import *



class Audio_model():
    def __init__(self, audio_path,is_recording):
        self.current_file=''
        self.is_recording=is_recording
        self.audio_chunk_size=1600
        self.audio_channels=1
        self.audio_format=pyaudio.paInt16
        self.audio_rate=16000


    def record_and_save(self):
        self.is_recording = True
        file_name=self.get_file_name(self.current_file)
        self.audio_file_name='./record/'+file_name+'.wav'
        threading.Thread(target=self.record,args=(self.audio_file_name,)).start()

    def get_file_name(self,file_path):
        file_name=os.path.basename(file_path).split('.')[0]
        return file_name

    def record(self,file_name):
        print(file_name)
        p=pyaudio.PyAudio()
        stream=p.open(
            format=self.audio_format,
            channels=self.audio_channels,
            rate=self.audio_rate,
            input=True,
            frames_per_buffer=self.audio_chunk_size
        )
        wf = wave.open(file_name, 'wb')
        wf.setnchannels(self.audio_channels)
        wf.setsampwidth(p.get_sample_size(self.audio_format))
        wf.setframerate(self.audio_rate)

        # 读取数据写入文件
        while self.is_recording:
            data = stream.read(self.audio_chunk_size)
            wf.writeframes(data)
        wf.close()
        stream.stop_stream()
        stream.close()
        p.terminate()

    def get_content(self,file_path):
        with open(file_path, "r") as f:
            file_content = f.read()
            return file_content

    def get_score(self,dict):
        result=[]
        #self.is_recording=False
        for path in dict:
            file_content=self.get_content(path)
            file_name=self.get_file_name(path)
            audio_path='./record/'+file_name+'.wav'
            print(file_content,audio_path)
            score_result=connect(audio_path,file_content)
            #处理结果，添加进结果集
            result.append( score_result)
        return result

