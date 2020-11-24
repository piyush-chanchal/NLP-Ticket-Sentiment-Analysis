# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 01:26:45 2020

@author: ChanchalP
"""

from tkinter import *
import requests
import json
import os
from textblob import TextBlob
#import textblob

#----------------------------------------------------------------------

class MainWindow():

    #----------------

    def __init__(self, root):
       
       
        self.bgColor = "#48D1CC"
       
       
        self.base_folder=os.path.dirname(os.path.abspath(__file__))
        photo = PhotoImage(file = str(self.base_folder) + r"/images/Icon.png")
        root.iconphoto(False, photo)
       
        root.configure(background=self.bgColor)
        root.title("Freshdesk Ticket Analysis")
        root.geometry("600x300")
         
        root.minsize(600,300)
       
        root.maxsize(900,500)
         
        self.heading = Label(root, text="Ticket Details", bg=self.bgColor,font=("Times", 16,"bold"))
         
        # create a Domain name label
        self.domainName = Label(root, text="Domain name", bg=self.bgColor,font=("Times", 11))
         
        self.apiKey = Label(root, text="API Key", bg=self.bgColor,font=("Times", 11))
         
        self.ticketNumber = Label(root, text="Ticket Number", bg=self.bgColor,font=("Times", 11))
       
       
       
        self.heading.grid(row=0, column=1)
        self.domainName.grid(row=1, column=0)
        self.apiKey.grid(row=2, column=0)
        self.ticketNumber.grid(row=3, column=0)
       
        self.txtBoxCol = "#F5F5F5"
       
        self.domain_field = Entry(root,bg=self.txtBoxCol)
        self.api_field = Entry(root,bg=self.txtBoxCol)
        self.ticket_field = Entry(root,bg=self.txtBoxCol)
       
       
        self.domain_field.grid(row=1, column=1, ipadx="100")
        self.api_field.grid(row=2, column=1, ipadx="100")
        self.ticket_field.grid(row=3, column=1, ipadx="100")
       
       
       
        global submitCNT
        global image_id
        global canvas
       
        submitCNT = 0
       
        # create a Submit Button and place into the root window
        self.submit = Button(root,font=("Times", 13),height=1,width=15, text="Submit", fg="#F5F5F5",bg="#696969",command=self.FdTicket)
        self.submit.grid(row=4, column=1)
#        
       
        self.empFrame = Frame(root)
        self.empFrame.grid(row=5)
       
       
       
        self.aRes = Frame(root,bg="#E0FFFF",height=165,width=225)
        self.aRes.grid(row=6, ipadx="186",columnspan=3)
       
       
        ############Menu section
        self.menu = Menu(root)
        root.config(menu=self.menu)
        self.filemenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='Exit', command=root.destroy)
       
        self.OpValue = IntVar(root)
        global submitOps
        submitOps = 0
       
        self.ExportMenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Analysis', menu=self.ExportMenu)
        self.ExportMenu.add_radiobutton(label='Text Analysis',var = self.OpValue, value=0, command=lambda idx=0: self.fun1(idx))
        self.ExportMenu.add_radiobutton(label='Fetch Ticket Details',var = self.OpValue, value=1, command=lambda idx=1: self.fun1(idx))
        self.helpmenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Help', menu=self.helpmenu)
        self.helpmenu.add_command(label='About',command=self.aboutMenu)
        ##############End of menu section
       

       
       
    def TextAnalysis(self):
        if hasattr(self,'canvas'):
            self.canvas.grid_forget()
        if hasattr(self,'canvas2'):
            self.canvas2.grid_forget()
        if hasattr(self,'canvas3'):
            self.canvas3.grid_forget()
        if hasattr(self,'canvas4'):
            self.canvas4.grid_forget()
        if hasattr(self,'aRes'):
            self.aRes.grid_forget()
        global ticket_id
        ticket_id=self.ticket_field.get()
        global submitCNT
        submitCNT = submitCNT + 1
       
       
        self.api_key = str(self.api_field.get())
        self.domain = str(self.domain_field.get())
        self.password = "x"
       
       
        self.r = requests.get("https://"+ self.domain +".freshdesk.com/api/v2/tickets/"+ticket_id + "/conversations", auth = (self.api_key, self.password))
       
        if self.r.status_code == 200:
          self.response = json.loads(self.r.content)
        else:
          self.errMsg = "Entered value in form fields are not valid."
          self.passMsg = self.errMsg
          self.errWin()
         
        self.txtvar = self.response[-1]['body_text']
        self.txtvar = self.txtvar + self.response[-2]['body_text']
        self.txtvar = self.txtvar + self.response[-3]['body_text']
        self.txtvar = self.txtvar + self.response[-4]['body_text']
        self.txtvar = self.txtvar + self.response[-5]['body_text']
       
       
       
       
       
       
       
#        self.passMsg = "Ident3"+str(submitCNT)
#        self.errWin()
       
        self.analysis = TextBlob(self.txtvar)
       
        global polarity
        polarity = self.analysis.sentiment.polarity
       
        global subjectivity
        subjectivity= self.analysis.sentiment.subjectivity
       
        global sentText
        global canvas
        global image_id
         
        if polarity<=-0.49:
            self.sentText = "Extreme Negative"
        if polarity<=-0.86 and polarity>=-0.50:
            self.sentText = "Negative"
        if polarity<=0.16 and polarity>=-0.86:
            self.sentText = "Neutral"
        if polarity>=0.17 and polarity<=0.49:
            self.sentText = "Positive"
        if polarity>=0.5:
            self.sentText = "Extreme Positive"
       
       
        self.aRes.grid_forget()
       
        if ((polarity+subjectivity)/2)>0.33:
            self.prediction = "Good"
            self.emojiFile = "Good.png"
        if ((polarity+subjectivity)/2)<=0.33 and ((polarity+subjectivity)/2)>-0.66:
            self.prediction = "Average"
            self.emojiFile = "Average.png"
        if ((polarity+subjectivity)/2)<=-0.66:
            self.prediction = "Poor"
            self.emojiFile = "Poor.png"
        self.base_folder = os.path.dirname(os.path.abspath(__file__))
        self.emojiPath = os.path.join(self.base_folder,r"images/", self.emojiFile)
       
       
       
       
        if submitCNT==1:
            self.canvas2 = Canvas(root, width = 200, height = 20,bg="#483D8B")
            self.txt_id2 = self.canvas2.create_text(80,10,fill="#FFFFFF",text="Rating Prediction",font=("Times",12,"bold"))
            self.canvas2.grid(row=7,column=0)

            self.canvas = Canvas(root, width = 200, height = 140,bg="#E0FFFF")
            self.img = PhotoImage(file = self.emojiPath)
            self.image_id = self.canvas.create_image(0, 0, anchor=NW, image=self.img)
            self.refImg = self.img
            self.txt_id = self.canvas.create_text(140,50,text=self.prediction,font=("Times",13))
            self.canvas.grid(row=8,column=0)
#            self.passMsg = "Test:"+self.emojiPath
#            self.errWin()
       
        if submitCNT>=2:
            self.canvas2 = Canvas(root, width = 200, height = 20,bg="#483D8B")
            self.txt_id2 = self.canvas2.create_text(80,10,fill="#FFFFFF",text="Rating Prediction",font=("Times",12,"bold"))
            self.canvas2.grid(row=7,column=0)
            self.canvas = Canvas(root, width = 200, height = 140,bg="#E0FFFF")
            self.img = PhotoImage(file = self.emojiPath)
            self.image_id = self.canvas.create_image(0, 0, anchor=NW, image=self.img)
            self.refImg2 = self.img
            self.txt_id = self.canvas.create_text(140,50,text=self.prediction,font=("Times",13))
            self.canvas.grid(row=8,column=0)
            self.imgChange()
#            self.passMsg = "Test:"+self.emojiPath
#            self.errWin()
           

       
        self.canvas3 = Canvas(root, width = 375, height = 60,bg=self.bgColor)
       
                             
        self.canvas3.grid(row=8,column=1)
       
       
        self.canvas3.create_rectangle(5, 0, 100, 30,fill="#ffffff")
       

       
        self.canvas3.create_rectangle(101, 0, 200, 30,fill="#ffffff")
       
       
        self.canvas3.create_rectangle(201, 0, 375, 30,fill="#ffffff")
       
       
        self.canvas3.create_rectangle(5, 31, 100, 60,fill="#ffffff")
       
        self.canvas3.create_rectangle(101, 31, 200, 60,fill="#ffffff")
       
       
        self.canvas3.create_rectangle(201, 31, 375, 60,fill="#ffffff")
       
        self.canvas3.create_text(20, 7, text="Polarity",fill="black",anchor="nw",font=("times",14,"bold"))
       
        self.canvas3.create_text(104, 7, text="Subjectivity",fill="black",anchor="nw",font=("times",14,"bold"))

        self.txtSubCol = self.canvas3.create_text(204, 7, text="Sentiment Analysis",fill="black",anchor="nw",font=("times",14,"bold"))
       
        self.canvas3.create_text(10, 37, text=str(round(float(polarity),2)),fill="black",anchor="nw",font=("times",14))
        self.canvas3.create_text(110, 37, text=str(round(float(subjectivity),2)),fill="black",anchor="nw",font=("times",14))
        self.canvas3.create_text(210, 37, text=str(self.sentText),fill="black",anchor="nw",font=("times",14))
   
       
    def FetchDetails(self):
        if hasattr(self,'canvas'):
            self.canvas.grid_forget()
        if hasattr(self,'canvas2'):
            self.canvas2.grid_forget()
        if hasattr(self,'canvas3'):
            self.canvas3.grid_forget()
        if hasattr(self,'canvas4'):
            self.canvas4.grid_forget()
        if hasattr(self,'aRes'):
            self.aRes.grid_forget()
       
#        self.aRes = Frame(root,bg="#E0FFFF",height=165,width=225)
#        self.aRes.grid(row=6, ipadx="186",columnspan=3)
        self.canvas4 = Canvas(root, width = 550, height = 200,bg=self.bgColor)
        self.canvas4.grid(row=8,column=0,columnspan=3)
        self.canvas4.create_rectangle(5, 0, 120, 30,fill="#ffffff")
       

       
        self.canvas4.create_rectangle(121, 0, 240, 30,fill="#ffffff")
       
       
        self.canvas4.create_rectangle(241, 0, 400, 30,fill="#ffffff")
       
       
        self.canvas4.create_rectangle(5, 31, 120, 60,fill="#ffffff")
       
        self.canvas4.create_rectangle(121, 31, 240, 60,fill="#ffffff")
       
       
        self.canvas4.create_rectangle(241, 31, 400, 60,fill="#ffffff")
                                     
        self.canvas4.create_rectangle(401, 0, 550, 30,fill="#ffffff")
        self.canvas4.create_rectangle(401, 31, 550, 60,fill="#ffffff")
                                     
        self.canvas4.create_rectangle(5, 70, 120, 90,fill="#ffffff")
        self.canvas4.create_rectangle(5, 91, 120, 120,fill="#ffffff")
        self.canvas4.create_rectangle(5, 121, 120, 150,fill="#ffffff")
                                     
        self.canvas4.create_text(7, 70, text="User Name",fill="black",anchor="nw",font=("times",14,"bold"))
        self.canvas4.create_text(7, 95, text="Email Id",fill="black",anchor="nw",font=("times",14,"bold"))
        self.canvas4.create_text(7, 125, text="Ticket Title",fill="black",anchor="nw",font=("times",14,"bold"))
                                     
                                     
        self.canvas4.create_rectangle(121, 70, 550, 90,fill="#ffffff")
        self.canvas4.create_rectangle(121, 91, 550, 120,fill="#ffffff")
        self.canvas4.create_rectangle(121, 121, 550, 150,fill="#ffffff")
                                     
        self.r = requests.get("https://"+ self.domain +".freshdesk.com/api/v2/tickets/"+ticket_id + "/conversations", auth = (self.api_key, self.password))
       
        if self.r.status_code == 200:
          self.response = json.loads(self.r.content)
        else:
          self.errMsg = "Entered value in form fields are not valid."
         
          self.passMsg = self.errMsg
          self.errWin()
         
         

       
       
        self.tInfo = requests.get("https://"+ self.domain +".freshdesk.com/api/v2/tickets/"+ ticket_id , auth = (self.api_key, self.password))
        if self.tInfo.status_code == 200:
            self.tResponse3 = json.loads(self.tInfo.content)
        else:
            self.errMsg = "Entered value in form fields are not valid."
           
            self.passMsg = self.errMsg
            self.errWin()
           
           
        self.tDetails = requests.get("https://"+ self.domain +".freshdesk.com/api/v2/tickets/"+ ticket_id + "?include=requester", auth = (self.api_key, self.password))
        if self.tDetails.status_code == 200:
            self.tResponse = json.loads(self.tDetails.content)
        else:
            self.errMsg = "Entered value in form fields are not valid."
           
            self.passMsg = self.errMsg
            self.errWin()
         
        usrName = str(self.tResponse['requester']['name'])
           
           
        self.canvas4.create_text(124, 71, text=usrName,fill="black",anchor="nw",font=("times",12))
        self.canvas4.create_text(124, 92, text=str(self.tResponse['requester']['email']),fill="black",anchor="nw",font=("times",12))
        self.canvas4.create_text(124, 122, text=str(self.tResponse3['subject']),fill="black",anchor="nw",font=("times",12))
       
        self.canvas4.create_text(10, 7, text="Ticket#",fill="black",anchor="nw",font=("times",14,"bold"))
       
        self.canvas4.create_text(124, 7, text="Agent Id",fill="black",anchor="nw",font=("times",14,"bold"))

        self.canvas4.create_text(244, 7, text="Date Created",fill="black",anchor="nw",font=("times",14,"bold"))
        self.canvas4.create_text(404, 7, text="Date Resolved",fill="black",anchor="nw",font=("times",14,"bold"))
       
       

        self.canvas4.create_text(10, 37, text=str(ticket_id),fill="black",anchor="nw",font=("times",12))
        self.canvas4.create_text(130, 37, text=str(self.tResponse['responder_id']),fill="black",anchor="nw",font=("times",12))
       
        self.tStats = requests.get("https://"+ self.domain +".freshdesk.com/api/v2/tickets/"+ ticket_id + "?include=stats", auth = (self.api_key, self.password))
        if self.tStats.status_code == 200:
            self.tResponse2 = json.loads(self.tStats.content)
        else:
            self.errMsg = "Entered value in form fields are not valid."
           
            self.passMsg = self.errMsg
            self.errWin()
           
       
        self.canvas4.create_text(250, 37, text=str(self.tResponse2['stats']['first_responded_at'])[0:10],fill="black",anchor="nw",font=("times",12))
        self.canvas4.create_text(410, 37, text=str(self.tResponse2['stats']['resolved_at'])[0:10],fill="black",anchor="nw",font=("times",12))
   
   
    def formVal(self):
        self.blankFields=""
        if (str(ticket_id)==""):
            self.blankFields="Ticket ID"
        if(str(self.api_key)==""):
            if not(self.blankFields==""):
                self.blankFields = self.blankFields + "," + "API Key"
            else:
                self.blankFields = "API Key"
        if(str(self.domain)==""):
            if not(self.blankFields==""):
                self.blankFields = self.blankFields + "," + "Domain"
            else:
                self.blankFields = "Domain"
        if not(self.blankFields==""):
            if not(self.blankFields.find(",")==-1):
                self.passMsg="Fields "+self.blankFields + " are blank, please resubmit."
            else:
                self.passMsg="Field "+self.blankFields + " is blank, please resubmit."
            self.errWin()

       
    def FdTicket(self):
        global ticket_id
        ticket_id=self.ticket_field.get()

        self.api_key = str(self.api_field.get())
        self.domain = str(self.domain_field.get())
        self.password = "x"
        self.formVal()
        if(submitOps==0):
            self.TextAnalysis()
        elif(submitOps==1):
            self.FetchDetails()
   
    def imgChange(self):
        # change image
        self.img = PhotoImage(file = self.emojiPath)
        self.canvas.itemconfig(self.image_id, image = self.img)
        self.canvas.itemconfig(self.txt_id, text = self.prediction)

       
   
    def fun1(self,value):
        global submitOps
        submitOps=value
   
       
    def errWin(self):
       self.AbtWin = Toplevel(root)
       self.AbtWin.overrideredirect(1)
       self.AbtWin.configure(bg="#DCDCDC",bd=1)
       self.AbtWin.geometry("+300+300")
       self.Msg = Message(self.AbtWin, text=self.passMsg,bg='#F5F5F5')
       self.Msg.pack()
       self.OKBtn= Button(self.AbtWin,text='OK',width=10,command=self.AbtWin.destroy,bg='#696969',fg='#ffffff')
       self.OKBtn.pack()
       self.AbtWin.mainloop()
     
    def aboutMenu(self):
       self.AbtWin = Toplevel(root)
       self.AbtWin.overrideredirect(1)
       self.AbtWin.configure(bg="#000000",bd=1)
       self.AbtWin.geometry("173x143+300+300")
       self.Msg = Message(self.AbtWin, text="This application is developed in Python by using TextBlob and TKinter library. In case of any concern, please contact to email id Piyush.Chanchal@hotmail.com",bg='#F5F5F5')
       self.Msg.pack()
       self.OKBtn= Button(self.AbtWin,text='OK',width=173,command=self.AbtWin.destroy,bg='#696969',fg='#ffffff')
       self.OKBtn.pack()
       self.AbtWin.mainloop()

#----------------------------------------------------------------------

root = Tk()
MainWindow(root)
root.mainloop()