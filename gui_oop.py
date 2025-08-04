from chatbot_oop import Chatbot
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
from PIL import Image,ImageTk
import io
from tkinter import filedialog
import pandas as pd

class GUI(Tk,Chatbot):
    def __init__(self):
        Tk.__init__(self)
        Chatbot.__init__(self)
        self.title("ShadowBot")
        self.geometry("600x600")
        self.ShadowBotIcon_imp = Image.open("shadowbots.icns")
        self.ShadowBotIcon = ImageTk.PhotoImage(self.ShadowBotIcon_imp)
        self.iconphoto(True,self.ShadowBotIcon)

        self.output = ScrolledText(self,wrap=WORD,font = ("Arial",15))
        self.output.configure(state=DISABLED)
        self.entry = Entry(self)
        self.entry.bind("<Return>",self.output_show)

        self.output.pack(fill="both",expand=True)
        self.entry.pack(fill="x")
        self.csv = None
        self.images= []
        self.reply_f = ""
    def output_show(self,event=None):
        self.inputx = self.entry.get()
        self.entry.delete(0,END)
        self.output.configure(state=NORMAL)
        self.output.insert(END,"\n\n")
        self.output.insert(END,f"You: {self.inputx}\n")
        if self.inputx == "upload csv":
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if file_path:
                df = pd.read_csv(file_path)
                self.csv = df
                self.output.insert(END,"Csv Uploaded\n\n")
                self.output.configure(state=NORMAL)
                return
            else:
                self.output.insert(END,"Failed to upload csv\n\n")
                self.output.configure(state=DISABLED)
                return
        if "line plot" in self.inputx.lower() or "bar plot" in self.inputx.lower() or "barh plot" in self.inputx.lower():
            image = Image.open(self.do_csv(self.inputx,self.csv))
            image_tk = ImageTk.PhotoImage(image)
            self.images.append(image_tk)
            self.output.image_create(END,image=image_tk)
            self.output.insert(END,"\n\n")
            
            self.output.configure(state=DISABLED)
            return
        
        if "search" not in self.inputx.lower():
            self.search = None
        else:
            self.search_thing(self.inputx)
        self.output.insert(END,f"AI: ")
        self.output_modify(self.reply_chtbot(self.inputx))
        self.output.insert("\n\n")
        self.output.configure(state=DISABLED)
    def do_csv(self,usertext,df):
        plt.cla()
        text_l = usertext.split()
        for_xaxis = text_l[text_l.index("by")+1]
        xaxis = "".join(i for i in df.columns if i.lower() == for_xaxis.lower())
        for j in text_l:
            if j == "by":
                break
            else:
                for i in df.columns:
                    if i.lower() == j.lower():
                        if text_l[0].lower() == "line":
                             plt.plot(df[xaxis],df[i],label=i)
                        elif text_l[0].lower() == "bar":
                             plt.bar(df[xaxis],df[i],label=i)
                        elif text_l[0].lower() == "barh":
                             plt.barh(df[xaxis],df[i],label=i)
        plt.legend()
        image_1 = io.BytesIO()
        plt.savefig(image_1,format="png")
        image_1.seek(0)
        return image_1
    def output_modify(self,reply):
        try:
            tokens = next(reply) 
            self.output.configure(state=NORMAL)
            self.output.insert(END,tokens)
            self.output.configure(state=DISABLED)
            self.output.after(30,self.output_modify,reply)
            self.reply_f += tokens
        except StopIteration:
            self.output.configure(state=DISABLED)
            self.context += f"User:{self.inputx},Ai:{self.reply_f}"
            self.reply_f = ""
gui = GUI()
gui.mainloop()
