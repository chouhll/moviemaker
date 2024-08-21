import os
from tkinter import Tk, Label, Button, Entry, filedialog, StringVar, OptionMenu, colorchooser
from moviepy.editor import *
from moviepy.video.fx.all import fadein, fadeout
from moviepy.config import change_settings

# 配置 ImageMagick 路径，根据你的安装路径进行调整
change_settings({"IMAGEMAGICK_BINARY": "path/to/convert"})

def create_video_with_audio(image_path, audio_path, output_path, transition_effect="fade", transition_duration=1):
    image_clip = ImageClip(image_path)
    audio_clip = AudioFileClip(audio_path)
    
    # Adjust image duration to match audio duration
    image_clip = image_clip.set_duration(audio_clip.duration)
    image_clip = image_clip.set_audio(audio_clip)

    # Apply transition effect
    if transition_effect == "fade":
        image_clip = fadein(image_clip, duration=transition_duration)
        image_clip = fadeout(image_clip, duration=transition_duration)
    
    # Write the video file
    image_clip.write_videofile(output_path, fps=24, codec='libx264')

def add_text_to_video(video_path, text, output_path, font='Arial', fontsize=24, color='white', bg_color=None):
    video_clip = VideoFileClip(video_path)
    txt_clip = TextClip(text, fontsize=fontsize, font=font, color=color, bg_color=bg_color)
    txt_clip = txt_clip.set_position('bottom').set_duration(video_clip.duration)
    video = CompositeVideoClip([video_clip, txt_clip])
    video.write_videofile(output_path, fps=24, codec='libx264')

def process_folders(image_folder, audio_folder, output_folder, text_folder=None, transition_effect="fade", transition_duration=1, font='Arial', fontsize=24, fontcolor='white', bgcolor=None):
    for image_file in os.listdir(image_folder):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_name = os.path.splitext(image_file)[0]
            image_path = os.path.join(image_folder, image_file)
            audio_path = os.path.join(audio_folder, file_name + '.mp3')
            output_path = os.path.join(output_folder, file_name + '.mp4')
            
            if os.path.exists(audio_path):
                create_video_with_audio(image_path, audio_path, output_path, transition_effect, transition_duration)

                if text_folder:
                    text_path = os.path.join(text_folder, file_name + '.txt')
                    if os.path.exists(text_path):
                        with open(text_path, 'r') as f:
                            text = f.read().strip()
                        add_text_to_video(output_path, text, output_path, font=font, fontsize=fontsize, color=fontcolor, bg_color=bgcolor)

def select_folder(var):
    folder_selected = filedialog.askdirectory()
    var.set(folder_selected)

def select_bg_color(var):
    color = colorchooser.askcolor(title ="Choose background color")[1]
    var.set(color)

def generate_videos():
    image_folder = image_folder_var.get()
    audio_folder = audio_folder_var.get()
    output_folder = output_folder_var.get()
    text_folder = text_folder_var.get()
    transition_effect = transition_effect_var.get()
    transition_duration = int(transition_duration_var.get())
    font = font_var.get()
    fontsize = int(fontsize_var.get())
    fontcolor = fontcolor_var.get()
    bgcolor = bgcolor_var.get()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    process_folders(image_folder, audio_folder, output_folder, text_folder, transition_effect, transition_duration, font, fontsize, fontcolor, bgcolor)

app = Tk()
app.title("Video Creator")

image_folder_var = StringVar()
audio_folder_var = StringVar()
output_folder_var = StringVar()
text_folder_var = StringVar()
transition_effect_var = StringVar(value='fade')
transition_duration_var = StringVar(value='1')
font_var = StringVar(value='Arial')
fontsize_var = StringVar(value='24')
fontcolor_var = StringVar(value='white')
bgcolor_var = StringVar()

Label(app, text="Image Folder").grid(row=0, column=0)
Entry(app, textvariable=image_folder_var, width=40).grid(row=0, column=1)
Button(app, text="Browse", command=lambda: select_folder(image_folder_var)).grid(row=0, column=2)

Label(app, text="Audio Folder").grid(row=1, column=0)
Entry(app, textvariable=audio_folder_var, width=40).grid(row=1, column=1)
Button(app, text="Browse", command=lambda: select_folder(audio_folder_var)).grid(row=1, column=2)

Label(app, text="Output Folder").grid(row=2, column=0)
Entry(app, textvariable=output_folder_var, width=40).grid(row=2, column=1)
Button(app, text="Browse", command=lambda: select_folder(output_folder_var)).grid(row=2, column=2)

Label(app, text="Text Folder").grid(row=3, column=0)
Entry(app, textvariable=text_folder_var, width=40).grid(row=3, column=1)
Button(app, text="Browse", command=lambda: select_folder(text_folder_var)).grid(row=3, column=2)

Label(app, text="Transition Effect").grid(row=4, column=0)
OptionMenu(app, transition_effect_var, "fade").grid(row=4, column=1)

Label(app, text="Transition Duration (seconds)").grid(row=5, column=0)
Entry(app, textvariable=transition_duration_var, width=10).grid(row=5, column=1)

Label(app, text="Font").grid(row=6, column=0)
Entry(app, textvariable=font_var, width=20).grid(row=6, column=1)

Label(app, text="Font Size").grid(row=7, column=0)
Entry(app, textvariable=fontsize_var, width=10).grid(row=7, column=1)

Label(app, text="Font Color").grid(row=8, column=0)
Entry(app, textvariable=fontcolor_var, width=10).grid(row=8, column=1)

Label(app, text="Background Color").grid(row=9, column=0)
Entry(app, textvariable=bgcolor_var, width=10).grid(row=9, column=1)
Button(app, text="Choose Color", command=lambda: select_bg_color(bgcolor_var)).grid(row=9, column=2)

Button(app, text="Generate Videos", command=generate_videos).grid(row=10, column=1)

app.mainloop()