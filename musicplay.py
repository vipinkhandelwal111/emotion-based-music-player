from tkinter import *
import random
import time
import os
import pygame
import vlc
import speech_recognition as sr 
import requests
#from mutagen.id3 import ID3
from tkinter.messagebox import *
from tkinter.ttk import *
import requests
import cv2


cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "xyz.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()




auth_headers = {
    'app_id': 'b9b48835',
    'app_key': '9d83ecd2df2d2ac31206265f5f5e3584'
}

url = 'https://api.kairos.com/v2/media'
files = {
    'source': open('xyz.png')
}
data = {
    'timeout': 60
}


response = requests.post(url, files=files, data=data, headers=auth_headers)

f = (response.json())

h = f['frames'][0]['people']
if (h == []):
	print("face can't recognize")
	exit(0)
else :
	g= f['frames'][0]['people'][0]['emotions']
	k = [(value,key) for key,value in g.items()]
	l = max(k)[1]
	
	print(f)
	print(g)
	print(l)

	root = Tk()
	root.geometry("1600x800+0+0")
	root.title("Music Player")

	text_Input = StringVar()
	operator = ""

	instance = vlc.Instance()
	player = instance.media_player_new()



	Tops = Frame(root, width = 1600, height = 50, bg = "Pink" ,relief = SUNKEN)
	Tops.pack(side=TOP)
	f1= Frame(root,width = 800, height = 700, bg = "Pink",relief = SUNKEN)
	f1.pack(side=LEFT)
	f2= Frame(root,width = 200,height = 700, bg = "Pink",relief = SUNKEN)
	f2.pack(side=RIGHT)

	#localtime = time.asctime(time.localtime(time.time()))
	lbifo = Label(Tops,font=('arial',50,"bold"),text="MUSIC PLAYER",fg="Red",bd =10,anchor ="w")
	lbifo.grid(row=0,column=0)	

	#lbifo1 = Label(Tops,font=('arial',20,"bold"),text=s,fg="Red",bd =10,anchor ="w")
	#lbifo1.grid(row=1,column=0)
	def timedisplay():
		localtime = time.asctime(time.localtime(time.time()))
		lbifo1 = Label(Tops,font=('arial',20,"bold"),text=localtime,fg="Red",bd =10,anchor ="w")
		lbifo1.grid(row=1,column=0)
	def displaytime():
		timedisplay()
		Tops.after(1000,displaytime)
	displaytime()
	
	e=[]
	d = []
	index = 0
	for dirname, dirnames, filenames in os.walk('.'):
		print (filenames)
	     #print path to all subdirectories first.
		for subdirname in dirnames:
	     		x = (os.path.join(dirname, subdirname))
		for filename in filenames:
			if filename.endswith(".mp3"):
				p=(os.path.join(dirname, filename))
				d.append(p)
				e.append(filename)
	listbox = Listbox(f2,width = 50,height = 20)
	listbox.grid(row =0,column=2)	

	for items in e:
		listbox.insert(0,items)
	
	
		
	
	def startsong():
		lsl=len(d)
		t=random.randint(0,lsl-1)
		#u = StringVar(f1,value =e[t])
		#q = player.audio_get_time(e[t])
		#print(q)
		songtex = Label(f1,font=('arial',16,"bold"),text=e[t] ,bd = 10,bg = "powder blue",justify ='right').grid(row=1,column=1)
		pb_hD = ttk.Progressbar(f1, orient='horizontal', mode='determinate')
		pb_hD.grid(row=2,column=1)
		#if(player.is_playing == 1):
		pb_hD.start(1000)
		media = instance.media_new(d[t])
		player.set_media(media)
		player.play()	
	def next():
		player.stop()
		startsong()

	def previous():
		player.stop()
		startsong()
	
	def stop():
		player.stop()
	def pp():
		if(player.is_playing()==0):
			player.play()
		else:
			player.pause()
	def volumeup():
		s = player.audio_get_volume()
		s = s+1
		player.audio_set_volume(s)
	def volumedown():
		s = player.audio_get_volume()
		s = s-1
		player.audio_set_volume(s)
	def mm():
		s=player.audio_get_volume()
		if(s!=0):
			player.audio_set_volume(0)
		else:
			player.audio_set_volume(50)
	

	#StartButton =Button(f2,padx=16,pady=16,bd=8,fg = "black",font=('arial',20,'bold'),text="Start Song",bg ="Pink",command =startsong).grid(row =4,column=3)
	NextButton =Button(f2,padx=16,pady=16,bd=8,fg = "black",font=('arial',20,'bold'),text="Next Song",bg ="Pink",command =next).grid(row=3,column=0)
	PreviousButton =Button(f2,padx=16,pady=16,bd=8,fg = "black",font=('arial',20,'bold'),text="Previous Song",bg ="Pink",command=previous).grid(row =3,column=1)
	#StopButton =Button(f2,padx=16,pady=16,bd=8,fg = "black",font=('arial',20,'bold'),text="Stop",bg ="Pink",command =stop).grid(row=1,column=2)
	ppButton =Button(f2,padx=16,pady=16,bd=8,fg = "black",font=('arial',20,'bold'),text="Pause/play",bg ="Pink",command =pp).grid(row=2,column=0)
	volumeupButton =Button(f2,padx=16,pady=16,bd=8,fg = "black",font=('arial',20,'bold'),text="Volume +",bg ="Pink",command =volumeup).grid(row =1,column=0)
	volumedownButton =Button(f2,padx=16,pady=16,bd=8,fg = "black",font=('arial',20,'bold'),text="Volume -",bg ="Pink",command =volumedown).grid(row =1,column=1)
	MuteButton =Button(f2,padx=16,pady=16,bd=8,fg = "black",font=('arial',20,'bold'),text="Mute",bg ="Pink",command =mm).grid(row=2,column=1)
		
	emotionleb= Label(f1,font=('arial',16,"bold"),text ="Emotion",bd = 16,anchor='w').grid(row=0,column=0)
	#v = StringVar(f1,value =l)
	emotiontex = Label(f1,font=('arial',16,"bold"),text=l ,bd = 10,bg = "powder blue",justify ='right').grid(row=0,column=1)
	songleb= Label(f1,font=('arial',16,"bold"),text ="Now Playing",bd = 16,anchor='w').grid(row=1,column=0)
	'''
	u = StringVar(f1,value =e[t])
	songtex = Entry(f1,font=('arial',16,"bold"),textvariable=u ,bd = 10,insertwidth = 4,bg = "powder blue",justify ='right').grid(row=1,column=1)
	pb_hD = ttk.Progressbar(f1, orient='horizontal', mode='indeterminate')
	pb_hD.grid(row=1,column=1)
	
	def baardisplay():
		u = StringVar(f1,value =e[t])
		songtex = Entry(f1,font=('arial',16,"bold"),textvariable=u ,bd = 10,insertwidth = 4,bg = "powder blue",justify ='right').grid(row=1,column=1)
		pb_hD = ttk.Progressbar(f1, orient='horizontal', mode='determinate')
		pb_hD.grid(row=2,column=1)
		pb_hD.start(100)
		
	def displaybaar():
		baardisplay()
		f1.after(1000,displaybaar)
	displaybaar()
	'''

	#showinfo(title = "Mood", message = l)
	startsong()

	

	root.mainloop()


