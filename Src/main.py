from tkinter import *
import tkinter.font as font
from PIL import ImageTk,Image
import mysql.connector as connector_
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk
import repackage
repackage.up()
from Src.custom_text import ScrolledText
import matplotlib.pyplot as mlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter.tix as tx
import time
import tkinter.filedialog as fd
import random
import cv2
from skimage.metrics import structural_similarity as ssim

class Base(tx.Tk):
    def __init__(self):
        super().__init__()
        self.main_database = connector_.connect(host="localhost",user="root",password="12345")
        self.cursor_1 = self.main_database.cursor()
        print("Enters...")
        self.cursor_1.execute("CREATE DATABASE IF NOT EXISTS fest_for_students;")
        self.cursor_1.execute("USE Fest_for_students;")
        self.cursor_1.execute("""CREATE TABLE IF NOT EXISTS user_data
                              (User_id varchar(70) primary key,
                              Username varchar(70) unique,
                              Grade int not null,
                              Section char(1) not null,
                              password int(11),
                              role varchar(30));""")
        self.cursor_1.execute("""CREATE TABLE IF NOT EXISTS tests
                                (test_id int primary key,
                                applicants longblob not null,
                                test_name varchar(50) not null,
                                host varchar(255) not null,
                                scheduled_time varchar(255) not null,
                                test_questions longblob not null);""")
        self.cursor_1.execute("USE fest_for_students;")
        self.title("Fest for students")
        self.geometry("800x500")
        self.resizable(0,0)
        self.proceed_with_img = False
        self.tree_font = font.Font(family="Century Gothic", weight="normal", size=10)
        self.font_title = font.Font(family="Gabriola", weight="bold", slant="roman",size=25)
        self.font_all = font.Font(family="Gabriola",weight="bold",slant="roman")
        self.font_general = font.Font(family="Comic Sans MS",weight="bold",slant="roman")
        """Reference font_3 for now in all places"""
        self.font_3 = font.Font(family="mono nerd",weight="normal",slant="roman")
        self.img_1 = ImageTk.PhotoImage(Image.open(r"Assets\bg_1.jpg"))
        self.label_1 = Label(self,image=self.img_1)
        self.label_1.place(x=0,y=0)
        self.label_2 = Label(self,text="FEST-FOR-STUDENTS",bg="#f5f4b0",fg="#1a181c",font=self.font_title)
        self.label_2.place(x=415,y=10)
        self.label_25 = Label(self,text="USERNAME",font=self.font_title,bg="orange",fg="black")
        self.label_25.place(x=155,y=110)
        self.label_26 = Label(self,text="PASSWORD",font=self.font_title,fg="black",bg="orange")
        self.label_26.place(x=155,y=220)
        self.entry_1 = Entry(self,bd=10,bg="lime green",fg="black",font=self.font_general,relief=RIDGE,highlightcolor="grey")
        self.entry_1.place(x=300,y=110)
        self.entry_2 = Entry(self,bd=10,bg="lime green",fg="black",font=self.font_general,relief=RIDGE,highlightcolor="grey",show="*")
        self.entry_2.place(x=300,y=210)
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
                self.label_8 = Label(self.frame_1,text="Hello {user_name}, The list of tests scheduled are enlisted below : ".format(user_name=self.login_userdata[1]), bg="#1a181c", fg="white",font=self.font_all)
                self.label_8.place(x=10, y=20)
                self.cursor_1.execute("SELECT * FROM tests;")
                self.test_1 = self.cursor_1.fetchall()
                if self.login_userdata[5] == "Student":
                    self.index_at = []
                    count_ = 0
                    for i in self.test_1:
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
                                                fieldbackground="#36393E", font=self.tree_font,rowheight=13)
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
                        self.button_14 = Button(self.frame_1,text="SHOW RESULT",bg="lime green",fg="black",font=self.font_general,bd=5,activebackground="black",activeforeground="black",relief=RIDGE,command=lambda:self.show_result())
                        self.button_14.place(x=305,y=435)
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
                        self.button_15 = Button(self.frame_1, text="DELETE TEST", bg="lime green", fg="black",
                                                font=self.font_all, relief=RIDGE, bd=5, highlightbackground="yellow",
                                                highlightcolor="black", activebackground="#1a181c",
                                                activeforeground="#1a181c", width=30,command=lambda: self.delete_test())
                        self.button_15.place(x=525,y=200)
                        self.button_16 = Button(self.frame_1, text="VIEW TEST", bg="lime green", fg="black",
                                                font=self.font_all, relief=RIDGE, bd=5, highlightbackground="yellow",
                                                highlightcolor="black", activebackground="#1a181c",
                                                activeforeground="#1a181c", width=30,command=lambda: self.view_test())
                        self.button_16.place(x=525,y=260)
        except ValueError:
            msgbox.showerror("Error","The pincode entered should consists only of numbers ,Please recheck your values...")
    def delete_test(self):
        try:
            self.req_delete_ref = self.treeview_3.focus()
            self.req_delete = self.treeview_3.item(self.req_delete_ref)
            self.cursor_1.execute("DELETE FROM tests WHERE test_id={req_test_id}".format(req_test_id=self.req_delete["values"][0]))
            self.login()
        except:
            msgbox.showerror("ERROR","Please make sure that you've selected an option from the list")
    def view_test(self):
        self.all_val=""
        if len(self.treeview_3.focus())!=0:
            self.focus_item = self.treeview_3.focus()
            self.attend_test_code = self.treeview_3.item(self.focus_item)["values"][0]
            self.all_val = self.treeview_3.item(self.focus_item)["values"]
        self.window_3 = tx.Toplevel()
        self.window_3.geometry("1350x750")
        self.frame_white = Frame(self,bg="white",height=720,width=1080)
        self.test_data = ""
        for i in self.test_1:
            if i[0] == self.all_val[0]:
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
        self.frame_4 = Frame(self.window_3, bd=0, height=self.h_1, width=self.w_1, bg="#111112")
        self.frame_4.grid(row=1, column=0, columnspan=2)
        self.frame_5_ref = tx.ScrolledWindow(self.frame_4, height=self.h_1, width=self.w_1, scrollbar="y",bg="#111112")
        self.frame_5 = self.frame_5_ref.window
        for i in self.frame_5_ref.subwidgets_all():
            i.config(bg="#111112")
        self.frame_5_ref.grid(row=0, column=0)
        self.frame_5.config(bg="#111112")
        self.frame_widg = []
        self.count_3 = 0
        self.global_count_frame = 1
        self.widg_list = []
        self.ans_var = []
        self.ans_key = []
        count_1 = 0
        self.stu_pics = []
        count_2 = 0  # for image display
        for i in range(len(eval(self.test_data[5]))):
            self.ans_var.append(StringVar())
        for i in eval(self.test_data[5]):
            self.widg_list.append([ScrolledText(root=self.frame_5, h=3, width=60, bg="#111112", fg="white",
                                                font=self.font_3, text=i, text_disable="disabled"),
                                   Label(self.frame_5, image="", bg="#111112"),
                                   Radiobutton(self.frame_5, text=eval(self.test_data[5])[i].split("-###-")[1],
                                               bg="#111112", fg="white", font=self.font_3, width=30,
                                               variable=self.ans_var[count_1],
                                               value=eval(self.test_data[5])[i].split("-###-")[1], indicator=0,
                                               selectcolor="black",state=DISABLED),
                                   Radiobutton(self.frame_5, indicator=0, selectcolor="black",
                                               text=eval(self.test_data[5])[i].split("-###-")[2], bg="#111112",
                                               fg="white", font=self.font_3, width=30, variable=self.ans_var[count_1],
                                               value=eval(self.test_data[5])[i].split("-###-")[2],state=DISABLED),
                                   Radiobutton(self.frame_5, indicator=0, selectcolor="black",
                                               text=eval(self.test_data[5])[i].split("-###-")[3], bg="#111112",
                                               fg="white", font=self.font_3, width=30, variable=self.ans_var[count_1],
                                               value=eval(self.test_data[5])[i].split("-###-")[3],state=DISABLED),
                                   Radiobutton(self.frame_5, indicator=0, selectcolor="black",
                                               text=eval(self.test_data[5])[i].split("-###-")[4], bg="#111112",
                                               fg="white", font=self.font_3, width=30, variable=self.ans_var[count_1],
                                               value=eval(self.test_data[5])[i].split("-###-")[4],state=DISABLED)])
            self.ans_key.append(eval(self.test_data[5])[i].split("-###-")[1])
            self.stu_pics.append(eval(self.test_data[5])[i].split("-###-")[0])
            count_1 += 1
        else:
            row_grid_array = [5, 6, 5, 6]
            col_grid_array = [0, 1, 0, 1]
            for i in self.widg_list[0]:
                if self.count_3 == 0:
                    Label(self.frame_5, text="QUESTION", bg="#111112", fg="white", font=self.font_title).grid(row=0,
                                                                                                              column=0,
                                                                                                              columnspan=2,
                                                                                                              sticky=EW,
                                                                                                              padx=10,
                                                                                                              pady=10)
                    i.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=EW)
                elif self.count_3 == 1:
                    try:
                        self.image_1 = ImageTk.PhotoImage(
                            Image.open(self.stu_pics[int(self.global_count_frame) - 1]).resize((375, 250)))
                        i.config(image=self.image_1)
                    except:
                        pass
                    i.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=EW)

                elif self.count_3 == 2:
                    Label(self.frame_5, text="OPTIONS", bg="#111112", fg="white", font=self.font_title).grid(row=4,
                                                                                                             column=0,
                                                                                                             columnspan=2,
                                                                                                             sticky=EW)
                if self.count_3 >= 2:
                    placement_row = random.choice(row_grid_array)
                    placement_col = random.choice(col_grid_array)
                    i.grid(row=placement_row, column=placement_col, padx=10, pady=10)
                    row_grid_array.remove(placement_row)
                    col_grid_array.remove(placement_col)
                self.count_3 += 1
        self.frame_6 = Frame(self.window_3, bg="#6c706d", height=550, width=350, bd=5, relief=RIDGE)
        self.frame_6.grid(row=1, column=3, columnspan=1)
        self.frame_6.grid_propagate(False)
        # Scrollbar for treeview
        self.scrollbar_4 = ttk.Scrollbar(self.frame_6, orient="vertical")
        self.scrollbar_4.grid(row=0, column=2, sticky=NSEW)
        # treeview configurations
        treeview_2_header = ("Question number")
        treeview_2_config = ttk.Style()
        treeview_2_config.theme_use("clam")
        treeview_2_config_h = ttk.Style()
        treeview_2_config_h.configure("Treeview.heading")
        treeview_2_config.configure("Treeview", background="#36393E", foreground="silver",
                                    fieldbackground="#36393E", font=self.tree_font,
                                    yscrollcommand=self.scrollbar_4.set, rowheight=44)
        treeview_2_config.map("Treeview", background=[("selected", "#808080")],
                              foreground=[("!selected", "white"), ("selected", "black")])
        treeview_2_config.map("Treeview.heading")
        self.treeview_2 = ttk.Treeview(self.frame_6, show="headings")
        self.scrollbar_4.configure(command=self.treeview_2.yview)
        self.treeview_2["columns"] = treeview_2_header
        self.treeview_2.column("#1", width=120, anchor=W)
        self.treeview_2.heading("#1", text="Question number", anchor=W)
        # frame_5 imp
        for i in range(1, len(eval(self.test_data[5])) + 1):
            self.treeview_2.insert("", END, values=i, iid=i)
        self.treeview_2.grid(row=0, column=0,sticky=W)
        self.button_7 = Button(self.frame_6, text="SWITCH", fg="black", bg="lime green", relief=RIDGE, bd=5,
                               activebackground="black", activeforeground="white", font=self.font_all, width=32,
                               command=lambda: self.s_switch())
        self.button_7.grid(row=1, column=0, ipadx=0, ipady=0, padx=1, pady=0)
        self.frame_7 = Frame(self.window_3, bg="#282e2a", bd=0, height=75, width=1200)
        self.frame_7.grid(row=3, column=0, sticky=EW, columnspan=10)
        self.button_8 = Button(self.frame_7, text="NEXT", bg="lime green", fg="black", bd=5, relief=RIDGE,
                               activebackground="black", activeforeground="black", font=self.font_all, width=21,
                               command=lambda: self.next_s())
        self.button_8.grid(row=0,column=0,padx=10,sticky=W)
        self.button_12 = Button(self.frame_7, text="EXIT", bg="lime green", fg="black", bd=5,
                                relief=RIDGE, activebackground="black", activeforeground="black",
                                font=self.font_all, width=21, command=lambda: self.exit_t())
        self.button_12.grid(row=0, column=4, padx=10,sticky=E)
    def filter_candidates(self,*args):
        hint = self.cand_1.get()
        self.listbox_1.delete(0,END)
        for i in self.user_data:
            if i[5]=="Student" and hint in i[1]:
                self.listbox_1.insert(END, i[1])
    def show_result(self):
        self.req_test_ref = self.treeview_1.focus()
        self.req_test = self.treeview_1.item(self.req_test_ref)
        self.cursor_1.execute("SELECT user_id from {test_code}_{test_name}_marks".format(test_code=self.req_test["values"][0],test_name=self.req_test["values"][1]))
        self.written_users = self.cursor_1.fetchall()
        self.bool_show_result = False
        for i in self.written_users:
            if int(i[0])==int(self.login_userdata[0]):
                self.bool_show_result = True
                break
        else:
            self.bool_show_result=False
        if self.bool_show_result==True:
            self.window_4 = tx.Toplevel()
            self.window_4.geometry("800x500")
            self.window_4.config(bg="#171717")
            self.window_4.resizable(0,0)
            self.frame_9 = Frame(self.window_4,height=500,width=800)
            self.answers = []
            self.cursor_1.execute("SELECT * from tests where test_id={req_test_id}".format(req_test_id=self.req_test["values"][0]))
            self.all_test_data = self.cursor_1.fetchall()[0]
            self.cursor_1.execute("SELECT test_questions from tests where test_id={req_test_id}".format(req_test_id=self.req_test["values"][0]))
            self.data_2 =(self.cursor_1.fetchall())[0][0]
            for i in eval(self.data_2):
                self.answers.append(eval(self.data_2)[i].split("-###-")[1])
            self.cursor_1.execute("SELECT answers_given from {test_id}_{test_name}_marks WHERE user_id= {login_user};".format(test_id=self.req_test["values"][0],test_name=self.req_test["values"][1],login_user=self.login_userdata[0]))
            self.user_ans = eval(self.cursor_1.fetchall()[0][0])
            self.cursor_1.execute("SELECT marks FROM {test_id}_{test_name}_marks WHERE user_id = {login_user};".format(test_id=self.req_test["values"][0],test_name=self.req_test["values"][1],login_user=self.login_userdata[0]))
            self.answers_correct = self.cursor_1.fetchall()[0][0]
            self.perc_ans_correct = (self.answers_correct/len(self.answers))
            self.perc_ans_incorrect = 1-self.perc_ans_correct
            self.scroll_win_ref = tx.ScrolledWindow(self.frame_9,height=500,width=800,scrollbar="y")
            self.scroll_win_ref.grid(row=0, column=0)
            self.scroll_win = self.scroll_win_ref.window
            for i in self.scroll_win_ref.subwidgets_all():
                i.config(bg="#111112")
            self.label_17 = Label(self.scroll_win,text="RESULTS",bg="#111112",fg="white",font=self.font_3)
            self.label_17.grid(row=0,column=0,padx=10,pady=10,columnspan=2,sticky=EW)
            self.fig = mlib.figure(figsize=(3,2),facecolor="#111112")
            data = [self.perc_ans_correct,self.perc_ans_incorrect]
            names = ["Correct","Incorrect"]
            col = ("green","red")
            explode=[0.07,0.05]
            wedges,text = mlib.pie(data,labels=names,explode=explode,colors=col,shadow=True,startangle=60)
            for i in text:
                i.set_color("white")
            self.canvas_1 = FigureCanvasTkAgg(self.fig,master=self.scroll_win)
            self.canvas_1.draw()
            self.canvas_1.get_tk_widget().grid(row=1,column=1,padx=10,pady=10,sticky=E)
            self.frame_11 = Frame(self.scroll_win,bg="#111112",width=450,height=300)
            self.frame_11.grid(row=1,column=0,padx=10,pady=10,sticky=W)
            self.label_18 = Label(self.frame_11,text="TOTAL MARKS : "+str(len(self.answers))+" pts",bg="#111112",fg="white",font=self.tree_font)
            self.label_19 = Label(self.frame_11,text="MARKS SECURED : "+str(self.answers_correct)+" pts",bg="#111112",fg="white",font=self.tree_font)
            self.label_20 = Label(self.frame_11,text="RECORDED PERCENTAGE : "+str(self.perc_ans_correct)+" pts",bg="#111112",fg="white",font=self.tree_font)
            self.label_18.grid(row=1,column=0,padx=10,pady=10,sticky=W,columnspan=1)
            self.label_19.grid(row=2, column=0,padx=10,pady=10,sticky=W,columnspan=1)
            self.label_20.grid(row=3, column=0,padx=10,pady=10,sticky=W,columnspan=1)
            self.frame_10 = Frame(self.scroll_win,bg="#111112",width=370,height=100)
            self.frame_10.grid(row=4,column=0,padx=10,pady=10,sticky=EW,columnspan=2)
            columns_ = ("QUESTION NUMBER", "GIVEN ANSWER", "CORRECT ANSWER")
            self.treeview_4 = ttk.Treeview(self.frame_10, columns=columns_, show="headings")
            self.treeview_4.column("#0", width=1, anchor=W)
            self.treeview_4.column("QUESTION NUMBER", width=120, anchor=W)
            self.treeview_4.column("GIVEN ANSWER", width=120, anchor=W)
            self.treeview_4.column("CORRECT ANSWER", width=120, anchor=W)
            self.treeview_4.heading("#0", text="")
            self.treeview_4.heading("QUESTION NUMBER", text="QUESTION NUMBER")
            self.treeview_4.heading("GIVEN ANSWER", text="GIVEN ANSWER")
            self.treeview_4.heading("CORRECT ANSWER", text="CORRECT ANSWER")
            self.treeview_4.grid(row=0, column=0)
            self.treeview_1_style = ttk.Style()
            self.treeview_1_style.theme_use("clam")
            self.treeview_1_config_h = ttk.Style()
            self.treeview_1_config_h.configure("Treeview.heading")
            self.treeview_1_style.configure("Treeview", background="#36393E", foreground="silver",
                                            fieldbackground="#36393E", font=self.tree_font)
            self.treeview_1_style.map("Treeview", background=[("selected", "#808080")],
                                      foreground=[("!selected", "white"), ("selected", "black")])
            self.treeview_1_style.map("Treeview.heading")
            #answers and user_answers
            for i in range(len(self.answers)):
                if self.user_ans:
                    self.value_1 = (i,"NIL",self.answers[i])
                else:
                    self.value_1 = (i,self.user_ans[i],self.answers[i])
                self.treeview_4.insert("", END, values=self.value_1)
            self.scrollbar_2 = ttk.Scrollbar(self.frame_10, orient="vertical")
            self.scrollbar_2.configure(command=self.treeview_4.yview)
            self.scrollbar_2.grid(row=0,column=1,sticky=NSEW)
            self.label_21 = Label(self.scroll_win,text="TEST-DETAILS",bg="#111112",fg="white",font=self.tree_font)
            self.label_21.grid(row=7,column=0,padx=20,pady=10,sticky=W)
            self.label_22 = Label(self.scroll_win,text="HOST : "+self.all_test_data[3],bg="#111112",fg="white",font=self.tree_font)
            self.label_23 = Label(self.scroll_win,text="TEST NAME : "+self.all_test_data[2],bg="#111112",fg="white",font=self.tree_font)
            self.label_24 = Label(self.scroll_win,text="SCHEDULED TIME : "+self.all_test_data[4],bg="#111112",fg="white",font=self.tree_font)
            self.label_22.grid(row=8,column=0,padx=20,pady=10,sticky=W)
            self.label_23.grid(row=9, column=0, padx=20, pady=10, sticky=W)
            self.label_24.grid(row=10, column=0, padx=20, pady=10, sticky=W)
            self.frame_9.grid(row=0,column=0)
    def angle_percent(self,n):
        return 360*n
    def attend(self):
        self.proceed_with_test=False
        self.attend_test_code = 0
        self.all_val = ""
        self.check_time = True
        self.record_existing = False
        if len(self.treeview_1.focus())!=0:
            self.focus_item = self.treeview_1.focus()
            self.attend_test_code = self.treeview_1.item(self.focus_item)["values"][0]
            self.all_val = self.treeview_1.item(self.focus_item)["values"]
            self.proceed_with_test = True
        else:
            self.attend_test_code = int(self.entry_10.get())
            for i in self.test_1:
                if i[0]==self.attend_test_code:
                    self.all_val = [i[0],i[2],i[4]]
                    self.proceed_with_test = True
                    break
            else:
                self.check_time = False
                msgbox.showerror("Error","Please make sure that you've entered the correct code")
        if self.check_time==True:
            self.cur_time = list(time.localtime()[3:6])
            if len(str(self.cur_time[0]))==1:
                self.cur_time[0] = "0"+str(self.cur_time[0])
            if len(str(self.cur_time[1]))==1:
                self.cur_time[1] = "0"+str(self.cur_time[1])
            self.applied_time = self.all_val[2].split("-")
            if str(self.cur_time[0])+":"+str(self.cur_time[1])>self.applied_time[0] and str(self.cur_time[0])+":"+str(self.cur_time[1])<self.applied_time[1]:
                self.proceed_with_test = True
            else:
                self.proceed_with_test=False
                msgbox.showinfo("Info","The test is yet to occur or would take place in a short amount of time")
        self.cursor_1.execute("SELECT user_id FROM {testcode}_{testname}_marks".format(testcode=self.all_val[0],testname=self.all_val[1]))
        self.data_1 = self.cursor_1.fetchall()
        for i in self.data_1:
            if int(i[0]) == int(self.login_userdata[0]):
                self.record_existing = True
        if self.record_existing==True:
            msgbox.showwarning("Warning","You've already written the test and can not write it any further")
        if self.proceed_with_test==True and self.record_existing==False:
            self.attend_test()
    def attend_test(self):
        "800x500"
        self.proceed_with_img = True
        self.frame_8 = Frame(self,bg="white",height=500,width=800)
        self.frame_8.place(x=0,y=0)
        self.check_true = True
        self.window_3 = tx.Toplevel()
        self.test_data = ""
        for i in self.test_1:
            if i[0]==self.all_val[0]:
                self.test_data = i
                break
        self.student_widgets = []
        self.window_3.config(bg="#1a181c")
        self.window_3.geometry("1400x750")
        self.window_3.resizable(0, 0)
        self.font_2 = font.Font(family="Century Gothic", size=26)
        self.label_16 = Label(self.window_3, text=self.test_data[3], bg="#1a181c", fg="white", font=self.font_2)
        self.label_16.grid(row=0, column=0, columnspan=3)
        self.h_1 = 550
        self.w_1 = 850
        self.frame_4 = Frame(self.window_3, bd=0, height=self.h_1, width=self.w_1,bg="#111112")
        self.frame_4.grid(row=1, column=0, columnspan=2)
        self.frame_5_ref = tx.ScrolledWindow(self.frame_4, height=self.h_1, width=self.w_1,scrollbar="y",bg="#111112")
        self.frame_5 = self.frame_5_ref.window
        for i in self.frame_5_ref.subwidgets_all():
            i.config(bg="#111112")
        self.frame_5_ref.grid(row=0, column=0)
        self.frame_5.config(bg="#111112")
        self.frame_widg = []
        self.count_3 = 0
        self.global_count_frame = 1
        self.widg_list = []
        self.ans_var = []
        self.ans_key = []
        count_1=0
        self.warning = 0
        self.stu_pics = []
        count_2 = 0 #for image display
        for i in range(len(eval(self.test_data[5]))):
            self.ans_var.append(StringVar())
        for i in eval(self.test_data[5]):
            self.widg_list.append([ScrolledText(root=self.frame_5,h=3,width=60,bg="#111112",fg="white",font=self.font_3,text=i,text_disable="disabled"),Label(self.frame_5,image="",bg="#111112"),Radiobutton(self.frame_5,text=eval(self.test_data[5])[i].split("-###-")[1],bg="#111112",fg="white",font=self.font_3,width=30,variable=self.ans_var[count_1],value=eval(self.test_data[5])[i].split("-###-")[1],indicator=0,selectcolor="black"),Radiobutton(self.frame_5,indicator=0,selectcolor="black",text=eval(self.test_data[5])[i].split("-###-")[2],bg="#111112",fg="white",font=self.font_3,width=30,variable=self.ans_var[count_1],value=eval(self.test_data[5])[i].split("-###-")[2]),Radiobutton(self.frame_5,indicator=0,selectcolor="black",text=eval(self.test_data[5])[i].split("-###-")[3],bg="#111112",fg="white",font=self.font_3,width=30,variable=self.ans_var[count_1],value=eval(self.test_data[5])[i].split("-###-")[3]),Radiobutton(self.frame_5,indicator=0,selectcolor="black",text=eval(self.test_data[5])[i].split("-###-")[4],bg="#111112",fg="white",font=self.font_3,width=30,variable=self.ans_var[count_1],value=eval(self.test_data[5])[i].split("-###-")[4])])
            self.ans_key.append(eval(self.test_data[5])[i].split("-###-")[1])
            self.stu_pics.append(eval(self.test_data[5])[i].split("-###-")[0])
            count_1 += 1
        else:
            row_grid_array = [5,6,5,6]
            col_grid_array = [0,1,0,1]
            for i in self.widg_list[0]:
                if self.count_3 == 0:
                    Label(self.frame_5, text="QUESTION", bg="#111112", fg="white", font=self.font_title).grid(row=0,
                                                                                                              column=0,
                                                                                                              columnspan=2,
                                                                                                              sticky=EW,
                                                                                                              padx=10,
                                                                                                              pady=10)
                    i.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=EW)
                elif self.count_3 == 1:
                    try:
                        self.image_1 = ImageTk.PhotoImage(
                            Image.open(self.stu_pics[int(self.global_count_frame) - 1]).resize((375, 250)))
                        i.config(image=self.image_1)
                    except:
                        pass
                    i.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=EW)

                elif self.count_3 == 2:
                    Label(self.frame_5, text="OPTIONS", bg="#111112", fg="white", font=self.font_title).grid(row=4,
                                                                                                             column=0,
                                                                                                             columnspan=2,
                                                                                                             sticky=EW)
                if self.count_3 >= 2:
                    placement_row = random.choice(row_grid_array)
                    placement_col = random.choice(col_grid_array)
                    i.grid(row=placement_row, column=placement_col, padx=10, pady=10)
                    row_grid_array.remove(placement_row)
                    col_grid_array.remove(placement_col)
                self.count_3 += 1

        self.frame_6 = Frame(self.window_3, bg="#6c706d", height=550, width=550, bd=5, relief=RIDGE)
        self.frame_6.grid(row=1, column=3, columnspan=1)
        self.frame_6.grid_propagate(False)
        # Scrollbar for treeview
        self.scrollbar_4 = ttk.Scrollbar(self.frame_6, orient="vertical")
        self.scrollbar_4.grid(row=0, column=1, sticky=NSEW)
        # treeview configurations
        treeview_2_header = ("Question number")
        treeview_2_config = ttk.Style()
        treeview_2_config.theme_use("clam")
        treeview_2_config_h = ttk.Style()
        treeview_2_config_h.configure("Treeview.heading")
        treeview_2_config.configure("TTreeview", background="#36393E", foreground="silver",
                                    fieldbackground="#36393E", font=self.tree_font,
                                    yscrollcommand=self.scrollbar_4.set, rowheight=44)
        treeview_2_config.map("TTreeview", background=[("selected", "#808080")],
                              foreground=[("!selected", "white"), ("selected", "black")])
        treeview_2_config.map("TTreeview.heading")
        self.treeview_2 = ttk.Treeview(self.frame_6, show="headings")
        self.scrollbar_4.configure(command=self.treeview_2.yview)
        self.treeview_2["columns"] = treeview_2_header
        self.treeview_2.column("#1", width=120, anchor=W)
        self.treeview_2.heading("#1", text="Question number", anchor=W)
        # frame_5 imp
        self.curr_img = "";self.pre_img="";self.ssim_val = 1.0;self.img_warning=0
        for i in range(1, len(eval(self.test_data[5]))+1):
            self.treeview_2.insert("", END, values=i, iid=i)
        self.treeview_2.grid(row=0, column=0)
        self.video_label = Label(self.frame_6,height=275, width=500)
        self.video_label.grid(row=5,column=0,padx=5,pady=5)
        self.webcam_ref = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.show_img()
        self.button_7 = Button(self.frame_6, text="SWITCH", fg="black", bg="lime green", relief=RIDGE, bd=5,
                               activebackground="black", activeforeground="white", font=self.font_all, width=32,
                               command=lambda: self.s_switch())
        self.button_7.grid(row=1, column=0, ipadx=0, ipady=0, padx=1, pady=0)
        self.frame_7 = Frame(self.window_3, bg="#282e2a", bd=0, height=75, width=1200)
        self.frame_7.grid(row=3, column=0, sticky=EW, columnspan=10)
        self.button_8 = Button(self.frame_7, text="NEXT", bg="lime green", fg="black", bd=5, relief=RIDGE,
                               activebackground="black", activeforeground="black", font=self.font_all, width=21,
                               command=lambda: self.next_s())
        self.button_8.grid(row=0, column=0, padx=15)
        self.button_9 = Button(self.frame_7, text="CLEAR", bg="lime green", fg="black", bd=5, relief=RIDGE,
                               activebackground="black", activeforeground="black", font=self.font_all, width=21,
                               command=lambda: self.clear_s())
        self.button_9.grid(row=0, column=1, padx=10)
        self.button_10 = Button(self.frame_7, text="CLEAR ALL ", bg="lime green", fg="black", bd=5, relief=RIDGE,
                                activebackground="black", activeforeground="black", font=self.font_all, width=21,
                                command=lambda: self.clear_all_s())
        self.button_10.grid(row=0, column=2, padx=10)
        self.button_11 = Button(self.frame_7, text="SUBMIT", bg="lime green", fg="black", bd=5, relief=RIDGE,
                                activebackground="black", activeforeground="black", font=self.font_all, width=21,
                                command=lambda: self.save_s())
        self.button_11.grid(row=0, column=3, padx=10)
        self.button_12 = Button(self.frame_7, text="EXIT", bg="lime green", fg="black", bd=5,
                                relief=RIDGE, activebackground="black", activeforeground="black",
                                font=self.font_all, width=21, command=lambda: self.exit_t())
        self.button_12.grid(row=0, column=4, padx=10)
        #self.window_3.bind("<Leave>",self.check_focus)
        #self.window_3.bind("<Enter>",self.check_focus_again)
        self.window_3.bind("<FocusOut>",self.event_handler)
        self.window_3.bind("<FocusIn>",self.event_handler_1)
    def show_img(self):
        self.user_img = cv2.cvtColor(self.webcam_ref.read()[1],cv2.COLOR_BGR2RGB)
        self.display_img  = ImageTk.PhotoImage(image=Image.fromarray(self.user_img))
        self.curr_img = self.user_img
        if self.img_warning>10:
            self.window_3.unbind(self.event_handler)
            self.window_3.unbind(self.event_handler_1)
            self.window_3.destroy()
            for i in self.ans_var:
                i.set("")
            self.save_s()
            msgbox.showwarning("Warning","Frequent abnormal motions detected and thereby the application rejects your entries")
        if str(self.pre_img)!="":
            self.pre_img= np.squeeze(self.pre_img)
            self.curr_img = np.squeeze(self.curr_img)
            self.ssim_val = ssim(self.pre_img, self.curr_img,channel_axis=-1, data_range=255)
            print(self.ssim_val)
            if self.ssim_val<0.570:
                self.check_true = False
                self.img_warning+=1
                if msgbox.showwarning("Warning","Questionable activities detected...Please make sure your postures are correct"):
                    time.sleep(0.5)
                    self.check_true=True
        self.pre_img = self.curr_img
        self.video_label.config(image=self.display_img)
        self.video_label.after(10,self.show_img)
    def event_handler_1(self,event):
        if self.check_true == False and self.warning <= 5 and event.widget == self.window_3:
            self.check_true = True
    def event_handler(self,event):
        if self.warning>5:
            self.window_3.unbind(self.event_handler)
            self.window_3.unbind(self.event_handler_1)
            self.window_3.destroy()
            for i in self.ans_var:
                i.set("")
            self.save_s()
            msgbox.showinfo("Info","You've navigated out of the screen for more than 5 thereby your entries will not be taken into consideration")
        if self.check_true and self.warning<=5 and self.window_3==event.widget:
            self.warning+=1
            self.check_true=False
    def clear_all_s(self):
        for i in self.widg_list:
            for j in i[2::1]:
                j.deselect()
    def save_s(self):
        self.user_ans = []
        for i in self.ans_var:
            self.user_ans.append(i.get())
        marks_scored = 0
        for i in range(len(self.user_ans)):
            if self.user_ans[i]==self.ans_key[i]:
                marks_scored+=1
        test_table = str(self.test_data[0])+"_"+str(self.test_data[2])+"_marks"
        self.cursor_1.execute(r'INSERT INTO {test_table} VALUES({user_id},"{user_name}",{marks},"{ans_given}")'.format(test_table=test_table,user_id=self.login_userdata[0],user_name=self.login_userdata[1],marks=marks_scored,ans_given=self.user_ans))
        msgbox.showinfo("INFO","Your tests has been successfully submitted")
    def clear_s(self):
        for i in self.widg_list[int(self.global_count_frame)-1][2::1]:
            i.deselect()
    def create_test(self):
        self.count_1 = 0
        self.window_2 = tx.Toplevel()
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
        print(self.frame_widg[int(self.global_count_frame)-1][1]["text"])
        if self.frame_widg[int(self.global_count_frame)-1][1]["text"] != "REMOVE IMAGE":
            file_name = fd.askopenfilename(filetypes=self.file_types)
            if file_name=="":
                pass
            else:
                self.frame_widg[int(self.global_count_frame)-1][1].config(text = "REMOVE IMAGE")
                self.frame_widg[int(self.global_count_frame)-1][1].config(bg="green")
                self.update()            
                self.quest_pics.insert(int(self.global_count_frame)-1,file_name)
        else:
            self.quest_pics[int(self.global_count_frame)-1] = 0
            self.frame_widg[int(self.global_count_frame)-1][1].config(text="OPEN PIC")
            self.frame_widg[int(self.global_count_frame)-1][1].config(bg="lime green")
            msgbox.showinfo("Info","The following image has been removed")
        print(self.quest_pics)
    def append_values(self):
        self.quest_pics=[]
        self.test_code = self.entry_5.get()
        self.password_1 = self.entry_6.get()
        self.test_name = self.entry_7.get()
        self.quest_no = self.entry_8.get()
        for i in range(int(self.quest_no)):
            self.quest_pics.append(0)
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
                    self.window_3 = tx.Toplevel()
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
                    self.frame_5_ref = tx.ScrolledWindow(self.frame_4,height=self.h_1,width=self.w_1,)
                    self.frame_5 = self.frame_5_ref.window
                    self.frame_5_ref.grid(row=0,column=0)
                    self.frame_widg = []
                    self.frame_5.config(bg="#111112")
                    self.count_3 = 0
                    self.global_count_frame = 1
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
                    treeview_2_config_h.configure("Treeview.heading")
                    treeview_2_config.configure("Treeview", background="#36393E", foreground="silver",
                                                fieldbackground="#36393E", font=self.tree_font,
                                                yscrollcommand=self.scrollbar_4.set,rowheight=44)
                    treeview_2_config.map("Treeview", background=[("selected", "#808080")],
                                          foreground=[("!selected", "white"), ("selected", "black")])
                    treeview_2_config.map("Treeview.heading")
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
                                      activebackground="black", activeforeground="white", font=self.font_all, width=32,command=lambda:self.switch())
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
        self.count_3 = 0
        if int(self.global_count_frame)<int(self.quest_no):
            for i in self.frame_widg[int(self.global_count_frame)-1]:
                i.forget()
            self.global_count_frame=int(self.global_count_frame)+1
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
        else:
            msgbox.showinfo("Info","Final question reached ...")
    def next_s(self):
        self.count_3 = 0
        if int(self.global_count_frame) < len(eval(self.test_data[5])):
            for i in self.widg_list[int(self.global_count_frame)-1]:
                i.grid_forget()
            row_grid_array = [5, 6, 5, 6]
            col_grid_array = [0, 1, 0, 1]
            self.global_count_frame = int(self.global_count_frame) + 1
            for i in self.widg_list[int(self.global_count_frame)-1]:
                if self.count_3 == 0:
                    Label(self.frame_5, text="QUESTION", bg="#111112", fg="white", font=self.font_title).grid(row=0,
                                                                                                              column=0,
                                                                                                              columnspan=2,
                                                                                                              sticky=EW,
                                                                                                              padx=10,
                                                                                                              pady=10)
                    i.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=EW)
                elif self.count_3 == 1:
                    try:
                        self.image_1 = ImageTk.PhotoImage(
                            Image.open(self.stu_pics[int(self.global_count_frame) - 1]).resize((375, 250)))
                        i.config(image=self.image_1)
                    except:
                        pass
                    i.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=EW)

                elif self.count_3 == 2:
                    Label(self.frame_5, text="OPTIONS", bg="#111112", fg="white", font=self.font_title).grid(row=4,
                                                                                                             column=0,
                                                                                                             columnspan=2,
                                                                                                             sticky=EW)
                if self.count_3 >= 2:
                    placement_row = random.choice(row_grid_array)
                    placement_col = random.choice(col_grid_array)
                    i.grid(row=placement_row, column=placement_col, padx=10, pady=10)
                    row_grid_array.remove(placement_row)
                    col_grid_array.remove(placement_col)
                self.count_3 += 1
        else:
            msgbox.showinfo("Info", "Final question reached ...")
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
        for i in self.frame_widg:
            d_1[i[0].return_text().rstrip()] = r'{a}-###-{b}-###-{c}-###-{d}-###-{e}'.format(a=self.quest_pics[count],b=i[2].get(),c=i[3].get(),d=i[4].get(),e=i[5].get())
            count += 1
        for i in d_1:
            if i.isspace() or i == "":
                msgbox.showerror("Error","bREAK1")
                break
        else:
            flag_1 = True
            for i in list(d_1.values()):
                for j in i.split("-###-"):
                    if type(j) == type("a"):
                        if j.isspace() or j == "":
                            msgbox.showerror("Error","Break2")
                            flag_1 = False
                            break
                    elif type(j) == type(0):
                        if i == 0 :
                            msgbox.showerror("Error","Error has occured")

                if flag_1==False:
                    break
            else:
                self.cursor_1.execute(r'INSERT INTO tests VALUES ({test_id},"{applicants}","{test_name}","{host}","{scheduled_time}","{test_questions}")'.format(test_id=int(self.test_code),applicants=str(self.applicants),test_name=str(self.test_name),host=self.user_name,scheduled_time=self.timestap,test_questions=d_1))
                self.clear_all_t()
                msgbox.showinfo("Info","The following test has been successfully created")
                self.cursor_1.execute("CREATE TABLE {table_name}(user_id int primary key,user_name varchar(255) not null,marks int not null,answers_given blob not null)".format(table_name=str(self.test_code)+"_"+str(self.test_name)+"_marks"))
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
    def s_switch(self):
       self.count_at = self.treeview_2.focus()
       for i in self.widg_list[int(self.global_count_frame)-1]:
           i.grid_forget()
       self.count_3 = 0
       self.global_count_frame = int(self.count_at)
       row_grid_array = [5, 6, 5, 6]
       col_grid_array = [0, 1, 0, 1]
       for i in self.widg_list[int(self.global_count_frame)-1]:
           if self.count_3 == 0:
               Label(self.frame_5, text="QUESTION", bg="#111112", fg="white", font=self.font_title).grid(row=0,column=0,columnspan=2,sticky=EW,padx=10,pady=10)
               i.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=EW)
           elif self.count_3 == 1:
               try:
                   self.image_1 = ImageTk.PhotoImage(
                       Image.open(self.stu_pics[int(self.global_count_frame) - 1]).resize((375, 250)))
                   i.config(image=self.image_1)
               except:
                   pass
               i.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=EW)

           elif self.count_3 == 2:
               Label(self.frame_5, text="OPTIONS", bg="#111112", fg="white", font=self.font_title).grid(row=4,column=0,columnspan=2,sticky=EW)
           if self.count_3 >= 2:
               placement_row = random.choice(row_grid_array)
               placement_col = random.choice(col_grid_array)
               i.grid(row=placement_row, column=placement_col, padx=10, pady=10)
               row_grid_array.remove(placement_row)
               col_grid_array.remove(placement_col)
           self.count_3 += 1

    def FrameWidth(self, event):
        canvas_width = event.width
        canvas_height = event.height
        self.canvas_1.itemconfig(self.frame_id, width=canvas_width,height=canvas_height)
    def OnFrameConfigure(self, event):
        self.canvas_1.configure(scrollregion=self.canvas_1.bbox("all"))
    def sign_up(self):
        self.window_1 = tx.Toplevel()
        self.window_1.wm_attributes("-topmost", 1)
        self.window_1.configure(bg="#282e2a")
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
        self.entry_4 = Entry(self.window_1,bd=5,bg="lime green",fg="black",font=self.font_general,relief=RIDGE,show="*")
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
        if self.signup_username != "" or self.signup_username.isspace() == False:
            for i in self.user_data:
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