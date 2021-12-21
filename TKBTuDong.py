
# CREDIT: DUONG TUNG AI&RB-K15 PKA



import ctypes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import logging
from datetime import datetime,timedelta,time,date
import os
import math
import random
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import base64
import codecs
from cryptography.fernet import Fernet
from time import sleep
import urllib3
import json
from GoogleCalendar import Calendar
import configparser
try:
    os.mkdir("./LogFiles/")
except :
    pass
format = "%(asctime)s: %(message)s"
logname =  "./LogFiles/Log_"+str(datetime.now().month) +"_"+ str(datetime.now().day)+"_"+ str(datetime.now().hour)+"_"+ str(datetime.now().minute)+".log"
logging.basicConfig(filename=logname,format=format, level=logging.INFO,datefmt="%H:%M:%S")
def Checkbool(ip):
    return True if ip == "true" or ip == "True"else False
class GlobalVariable(): #---------------------------CHINH SUA CAI DAT O DAY-----------------------------------------
    TG1 = ["7h30 - 8h20","8h25 - 9h15","9h20 - 10h10","10h15 - 11h05","11h10 - 12h00","13h00 - 13h50","13h55 - 14h45","14h50 - 15h40","15h45 - 16h35","16h40 - 17h30","17h35 - 18h25","18h30 - 19h20"]
    TG2 = ["6h45 - 7h35","7h40 - 8h30","8h35 - 9h25","9h30 - 10h20","10h25 - 11h15","11h20 - 12h10","13h00 - 13h50","13h55 - 14h45","14h50 - 15h40","15h45 - 16h35","16h40 - 17h30","17h35 - 18h25"]

    FORCE_INTERNET_OFF = False
    KeyFiles = "UserKey.enc"
    UserDataFile = "UserData.enc"
    BackGroundFiles = "./Backgrounds/"
    GoogleCalendarIDsFile = "GoogleCalendarIDs.txt"
    Font = "calibril.ttf"
    GC_delete_after = 2
    ABSOLUTE_OUTPUT_PATH = "\\output.png"
    LoginURL = 'https://qldt.phenikaa-uni.edu.vn/Login.aspx'
    LichHocURL = 'https://qldt.phenikaa-uni.edu.vn/KetQuaDangKy.aspx'
    UserData_check = False
    Tuan = ["Thứ 2","Thứ 3", "Thứ 4","Thứ 5","Thứ 6","Thứ 7"]
    #------- THỜI GIAN VÀO LỚP---------- TG1 hoặc TG2
    ThoiGianBieu = TG1
    #------------------------------------------------
    EnableBG = True
    SELENIUM_HEADLESS = True
    DSTiet = [ "Tiết "+str(t_) for t_ in range(1,13) ]
    SoNgayHienThi = 7
    width, height = 2400,1200 #TABLE
    Cord = [-200,1200]
    XuongDong = 12
    VietTat = XuongDong * 2
    TextAlpha = 200
    TableColors = {"Text":[255,255,255,TextAlpha],"LineNormal":"#ffffff","LineToday":"#2200ff","LineInSession":"#fc0303","LineNext":"#ffe600"}
    LineThickness = 2
    CREDENTIALS_FILE = './client_secret_431692909921-5oud82jo99c4sfne77c96t2livor8rvd.apps.googleusercontent.com.json'
    internet_connected = True

#------------------------------------------------------------------------------------------------
class Tiet(): #Tiet trong ngay
    def __init__(self,tiet = 0, ID_mon = "",Thu = 0):
        self.tiet = tiet
        self.ID_mon = ID_mon 
        self.Thu = Thu
        Console.Log("Da them tiet",ID_mon,"Tiet so",tiet,"Vao thu",GlobalVariable.Tuan[Thu])
def getConfiguration():
    Console.Log("Dang lay cai dat tu TKBSetting.cfg")
    try:
        config = configparser.ConfigParser()
        config.read('TKBSetting.cfg')
        GlobalVariable.ThoiGianBieu = GlobalVariable.TG1 if  int(config['Thoi gian vao lop']['default']) == 0 else GlobalVariable.TG2
        GlobalVariable.EnableBG = Checkbool(config['Cai dat hinh nen']['Enable'])
        GlobalVariable.Font = config['Cai dat hinh nen']['Font']
        GlobalVariable.GC_delete_after = int(config['Cai dat chung']['SO_NGAY_XOA_EVENT_GOOGLE_CALENDAR'])
        GlobalVariable.SELENIUM_HEADLESS = Checkbool(config['Cai dat chung']['SELENIUM_HEADLESS'])
        GlobalVariable.FORCE_INTERNET_OFF = config['Cai dat chung']['FORCE_INTERNET_OFF']
        GlobalVariable.CREDENTIALS_FILE = config['Cai dat chung']['CREDENTIALS_FILE']
        GlobalVariable.BackGroundFilesPath = config['Cai dat chung']['BackGroundFilesPath']
        GlobalVariable.UserDataEncrypt = config['Cai dat chung']['UserDataEncrypt']
        GlobalVariable.LoginURL = config['Cai dat chung']['LoginURL']
        GlobalVariable.LichHocURL = config['Cai dat chung']['LichHocURL']
        Console.Log("Cai dat thanh cong")
    except:
        Console.Error("Cai dat that bai!")
class Console():
    def Log(*arg):
        msg = ""
        for inf in arg:
            msg += str(inf) + " "
        logging.info("INFO "+msg)
        print("INFO "+msg)
    def Warning(*arg):
        msg = ""
        for inf in arg:
            msg += str(inf) + " "
        logging.warning("WARNING "+msg)
        print("WARNING "+msg)
    def Error(*arg):
        msg = ""
        for inf in arg:
            msg += str(inf) + " "
        logging.error("ERROR "+msg)
        print("ERROR "+msg)

class Main():
    
    def __init__(self):
        getConfiguration()
        self.UserID = ""
        self.UserPassword = ""
        self.GetUserData()
        try:
            http = urllib3.PoolManager()
            r = http.request('GET',GlobalVariable.LoginURL )
        except: 
            Console.Error("Can't connect to internet")
            self.PageSource = codecs.open("./pageBackup.html","r","utf-8").read()
            GlobalVariable.internet_connected = False
        else:
            opts = Options()
            opts.headless = GlobalVariable.SELENIUM_HEADLESS
            #assert opts.headless  # Operating in headless mode  options=opts 
            self.driver = webdriver.Chrome('.\chromedriver.exe',options=opts)  # Optional argument, if not specified will search path.
            #self.driver.execute(Command.SET_TIMEOUTS, {'ms': float(15 * 1000), 'type': 'page load'})
            self.Login()
            Console.Log("Dang nhap thanh cong")
            if GlobalVariable.UserData_check == False:
                if input("Ban co muon luu ten dang nhap va mat khau? y/n ").lower() == "y":
                    self.SaveUserData()
            self.driver.get(GlobalVariable.LichHocURL)
            GlobalVariable.internet_connected = True if GlobalVariable.FORCE_INTERNET_OFF == False else False
            sleep(1)
            self.PageSource = self.driver.page_source
                

            self.DataTable = pd.read_html(self.PageSource,attrs={'id':'grd'})[0]
            with codecs.open("pageBackup.html","w+","utf-8") as f:
                f.write(str(self.PageSource))
                f.close()
            self.DataProcess()

                
        Console.Log("Lay thong tin thanh cong")
        Console.Log(self.DataTable)
        Console.Log("Xu li du lieu...")

        Console.Log("Xu li du lieu hoan tat")
        Console.Log("Khoi tao bang...")
        self.GetIMG()
        
        Console.Log("Hoan tat")
        




    def Login(self):
        if self.UserID == "" or self.UserPassword == "":
            sleep(2)
            Console.Log("Nhap thong tin dang nhap:")
            self.UserID = input("Ten dang nhap: ")
            self.UserPassword = input("Mat khau: ")
        self.driver.get(GlobalVariable.LoginURL)
        email = self.driver.find_element_by_id('txtusername')
        email.send_keys(self.UserID)
        pass_box = self.driver.find_element_by_name('txtpassword')
        pass_box.send_keys(self.UserPassword)
        pass_box.submit()
        button = self.driver.find_element_by_name('btnDangNhap')
        button.click() 
        sleep(1)
        while str(self.driver.current_url).find(GlobalVariable.LoginURL) >= 0  :
             try:
                self.driver.find_element_by_id('lblThong_bao')
             except:
                  continue
             else:
                 
                 Console.Warning("Mat khau/Tai khoan khong dung!")
                 self.driver.refresh()
                 self.UserID = ""
                 self.UserPassword = ""
                 self.Login()
             continue
        
    def unique_list(self,l):
        ulist = []
        [ulist.append(x) for x in l if x not in ulist]
        return ulist
    def GetUserData(self):
        
        Key = None
        try:
            with open(GlobalVariable.KeyFiles,"rb") as  KeyFile:
                Key = KeyFile.read()
                fernet = Fernet(Key)
                with open(GlobalVariable.UserDataFile,"rb") as  DataFile:
                    Data = fernet.decrypt(DataFile.read()).decode()
                    self.UserID = Data.split("\n")[0]
                    self.UserPassword = Data.split("\n")[1]
                    Console.Log("Lay thong tin nguoi dung thanh cong")
                    GlobalVariable.UserData_check = True
        except:
            Console.Error("Chua thiet lap thong tin dang nhap!")
            GlobalVariable.UserData_check = False
    def SaveUserData(self):
        with open(GlobalVariable.KeyFiles,"wb+") as  KeyFile:
            Key = Fernet.generate_key()
            fernet = Fernet(Key)
            UserData = self.UserID+"\n"+self.UserPassword
            enc = fernet.encrypt(UserData.encode())
            KeyFile.write(Key)
            with open(GlobalVariable.UserDataFile,"wb+") as  DataFile:
                DataFile.write(enc)
                DataFile.flush()
                DataFile.close()
            KeyFile.flush()
            KeyFile.close()
    def nextPeriod(self):
        exec_time = datetime.now()
        next_P = datetime(2200,10,10)
        next_P_location = []
        if GlobalVariable.internet_connected == True:
         try:
            GGFile = open(GlobalVariable.GoogleCalendarIDsFile,'r+')
            newFile = False if GGFile.read() != "" else True
         except:
            GGFile = open(GlobalVariable.GoogleCalendarIDsFile,'w+')
            newFile = True

        gg_event_range = [datetime(1900,1,1),datetime(1900,1,1)]
        jsonRead = dict()
        if GlobalVariable.internet_connected == True and newFile == False:
            jsonRead = json.load(open(GlobalVariable.GoogleCalendarIDsFile,'r'))
            IDs = jsonRead.keys()
            for ID in IDs:
                ev_time  = datetime.fromisoformat(jsonRead[ID])
                if datetime.now().astimezone() - ev_time >= timedelta(GlobalVariable.GC_delete_after):
                    Console.Log("Deleting event",ID,datetime.now().astimezone(),ev_time,datetime.now().astimezone() - ev_time)
                    Calendar(GlobalVariable.CREDENTIALS_FILE).DeleteEvent(ID)
                    jsonRead = jsonRead.copy()
                    jsonRead.pop(ID)
        
        for next_d in range(0,GlobalVariable.SoNgayHienThi):
          for thu in range(0,len(self.DanhSachTiet)):
            for tiet in range(0,len(self.DanhSachTiet[thu])):
                if self.DanhSachTiet[thu][tiet] >= 0:
                    tg_tiet =  GlobalVariable.ThoiGianBieu[tiet - 1].split(" - ")
                    #Console.Log(tg_tiet,thu)
                    start_h = [ int(a) for a in tg_tiet[0].split("h")]
                    start_t = datetime.combine(date(exec_time.year,exec_time.month,exec_time.day) + timedelta(next_d),time(start_h[0],start_h[1]))
                    end_h = [ int(a) for a in tg_tiet[1].split("h")]
                    end_t = datetime.combine(date(exec_time.year,exec_time.month,exec_time.day) + timedelta(next_d),time(end_h[0],end_h[1]))
                    if start_t.weekday() == thu:

                     Console.Log("Checking..",start_t)
                     #---------------Google calendar
                     
                     if (GlobalVariable.internet_connected == True  ):        
                         
                         if self.DanhSachTiet[thu][tiet +1] == self.DanhSachTiet[thu][tiet]:
                             if tiet != 0:
                                if self.DanhSachTiet[thu][tiet -1] != self.DanhSachTiet[thu][tiet]:
                                 gg_event_range[0] = start_t
                             else:
                                 pass
                         elif self.DanhSachTiet[thu][tiet +1] == self.DanhSachTiet[thu][tiet] and  self.DanhSachTiet[thu][tiet - 1] == self.DanhSachTiet[thu][tiet]:
                             pass
                         elif tiet == 0:
                             tenGV = ""
                             if type(self.DataTable['Giáo viên'][self.DanhSachTiet[thu][tiet]]) is str:
                                 tenGV = ' '.join(self.unique_list(self.DataTable['Giáo viên'][self.DanhSachTiet[thu][tiet]].split(" ")))
                             if type(self.DataTable['Phòng học'][self.DanhSachTiet[thu][tiet]]) is str:
                                 tenLOP = ' '.join(self.unique_list(self.DataTable['Phòng học'][self.DanhSachTiet[thu][tiet]].split(" ")))
                             else:
                                 tenLOP = "Online"
                             desc = "" + ("Giáo viên: "+ tenGV if tenGV != "" and  tenGV != ' ' else "") + (" Lớp học: "+ tenLOP if tenLOP != "" and tenLOP != ' ' else "")
                             if ((gg_event_range[0].astimezone().isoformat()  in jsonRead.values()) == False):
                                 result_id,result_sum,result_start,result_end = Calendar(GlobalVariable.CREDENTIALS_FILE).CreateEvent(self.DataTable['Tên học phần'][self.DanhSachTiet[thu][tiet]],desc,start_t.isoformat(),end_t.isoformat(),tenGV,tenLOP)
                                 Console.Log("created event")
                                 Console.Log("id: ", result_id)
                                 Console.Log("summary: ", result_sum)
                                 Console.Log("starts at: ", result_start)
                                 Console.Log("ends at: ", result_end)
                                 #result['id'],result['summary'],result['start']['dateTime'],result['end']['dateTime']
                                 jsonRead[str(result_id)] = result_start
                         elif self.DanhSachTiet[thu][tiet - 1] == self.DanhSachTiet[thu][tiet]:
                             gg_event_range[1] = end_t
                             tenGV = ""
                             if type(self.DataTable['Giáo viên'][self.DanhSachTiet[thu][tiet]]) is str:
                                 tenGV = ' '.join(self.unique_list(self.DataTable['Giáo viên'][self.DanhSachTiet[thu][tiet]].split(" ")))
                             if type(self.DataTable['Phòng học'][self.DanhSachTiet[thu][tiet]]) is str:
                                 tenLOP = ' '.join(self.unique_list(self.DataTable['Phòng học'][self.DanhSachTiet[thu][tiet]].split(" ")))
                             else:
                                 tenLOP = "Online"
                             desc = "" + ("Giáo viên: "+ tenGV if tenGV != "" and tenGV != ' ' else "") + (" Lớp học: "+ tenLOP if tenLOP != "" and tenLOP != ' ' else "")
                             if ((gg_event_range[0].astimezone().isoformat()  in jsonRead.values()) == False):

                                 result_id,result_sum,result_start,result_end = Calendar(GlobalVariable.CREDENTIALS_FILE).CreateEvent(self.DataTable['Tên học phần'][self.DanhSachTiet[thu][tiet]],desc,gg_event_range[0].isoformat(),gg_event_range[1].isoformat(),tenGV,tenLOP)
                                 #Subject = "",desc = "",start = datetime(),end = datetime(),organizer = "",location = ''
                                 Console.Log("created event")
                                 Console.Log("id: ", result_id)
                                 Console.Log("summary: ", result_sum)
                                 Console.Log("starts at: ", result_start)
                                 Console.Log("ends at: ", result_end)
                                 #result['id'],result['summary'],result['start']['dateTime'],result['end']['dateTime']
                                 jsonRead[str(result_id)] = result_start

                         
                     if exec_time >= start_t and  exec_time <= end_t:
                        Console.Log("In session")
                        next_P_location = [self.DanhSachTiet.index(self.DanhSachTiet[thu]),tiet]
                        return 1,end_t,next_P_location

                     elif (next_P - exec_time) > (start_t - exec_time) and exec_time < end_t:

                        Console.Log("Changed order", next_P,"compare to",start_t)
                        next_P = start_t
                        next_P_location = [self.DanhSachTiet.index(self.DanhSachTiet[thu]),tiet]
        Console.Log("Tiep theo la tiet",next_P_location)
        if GlobalVariable.internet_connected == True:
         GGFile = open(GlobalVariable.GoogleCalendarIDsFile,'w+')
         json.dump(jsonRead,GGFile)
         GGFile.close()
        if next_P.day == exec_time.day:
            return 2, next_P,next_P_location
        else:
            return 3, next_P,next_P_location
        

    def DataProcess(self):
        self.SoMonHoc = len(self.DataTable['Mã học phần'])
        self.DanhSachTiet = []
        for i in range(len(GlobalVariable.Tuan)+1):
            t_tuan = []
            for i_ in range(0,len(GlobalVariable.ThoiGianBieu)+1):
                t_tuan.append(-1)
            self.DanhSachTiet.append(t_tuan)
        DSngayHienThi = []
        for count in range(0,GlobalVariable.SoNgayHienThi):
            DSngayHienThi.append(datetime.now().date()+timedelta(count))
        for STT in range(0,self.SoMonHoc):
            LH = self.DataTable['Lịch học'][STT]#.astype('string')
            StDateStr = LH.split("-")[0]
            StDate = datetime.strptime(StDateStr,'%d/%m/%y')
            EndDateStr = LH.split("-")[1][:str(LH.split("-")[1]).find("Th")]
            EndDate = datetime.strptime(EndDateStr,'%d/%m/%y')
            ThuTrongTuan = [ int(thu[:thu.find("(")]) - 2 for thu in LH.split("Thứ ")[1:]] #0-6
            Tiet_ = [ tiet_[:tiet_.find(")")] for tiet_ in LH.split("(T")[1:]  ] # 1-2
            Console.Log(STT,Tiet_)
            for Thu in range(0,len(ThuTrongTuan)):
                    check = False
                    for ngay_trong_ds in DSngayHienThi:
                        if ngay_trong_ds.weekday() == ThuTrongTuan[Thu]:
                            if (ngay_trong_ds < StDate.date()) or (ngay_trong_ds > EndDate.date()):
                                Console.Log("Not in range")
                                check = True
                    if check == False:
                        DSTietgioihan_ngay = [int(t) for t in Tiet_[Thu].split("-")]
                        DStiet_ngay = [ t_ for t_ in range(DSTietgioihan_ngay[0],DSTietgioihan_ngay[1]+1)]
                        for tietTrongDSngay in DStiet_ngay:
                            self.DanhSachTiet[ThuTrongTuan[Thu]][tietTrongDSngay] = STT
            Console.Log(ThuTrongTuan) 
    def GetIMG(self):
        BGFiles_name  = os.listdir(GlobalVariable.BackGroundFiles)
        self.BGFile = random.choice(BGFiles_name)
        try: 
            configFile = open("PicturesConfiguation.json",'r')
            configData = json.load(configFile)
            configFile.close()
        except:
            configData = {}

        for BGFile_ in BGFiles_name:
           if configData.get(BGFile_,"") == "":
             configured =False
             while True:
               Console.Error("Ảnh ",BGFile_,"chưa được cài đặt vị trí TKB,xin hãy nhập theo dạng x,y")
               x,y = None,None
               configData[BGFile_] = {}
               while x== None and y == None:
                   inp = input("\n>")
                   try:
                       x=int(inp.split(",")[0])
                       y=int(inp.split(",")[1])
                   except:
                       Console.Error("Định dạng không hợp lệ")
               Console.Log("Thêm thành công với x=",x,",y=",y,"vào ảnh",BGFile_)
               configData[BGFile_]["Vi tri"] = [x,y]
               rgba = [None,None,None,None]
               Console.Log("Nhập màu chữ muốn hiển thị với dạng r,g,b,a")
               while None in rgba:
                    inp = input("\n>")
                    if inp == "":
                        break
                    try:
                        rgba= [int(userinp) for userinp in inp.split(",")]
                        GlobalVariable.TableColors["Text"] = rgba
                    except:
                        Console.Error("Định dạng không hợp lệ")
               
               if inp != "":
                for cor in GlobalVariable.TableColors:
                   if cor != "Text":
                       Console.Log("Nhập màu cho",cor,"với định dạng HEX (vd:#ffe600)")
                       inp = input(">")
                       if inp == "":
                           Console.Log("Bỏ qua")
                       elif inp[0]=="#":
                           GlobalVariable.TableColors[cor] = inp
               configData[BGFile_]["Colors"] = dict(GlobalVariable.TableColors)
               Console.Log(configData[BGFile_])
               GlobalVariable.Cord = [configData[BGFile_]["Vi tri"][0],configData[BGFile_]["Vi tri"][1]]
               self.BGFile = BGFile_
               self.CreateTable()
               if (input("Confirm y/n?  ")) == "y":
                   break
        GlobalVariable.Cord = [configData[self.BGFile]["Vi tri"][0],configData[self.BGFile]["Vi tri"][1]]
        GlobalVariable.TableColors = configData[self.BGFile]["Colors"]
        configFile = open("PicturesConfiguation.json",'w+')
        json.dump(configData,configFile )
        configFile.close()
        self.CreateTable()
    def CreateTable(self):
        baseSample = Image.open((GlobalVariable.BackGroundFiles + self.BGFile))
        BG = baseSample.convert("RGBA")
        Overlay = Image.new("RGBA", BG.size, (255,255,255,0))
        TableOverlay = ImageDraw.Draw(Overlay)
        fnt = ImageFont.truetype(GlobalVariable.Font,45)
        width = GlobalVariable.width 
        height = GlobalVariable.height
        Cursor_Y = int(height*((1)/len(GlobalVariable.DSTiet)))
        col = 9
        coTietHomNay,nx_Period,nx_Location = self.nextPeriod()
        IDTiethoc = self.DanhSachTiet[nx_Location[0]][nx_Location[1]]
        LineOffset =  int((height*(1/len(GlobalVariable.DSTiet)))/2)
        textColor = (GlobalVariable.TableColors["Text"][0],GlobalVariable.TableColors["Text"][1],GlobalVariable.TableColors["Text"][2],GlobalVariable.TableColors["Text"][3])
        self.BangVietTat = []
        #TableOverlay.rectangle([(GlobalVariable.Cord[0]+(width/9*nx_Location[0]),GlobalVariable.Cord[1]+int(height*((nx_Location[1]+2)/len(GlobalVariable.DSTiet)))- LineOffset/2),     (GlobalVariable.Cord[0]+(width/9*nx_Location[0])+((width/9)*0.6),GlobalVariable.Cord[1]+int(height*((nx_Location[1]+2)/len(GlobalVariable.DSTiet)))+ LineOffset/2)],None,"#e1ed00",GlobalVariable.width)
        for Y in range(0,len(GlobalVariable.DSTiet) ):
            Cursor_X = int(width/9)
            
            TableOverlay.text((GlobalVariable.Cord[0]+Cursor_X,GlobalVariable.Cord[1]+Cursor_Y), GlobalVariable.DSTiet[Y], font=fnt, fill=textColor)
            Cursor_X = int(width/9*1.7)
            TableOverlay.text((GlobalVariable.Cord[0]+Cursor_X,GlobalVariable.Cord[1]+Cursor_Y), GlobalVariable.ThoiGianBieu[Y], font=fnt, fill=textColor)
            TableOverlay.line([(GlobalVariable.Cord[0]+int(width/9),GlobalVariable.Cord[1]+Cursor_Y+ LineOffset),(GlobalVariable.Cord[0]+GlobalVariable.width-LineOffset*1.47,GlobalVariable.Cord[1]+Cursor_Y+LineOffset)],fill=GlobalVariable.TableColors["LineNormal"],width= GlobalVariable.LineThickness)
            for X in range(3,col):
                Cursor_X = int(width/9*X)
                if  Y == 0:
                    TableOverlay.text((GlobalVariable.Cord[0]+Cursor_X,GlobalVariable.Cord[1]), GlobalVariable.Tuan[X-3], font=fnt, fill=textColor)
                    if nx_Location[0] != datetime.now().weekday() and nx_Location[0] == X-3:
                        TableOverlay.line([(GlobalVariable.Cord[0]+int(width/9*X -(width/32) ),GlobalVariable.Cord[1] ),(GlobalVariable.Cord[0]+int(width/9*X -(width/32) ),GlobalVariable.Cord[1]+height+LineOffset)],fill=GlobalVariable.TableColors["LineNext"],width= GlobalVariable.LineThickness)
                        TableOverlay.line([(GlobalVariable.Cord[0]+int(width/9*(X+1) -(width/32) ),GlobalVariable.Cord[1] ),(GlobalVariable.Cord[0]+int(width/9*(X+1) -(width/32) ),GlobalVariable.Cord[1]+height+LineOffset)],fill=GlobalVariable.TableColors["LineNext"],width= GlobalVariable.LineThickness)
                    elif  datetime.now().weekday() == X-3 and  datetime.now().weekday() < 6:
                        lineColor = GlobalVariable.TableColors["LineNormal"] if nx_Location[0] != datetime.now().weekday() else (GlobalVariable.TableColors["LineInSession"]  if coTietHomNay == 1 else GlobalVariable.TableColors["LineToday"]) 
                        TableOverlay.line([(GlobalVariable.Cord[0]+int(width/9*X -(width/32) ),GlobalVariable.Cord[1] ),(GlobalVariable.Cord[0]+int(width/9*X -(width/32) ),GlobalVariable.Cord[1]+height+LineOffset)],fill=lineColor,width= GlobalVariable.LineThickness)
                        TableOverlay.line([(GlobalVariable.Cord[0]+int(width/9*(X+1) -(width/32) ),GlobalVariable.Cord[1] ),(GlobalVariable.Cord[0]+int(width/9*(X+1) -(width/32) ),GlobalVariable.Cord[1]+height+LineOffset)],fill=lineColor,width= GlobalVariable.LineThickness)
               


            Cursor_Y = int(height*((Y+2)/len(GlobalVariable.DSTiet)))
            
        p_list_max =0
        for t_0 in range(0,len(self.DanhSachTiet)):
                baseY = int(height*((1)/len(GlobalVariable.DSTiet)))
                for t_1 in range(0,len(self.DanhSachTiet[t_0])):
                    if self.DanhSachTiet[t_0][t_1] >= 0:
                      raw_DataToWrite = self.DataTable['Tên học phần'][self.DanhSachTiet[t_0][t_1]]
                      Cursor_Y =  baseY * t_1
                      #if t_1 >= 9:
                      #    Cursor_Y -= int(height*((2)/len(GlobalVariable.DSTiet)))
                      tempCursor_Y  = Cursor_Y - baseY/3  if len(raw_DataToWrite) >= GlobalVariable.XuongDong and len(raw_DataToWrite) < GlobalVariable.VietTat else Cursor_Y
                      DataToWrite = raw_DataToWrite
                      if len(raw_DataToWrite) >= GlobalVariable.VietTat:
                         UpcaseList = [a[0] for a in  raw_DataToWrite.split(" ") ]
                         DataToWrite = ""
                         
                         for char_1 in UpcaseList:
                             DataToWrite += char_1.upper()
                         if [DataToWrite,raw_DataToWrite] not in self.BangVietTat:
                            self.BangVietTat.append([DataToWrite,raw_DataToWrite])
                      elif len(raw_DataToWrite) >= GlobalVariable.XuongDong:
                        for char in range(GlobalVariable.XuongDong -1,-1,-1):
                         if raw_DataToWrite[char] == " ":
                            DataToWrite = raw_DataToWrite[:char] + "\n" + raw_DataToWrite[char:]
                            break
                      Cursor_X = int(width/9*(t_0+3))
                      Console.Log(Cursor_X,Cursor_Y,tempCursor_Y,DataToWrite)
                      TableOverlay.text((GlobalVariable.Cord[0]+Cursor_X - (width/9/4) ,GlobalVariable.Cord[1]+tempCursor_Y),DataToWrite, font=fnt, fill=textColor)
        #for i in [ f for f in self.DanhSachTiet[nx_Location[0]] if f != -1]:
        st_ = "Tiết tiếp theo: " if coTietHomNay != 1 else "Đang trong tiết: "
        tietTiepTheo_Str = st_+ self.DataTable['Tên học phần'][IDTiethoc] +"      Thời gian "+str(nx_Period.hour)+"h"+str(nx_Period.minute if not nx_Period.minute < 10 else "0" +str(nx_Period.minute))+"  ngày "+str(nx_Period.day)+"/"+str(nx_Period.month)+"/"+str(nx_Period.year)
        if type(self.DataTable['Giáo viên'][IDTiethoc]) is str:
            tenGV = ' '.join(self.unique_list(self.DataTable['Giáo viên'][IDTiethoc].split(" ")))
            tietTiepTheo_Str += "  Giáo viên: "+ tenGV
        if type(self.DataTable['Phòng học'][IDTiethoc]) is str:
            tenLOP = ' '.join(self.unique_list(self.DataTable['Phòng học'][IDTiethoc].split(" ")))
            tietTiepTheo_Str += "  Phòng học: "+tenLOP
        tietTiepTheo_Str += "\n"
        for vt in self.BangVietTat:
            tietTiepTheo_Str += "\n"+vt[0] + ": "+ vt[1]
        TableOverlay.text((GlobalVariable.Cord[0]+ width*0.12,GlobalVariable.Cord[1]+height*(1.05+(p_list_max/20))),tietTiepTheo_Str, font=fnt, fill=textColor)
        #p_list_max += 1
        if GlobalVariable.EnableBG == True:
            out = Image.alpha_composite(BG, Overlay)
            out.save(str(GlobalVariable.ABSOLUTE_OUTPUT_PATH[1:]))
            img_path = os.getcwd()+GlobalVariable.ABSOLUTE_OUTPUT_PATH
            ctypes.windll.user32.SystemParametersInfoW(20,0,img_path,1)
        


Main()