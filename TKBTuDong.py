
# CREDIT: DUONG TUNG AI&RB-K15 PKA
import ctypes
ABSOLUTE_BASE_PATH = 'D:\\2021-2022\\TKB\\TKBTuDong\\sample.jpg'
ctypes.windll.user32.SystemParametersInfoW(20,0,ABSOLUTE_BASE_PATH,0)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import logging
from datetime import datetime,timedelta,time,date
from win10toast import ToastNotifier
import os
import math
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import base64
import codecs
from cryptography.fernet import Fernet
from time import sleep
import urllib3
from GoogleCalendar import Calendar
try:
    os.mkdir("./LogFiles/")
except :
    pass
format = "%(asctime)s: %(message)s"
logname =  "./LogFiles/Log_"+str(datetime.now().month) +"_"+ str(datetime.now().day)+"_"+ str(datetime.now().hour)+"_"+ str(datetime.now().minute)+".log"
logging.basicConfig(filename=logname,format=format, level=logging.INFO,datefmt="%H:%M:%S")

class GlobalVariable():
    KeyFiles = "UserKey.enc"
    UserDataFile = "UserData.enc"
    BackGroundFile = "./sample.jpg"
    GoogleCalendarIDsFile = "GoogleCalendarIDs.txt"
    Font = "calibril.ttf"
    GoogleCalendarDeleteEventTime = 7
    ABSOLUTE_OUTPUT_PATH = "\\output.png"
    LoginURL = 'https://qldt.phenikaa-uni.edu.vn/Login.aspx'
    LichHocURL = 'https://qldt.phenikaa-uni.edu.vn/wfrmDangKyLopTinChiB3.aspx'
    UserData_check = False
    Tuan = ["Thứ 2","Thứ 3", "Thứ 4","Thứ 5","Thứ 6","Thứ 7"]
    ThoiGianBieu = ["7h30 - 8h20","8h25 - 9h15","9h20 - 10h10","10h15 - 11h05","11h10 - 12h00","13h00 - 13h50","13h55 - 14h45","14h50 - 15h40","15h45 - 16h35","16h40 - 17h30","17h35 - 18h25","18h30 - 19h20"]
    DSTiet = [ "Tiết "+str(t_) for t_ in range(1,13) ]
    SoNgayHienThi = 7
    width, height = 2400,1200 #TABLE
    Cord = [-200,1200]
    XuongDong = 10
    TextAlpha = 200
    LineThickness = 2
    CREDENTIALS_FILE = './client_secret_431692909921-5oud82jo99c4sfne77c96t2livor8rvd.apps.googleusercontent.com.json'
    internet_connected = True

class Tiet(): #Tiet trong ngay
    def __init__(self,tiet = 0, ID_mon = "",Thu = 0):
        self.tiet = tiet
        self.ID_mon = ID_mon 
        self.Thu = Thu
        Console.Log("Da them tiet",ID_mon,"Tiet so",tiet,"Vao thu",GlobalVariable.Tuan[Thu])

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
            opts.set_headless() 
            assert opts.headless  # Operating in headless mode  options=opts
            self.driver = webdriver.Chrome('D:\\2021-2022\\TKB\\TKBTuDong\\chromedriver.exe',options=opts)  # Optional argument, if not specified will search path.
            #self.driver.execute(Command.SET_TIMEOUTS, {'ms': float(15 * 1000), 'type': 'page load'})
            self.Login()
            Console.Log("Dang nhap thanh cong")
            if GlobalVariable.UserData_check == False:
                if input("Ban co muon luu ten dang nhap va mat khau? y/n ").lower() == "y":
                    self.SaveUserData()
            self.driver.get(GlobalVariable.LichHocURL)
            sleep(1)
            self.PageSource = self.driver.page_source
            with codecs.open("pageBackup.html","w+","utf-8") as f:
                f.write(str(self.PageSource))
                f.close()
            GlobalVariable.internet_connected = True
        self.DataTable = pd.read_html(self.PageSource,attrs={'id':'grdViewLopDangKy'})[0]
        Console.Log("Lay thong tin thanh cong")
        Console.Log(self.DataTable)
        Console.Log("Xu li du lieu...")
        self.DataProcess()
        Console.Log("Xu li du lieu hoan tat")
        Console.Log("Khoi tao bang...")
        self.CreateTable()
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
        GlobalVariable.UserData_check = True
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
        except:
            Console.Error("File loi hoac khong tim thay file nguoi dung")
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
        try :
            G_file = open(GlobalVariable.GoogleCalendarIDsFile,"r+")
            G_dat = G_file.read().split("|\n|")
        except:
            Console.Warning("IDs file not found, creating...")
            G_file = open(GlobalVariable.GoogleCalendarIDsFile,"w+")
            G_dat = G_file.read().split("|\n|")
        gg_event_range = [datetime(1900,1,1),datetime(1900,1,1)]
        if G_dat[0] != "" and GlobalVariable.internet_connected == True:
            for data_ in G_dat:
                ID = data_.split("|DT|")[0]
                ev_time  = datetime.fromisoformat(data_.split("|DT|")[1])
                if datetime.now() - ev_time >= timedelta(GlobalVariable.GoogleCalendarDeleteEventTime):
                    Calendar.DeleteEvent(ID)
                    Console.Log("Deleting event",ID)
        G_data_to_write = ""
        for next_d in range(0,7):
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
                     if (GlobalVariable.internet_connected == True):
                         result = []
                         if self.DanhSachTiet[thu][tiet +1] == self.DanhSachTiet[thu][tiet]:
                             gg_event_range[0] = start_t
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
                             result_id,result_sum,result_start,result_end = Calendar(GlobalVariable.CREDENTIALS_FILE).CreateEvent(self.DataTable['Tên học phần'][self.DanhSachTiet[thu][tiet]],desc,start_t.isoformat(),end_t.isoformat(),tenGV,tenLOP)
                             Console.Log("created event")
                             Console.Log("id: ", result_id)
                             Console.Log("summary: ", result_sum)
                             Console.Log("starts at: ", result_start)
                             Console.Log("ends at: ", result_end)
                             #result['id'],result['summary'],result['start']['dateTime'],result['end']['dateTime']
                             G_data_to_write += str(result_id)+"|DT|"+result_start+"|\n|"
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
                             result_id,result_sum,result_start,result_end = Calendar(GlobalVariable.CREDENTIALS_FILE).CreateEvent(self.DataTable['Tên học phần'][self.DanhSachTiet[thu][tiet]],desc,gg_event_range[0].isoformat(),gg_event_range[1].isoformat(),tenGV,tenLOP)
                             #Subject = "",desc = "",start = datetime(),end = datetime(),organizer = "",location = ''
                             Console.Log("created event")
                             Console.Log("id: ", result_id)
                             Console.Log("summary: ", result_sum)
                             Console.Log("starts at: ", result_start)
                             Console.Log("ends at: ", result_end)
                             #result['id'],result['summary'],result['start']['dateTime'],result['end']['dateTime']
                             G_data_to_write += str(result_id)+"|DT|"+result_start+"|\n|"

                         
                     if exec_time >= start_t and  exec_time <= end_t:
                        Console.Log("In session")
                        next_P_location = [self.DanhSachTiet.index(self.DanhSachTiet[thu]),tiet]
                        return 1,end_t,next_P_location

                     elif (next_P - exec_time) > (start_t - exec_time) and exec_time < end_t:

                        Console.Log("Changed order", next_P,"compare to",start_t)
                        next_P = start_t
                        next_P_location = [self.DanhSachTiet.index(self.DanhSachTiet[thu]),tiet]
        Console.Log("Tiep theo la tiet",next_P_location)
        G_file.write(G_data_to_write)
        G_file.flush()
        G_file.close()
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
        
        for STT in range(0,self.SoMonHoc):
            LH = self.DataTable['Lịch học'][STT]#.astype('string')
            EndDateStr = LH.split("-")[0][:str(LH).find("Th")]
            EndDate = datetime.strptime(EndDateStr,'%d/%m/%y')
            ThuTrongTuan = [ int(thu[:thu.find("(")]) - 2 for thu in LH.split("Thứ ")[1:]] #0-6
            Tiet_ = [ tiet_[:tiet_.find(")")] for tiet_ in LH.split("(T")[1:]  ] # 1-2
            for Thu in range(0,len(ThuTrongTuan)):
                    DSTietgioihan_ngay = [int(t) for t in Tiet_[Thu].split("-")]
                    DStiet_ngay = [ t_ for t_ in range(DSTietgioihan_ngay[0],DSTietgioihan_ngay[1]+1)]
                    for tietTrongDSngay in DStiet_ngay:
                        self.DanhSachTiet[ThuTrongTuan[Thu]][tietTrongDSngay] = STT
            Console.Log(ThuTrongTuan)       
    def CreateTable(self):
        BG = Image.open(GlobalVariable.BackGroundFile).convert("RGBA")
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
        #TableOverlay.rectangle([(GlobalVariable.Cord[0]+(width/9*nx_Location[0]),GlobalVariable.Cord[1]+int(height*((nx_Location[1]+2)/len(GlobalVariable.DSTiet)))- LineOffset/2),     (GlobalVariable.Cord[0]+(width/9*nx_Location[0])+((width/9)*0.6),GlobalVariable.Cord[1]+int(height*((nx_Location[1]+2)/len(GlobalVariable.DSTiet)))+ LineOffset/2)],None,"#e1ed00",GlobalVariable.width)
        for Y in range(0,len(GlobalVariable.DSTiet)):
            Cursor_X = int(width/9)
            
            TableOverlay.text((GlobalVariable.Cord[0]+Cursor_X,GlobalVariable.Cord[1]+Cursor_Y), GlobalVariable.DSTiet[Y], font=fnt, fill=(255,255,255,GlobalVariable.TextAlpha))
            Cursor_X = int(width/9*1.7)
            TableOverlay.text((GlobalVariable.Cord[0]+Cursor_X,GlobalVariable.Cord[1]+Cursor_Y), GlobalVariable.ThoiGianBieu[Y], font=fnt, fill=(255,255,255,GlobalVariable.TextAlpha))
            TableOverlay.line([(GlobalVariable.Cord[0]+int(width/9),GlobalVariable.Cord[1]+Cursor_Y+ LineOffset),(GlobalVariable.Cord[0]+GlobalVariable.width-LineOffset*1.47,GlobalVariable.Cord[1]+Cursor_Y+LineOffset)],fill="#FFFFFF",width= GlobalVariable.LineThickness)
            for X in range(3,col):
                if self.DanhSachTiet[X-3][Y-1] >= 0:
                    raw_DataToWrite = self.DataTable['Tên học phần'][self.DanhSachTiet[X-3][Y-1]]
                    Console.Log("Cursor position: ", Cursor_X,Cursor_Y,raw_DataToWrite)
                else:
                    raw_DataToWrite = ""
                DataToWrite = raw_DataToWrite
                tempCursor_Y  = Cursor_Y - (height/len(GlobalVariable.DSTiet)*2.3) if len(raw_DataToWrite) >= GlobalVariable.XuongDong else Cursor_Y
                if len(raw_DataToWrite) >= GlobalVariable.XuongDong:
                    for char in range(GlobalVariable.XuongDong,-1,-1):
                        if raw_DataToWrite[char] == " ":
                            DataToWrite = raw_DataToWrite[:char] + "\n" + raw_DataToWrite[char:]
                            break
                Cursor_X = int(width/9*X)
                if  Y == 0:
                    TableOverlay.text((GlobalVariable.Cord[0]+Cursor_X,GlobalVariable.Cord[1]+tempCursor_Y),DataToWrite, font=fnt, fill=(255,255,255,GlobalVariable.TextAlpha))
                    TableOverlay.text((GlobalVariable.Cord[0]+Cursor_X,GlobalVariable.Cord[1]), GlobalVariable.Tuan[X-3], font=fnt, fill=(255,255,255,GlobalVariable.TextAlpha))
                    if nx_Location[0] != datetime.now().weekday() and nx_Location[0] == X-3:
                        TableOverlay.line([(GlobalVariable.Cord[0]+int(width/9*X -(width/32) ),GlobalVariable.Cord[1] ),(GlobalVariable.Cord[0]+int(width/9*X -(width/32) ),GlobalVariable.Cord[1]+height+LineOffset)],fill="#ffe600",width= GlobalVariable.LineThickness)
                        TableOverlay.line([(GlobalVariable.Cord[0]+int(width/9*(X+1) -(width/32) ),GlobalVariable.Cord[1] ),(GlobalVariable.Cord[0]+int(width/9*(X+1) -(width/32) ),GlobalVariable.Cord[1]+height+LineOffset)],fill="#ffe600",width= GlobalVariable.LineThickness)
                    elif  datetime.now().weekday() == X-3 and  datetime.now().weekday() < 6:
                        lineColor = "#ffffff" if nx_Location[0] != datetime.now().weekday() else ("#fc0303"  if coTietHomNay == 1 else "#2200ff") 
                        TableOverlay.line([(GlobalVariable.Cord[0]+int(width/9*X -(width/32) ),GlobalVariable.Cord[1] ),(GlobalVariable.Cord[0]+int(width/9*X -(width/32) ),GlobalVariable.Cord[1]+height+LineOffset)],fill=lineColor,width= GlobalVariable.LineThickness)
                        TableOverlay.line([(GlobalVariable.Cord[0]+int(width/9*(X+1) -(width/32) ),GlobalVariable.Cord[1] ),(GlobalVariable.Cord[0]+int(width/9*(X+1) -(width/32) ),GlobalVariable.Cord[1]+height+LineOffset)],fill=lineColor,width= GlobalVariable.LineThickness)
                else:
                    TableOverlay.text((GlobalVariable.Cord[0]+Cursor_X - (width/9/4) ,GlobalVariable.Cord[1]+tempCursor_Y),DataToWrite, font=fnt, fill=(255,255,255,GlobalVariable.TextAlpha))


            Cursor_Y = int(height*((Y+2)/len(GlobalVariable.DSTiet)))
            
        p_list_max =0
        #for i in [ f for f in self.DanhSachTiet[nx_Location[0]] if f != -1]:
        st_ = "Tiết tiếp theo: " if coTietHomNay != 1 else "Đang trong tiết: "
        tietTiepTheo_Str = st_+ self.DataTable['Tên học phần'][IDTiethoc] +"              Thời gian "+str(nx_Period.hour)+"h"+str(nx_Period.minute if not nx_Period.minute < 10 else "0" +str(nx_Period.minute))+"  ngày "+str(nx_Period.day)+"/"+str(nx_Period.month)+"/"+str(nx_Period.year)
        if type(self.DataTable['Giáo viên'][IDTiethoc]) is str:
            tenGV = ' '.join(self.unique_list(self.DataTable['Giáo viên'][IDTiethoc].split(" ")))
            tietTiepTheo_Str += "  Giáo viên: "+ tenGV
        if type(self.DataTable['Phòng học'][IDTiethoc]) is str:
            tenLOP = ' '.join(self.unique_list(self.DataTable['Phòng học'][IDTiethoc].split(" ")))
            tietTiepTheo_Str += "  Phòng học: "+tenLOP
        TableOverlay.text((GlobalVariable.Cord[0]+ width*0.12,GlobalVariable.Cord[1]+height*(1.05+(p_list_max/20))),tietTiepTheo_Str, font=fnt, fill=(255,255,255,GlobalVariable.TextAlpha))
        #p_list_max += 1
        out = Image.alpha_composite(BG, Overlay)
        out.save(str(GlobalVariable.ABSOLUTE_OUTPUT_PATH[1:]))
        img_path = os.getcwd()+GlobalVariable.ABSOLUTE_OUTPUT_PATH
        ctypes.windll.user32.SystemParametersInfoW(20,0,img_path,1)
        


Main()