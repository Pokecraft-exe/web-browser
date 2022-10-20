import sounddevice
import pydub
import time
import numpy

class Audio():
    def __init__(self):
        pass
    def openfile(self, filepath):
        if ".mp3" in filepath:
            self.segment = pydub.AudioSegment.from_file(filepath,codec="mp3")
        elif ".wav" in filepath:
            self.segment = pydub.AudioSegment.from_file(filepath,codec="wav")
        elif ".mp4" in filepath:
            self.segment = pydub.AudioSegment.from_file(filepath)
        else:
            self.segment = pydub.AudioSegment.from_file(filepath)
    def play(self, place=0):
        if self.segment.channels != 1:
            self.samples = numpy.array(self.segment.get_array_of_samples().tolist(),dtype="int16").reshape(-1,self.segment.channels)
        else:
            self.samples = numpy.array(self.segment.get_array_of_samples().tolist(),dtype='int16')
        sounddevice.play(self.samples,self.segment.frame_rate)
    def stop(self):
        sounddevice.stop()