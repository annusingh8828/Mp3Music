from tkinter import *
import pygame
from tkinter import filedialog 
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import time

root = Tk()
root.title('MUSIC PLAYER')
root.geometry("500x400")

pygame.mixer.init()

def play_time():
    if stopped:
        return

    current_time= pygame.mixer.music.get_pos()/1000
    converted_current_time = time.strftime('%M:%S',time.gmtime(current_time))
    current_song = song_box.curselection()  
    song = song_box.get(ACTIVE)  
    song = f'C:/GUI/Audio/{song}.mp3'

    song_mut = MP3(song)
    
    global song_length
    song_length = song_mut.info.length 
    converted_song_length = time.strftime('%M:%S',time.gmtime(song_length))
   
    current_time+=1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time elapsed: {converted_song_length}')
    
    elif paused:
        pass

    elif int(my_slider.get()) == int(current_time):
        slider_position = int(song_length)
        my_slider.config(to = slider_position, value=int(current_time))

    else:
        slider_position = int(song_length)
        my_slider.config(to = slider_position, value=int(my_slider.get()))
        converted_current_time = time.strftime('%M:%S',time.gmtime(int(my_slider.get())))
        status_bar.config(text=f'Time elapsed: {converted_current_time} of {converted_song_length}')
        
        next_time = int(my_slider.get())+1
        my_slider.config(value=next_time)
    
    status_bar.after(1000,play_time)
    

def add_song():
    song = filedialog.askopenfilename(initialdir = 'C:/GUI/Audio/',title="Choose a Song",filetypes=(("mp3 Files","*.mp3"),))
    song = song.replace("C:/GUI/Audio/","")
    song = song.replace(".mp3","")
    song_box.insert(END,song) 

def add_many_song():
    songs = filedialog.askopenfilenames(initialdir = 'C:/GUI/Audio/',title="Choose a Song",filetypes=(("mp3 Files","*.mp3"),))

    for song in songs:
        song = song.replace("C:/GUI/Audio/","")
        song = song.replace(".mp3","")
        song_box.insert(END,song)

def play():
    global stopped
    stopped = False
    song = song_box.get(ACTIVE) 
    song = f'C:/GUI/audio/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)   

    play_time()

global stopped
stopped = False
def stop():
    status_bar.config(text='')
    my_slider.config(value=0)
   
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    status_bar.config(text='')

    global stopped
    stopped = True

def next_song():
    status_bar.config(text='')
    my_slider.config(value=0)

    next_one = song_box.curselection()  
    next_one = next_one[0]+1 
    song = song_box.get(next_one)  
    song = f'C:/GUI/Audio/{song}.mp3' 
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0,END) 

    song_box.activate(next_one)
    song_box.selection_set(next_one,last=None) 

def previous_song():
	
    status_bar.config(text='')
    my_slider.config(value=0)
    
    next_one = song_box.curselection()  
    next_one = next_one[0]-1  
    song = song_box.get(next_one)  
    song = f'C:/GUI/Audio/{song}.mp3'  
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.selection_clear(0,END) 

    song_box.activate(next_one)
    song_box.selection_set(next_one,last=None)

global paused
paused = False

def pause(is_paused):
    global paused    
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()  
        paused = False

    else:
        pygame.mixer.music.pause()
        paused = True

def delete_song():  
    stop()
    song_box.delete(ANCHOR) 
    pygame.mixer.music.stop()

def delete_all_songs():
    stop()
    song_box.delete(0,END)  
    pygame.mixer.music.stop() 

def slide(x):
    song = song_box.get(ACTIVE) 
    song = f'C:/GUI/audio/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))


song_box = Listbox(root,bg="black",fg="white",width=60,
selectbackground = "green", selectforeground="black")   
song_box.pack(pady=30)  

back_button_img = PhotoImage(file='C:/GUI/Images/back.png')
forward_button_img = PhotoImage(file='C:/GUI/Images/forward.png')
play_button_img = PhotoImage(file='C:/GUI/Images/play.png')
pause_button_img = PhotoImage(file='C:/GUI/Images/pause.png')
stop_button_img = PhotoImage(file='C:/GUI/Images/stop.png')

controls_frame = Frame(root)
controls_frame.pack()

back_button = Button(controls_frame, image=back_button_img,borderwidth=0,command=previous_song) 
forward_button = Button(controls_frame, image=forward_button_img,borderwidth=0,command=next_song)
play_button = Button(controls_frame, image=play_button_img,borderwidth=0,command=play)
pause_button = Button(controls_frame, image=pause_button_img,borderwidth=0,command=lambda:pause(paused))
stop_button = Button(controls_frame, image=stop_button_img,borderwidth=0,command=stop)

back_button.grid(row=0,column=0,padx=10)
forward_button.grid(row=0,column=1, padx=10)
play_button.grid(row=0 ,column=2,padx=10 )
pause_button.grid(row=0 ,column=3 ,padx=10)
stop_button.grid(row= 0,column=4,padx=10 )

my_menu = Menu(root)
root.config(menu = my_menu)

add_song_menu = Menu(my_menu)

my_menu.add_cascade(label = "ADD SONGS",menu=add_song_menu)

add_song_menu.add_command(label="ADD ONE SONG TO PLAYLIST",command=add_song)

add_song_menu.add_command(label="ADD MANY SONGS TO PLAYLIST",command=add_many_song)

remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label = "REMOVE SONGS", menu = remove_song_menu)
remove_song_menu.add_command(label="DELETE A SONG FROM PLAYLIST", command=delete_song)
remove_song_menu.add_command(label="DELETE ALL SONGS FROM PLAYLIST",command=delete_all_songs)

status_bar = Label(root, text='',bd=1,relief = GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)
                
my_slider = ttk.Scale(root, from_ = 0, to=100,value=0,command = slide,length=360)
my_slider.pack(pady=40) 

root.mainloop()