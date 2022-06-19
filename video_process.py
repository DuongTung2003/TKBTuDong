from concurrent.futures import thread
import ctypes
import urllib3
import cv2
import os
import PIL
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import numpy as np
import threading
import time
def updateSlider1(val):
        processor.offsetX = val
def updateSlider2(val):
        processor.offsetY = val
def updateSlider3(val):
        processor.resize_factor = val
def updateSlider4(val):
        processor.overlay_scale = val
def bt(val):
    processor.visual_scale = not processor.visual_scale
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)
def show_resizing_image(img):
    while not processor.resized:
            frame = PIL.Image.fromarray(img)
            frame = frame.resize((int(frame.width*processor.resize_factor),int(frame.height*processor.resize_factor)),PIL.Image.ANTIALIAS)
            #Crop the frame using offsetX and offsetY, and resize it to X and Y
            frame = frame.crop((processor.offsetX,processor.offsetY,processor.offsetX+processor.X,processor.offsetY+processor.Y))
            cv2.imshow("Frame",ResizeWithAspectRatio(np.array(frame),960, 540) if processor.visual_scale else np.array(frame))
            if cv2.waitKey(5) & 0b11111111 == ord('q'):
                break
    processor.resized_img = frame
class processor:
    offsetX = 0
    offsetY = 0
    resize_factor = 1
    X = 1920
    Y = 1080
    overlay_scale = 1
    resized_img = None
    resized = False
    visual_scale = True
    def __init__(self):
        self.accepted_format = ['mp4','avi']
        self.output_format = '.jpg'
    def resize_frame(self,path:str,overlay = None):
        #Read the first frame
        cap = cv2.VideoCapture(path)
        #Get the frame count
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        c = 0
        ret, frame = cap.read()
        while c < frame_count//4:
            c += 1
            ret, frame = cap.read()
        axx = plt.axes([0.25, 0.2, 0.65, 0.1])
        xSlider = Slider(ax=axx, label="offsetX", valmin=-frame.shape[1]//2, valmax= frame.shape[1]//2, valinit=0, valstep=1,orientation="horizontal",valfmt="%d")
        axy = plt.axes([0.25, 0.4, 0.65, 0.1])
        ySlider = Slider(ax=axy, label="offsetY", valmin=-frame.shape[0]//2, valmax=frame.shape[0]//2, valinit=0, valstep=1,orientation="horizontal",valfmt="%d")
        ax_r = plt.axes([0.25, 0.6, 0.65, 0.1])
        rSlider = Slider(ax=ax_r, label="Resize factor", valmin=0.4, valmax=2, valinit=1, valstep=0.01,orientation="horizontal",valfmt="%d")
        if overlay:
            ax_o = plt.axes([0.25, 0.8, 0.65, 0.1])
            oSlider = Slider(ax=ax_o, label="Overlay", valmin=0, valmax=1, valinit=0, valstep=0.01,orientation="horizontal",valfmt="%d")
            oSlider.on_changed(updateSlider4)
        #Create a button on the plot
        ax_b = plt.axes([0.25, 0.9, 0.65, 0.1])
        btn = Button(ax_b, "Resize")
        btn.on_clicked(bt)
        xSlider.on_changed(updateSlider1)
        ySlider.on_changed(updateSlider2)
        rSlider.on_changed(updateSlider3)
        processor.resized = False
        threading.Thread(target=show_resizing_image,args=(frame,)).start()
        plt.show()
        processor.resized = True
        while not processor.resized_img:
            pass
        return {'resize_factor':processor.resize_factor,'X':processor.X,'Y':processor.Y,'offsetX':processor.offsetX,'offsetY':processor.offsetY}
        
    def process_video(self,path:str,resize_data,folder_name='video_frame/'):
        if path[-3:].lower() not in self.accepted_format:
            return print(path[-3:].lower(),"format not supported(yet)")
        if not os.path.exists(folder_name + path.split('\\')[-1][:-4]):
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)
            os.mkdir(folder_name + path.split('\\')[-1][:-4])
        folder_name = folder_name + path.split('\\')[-1][:-4]
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            return print("Error opening video stream or file")
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        current_frame = 0
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                current_frame += 1
                print(f"\rProcessed {current_frame}/{frame_count}: {round(current_frame/frame_count*100,2)}%",end='')
                frame = PIL.Image.fromarray(frame)
                frame = frame.resize((int(frame.width*resize_data['resize_factor']),int(frame.height*resize_data['resize_factor'])),PIL.Image.ANTIALIAS)
                frame = frame.crop((resize_data['offsetX'],resize_data['offsetY'],resize_data['offsetX']+resize_data['X'],resize_data['offsetY']+resize_data['Y']))
                cv2.imwrite(folder_name+"/frame_"+str(current_frame)+self.output_format,np.array(frame))
            else:
                break
        cap.release()
        print("\nDone")
        
    def is_processed(self,path:str):
        #Check if the video is already processed by find the folder with the same name as the video
        if os.path.exists(path[:-4]):
            return True
        else:
            return False
    def read_video(self,path:str):
        #Read the files in the folder and return a list of paths as a generator
        lst_dr = os.listdir(path)
        for i in range(1,len(lst_dr)+1):
            if lst_dr[i].endswith(self.output_format):
                yield 'frame_'+str(i)+self.output_format
        
if __name__ == "__main__":
    #  processor = processor()
    #  a = processor.resize_frame("D:\\2021-2022\\TKB\\TKBTuDong\\Backgrounds\\test.mp4")
    #  print(a)
    #  processor.process_video("D:\\2021-2022\\TKB\\TKBTuDong\\Backgrounds\\test.mp4",a)
    processor = processor()
    path = "D:\\2021-2022\\TKB\\TKBTuDong\\Backgrounds\\test.mp4"
    #get len of list of frames
    cap = cv2.VideoCapture(path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in processor.read_video("D:\\2021-2022\\TKB\\TKBTuDong\\video_frame\\test\\"):
        img_path = "D:\\2021-2022\\TKB\\TKBTuDong\\video_frame\\test\\"+i
        print(img_path,os.path.getsize(img_path))
        ctypes.windll.user32.SystemParametersInfoW(20,0,img_path,1)
        #sleep with time is fps
        time.sleep(1/cap.get(cv2.CAP_PROP_FPS))
    