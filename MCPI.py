#This file is released under the terms of the MIT license.

#imports
import tkinter as tk
import tkinter.filedialog as filedialog #for the save as file dialogue
import requests #to get requests from the Mojang API
import json
import base64
from urllib.request import urlopen #to open the images
from PIL import Image, ImageTk, ImageDraw #to display images, get images from the link and to make the error image
from time import sleep
from pyperclip import copy #uses the copy function to add the UUID to the clipboard
#------

#The entire software: the GUI and displaying everything from the PlayerProperties
class Software():
    def __init__(self):
        self.root = tk.Tk()

        self.root.geometry("1000x525")
        self.root.config(bg = "#00838F")

        #if icon.ico exists it will set it as the gui's icon
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        #sets minimum size to 1000x525
        self.root.minsize(1000, 525)

        self.user_label = tk.Label(self.root,text="MC Player Information", font=("Calibri",30,"bold"), fg="white" ,bg="#006064", width=1000)
        self.user_label.pack(pady=0)

        self.username_text = tk.Label(self.root,text="Username:", font=("Calibri",15,"bold"), bg="#00838F", fg="white")
        self.username_text.pack(pady=5)    

        self.user_entry = tk.Entry(self.root, width=60, font=("Calibri",18),fg="white", bg="#26C6DA", border=0)
        self.user_entry.pack()

        self.info_button = tk.Button(self.root, height=1, width=10,text="FIND INFO", font=("Calibri",14), command=lambda:self.getPlayerProperties(),fg="white", bg="#006064", border=0, activebackground='#007782', activeforeground='white')
        self.info_button.pack(pady=20)

        #creates a playerProperties object to display when opening the softwarez before checking other usernames
        first_skin = PlayerProperties("Technoblade")

        self.uuid_text = tk.Label(self.root,text="UUID:", font=("Calibri",15,"bold"), bg="#00838F", fg="white")
        self.uuid_text.pack()

        self.uuid = tk.Label(self.root,text=first_skin.playerId, font=("Calibri",13), bg="#00838F", fg="white")
        self.uuid.pack()

        #the UUID saved so the user will be able to copy it using the copy button, value changes everytime the user is checking another player.
        self.uuid_val = first_skin.playerId

        self.copy_bttn = tk.Button(self.root, height=1, width=10,text="COPY", font=("Calibri",14), command=lambda:self.copy_UUID(),fg="white", bg="#006064", border=0, activebackground='#007782', activeforeground='white')
        self.copy_bttn.pack(pady=20)        

        self.skin_text = tk.Label(self.root,text="Skin:", font=("Calibri",15,"bold"), bg="#00838F", fg="white")
        self.skin_text.pack()

        #skin image url
        self.url = first_skin.skin_url

        #the image
        self.img = Image.open(urlopen(self.url))

        #the image so it will be used in the tkinter GUI
        self.tk_img = ImageTk.PhotoImage(self.img)

        #displays the skin png
        self.skinPNG = tk.Label(image=self.tk_img, bg="#26C6DA")
        self.skinPNG.pack()

        #error image that will be displayed when there's no user with the given name
        self.error_image = Image.new('RGB', (64, 64), color = '#26C6DA')
        ImageDraw.Draw(self.error_image).text((14, 11),'PLAYER\nNOT\nFOUND',(255,255,255))
        self.tk_error_image = ImageTk.PhotoImage(self.error_image)

        self.download_bttn = tk.Button(self.root, height=1, width=10,text="DOWNLOAD", font=("Calibri",14), command=lambda:self.save_skin(),fg="white", bg="#006064", border=0, activebackground='#007782', activeforeground='white')
        self.download_bttn.pack(pady=20)

        tk.mainloop()


    def getPlayerProperties(self):
        try:
            #new PlayerProperties Object to get all of the player's info, getting the input from the entry widget
            newSkin = PlayerProperties(self.user_entry.get())

            #updates the skin URL
            self.url = newSkin.skin_url

            #the image
            self.img = Image.open(urlopen(self.url))

            #the image so it will be used in the tkinter GUI
            self.tk_img = ImageTk.PhotoImage(self.img)

            #configures the image to be the new image
            self.skinPNG.configure(image=self.tk_img)
            self.skinPNG.pack()

            #changes the saved uuid value so the user will be able to copy the UUID
            self.uuid_val = newSkin.playerId

            #configures the UUID text to the updated UUID
            self.uuid.configure(text=newSkin.playerId)
            self.uuid.pack()

            self.root.bind("<Return>")

        #if username is not correct it won't do anything
        except:
            errorUUID = "Error: PLAYER NOT FOUND"

            #configures the new UUID to errorUUID
            self.uuid.configure(text=errorUUID)
            self.uuid.pack()

            #configures the new skinPNG to the error image
            self.skinPNG.configure(image=self.tk_error_image)
            self.skinPNG.pack()

            self.uuid_val = errorUUID
            
            self.root.bind("<Return>")
    
    #adds the UUID to the clipboard
    def copy_UUID(self):
        copy(self.uuid_val)
    

    def save_skin(self):
        try:
            file=filedialog.asksaveasfilename(filetypes=[('PNG', '*.png')], defaultextension=".png")
            Image.open(urlopen(self.url)).save(file)

        #to not show the error when clicking cancel or not saving
        except:
            pass

        tk.mainloop()

#handling the Mojang API requests
class PlayerProperties():
    def __init__(self,username):
        #GET request to the Mojang API to get the player's uuid
        get_request = requests.get("https://api.mojang.com/users/profiles/minecraft/"+username)
         
        loaded_req = json.loads(get_request.text)

        #get the player's uuid from the loaded json request
        self.playerId = loaded_req["id"]

        #GET request to the Mojang API to get the skin of the player
        get_skin = requests.get("https://sessionserver.mojang.com/session/minecraft/profile/"+str(self.playerId))

        loaded_get_skin = json.loads(get_skin.text)

        #get the value from the loaded request and decodes it from base64
        decoded_props = base64.b64decode(loaded_get_skin["properties"][0]["value"])

        #load the decoded value
        json_new_props = json.loads(decoded_props)

        #get the skin's url from the decoded and loaded json
        self.skin_url = json_new_props["textures"]["SKIN"]["url"]

if __name__ == '__main__':
    try:
        Software()
    #if there's a connection error:
    except:
        #prints this to the console and not to a tkinter gui
        print("Error: Check your network connection OR check if you're connected behind a firewall.", end="\n\n")
        print("The Software will close soon")
        
        sleep(5)
        quit()
