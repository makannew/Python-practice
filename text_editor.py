# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 19:26:11 2019

@author: MAKAN
"""

import tkinter 
import tkinter.filedialog,tkinter.messagebox
class text_editor(tkinter.Tk):
    def __init__(self,*args , **kwargs):
        #check if filename passed to the class
        if "filename" in kwargs:
            self.start_up_file=kwargs["filename"]
            #remove filename to prevent conflict with tkinter.Tk kwargs
            del kwargs["filename"]
        else:
            self.start_up_file=""
        #initialize tkinter toplevel base
        tkinter.Tk.__init__(self, *args, **kwargs)
        #Do other things after tkinter.TK initialization
        main_frame = tkinter.Frame(self) 
        main_frame.grid(column=0,row=0,sticky="nsew")
        #text editing area inside main_frame
        self.text_box = tkinter.Text(main_frame, wrap="word", yscrollcommand=True,padx=5,pady=5)
        self.text_box.grid(column=0,row=0,sticky="nsew")
        #scrolling widget for text_box
        sbar=tkinter.Scrollbar(main_frame,command=self.text_box.yview)
        sbar.grid(column=1,row=0,sticky="ns")
        #allow resizing 
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        main_frame.columnconfigure(0,weight=1)
        main_frame.rowconfigure(0,weight=1)
        #create menu widgets
        self.menu_bar=tkinter.Menu(self)
        self["menu"]=self.menu_bar
        self.menu_file=tkinter.Menu(self.menu_bar,tearoff=0)
        menu_edit=tkinter.Menu(self.menu_bar,tearoff=0)
        self.menu_bar.add_cascade(menu=self.menu_file,label="File")
        self.menu_bar.add_cascade(menu=menu_edit,label="Edit")
        #create menu items
        self.menu_file.add_command(label="Open", command=self.open_file)
        self.menu_file.add_command(label="Save",command=self.save_file)
        self.menu_file.add_command(label="Save As...",command=self.save_as)
        self.menu_file.add_command(label="Exit",command=self.exit_editor)
        #preload default filename of file
        if (self.start_up_file==""):
            self.filename="untitled.txt"
            self.instant_save=False
            self.menu_file.entryconfig("Save",state="disabled")
            tkinter.Tk.title(self,self.filename)
        else:
            self.filename=self.start_up_file
            if (self.read_file(self.filename)):
                self.instant_save=True
            else:
                self.instant_save=False
                self.filename="untitled.txt"
                
    def open_file(self):
        filename=tkinter.filedialog.askopenfilename()
        self.read_file(filename)

    def read_file(self,filename):
        if (filename==""):
            return False
        try:
            file=open(filename,"r")
            #delete text_box content
            self.text_box.delete(1.0,"end")
            self.text_box.insert("end",file.read())
            self.filename=filename
            file.close()
            #set title to file name
            tkinter.Tk.title(self,self.filename)
            #Enable instant save item in menu bar
            self.menu_file.entryconfig("Save",state="normal")
            return True
        except:
            tkinter.messagebox.showerror(parent=self,title="Error",message="Error while trying to read the file")
            return False
    def save_as(self):
        filename=tkinter.filedialog.asksaveasfile(mode="w",initialfile=self.filename,defaultextension="txt")
        if (filename.name==""):
            return
        self.filename=filename.name
        self.save_file()
        return
    def save_file(self):

        try:
            file=open(self.filename,"w")
            file.write(self.text_box.get("1.0","end-1c"))
            file.close
            self.instant_save=True
        except:
            tkinter.messagebox.showerror(parent=self,title="Error",message="Error while trying to save the file")
       
    def exit_editor(self):
        self.destroy()
        
#instantiate an text_editor 
editor1 = text_editor()
editor1.geometry("800x600")

editor1.mainloop()

        
        