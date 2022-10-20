import tkinter
from tkinter import ttk
import imageio
from PIL import ImageTk, Image
import time
import threading
import sys
from imageio.plugins.ffmpeg import FfmpegFormat

class Video():
    def __init__(self, frame, file_path, master):
        format = FfmpegFormat(
            "ffmpeg",
            "Many video formats and cameras (via ffmpeg)",
            ".mov .avi .mpg .mpeg .mp4 .mkv .wmv .webm",
            "I",
            )
        imageio.formats.add_format(format,True)#Rendez-le compatible avec webm.(Tout à fait de force)

        self.paused = 0
        self.stopped = 0
        self.master = master
        self.mainframe = ttk.Frame(frame)
        self.frame = ttk.Label(self.mainframe)
        self.pbframe = ttk.Frame(self.mainframe)
        self.s = ttk.Style(self.pbframe)
        self.s.layout("LabeledProgressbar",
                [('LabeledProgressbar.trough',
                {'children': [('LabeledProgressbar.pbar',
                                {'side': 'left', 'sticky': 'ns'}),
                                ("LabeledProgressbar.label",   # label inside the bar
                                {"sticky": ""})],
                'sticky': 'nswe'})])
        self.pb = ttk.Progressbar(self.pbframe, orient="horizontal", mode = "determinate", length = self.pbframe.winfo_width(), style="LabeledProgressbar")
        self.btn = ttk.Button(self.pbframe, text="►", command=self.pause)
        try:
            self.video = imageio.get_reader(file_path)
        except imageio.core.fetching.NeedDownloadError:
            imageio.plugins.avbin.download()
            self.video = imageio.get_reader(file_path)
            
    def play(self):
        self.video_thread = threading.Thread(target=self._stream, name = 'video')
        self.video_thread.setDaemon(True)
        self.video_thread.start()
        self.mainframe.pack()
        self.frame.pack(side='top')
        self.pbframe.pack(side='bottom')
        self.pb.pack(side='left')
        self.btn.pack(side='right')
        
    def pause(self):
        if self.paused == 1:
            self.btn['text'] = '►'
            self.paused = 0
        else:
            self.btn['text'] = '| |'
            self.paused = 1

    def stop(self):
        self.mainframe.destroy()
        self.frame.destroy()
        self.pbframe.destroy()
        self.pb.destroy()
        self.btn.destroy()
        
    def stopf(self):
        print("video stopped")
        
        self.stopped = 1
        self.video.close()
        self.video_thread.join()
    def _stream(self):
        while 1:
            if not (self.master.exist):
                self.stopf()
                return
            start_time=time.time()
            sleeptime = 1/self.video.get_meta_data()["fps"]
            frame_now = 0
            i = 0
            for image in self.video.iter_data():
                while self.paused == 1:
                    if i == 10:
                        i = 0
                    else:
                        i = i + 1
                frame_now = frame_now + 1
                if frame_now*sleeptime >= time.time()-start_time:
                    frame_image = ImageTk.PhotoImage(Image.fromarray(image))
                    self.pb['length'] = Image.fromarray(image).size[0]
                    self.pb.update()
                    self.frame.config(image=frame_image)
                    drn = frame_now / self.video.get_meta_data()["fps"]
                    self.pb['value'] = (frame_now / (self.video.get_meta_data()["fps"] * self.video.get_meta_data()["duration"])) * 100
                    self.s.configure("LabeledProgressbar", text="%.2f" % drn + " / " + str(self.video.get_meta_data()["duration"]))
                    self.frame.image = frame_image
                    time.sleep(sleeptime)
                else:
                    pass
