import subprocess
import tkinter as tk
import util
import cv2
from PIL import Image, ImageTk
import os 

class App:
    def __init__(self) -> None:
        self.main_window=tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.login_button=util.get_button(self.main_window,'Log In','blue',self.login)
        self.login_button.place(x=750,y=300)

        self.register_new_user_button=util.get_button(self.main_window,"Register",'gray',self.register_new_user,fg='black')
        self.register_new_user_button.place(x=750,y=400)

        self.webcam_label=util.get_img_label(self.main_window)
        self.webcam_label.place(x=10,y=0,width=700,height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir='./db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

    def add_webcam(self,label):
        if 'cap' not in self.__dict__:
          self.cap=cv2.VideoCapture(0)
        self._label=label
        self.process_webcam()

    def process_webcam(self):
        ret,frame=self.cap.read()
        self.recent_capture=frame
        img_=cv2.cvtColor(self.recent_capture,cv2.COLOR_BGR2RGB)
        self.recent_capture_pil=Image.fromarray(img_)
        imgtk=ImageTk.PhotoImage(image=self.recent_capture_pil)
        self._label.imgtk=imgtk
        if not hasattr(self, '_label_widget'):
          self._label_widget = tk.Label(self.main_window, image=imgtk)
          self._label_widget.place(x=10, y=0, width=700, height=500)
        else:
           self._label_widget.configure(image=imgtk)

        self._label_widget.after(20, self.process_webcam)
       

   
    


    

    
    def login(self):
        unkown_img='./.tmp.jpg'
        cv2.imwrite(unkown_img,self.recent_capture)
        output=subprocess.check_output(['face_recognition',self.db_dir,unkown_img])
        print(output)

        
    def register_new_user(self):
        self.register_new_user_window=tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+350+120")
        
        self.accept_button_register_new_user=util.get_button(self.register_new_user_window,'Accept','green',self.accept_register_new_user)
        self.accept_button_register_new_user.place(x=750,y=300)

        self.try_again_button_register_new_user=util.get_button(self.register_new_user_window,'Try again','red',self.try_again)
        self.try_again_button_register_new_user.place(x=750,y=400)

        self.capture_label=util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10,y=0,width=700,height=500)

        self.add_img_to_label()

        self.add_new_username=util.get_entry_text(self.register_new_user_window)
        self.add_new_username.place(x=750,y=150)

        self.text_newUser_label=util.get_text_label(self.register_new_user_window,'Enter Username:  ')
        self.text_newUser_label.place(x=750,y=80)

        
    
    
   


    def add_img_to_label(self):
        imgtk=ImageTk.PhotoImage(image=self.recent_capture_pil)
        self.capture_label.imgtk=imgtk
        self.capture_label.configure(image=imgtk)

        self.new_user_capture=self.recent_capture.copy()

    
    def accept_register_new_user(self):
        name=self.add_new_username.get(1.0,"end-1c")
        cv2.imwrite(os.path.join(self.db_dir,'{}.jpg'.format(name)),self.new_user_capture)

        util.msg_box('Success!','Registered Successfully')
        self.register_new_user_window.destroy()


    def try_again(self):
        self.register_new_user_window.destroy()




        

    
    def start(self):
        self.main_window.mainloop()


if __name__=="__main__":
    app=App()
    app.start()