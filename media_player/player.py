import os
import random
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Style

import keyboard
import pygame
from PIL import Image, ImageFont
from PIL import ImageTk

font = ImageFont.truetype("content/LabGrotesque-Regular.ttf", size=10)

#отвечает за автоматическое переключение песни на первую, без перескакивания
minus_time_min, minus_time, minutes, seconds, minutes_set, seconds_set, index_next, paused_time = 0, 0, 0, 0, 0, 0, 0, 0
set_the_time, switch, the_last, last_track, check_style = False, False, False, False, True
music_from_switch=""
root = Tk()
root.title("3 laba")
root.geometry("700x500")
custom_font = font
bg="#F6F6F6"
fg="#222222"
width_btn = 70
heigth_btn = 30
style = Style()
style.configure('.', font=(font, 10))
root.grid_rowconfigure(3, weight=1)  # Например, создаем 4 строки (нумерация с 0)
root.grid_columnconfigure(3, weight=1) # 3 rows
root.resizable(False, False)
root.configure(bg=bg)

previous_white_img = ImageTk.PhotoImage(Image.open('content/backward.png'))
previous_black_img = ImageTk.PhotoImage(Image.open('content/backward_night.png'))
next_white_img = ImageTk.PhotoImage(Image.open('content/forward.png'))
next_black_img = ImageTk.PhotoImage(Image.open('content/forward_night.png'))
pause_white_img = ImageTk.PhotoImage(Image.open('content/pause.png'))
pause_black_img = ImageTk.PhotoImage(Image.open('content/pause_night.png'))
continue_white_img = ImageTk.PhotoImage(Image.open('content/play.png'))
continue_black_img = ImageTk.PhotoImage(Image.open('content/play_night.png'))
change_theme_white_img = ImageTk.PhotoImage(Image.open('content/mode.png'))
change_theme_black_img = ImageTk.PhotoImage(Image.open('content/mode_night.png'))
bad_views_white_img = ImageTk.PhotoImage(Image.open('content/sleep.png'))
bad_views_black_img = ImageTk.PhotoImage(Image.open('content/sleep_night.png'))
add_white_img = ImageTk.PhotoImage(Image.open('content/add.png'))
add_black_img = ImageTk.PhotoImage(Image.open('content/add_night.png'))


first = True #Проигрывается ли песня первый раз
closed = False #Отвечает за списком песен
stopped = True #Отвечает за состояние песни

def change_theme(event=None):
    global bg, fg
    if bg == "#F6F6F6":
        bg = "#222222"
        fg = "#F6F6F6"
        root.configure(bg=bg)
        last_btn.configure(image=previous_black_img, command=last_func)
        next_btn.configure(image=next_black_img, command=next_func)
        change_theme_btn.configure(image=change_theme_black_img, command=change_theme)
        if stopped:
            pause_continue_btn.configure(image=pause_black_img, command=continue_pause_func)
        else:
            pause_continue_btn.configure(image=continue_black_img, command=continue_pause_func)

        add_btn.configure(image=add_black_img, command=add)
        music_list.configure(bg=bg, fg=fg)
        name.configure(bg=bg, fg=fg)
        shuffle_btn.configure(bg=bg, fg=fg)
        delete_btn.configure(bg=bg, fg=fg)
        zoom_btn.configure(bg=bg, fg=fg)
        player_frame.configure(bg=bg)
        music_time.configure(bg=bg,fg=fg)
        frame_button_play.configure(bg=bg)
        button_special_frame.configure(bg=bg)

    else:
        bg = "#F6F6F6"
        fg = "#222222"
        root.configure(bg=bg)
        last_btn.configure(image=previous_white_img, command=last_func)
        next_btn.configure(image=next_white_img, command=next_func)
        change_theme_btn.configure(image=change_theme_white_img, command=change_theme)
        if stopped:
            pause_continue_btn.configure(image=pause_white_img, command=continue_pause_func)
        else:
            pause_continue_btn.configure(image=continue_white_img, command=continue_pause_func)

        add_btn.configure(image=add_white_img, command=add)
        music_list.configure(bg=bg, fg=fg)
        name.configure(bg=bg, fg=fg)
        shuffle_btn.configure(bg=bg, fg=fg)
        delete_btn.configure(bg=bg, fg=fg)
        music_time.configure(bg=bg, fg=fg)
        zoom_btn.configure(bg=bg, fg=fg)
        player_frame.configure(bg=bg)
        frame_button_play.configure(bg=bg)
        button_special_frame.configure(bg=bg)

music = []
music_name = []

for i in open('playlist.txt', 'r').read().replace('[','').replace(']','').split(', '):
    if os.path.isfile(i.replace("'", '')):
        music.append(i.replace("'", ''))
    else:
        print(i.replace("'", ''))

open('playlist.txt', 'r+').truncate()
open('playlist.txt', 'w').write(str(music))

pygame.mixer.init()

if music:
    music_now = music[0]
else:
    music_now = ''
if music_now != '':
    music_length = pygame.mixer.Sound(music_now).get_length()*1000

music_pos = 0

for i in music:
    music_name.append(i.split('/')[-1])

#функция паузы и продолжения
#with None can be use also calling from another
#part of programm
def continue_pause_func(event=None):
    global stopped, first, paused_position, paused_time
    if stopped:
        if bg == "white":
            pause_continue_btn['image'] = continue_black_img
        else:
            pause_continue_btn['image'] = continue_white_img
        if music_now != '':
            pygame.mixer.music.pause()
        stopped = False
    else:
        if first:
            if music_now != '':
                pygame.mixer.music.load(music_now)
                pygame.mixer.music.play()
            first = False
        if bg == "white":
            pause_continue_btn['image'] = pause_black_img
        else:
            pause_continue_btn['image'] = pause_white_img

        if music_now != '':
            pygame.mixer.music.unpause()
        stopped = True

def set_music(music_this):
    global return_name, music_now, music_length, music_pos, first, stopped
    music_now = music_this
    music_pos = 0
    pygame.mixer.music.pause()
    music_length = pygame.mixer.Sound(music_now).get_length()*1000
    return_name = music_now.split('/')[-1][0:25]
    first = True
    stopped = False
    continue_pause_func()
    pygame.mixer.music.unpause()

#music_now с ПУТЕМ
def next_func(event=None):
    global music_now, music_length, music_pos, first, stopped, music, index_next, switch, music_from_switch, index
    if music_from_switch != "":
        index = music.index(music_from_switch)
        if index != len(music)-1:
            set_music("D:/music/" + music[index].split('/')[-1])
        else:
            set_music(music[0])
        music_from_switch = ""

    #print(music[len(music)-1], music_now)
    if music_now == music[len(music)-1]:
        set_music("D:/music/" + music[0].split('/')[-1])
    else:
        for i in range(0, len(music)):
            if music[i] == music_now:
                if i + 1 != len(music):
                    music_pos = 0
                    pygame.mixer.music.pause()
                    music_now = music[i + 1]
                    music_length = pygame.mixer.Sound(music_now).get_length()*1000
                    return_name = music_now.split('/')[-1][0:25]
                    first = True
                    stopped = False
                    update_slider_position()  # Запустить обновление ползунка
                    continue_pause_func()
                    pygame.mixer.music.unpause()
                    break

#plays the last music in the playlist
def last_func(event=None):
    global return_name, music_now, music_length, music_pos, first, stopped
    if music_now == music[0]:
        set_music("D:/music/" + music[len(music)-1].split('/')[-1])
    else:
        for i in range(0, len(music)):
            if music[i] == music_now:
                if i != 0:
                    music_pos = 0
                    pygame.mixer.music.pause()
                    music_now = music[i - 1]
                    music_length = pygame.mixer.Sound(music_now).get_length()*1000
                    return_name = music_now.split('/')[-1][0:25]
                    first = True
                    stopped = False
                    continue_pause_func()
                    pygame.mixer.music.unpause()
                    break

def shuffle(event=None):
    global music
    music_list.delete(0, END)
    random.shuffle(music)
    for song in music:
        music_list.insert(END, song.split('/')[-1])
        set_music(music[0])

#add music
def add(event=None):
    global music
    possible_files = [('MUSIC', '*.mp3;*.wav;*oog;')]
    file = filedialog.askopenfilename(filetypes=possible_files)
    if file != '':
        if file not in music:
            music.append(file)
            open('playlist.txt', 'r+').truncate()
            open('playlist.txt', 'w').write(str(music))
            music_list.insert(END, music[-1].split('/')[-1])
            set_music(music[-1])

def zoom(event=None):
    global custom_font, check_style, width_btn, heigth_btn
    if check_style:
        custom_font = (font, 20)
        root.geometry("1100x500")
        heigth_btn = 5
        width_btn = 10
        new_size_next = next_btn.winfo_height() * 2, next_btn.winfo_width() * 2
        last_btn.configure(font=custom_font, height=new_size_next[0], width=new_size_next[1])
        zoom_btn.configure(font=custom_font)
        music_time.configure(font=custom_font)
        next_btn.configure(font=custom_font, height=new_size_next[0], width=new_size_next[1])
        pause_continue_btn.configure(font=custom_font, height=new_size_next[0], width=new_size_next[1])
        add_btn.configure(font=custom_font, height=new_size_next[0], width=new_size_next[1])
        music_list.configure(font=custom_font)
        name.configure(font=custom_font)
        change_theme_btn.configure(font=custom_font, height=new_size_next[0], width=new_size_next[1])
        shuffle_btn.configure(font=custom_font)
        delete_btn.configure(font=custom_font)
        check_style = False
    else:
        new_size_next = next_btn.winfo_height() / 3, next_btn.winfo_width() / 3
        root.geometry("700x500")
        custom_font = (font, 10)
        last_btn.configure(font=custom_font, height=new_size_next[0], width=new_size_next[1])
        zoom_btn.configure(font=custom_font)
        music_time.configure(font=custom_font)
        next_btn.configure(font=custom_font, height=new_size_next[0], width=new_size_next[1])
        pause_continue_btn.configure(font=custom_font, height=new_size_next[0], width=new_size_next[1])
        add_btn.configure(font=custom_font, height=new_size_next[0], width=new_size_next[1])
        music_list.configure(font=custom_font)
        name.configure(font=custom_font)
        change_theme_btn.configure(font=custom_font, height=new_size_next[0], width=new_size_next[1])
        shuffle_btn.configure(font=custom_font)
        delete_btn.configure(font=custom_font)
        check_style = True

def set_music_position(val):
    global music_length, music_pos, minutes_set, seconds_set, minutes, seconds, \
        set_the_time, music, minus_time, minus_time_min
    set_the_time = True

    minus_time = int((pygame.mixer.music.get_pos() / 1000) % 60)
    minus_time_min = int((pygame.mixer.music.get_pos()/1000) // 60)
    minutes = 0
    seconds = 0
    music_pos = int(val) / 100 * music_length
    pygame.mixer.music.set_pos(music_pos / 1000)
    minutes_set = int((music_pos / 1000) // 60)
    seconds_set = int((music_pos / 1000) % 60)
    '''min = minutes + minutes_set
    sec = seconds_set + seconds
    if sec > 59:
        min = min + (sec // 60)
        sec = sec % 60'''
    formated_text = f"{minutes_set}:{seconds_set}"
    music_time.configure(text=formated_text)

#получаем песню без пути!
def delete_song(event=None):
    global music, music_name, music_now
    selected_indices_without_path = get_selected_song()
    if selected_indices_without_path is None:
        return
    selected_indices_with_path = "D:/music/" + selected_indices_without_path
    #switch next if we delete music now
    if music_now == selected_indices_with_path:
        next_func()
    music.remove(selected_indices_with_path)
    music_name.remove(selected_indices_without_path)
    music_list.delete(0, END)
    for song in music:
        music_list.insert(END, song.split('/')[-1])

def get_selected_song():
    selected_indices = music_list.curselection()
    if selected_indices:
        selected_index = selected_indices[0]  # Берем первый выбранный индекс (если есть)
        selected_song = music_name[selected_index]  # Получаем выбранную песню из списка
        return selected_song
    else:
        return None
index = 0
def on_double_click(event):
    global music, index
    selected_song = get_selected_song()
    #Костыль
    selected_song = "D:/music/" + selected_song
    if selected_song in music:
        index = music.index(selected_song)
        #print(index)
    if selected_song is not None:
        #print(selected_song)
        set_music(music[index])

def get_current_time(): # Функция для вычисления времени
    current_time = pygame.mixer.music.get_pos() / 1000  # Конвертирование в секунды
    return f"{int(current_time // 60):02}:{int(current_time % 60):02}"

def check_possitive_seconds():
    global minutes, seconds
    if seconds < 0:
        minutes = minutes - 1
        seconds = seconds + 60

def update_slider_position():
    global music_length, music_now, stopped, index, music, switch, music_from_switch, the_last, seconds, \
        minutes, minutes_set, seconds_set, set_the_time, minus_time, minus_time_min

    selected_song=""
    if music_now == music[len(music)-1]:
        the_last=True
    else:
        the_last=False
    try:
        selected_song = get_selected_song()
        selected_song = "D:/music/" + selected_song
    except:
        pass
    if selected_song in music:
        index = music.index(selected_song)
    #песня закончила играть
    if pygame.mixer.music.get_pos() == -1:
        minutes,seconds,minutes_set,seconds_set=0,0,0,0
        if the_last:
            set_music(music[0])
        else:
            music_from_switch = music_now
            next_func()
    if music_now != '':
        name.configure(text=music_now.split('/')[-1])
    if not stopped and music_now != '':
        current_position = pygame.mixer.music.get_pos() / 1000.0  # Текущая позиция воспроизведения в секундах
        slider_position = (current_position / music_length) * 100.0  # Преобразование в проценты
        music_position_slider.set(slider_position)


    current_music_time = pygame.mixer.music.get_pos()/1000
    #print((pygame.mixer.music.get_pos()/1000) % 60)
    minutes = int(current_music_time // 60) 
    seconds = int(current_music_time % 60)

    if set_the_time:
        set_the_time = False
        minutes = minutes_set
        seconds = seconds_set
        check_possitive_seconds()
        formated_text = f"{minutes}:{seconds-minus_time}"
        #print(seconds)
        music_time.configure(text=formated_text)
    else:
        if seconds + (seconds_set % 60) > 59:
            minutes = minutes + minutes_set + seconds // 60
            seconds = (seconds + (seconds_set % 60)) % 60
            check_possitive_seconds()
            formated_text = f"{minutes}:{seconds-minus_time}"
            music_time.configure(text=formated_text)
            #print(seconds)
        else:
            check_possitive_seconds()
            formated_text = f"{minutes + minutes_set}:{seconds+seconds_set-minus_time}"
            music_time.configure(text=formated_text)
            #print(seconds+seconds_set)
    #music_time.configure(text=get_current_time())
    root.after(1000, update_slider_position)

main_frame = Frame(root)
main_frame.pack(fill=BOTH,expand=True,padx=10, pady=10)
main_frame.configure(bg=bg)

player_frame = Frame(main_frame)
player_frame.pack(fill=BOTH, expand=True,side=LEFT)
player_frame.configure(bg=bg)

music_frame = Frame(main_frame)
music_frame.pack(fill=BOTH, expand = True, side=LEFT)

music_list = Listbox(music_frame, listvariable=StringVar(value=music_name))
music_list.configure(bg=bg,fg=fg, width= 200)
music_list.pack(fill=BOTH, expand=True)

name = Label(player_frame)
name.configure(bg=bg,fg=fg)
name.pack(side=TOP,fill=BOTH,expand=True)

music_time = Label(player_frame)
music_time.configure(text="00:00",bg=bg, fg=fg)
music_time.pack(side=TOP, fill=BOTH, expand=True)

button_special_frame = Frame(player_frame)
button_special_frame.pack(side=TOP, padx=10, pady=10)
button_special_frame.configure(bg=bg)

add_btn = Button(button_special_frame)
add_btn.configure(image = add_white_img, command=add)
add_btn.pack(side=LEFT)

change_theme_btn = Button(button_special_frame)
change_theme_btn.configure(image = change_theme_white_img, text="Change theme", command=change_theme)
change_theme_btn.pack(side=LEFT)

zoom_btn = Button(button_special_frame)
zoom_btn.configure(bg=bg,fg=fg,text="Zoom", command=zoom)
zoom_btn.pack(side=LEFT)

delete_btn = Button(button_special_frame)
delete_btn.configure(bg=bg,fg=fg, text="Delete", command=delete_song)
delete_btn.pack(side=LEFT)

shuffle_btn = Button(button_special_frame)
shuffle_btn.configure(bg=bg,fg=fg, text="Shuffle tracks", command=shuffle)
shuffle_btn.pack(side=LEFT)

frame_line = Frame(player_frame)
frame_line.pack(side=TOP)
music_position_slider = Scale(frame_line, from_=0, to=100, length=300, orient="horizontal", command=set_music_position)
music_position_slider.grid(column =2, row = 2, sticky="ew")
music_position_slider.set(0)

frame_button_play = Frame(player_frame)
frame_button_play.pack(side=TOP)
frame_button_play.configure(bg=bg)

last_btn = Button(frame_button_play)
last_btn.configure(image=previous_white_img, command=last_func)
last_btn.pack(side=LEFT)

pause_continue_btn = Button(frame_button_play)
pause_continue_btn.configure(image=continue_white_img, command=continue_pause_func)
pause_continue_btn.pack(side=LEFT)

next_btn = Button(frame_button_play)
next_btn.configure(image = next_white_img, command=next_func)
next_btn.pack(side=LEFT)

#bind all the button
music_list.bind("<Double-Button-1>", on_double_click)
root.bind("<Right>", next_func)
root.bind("<Left>", last_func)
root.bind("<space>", continue_pause_func)
root.bind("<Up>", shuffle)
root.bind("<Down>", change_theme)
keyboard.add_hotkey('z', zoom)
keyboard.add_hotkey('d', delete_song)
keyboard.add_hotkey('a', add)

set_music(music[0])
continue_pause_func()
update_slider_position()
root.mainloop()
