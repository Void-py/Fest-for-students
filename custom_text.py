from tkinter import *
from tkinter import ttk as ttk

class ScrolledText(Frame):
    def __init__(self,root,h,width,bg,fg,font):
        Frame.__init__(self,root)
        self.master=root
        self.height = h
        self.width = width
        self.bg = bg
        self.text_1 = Text(self,bg=bg,fg=fg,font=font,height=h,width=width)
        self.scrollbar_1 = Scrollbar(self,orient=VERTICAL)
        self.scrollbar_1.configure(command=self.text_1.yview)
        self.scrollbar_1.pack(side=RIGHT,fill=BOTH,expand=1)
        self.text_1.pack(side=LEFT,fill=BOTH,expand=1)
    def return_text(self):
        return self.text_1.get("1.0",END)



