import os
from moviepy.editor import *
from moviepy.video.fx.all import fadein, fadeout

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

def add_text_to_video(video_path, text, output_path, font='Arial', fontsize=24, color='white', bg_color='black'):
    video_clip = VideoFileClip(video_path)
    txt_clip = TextClip(text, fontsize=fontsize, font=font, color=color, bg_color=bg_color)
    txt_clip = txt_clip.set_position('bottom').set_duration(video_clip.duration)
    video = CompositeVideoClip([video_clip, txt_clip])
    video.write_videofile(output_path, fps=24, codec='libx264')

def process_folders(image_folder, audio_folder, output_folder, text_folder):
    for image_file in os.listdir(image_folder):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_name = os.path.splitext(image_file)[0]
            image_path = os.path.join(image_folder, image_file)
            audio_path = os.path.join(audio_folder, file_name + '.mp3')
            output_path = os.path.join(output_folder, file_name + '.mp4')
            
            if os.path.exists(audio_path):
                create_video_with_audio(image_path, audio_path, output_path)

                if text_folder:
                    text_path = os.path.join(text_folder, file_name + '.txt')
                    if os.path.exists(text_path):
                        with open(text_path, 'r') as f:
                            text = f.read().strip()
                        add_text_to_video(output_path, text, output_path)

if __name__ == "__main__":
    image_folder = '/Users/i323583/Desktop/abc'
    audio_folder = '/Users/i323583/Desktop/abc'
    output_folder = '/Users/i323583/Desktop/abc'
    text_folder = '/Users/i323583/Desktop/abc'  # Set to None if no text

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    process_folders(image_folder, audio_folder, output_folder, text_folder)