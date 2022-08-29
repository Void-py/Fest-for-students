from tkinter import *
import tkinter.font as font
from PIL import ImageTk,Image
import mysql.connector as connector_
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk
import repackage
repackage.up()
from Src.custom_text import ScrolledText
import sys
import time
import tkinter.filedialog as fd
#all_val has all the values req for writing the test ...refer that idiot
class Base(Tk):
    def __init__(self):
        super().__init__()
        try:
            self.main_database = connector_.connect(host="localhost",user="root",password="",database="Fest_for_students")
            self.cursor_1 = self.main_database.cursor()
        except connector_.errors.ProgrammingError:
            self.main_database = connector_.connect(host="localhost",user="root",password="")
            self.cursor_1 = self.main_database.cursor()
            self.cursor_1.execute("CREATE DATABASE Fest_for_students;")
            self.cursor_1.execute("USE DATABASE Fest_for_students;")
            self.cursor_1.execute("""CREATE TABLE user_data
                                  (User_id varchar(70) primary key,
                                  Username varchar(70) unique,
                                  Grade int not null,
                                  Section char(1) not null
                                  password int(11))
                                  role varchar(30));""")
            self.cursor_1.execute("""CREATE TABLE tests
                                    (test_id int primary key,
                                    applicants longblob not null,
                                    test_name varchar(50) not null),
                                    host varchar(255) not null,
                                    scheduled_time varchar(255) not null
                                    test_questions longblob not null;""")
        self.cursor_1.execute("USE fest_for_students;")
        self.title("Fest for students")
        self.geometry("800x500")
        self.resizable(0,0)
        self.tree_font = font.Font(family="Century Gothic", weight="normal", size=10)
        self.font_title = font.Font(family="Gabriola", weight="bold", slant="roman",size=25)
        self.font_all = font.Font(family="Gabriola",weight="bold",slant="roman")
        self.font_general = font.Font(family="Comic Sans MS",weight="bold",slant="roman")
        self.label_2 = Label(self,text="FEST-FOR-STUDENTS",bg="#f5f4b0",fg="#1a181c",font=self.font_title)
        self.label_2.place(x=415,y=10)
        self.entry_1 = Entry(self,bd=10,bg="lime green",fg="black",font=self.font_general,relief=RIDGE,highlightcolor="grey")
        self.entry_1.place(x=300,y=110)
        self.entry_2 = Entry(self,bd=10,bg="lime green",fg="black",font=self.font_general,relief=RIDGE,highlightcolor="grey")
        self.entry_2.place(x=300,y=210)
        self.entry_1.insert(0,"Username")
        self.entry_2.insert(0, "Password")
        self.button_1 = Button(self,text="Login",fg="black",bg="lime green",bd=5,relief=RIDGE,activebackground="#f5f4b0",font=self.font_general,highlightbackground="black",highlightcolor="black",width=10,command=lambda:self.login())
        self.button_1.place(x=495,y=300)
        self.button_2 = Button(self, text="Sign up", fg="black", bg="lime green", bd=5, relief=RIDGE,activebackground="#f5f4b0", font=self.font_general, highlightbackground="black",highlightcolor="black", width=10,command=lambda:self.sign_up())
        self.button_2.place(x=335,y=300)
    def login(self):
        try:
            self.user_name = str(self.entry_1.get())
            self.password = int(self.entry_2.get())
            self.cursor_1.execute("SELECT * FROM user_data")
            self.user_data = self.cursor_1.fetchall()
            self.next_frame = False
            for i in self.user_data:
                if i[1] == self.user_name:
                    if i[4] == self.password:
                        self.login_userdata = i
                        self.next_frame = True
                        break
            else:
                msgbox.showerror("Error","The user does not exist (or) the password is incorrect")
            if self.next_frame:
                self.frame_1 = Frame(self,bg="#1a181c",width=800,height=500)
                self.frame_1.place(x=0,y=0)
                print(self.login_userdata)
                self.label_8 = Label(self.frame_1,text="Hello {user_name}, The list of tests scheduled are enlisted below : ".format(user_name=self.login_userdata[1]), bg="#1a181c", fg="white",font=self.font_all)
                self.label_8.place(x=10, y=20)
                self.cursor_1.execute("SELECT * FROM tests;")
                self.test_1 = self.cursor_1.fetchall()
                if self.login_userdata[5] == "Student":
                    self.index_at = []
                    count_ = 0
                    for i in self.test_1:
                        print(eval(i[1]))
                        if self.login_userdata[1] not in eval(i[1]):
                            self.index_at.append(count_)
                        count_+=1
                    for i in self.index_at:
                        del self.test_1[i]
                    #test_1 redefined here
                    if len(self.test_1)!=0:
                        columns_ = ("TEST_ID","TEST_NAME","SCHEDULED_TIME")
                        self.treeview_1 = ttk.Treeview(self.frame_1,columns=columns_,show="headings")
                        self.treeview_1.column("#0", width=1, anchor=W)
                        self.treeview_1.column("TEST_ID", width=120, anchor=W)
                        self.treeview_1.column("TEST_NAME", width=120, anchor=W)
                        self.treeview_1.column("SCHEDULED_TIME", width=120, anchor=W)
                        self.treeview_1.heading("#0", text="")
                        self.treeview_1.heading("TEST_ID", text="TEST ID")
                        self.treeview_1.heading("TEST_NAME",text="TEST NAME")
                        self.treeview_1.heading("SCHEDULED_TIME",text="SCHEDULED TIME")
                        self.treeview_1.place(x=100,y=200)
                        self.treeview_1_style = ttk.Style()
                        self.treeview_1_style.theme_use("clam")
                        self.treeview_1_config_h = ttk.Style()
                        self.treeview_1_config_h.configure("Treeview.heading")
                        self.treeview_1_style.configure("Treeview", background="#36393E", foreground="silver",
                                                fieldbackground="#36393E", font=self.tree_font)
                        self.treeview_1_style.map("Treeview", background=[("selected", "#808080")],
                                          foreground=[("!selected", "white"), ("selected", "black")])
                        self.treeview_1_style.map("Treeview.heading")
                        for i in self.test_1:
                            self.value_1 = (i[0],i[2],i[4])
                            self.treeview_1.insert("",END,values=self.value_1)
                        self.scrollbar_4 = Scrollbar(self.frame_1,orient=VERTICAL)
                        self.scrollbar_4.configure(command=self.treeview_1.yview)
                        self.scrollbar_4.place(x=465,y=200,height=230)
                        self.entry_10 = Entry(self.frame_1,bg="lime green",fg="black",font=self.font_general,bd=5,relief=RIDGE)
                        self.entry_10.place(x=500,y=235)
                        self.button_13 = Button(self.frame_1,text="ATTEND",bg="lime green",fg="black",font=self.font_general,bd=5,activebackground="black",activeforeground="black",relief=RIDGE,command=lambda:self.attend())
                        self.button_13.place(x=575,y=335)
                    else:
                        self.frame_2 = Frame(self.frame_1,height=200,width=450,bg="#474747")
                        self.label_9 = Label(self.frame_1,bg="#474747",fg="white",font=self.font_all,text="No tests are scheduled for you at the moment")
                        self.label_9.place(x=173,y=272)
                        self.frame_2.place(x=100,y=200)

                elif self.login_userdata[5] == "Teacher":
                    self.cursor_1.execute("SELECT * FROM tests WHERE host = \'{username}\'".format(username=self.login_userdata[1]))
                    self.scheduled_tests = self.cursor_1.fetchall()
                    self.button_4 = Button(self.frame_1,text="CREATE TEST",bg="lime green",fg="black",font=self.font_all,relief=RIDGE,bd=5,highlightbackground="yellow",highlightcolor="black",activebackground="#1a181c",activeforeground="#1a181c",command=lambda:self.create_test())
                    self.button_4.place(x=570,y=10)
                    if len(self.scheduled_tests)==0:
                        self.frame_3 = Frame(self.frame_1,height=200,width=450,bg="#474747")
                        self.label_10 = Label(self.frame_1,text="NO tests scheduled by you at the particular moment",bg="#474747",fg="white",font=self.font_all)
                        self.label_10.place(x=173,y=272)
                        self.frame_3.place(x=100,y=200)
                    else:
                        columns_ = ("TEST_ID", "TEST_NAME", "SCHEDULED_TIME")
                        self.treeview_3 = ttk.Treeview(self.frame_1, columns=columns_, show="headings")
                        self.treeview_3.column("#0", width=1, anchor=W)
                        self.treeview_3.column("TEST_ID", width=120, anchor=W)
                        self.treeview_3.column("TEST_NAME", width=120, anchor=W)
                        self.treeview_3.column("SCHEDULED_TIME", width=120, anchor=W)
                        self.treeview_3.heading("#0", text="")
                        self.treeview_3.heading("TEST_ID", text="TEST ID")
                        self.treeview_3.heading("TEST_NAME", text="TEST NAME")
                        self.treeview_3.heading("SCHEDULED_TIME", text="SCHEDULED TIME")
                        self.treeview_3.place(x=100, y=200)
                        self.treeview_3_style = ttk.Style()
                        self.treeview_3_style.theme_use("clam")
                        self.treeview_3_config_h = ttk.Style()
                        self.treeview_3_config_h.configure("Treeview.heading")
                        self.treeview_3_style.configure("Treeview", background="#36393E", foreground="silver",
                                                        fieldbackground="#36393E", font=self.tree_font)
                        self.treeview_3_style.map("Treeview", background=[("selected", "#808080")],
                                                  foreground=[("!selected", "white"), ("selected", "black")])
                        self.treeview_3_style.map("Treeview.heading")
                        for i in self.scheduled_tests:
                            self.value_1 = (i[0],i[2],i[4])
                            self.treeview_3.insert("",END,values=self.value_1)
                        self.scrollbar_4 = Scrollbar(self.frame_1, orient=VERTICAL)
                        self.scrollbar_4.configure(command=self.treeview_3.yview)
                        self.scrollbar_4.place(x=465, y=200, height=230)
        except ValueError:
            msgbox.showerror("Error","The pincode entered should consists only of numbers ,Please recheck your values...")
    def filter_candidates(self,*args):
        hint = self.cand_1.get()
        self.listbox_1.delete(0,END)
        for i in self.user_data:
            if i[5]=="Student" and hint in i[1]:
                self.listbox_1.insert(END, i[1])
    def attend(self):
        self.proceed_with_test=False
        self.attend_test_code = 0
        self.all_val = ""
        self.check_time = True
        if len(self.treeview_1.focus())!=0:
            self.focus_item = self.treeview_1.focus()
            print(self.treeview_1.item(self.focus_item),"What the heck")
            self.attend_test_code = self.treeview_1.item(self.focus_item)["values"][0]
            self.all_val = self.treeview_1.item(self.focus_item)["values"]
            print(self.all_val)
            self.proceed_with_test = True
            print(self.attend_test_code)
        else:
            print("It does enter")
            self.attend_test_code = int(self.entry_10.get())
            for i in self.test_1:
                if i[0]==self.attend_test_code:
                    self.all_val = [i[0],i[2],i[4]]
                    self.proceed_with_test = True
                    break
            else:
                self.check_time = False
                msgbox.showerror("Error","Please make sure that you've entered the correct code")

        print(self.all_val,"-------")
        if self.check_time==True:
            self.cur_time = list(time.localtime()[3:6])
            self.applied_time = self.all_val[2].split("-")
            if str(self.cur_time[0])+":"+str(self.cur_time[1])>self.applied_time[0] and str(self.cur_time[0])+":"+str(self.cur_time[1])<self.applied_time[1]:
                self.proceed_with_test = True
            else:
                self.proceed_with_test=False
                msgbox.showinfo("Info","The test is yet to occur or would take place in a short amount of time")
        if self.proceed_with_test==True:
            self.attend_test()
    def attend_test(self):
        "800x500"
        self.frame_8 = Frame(self,bg="white",height=500,width=800)
        self.frame_8.place(x=0,y=0)
        self.window_3 = Toplevel()
        self.window_3.geometry("1350x750")
        self.test_data = ""
        for i in self.test_1:
            if i[0]==self.all_val[0]:
                self.test_data = i
                break
        self.student_widgets = []
        self.window_3.config(bg="#1a181c")
        self.window_3.geometry("1200x750")
        self.window_3.resizable(0, 0)
        self.font_2 = font.Font(family="Century Gothic", size=26)
        self.label_16 = Label(self.window_3, text=self.test_data[3], bg="#1a181c", fg="white", font=self.font_2)
        self.label_16.grid(row=0, column=0, columnspan=3)
        self.h_1 = 550
        self.w_1 = 850
        self.frame_4 = Frame(self.window_3, bd=0, height=self.h_1, width=self.w_1)
        self.frame_4.grid(row=1, column=0, columnspan=2)
        self.scrollbar_2 = ttk.Scrollbar(self.frame_4, orient=VERTICAL)
        self.scrollbar_3 = ttk.Scrollbar(self.frame_4, orient=HORIZONTAL)
        self.canvas_1 = Canvas(self.frame_4, bd=0, highlightthickness=0, yscrollcommand=self.scrollbar_2.set,
                               height=self.h_1, width=self.w_1 - 10, xscrollcommand=self.scrollbar_3.set)
        self.canvas_1.grid(row=0, column=0)
        self.scrollbar_2.grid(row=0, column=1, sticky=NSEW)
        self.scrollbar_2.config(command=self.canvas_1.yview)
        self.scrollbar_3.grid(row=1, column=0, sticky=NSEW)
        self.frame_5 = Frame(self.canvas_1, bg="#111112")
        self.frame_5.grid(row=0, column=0)
        self.scrollbar_3.config(command=self.canvas_1.xview)
        self.frame_id = self.canvas_1.create_window(0, 0, window=self.frame_5)
        self.frame_5.bind("<Configure>", self.OnFrameConfigure)
        self.canvas_1.bind('<Configure>', self.FrameWidth)
        self.frame_widg = []
        """self.count_3 is the frame count variable"""
        self.count_3 = 0
        self.global_count_frame = 0
        self.widg_list = []
        self.ans_var = []
        count_1=0
        count_3 = 0
        for i in range(len(self.test_data)):
            self.ans_var.append(StringVar())
        for i in eval(self.test_data[5]):
            self.widg_list.append([Label(self.frame_5,i,bg="#111112",font=self.font_2,fg="white"),Label(self.frame_5,image=""),Checkbutton(self.frame_5,text=,bg="#dfdfe6",fg="black"),Checkbutton(self.frame_5,text=list(eval(self.test_data[i]))[2],bg="#dfdfe6",fg="black"),Checkbutton(self.frame_5,text=list(eval(self.test_data[i]))[3],bg="#dfdfe6",fg="black"),Checkbutton(self.frame_5,text=list(eval(self.test_data[i]))[4],bg="#dfdfe6",fg="black")])
            count_1 += 1
        else:
            for i in self.frame_widg[0]:
                if self.count_3 == 0:
                    Label(self.frame_5, text="QUESTION", bg="#282e2a", fg="white", font=self.font_title).grid(row=0,column=0,columnspan=2)
                    i.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
                elif self.count_3 == 1:
                    i.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
                elif self.count_3 == 2:
                    Label(self.frame_5, text="OPTIONS", bg="#282e2a", fg="white", font=self.font_title).grid(
                        row=4, column=0, columnspan=2)
                    i.grid(row=5, column=0, columnspan=1, padx=10, pady=10)
                elif self.count_3 == 3:
                    i.grid(row=5, column=1, columnspan=1, padx=10, pady=10)
                elif self.count_3 == 4:
                    i.grid(row=6, column=0, columnspan=1, padx=10, pady=10)
                elif self.count_3 == 5:
                    i.grid(row=6, column=1, columnspan=1, padx=10, pady=10)
                self.count_3 += 1

    def create_test(self):
        self.count_1 = 0
        self.window_2 = Toplevel()
        self.window_2.geometry("800x600")
        self.window_2.resizable(0,0)
        self.window_2.config(bg="#1a181c")
        self.label_11 = Label(self.window_2,text="ENTER THE TEST DETAILS",bg="#1a181c",fg="white",font=self.font_all)
        self.label_11.place(x=375,y=10)
        self.label_12 = Label(self.window_2,text="TEST CODE        ",bg="#1a181c",fg="white",font=self.font_all)
        self.label_12.place(x=1,y=100)
        self.entry_5 = Entry(self.window_2,bg="lime green",fg="black",relief=RIDGE,bd=5,font=self.font_general)
        self.entry_5.place(x=200,y=100)
        self.label_13 = Label(self.window_2,text="PASSWORD         ",bg="#1a181c",fg="white",font=self.font_all)
        self.label_13.place(x=1,y=150)
        self.entry_6 = Entry(self.window_2,bg="lime green",fg="black",font=self.font_general,relief=RIDGE,bd=5)
        self.entry_6.place(x=200,y=150)
        self.label_13 = Label(self.window_2, text="TEST NAME        ", bg="#1a181c", fg="white", font=self.font_all)
        self.label_13.place(x=1, y=200)
        self.entry_7 = Entry(self.window_2, bg="lime green", fg="black", font=self.font_general, relief=RIDGE, bd=5)
        self.entry_7.place(x=200, y=200)
        self.label_14 = Label(self.window_2,text="NO OF QUESTIONS   ",bg="#1a181c",fg="white",font=self.font_all)
        self.label_14.place(x=1,y=250)
        self.entry_8 = Entry(self.window_2,bg="lime green",fg="black",font=self.font_general,relief=RIDGE,bd=5)
        self.entry_8.place(x=200,y=250)
        self.label_15 = Label(self.window_2,text="SCHEDULED TIME    ",bg="#1a181c",fg="white",font=self.font_all)
        self.label_15.place(x=1,y=300)
        self.spinbox_1 = Spinbox(self.window_2,from_=0,to=23,bg="lime green",fg="black",font=self.font_general,bd=5,relief=RIDGE,width=2,state="readonly")
        self.spinbox_1.place(x=200,y=300)
        self.spinbox_2 = Spinbox(self.window_2, from_=0, to=59,bg="lime green",fg="black",font=self.font_general,bd=5,relief=RIDGE,width=2,state="readonly")
        self.spinbox_2.place(x=275, y=300)
        self.spinbox_3 = Spinbox(self.window_2, from_=0, to=59, bg="lime green", fg="black", font=self.font_general,bd=5, relief=RIDGE,width=2,state="readonly")
        self.spinbox_3.place(x=200, y=375)
        self.spinbox_4 = Spinbox(self.window_2, from_=0, to=59, bg="lime green", fg="black", font=self.font_general,bd=5, relief=RIDGE,width=2,state="readonly")
        self.spinbox_4.place(x=275, y=375)
        self.cand_1 = StringVar()
        self.entry_9 = Entry(self.window_2,fg="black",bg="lime green",relief=RIDGE,bd=5,font=self.font_general,width=20,textvariable=self.cand_1)
        self.cand_1.trace("w",self.filter_candidates)
        self.entry_9.place(x=500,y=75)
        self.font_1 = font.Font(family="Copperplate Gothic",size=11,weight="bold")
        self.listbox_1 = Listbox(self.window_2,selectmode="multiple",bg="#515459",fg="white",width=33,height=21,font=self.font_1)
        self.listbox_1.place(x=500,y=125)
        for i in self.user_data:
            if i[5]=="Student":
                self.listbox_1.insert(END,i[1])
        self.scrollbar_1 = ttk.Scrollbar(self.window_2,orient=VERTICAL,command=self.listbox_1.yview)
        self.scrollbar_1.place(x=751,y=125,height=405)
        self.button_6 = Button(self.window_2,text="Confirm",bg="lime green",fg="black",font=self.font_general,bd=5,relief=RIDGE,command=lambda:self.append_values())
        self.button_6.place(x=218,y=500)
    def open_file(self):
        self.file_types=(("PNG","*.png"),("JPG","*.jpg"),("JPEG","*.jpeg"))

        file_name = fd.askopenfilename(filetypes=self.file_types)
        self.quest_pics.insert(self.global_count_frame-1,file_name)



    def append_values(self):
        self.quest_pics=[]
        self.test_code = self.entry_5.get()
        self.password_1 = self.entry_6.get()
        self.test_name = self.entry_7.get()
        self.quest_no = self.entry_8.get()
        for i in range(int(self.quest_no)):
            self.quest_pics.append("")
        self.hr_1 = self.spinbox_1.get()
        self.min_1 = self.spinbox_2.get()
        self.hr_2 = self.spinbox_3.get()
        self.min_2 = self.spinbox_4.get()
        self.applicants = []
        for i in self.listbox_1.curselection():
            self.applicants.append(self.listbox_1.get(i))
        if str(self.hr_1)+str(self.min_1) == str(self.hr_2)+str(self.min_2):
            msgbox.showerror("ERROR","Please make sure the starting time and ending time arent the same")
        else:
            for i in self.test_1:
                if self.test_code==str(i[0]):
                    msgbox.showwarning("WARNING",
                                       "A test with that test code already exist please enter a different code")
                    break
            else:
                if self.test_code.isdigit()==True and self.password_1.isdigit()==True and len(self.test_name)<=50 and self.test_name != "" and self.quest_no.isdigit()==True and len(self.applicants) != 0:
                    self.timestap = ""
                    if len(self.hr_1)==1:
                        self.timestap+="0"+self.hr_1
                    else:
                        self.timestap+=self.hr_1
                    self.timestap+=":"
                    if len(self.min_1)==1:
                        self.timestap+="0"+self.min_1
                    else:
                        self.timestap+=self.min_1
                    self.timestap+="-"
                    if len(self.hr_2)==1:
                        self.timestap+="0"+self.hr_2
                    else:
                        self.timestap+=self.hr_2
                    self.timestap+=":"
                    if len(self.min_2)==1:
                        self.timestap+="0"+self.min_2
                    else:
                        self.timestap+=self.min_2
                    self.window_3 = Toplevel()
                    self.window_2.destroy()
                    self.window_3.config(bg="#1a181c")
                    self.window_3.geometry("1200x750")
                    self.window_3.resizable(0,0)
                    self.font_2 = font.Font(family="Century Gothic",size=26)
                    self.label_16 = Label(self.window_3,text=self.test_name,bg="#1a181c",fg="white",font=self.font_2)
                    self.label_16.grid(row=0,column=0,columnspan=3)
                    self.h_1 = 535
                    self.w_1 = 757
                    self.frame_4 = Frame(self.window_3,bd=0,height=self.h_1,width=self.w_1)
                    self.frame_4.grid(row=1,column=0,columnspan=2)
                    self.scrollbar_2 = ttk.Scrollbar(self.frame_4, orient=VERTICAL)
                    self.scrollbar_3 = ttk.Scrollbar(self.frame_4, orient=HORIZONTAL)
                    self.canvas_1 = Canvas(self.frame_4, bd=0, highlightthickness=0, yscrollcommand=self.scrollbar_2.set,height=self.h_1,width=self.w_1-10,xscrollcommand=self.scrollbar_3.set)
                    self.canvas_1.grid(row=0,column=0)
                    self.scrollbar_2.grid(row=0,column=1,sticky=NSEW)
                    self.scrollbar_2.config(command=self.canvas_1.yview)
                    self.scrollbar_3.grid(row=1, column=0, sticky=NSEW)
                    self.frame_5 = Frame(self.canvas_1,bg="#282e2a")
                    self.frame_5.grid(row=0,column=0)
                    self.scrollbar_3.config(command=self.canvas_1.xview)
                    self.frame_id = self.canvas_1.create_window(0,0,window=self.frame_5)
                    self.frame_5.bind("<Configure>", self.OnFrameConfigure)
                    self.canvas_1.bind('<Configure>', self.FrameWidth)
                    self.frame_widg = []
                    """self.count_2 is the frame count variable"""
                    self.count_3 = 0
                    self.global_count_frame = 0
                    """count_3 is for widget alignment"""
                    self.user_returns = []
                    self.f_type = (("PNG","*.png"),("jpg","*.jpg"))
                    for i in range(int(self.quest_no)):
                        self.frame_widg.append([ScrolledText(root=self.frame_5,h=3,width=40,bg="lime green",font=self.font_general,fg="black"),Button(self.frame_5, text="Open pic", fg="black", bg="lime green", relief=RIDGE, bd=5,activebackground="black", activeforeground="white", font=self.font_all, width=44,command=lambda:self.open_file()),Entry(self.frame_5,bg="lime green",font=self.font_general),Entry(self.frame_5,bg="#f51505",font=self.font_general),Entry(self.frame_5,bg="#f51505",font=self.font_general),Entry(self.frame_5,bg="#f51505",font=self.font_general)])
                    else:
                        for i in self.frame_widg[0]:
                            if self.count_3 ==0 :
                                Label(self.frame_5,text="QUESTION",bg="#282e2a",fg="white",font=self.font_title).grid(row=0,column=0,columnspan=2)
                                i.grid(row=1,column=0,columnspan=2,padx=10,pady=10)
                            elif self.count_3==1:
                                Label(self.frame_5, text="PICTURE (IF ANY)", bg="#282e2a", fg="white", font=self.font_title).grid(
                                    row=2, column=0, columnspan=2)
                                i.grid(row=3,column=0,columnspan=2,padx=10,pady=10)
                            elif self.count_3==2:
                                Label(self.frame_5, text="OPTIONS", bg="#282e2a", fg="white", font=self.font_title).grid(
                                    row=4, column=0, columnspan=2)
                                i.grid(row=5,column=0,columnspan=1,padx=10,pady=10)
                            elif self.count_3==3:
                                i.grid(row=5,column=1,columnspan=1,padx=10,pady=10)
                            elif self.count_3==4:
                                i.grid(row=6,column=0,columnspan=1,padx=10,pady=10)
                            elif self.count_3==5:
                                i.grid(row=6,column=1,columnspan=1,padx=10,pady=10)
                            self.count_3+=1
                    print(self.w_1)
                    print(self.h_1)
                    self.frame_6 = Frame(self.window_3,bg="#6c706d",height=550,width=757,bd=5,relief=RIDGE)
                    self.frame_6.grid(row=1,column=3,columnspan=1)
                    self.frame_6.grid_propagate(False)
                    # Scrollbar for treeview
                    self.scrollbar_4 = ttk.Scrollbar(self.frame_6, orient="vertical")
                    self.scrollbar_4.grid(row=0,column=5,sticky=NS)
                    # treeview configurations
                    treeview_2_header = ("Question number")
                    treeview_2_config = ttk.Style()
                    treeview_2_config.theme_use("clam")
                    treeview_2_config_h = ttk.Style()
                    treeview_2_config_h.configure("TTreeview.heading")
                    treeview_2_config.configure("TTreeview", background="#36393E", foreground="silver",
                                                fieldbackground="#36393E", font=self.tree_font,
                                                yscrollcommand=self.scrollbar_4.set,rowheight=44)
                    treeview_2_config.map("TTreeview", background=[("selected", "#808080")],
                                          foreground=[("!selected", "white"), ("selected", "black")])
                    treeview_2_config.map("TTreeview.heading")
                    self.treeview_2 = ttk.Treeview(self.frame_6, show="headings")
                    self.scrollbar_4.configure(command=self.treeview_2.yview)
                    self.treeview_2["columns"]=treeview_2_header
                    self.treeview_2.column("#1", width=120, anchor=W)
                    self.treeview_2.heading("#1", text="Question number",anchor=W)
                    #frame_5 imp
                    for i in range(1,int(self.quest_no)+1):
                        self.treeview_2.insert("",END,values=i,iid=i)
                    self.treeview_2.grid(row=0,column=0)
                    self.button_7 = Button(self.frame_6, text="SWITCH", fg="black", bg="lime green", relief=RIDGE, bd=5,
                                      activebackground="black", activeforeground="white", font=self.font_all, width=44,command=lambda:self.switch())
                    self.button_7.grid(row=1,column=0,ipadx=0,ipady=0,padx=1,pady=0)
                    self.frame_7 = Frame(self.window_3,bg="#282e2a",bd=0,height=75,width=1200)
                    self.frame_7.grid(row=3,column=0,sticky=EW,columnspan=10)
                    self.button_8 = Button(self.frame_7,text="NEXT",bg="lime green",fg="black",bd=5,relief=RIDGE,activebackground="black",activeforeground="black",font=self.font_all,width=21,command=lambda:self.next_t())
                    self.button_8.grid(row=0,column=0,padx=15)
                    self.button_9 = Button(self.frame_7,text="CLEAR",bg="lime green",fg="black",bd=5,relief=RIDGE,activebackground="black",activeforeground="black",font=self.font_all,width=21,command=lambda:self.clear_t())
                    self.button_9.grid(row=0,column=1,padx=10)
                    self.button_10 = Button(self.frame_7,text="CLEAR ALL ",bg="lime green",fg="black",bd=5,relief=RIDGE,activebackground="black",activeforeground="black",font=self.font_all,width=21,command=lambda:self.clear_all_t())
                    self.button_10.grid(row=0,column=2,padx=10)
                    self.button_11 = Button(self.frame_7,text="SUBMIT",bg="lime green",fg="black",bd=5,relief=RIDGE,activebackground="black",activeforeground="black",font=self.font_all,width=21,command=lambda:self.save_t())
                    self.button_11.grid(row=0,column=3,padx=10)
                    self.button_12 = Button(self.frame_7, text="EXIT", bg="lime green", fg="black", bd=5,
                                            relief=RIDGE, activebackground="black", activeforeground="black",
                                            font=self.font_all, width=21,command=lambda:self.exit_t())
                    self.button_12.grid(row=0, column=4, padx=10)
                else:
                    msgbox.showerror("Error","Please make sure the entered values are correct")

    def next_t(self):
        print("next")
        self.count_3 = 0
        print(self.global_count_frame)
        if int(self.global_count_frame)<int(self.quest_no)-1:
            for i in self.frame_widg[int(self.global_count_frame)-1]:
                i.forget()
            self.global_count_frame=int(self.global_count_frame)+1
            for i in self.frame_widg[int(self.global_count_frame) - 1]:
                if self.count_3 == 0:
                    i.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
                elif self.count_3 == 1:
                    i.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
                elif self.count_3 == 2:
                    i.grid(row=5, column=0, columnspan=1, padx=10, pady=10)
                elif self.count_3 == 3:
                    i.grid(row=5, column=1, columnspan=1, padx=10, pady=10)
                elif self.count_3 == 4:
                    i.grid(row=6, column=0, columnspan=1, padx=10, pady=10)
                elif self.count_3 == 5:
                    i.grid(row=6, column=1, columnspan=1, padx=10, pady=10)
                self.count_3 += 1
        else:
            msgbox.showinfo("Info","Final question reached ...")

    def clear_t(self):
        for i in self.frame_widg[int(self.global_count_frame)-1]:
            i.delete(0,END)
    def clear_all_t(self):
        for i in self.frame_widg:
            i[0].text_1.delete("1.0",END)
        for i in self.frame_widg:
            for j in i[2::]:
                j.delete(0,END)
    def exit_t(self):
        if msgbox.showwarning("Warning","Are you sure you wanna exit. Changes might not be saved..."):
            self.window_3.destroy()
        else:
            pass
    def save_t(self):
        d_1 = {}
        count = 0
        print("len:",len(self.quest_pics))
        for i in self.frame_widg:
            print(len(i))
            d_1[i[0].return_text().rstrip()] = "\"{a}\",{b},{c},{d},{e}".format(a=self.quest_pics[count],b=i[2].get(),c=i[3].get(),d=i[4].get(),e=i[5].get())
            print(count)
            count += 1
        print(d_1)
        for i in d_1:
            if i.isspace() or i == "":
                msgbox.showerror("Error","bREAK1")
                break
        else:
            flag_1 = True
            for i in list(d_1.values()):
                for j in eval(i)[1::]:
                    if type(j) == type("a"):
                        if j.isspace() or j == "":
                            print("VALUE OF J : ",j)
                            msgbox.showerror("Error","Break2")
                            flag_1 = False
                            break
                    elif type(j) == type(0):
                        if i == 0 :
                            msgbox.showerror("Error","Error has occured")

                if flag_1==False:
                    break
            else:
                #print("INSERT INTO tests VALUES ({test_id},\"{applicants}\",\"{test_name}\",\"{host}\",\"{scheduled_time}\",\"{test_questions}\")".format(test_id=int(self.test_code),applicants=str(self.applicants),test_name=str(self.test_name),host=self.user_name,scheduled_time=self.timestap,test_questions=d_1))
                self.cursor_1.execute("INSERT INTO tests VALUES ({test_id},\"{applicants}\",\"{test_name}\",\"{host}\",\"{scheduled_time}\",\"{test_questions}\")".format(test_id=int(self.test_code),applicants=str(self.applicants),test_name=str(self.test_name),host=self.user_name,scheduled_time=self.timestap,test_questions=d_1))
                self.clear_all_t()
                msgbox.showinfo("Info","The following test has been successfully created")
                self.window_3.destroy()
                self.login()
    def switch(self):
        try:
            self.count_at = self.treeview_2.focus()
            for i in self.frame_widg[int(self.global_count_frame)-1]:
                i.grid_forget()
            self.count_3 = 0
            self.global_count_frame = self.count_at
            for i in self.frame_widg[int(self.global_count_frame)-1]:
                if self.count_3 == 0:
                    i.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
                elif self.count_3 == 1:
                    i.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
                elif self.count_3 == 2:
                    i.grid(row=5, column=0, columnspan=1, padx=10, pady=10)
                elif self.count_3 == 3:
                    i.grid(row=5, column=1, columnspan=1, padx=10, pady=10)
                elif self.count_3 == 4:
                    i.grid(row=6, column=0, columnspan=1, padx=10, pady=10)
                elif self.count_3 == 5:
                    i.grid(row=6, column=1, columnspan=1, padx=10, pady=10)
                self.count_3 += 1
        except:
            msgbox.showerror("Error","Please make sure you've selected an option from the list")

    def FrameWidth(self, event):
        canvas_width = event.width
        canvas_height = event.height
        print("Event called")
        self.canvas_1.itemconfig(self.frame_id, width=canvas_width,height=canvas_height)
    def OnFrameConfigure(self, event):
        self.canvas_1.configure(scrollregion=self.canvas_1.bbox("all"))
        print("Bbox activate")



    def sign_up(self):
        self.window_1 = Toplevel()
        self.window_1.wm_attributes("-topmost", 1)
        self.window_1.geometry("600x450")
        self.window_1.resizable(0,0)
        self.label_3 = Label(self.window_1,text="SIGN-UP",fg="white",bg="#282e2a",font=self.font_title)
        self.label_3.place(x=260,y=23)
        self.label_4 = Label(self.window_1,text="Username",fg="white",bg="#282e2a",font=self.font_title)
        self.label_4.place(x=30,y=100)
        self.label_5 = Label(self.window_1, text="Password", fg="white", bg="#282e2a", font=self.font_title)
        self.label_5.place(x=30, y=200)
        self.entry_3 = Entry(self.window_1,bd=5,bg="lime green",fg="black",font=self.font_general,relief=RIDGE)
        self.entry_3.place(x=175,y=110)
        self.entry_4 = Entry(self.window_1,bd=5,bg="lime green",fg="black",font=self.font_general,relief=RIDGE)
        self.entry_4.place(x=175,y=210)
        self.gradelist = []
        for i in range(1,13):
            self.gradelist.append(i)
        self.grade_ = IntVar()
        self.grade_.set(1)
        self.dropmenu_1 = OptionMenu(self.window_1,self.grade_,*self.gradelist)
        self.dropmenu_1.config(width=6)
        self.dropmenu_1.place(x=475,y=175)
        self.label_6 = Label(self.window_1,text="GRADE",fg="white",bg="#282e2a",font=self.font_title)
        self.label_6.place(x=475,y=95)
        self.label_6 = Label(self.window_1, text="SECTION", fg="white", bg="#282e2a", font=self.font_title)
        self.label_6.place(x=475, y=250)
        self.seclist = []
        for i in range(65,91):
            self.seclist.append(chr(i))
        self.sec_ = StringVar()
        self.sec_.set(self.seclist[0])
        self.dropmenu_2 = OptionMenu(self.window_1,self.sec_,*self.seclist)
        self.dropmenu_2.config(width=6)
        self.dropmenu_2.place(x=475,y=305)
        self.button_3 = Button(self.window_1,text="SIGN-UP",font=self.font_general,bg="lime green",fg="black",relief=RIDGE,bd=5,command=lambda:self.backend_signup())
        self.button_3.place(x=195,y=310)
        self.label_7 = Label(self.window_1,text="ROLE : ",font=self.font_title,bg="#282e2a",fg="white")
        self.label_7.place(x=345,y=375)
        self.role_ = StringVar()
        self.radio_1 = Radiobutton(self.window_1,text="Teacher",variable=self.role_,value="Teacher",bg="#282e2a",fg="white",font=self.font_all,padx=0,pady=0,activebackground="#282e2a",activeforeground="white",selectcolor="red",indicator=0)
        self.radio_1.place(x=435,y=350)
        self.radio_2 = Radiobutton(self.window_1, text="Student",variable=self.role_,value="Student",bg="#282e2a",fg="white",font=self.font_all,padx=0,pady=0,activebackground="#282e2a",activeforeground="white",selectcolor="red",indicator=0)
        self.radio_2.place(x=435, y=395)
    def backend_signup(self):
        self.cursor_1.execute("SELECT * FROM user_data")
        self.user_data = self.cursor_1.fetchall()
        self.signup_username = str(self.entry_3.get())
        self.signup_password = str(self.entry_4.get())
        self.signup_role = str(self.role_.get())
        self.signup_sec = self.sec_.get()
        self.signup_grade = self.grade_.get()
        self.user_exist = True
        self.user_msg_1 = ""
        print(self.user_data)
        if self.signup_username != "" or self.signup_username.isspace() == False:
            for i in self.user_data:
                print(i[1])
                if i[1] == self.signup_username:
                    self.user_exist = True
                    break
                else:
                    pass
            else:
                self.user_exist = False
        else:
            self.user_exist = True
        if self.user_exist == True:
            msgbox.showwarning("Warning","A user with such a username already exist")
        else:
            print(self.signup_grade)
            if self.signup_password.isdigit() == False or self.signup_role not in ("Teacher","Student") or (self.signup_grade) not in range(1,13) or ord(self.signup_sec) not in range(65,91):
                msgbox.showinfo("Info","Please make sure the values are entered correctly")
            else:
                if len(self.user_data) == 0:
                    self.generated_id = 100
                else:
                    self.generated_id = int(self.user_data[-1][0])+1
                self.query_1 = "INSERT INTO user_data VALUES({user_id},'{user_name}','{grade}','{section}',{password},'{role}')".format(user_id = self.generated_id,user_name=self.signup_username,grade=self.signup_grade,section=self.signup_sec,password=self.signup_password,role=self.signup_role)
                self.cursor_1.execute(self.query_1)
                msgbox.showinfo("Info","The following account has been successfully created")
                self.window_1.destroy()

if __name__=="__main__":
    mainframe_1 = Base()
    mainframe_1.mainloop()


