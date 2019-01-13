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
        #handle closing window by user
        self.protocol("WM_DELETE_WINDOW",self.exit_editor)
        #Do other things after tkinter.TK initialization
        main_frame = tkinter.Frame(self) 
        main_frame.grid(column=0,row=0,sticky="nsew")
        #scrolling widget for text_box
        self.sbar=tkinter.Scrollbar(main_frame)
        self.sbar.grid(column=1,row=0,sticky="ns")
        #text editing area inside main_frame
        self.text_box = tkinter.Text(main_frame, wrap="word", yscrollcommand=self.sbar.set,padx=5,pady=5)
        self.text_box.grid(column=0,row=0,sticky="nsew")
        #config scrollbar after text_box instantiation
        self.sbar.config(command=self.text_box.yview)

        #allow resizing 
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        main_frame.columnconfigure(0,weight=1)
        main_frame.rowconfigure(0,weight=1)
        #create menu widgets
        self.menu_bar=tkinter.Menu(self)
        self["menu"]=self.menu_bar
        self.menu_file=tkinter.Menu(self.menu_bar,tearoff=0)
        self.menu_edit=tkinter.Menu(self.menu_bar,tearoff=0,postcommand=self.refresh_edit_states)
        self.menu_bar.add_cascade(menu=self.menu_file,label="File")
        self.menu_bar.add_cascade(menu=self.menu_edit,label="Edit")
        #create menu items
        self.menu_file.add_command(label="Open", command=self.open_file)
        self.menu_file.add_command(label="Save",command=self.save_file)
        self.menu_file.add_command(label="Save As...",command=self.save_as)
        self.menu_file.add_command(label="Exit",command=self.exit_editor)
        self.menu_edit.add_command(label="Copy",state="disabled",command=self.copy_text)
        self.menu_edit.add_command(label="Cut",state="disabled",command=self.cut_text)
        self.menu_edit.add_command(label="Paste",state="disabled",command=self.paste_text)
        #create right-click menue
        self.rclick_menu=tkinter.Menu(self,tearoff=0,postcommand=self.refresh_edit_states)
        self.rclick_menu.add_command(label="Copy",state="disabled",command=self.copy_text)
        self.rclick_menu.add_command(label="Cut",state="disabled",command=self.cut_text)
        self.rclick_menu.add_command(label="Paste",state="disabled",command=self.paste_text)

        
        #popup right-click menu according operation system
        if (self.tk.call('tk', 'windowingsystem')=='aqua'):
            #keep it cross-platform
            self.text_box.bind("<2>",lambda e:self.rclick_menu.post(e.x_root,e.y_root))
            self.text_box.bind("<Control-1>",lambda e:self.rclick_menu.post(e.x_root,e.y_root))
        else:
            self.text_box.bind("<3>",lambda e:self.rclick_menu.post(e.x_root,e.y_root))
            
        
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
    def refresh_edit_states(self):
        try:
            if(self.clipboard_get()!=""):
                self.rclick_menu.entryconfig("Paste",state="normal")
                self.menu_edit.entryconfig("Paste",state="normal")
            else:
                self.rclick_menu.entryconfig("Paste",state="disabled")
                self.menu_edit.entryconfig("Paste",state="disabled")
        except:
                self.rclick_menu.entryconfig("Paste",state="disabled")
                self.menu_edit.entryconfig("Paste",state="disabled")            
        try:
            self.text_box.selection_get()
            self.rclick_menu.entryconfig("Copy",state="normal")
            self.menu_edit.entryconfig("Copy",state="normal")
            self.rclick_menu.entryconfig("Cut",state="normal")
            self.menu_edit.entryconfig("Cut",state="normal")
        except:
            self.rclick_menu.entryconfig("Copy",state="disabled")
            self.menu_edit.entryconfig("Copy",state="disabled")
            self.rclick_menu.entryconfig("Cut",state="disabled")
            self.menu_edit.entryconfig("Cut",state="disabled")
        
    def copy_text(self):
        self.clipboard_clear()
        self.clipboard_append(self.text_box.selection_get())
    
    def paste_text(self):
        try:
            self.text_box.delete("sel.first","sel.last")
        except:
            pass
        self.text_box.insert("insert",self.clipboard_get())
    
    def cut_text(self):
        self.copy_text()
        self.text_box.delete("sel.first","sel.last")
           
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
        try:
            self.filename=filename.name
            self.save_file()
        except:
            pass
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
        if (self.text_box.get("1.0","end-1c")==""):
            self.destroy()
            return
        try:
            file=open(self.filename,"r")
            if(file.read()==self.text_box.get("1.0","end-1c")):
               file.close
               self.destroy()
               return
        except:
            pass
        save_on_close = tkinter.messagebox.askyesnocancel(message="Do you want save changes?",)
        if (save_on_close==False):
            self.destroy()
            return
        elif(save_on_close==None):
            return
        else:
            if(self.menu_file.entrycget("Save","state")=="normal"):
                try:
                    self.save_file()
                    self.destroy()
                    return
                except:
                    return
            else:
                try:
                    self.save_as()
                    if(self.instant_save):
                        self.destroy()
                        return
                    else:
                        return
                except:
                    return
            return
        
#instantiate a text_editor and load a file
if (__name__=="__main__"):
    editor1 = text_editor(filename="readme.md")
    editor1.geometry("800x600")
    editor1.mainloop()

        
        