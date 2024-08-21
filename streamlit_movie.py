import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.all import fadein, fadeout
import streamlit as st

# 设置页面标题
st.title("图片音频合成工具")

# 输入图片文件夹路径
image_folder = st.text_input("图片文件夹路径", "images")
# 输入音频文件夹路径
audio_folder = st.text_input("音频文件夹路径", "audios")
# 输入输出视频文件夹路径
output_folder = st.text_input("输出视频文件夹路径", "output_videos")

# 选择转场效果
transition_options = {
    "淡入淡出": (fadein, fadeout),
    "交叉淡入": (fadeout)
}
transition_name = st.selectbox("选择转场效果", list(transition_options.keys()))

# 字幕格式设置
font_size = st.number_input("字幕字体大小", value=24)
color = st.color_picker("字幕颜色", "#ffffff")
bg_color = st.color_picker("字幕背景色", "#000000")

def create_video(image_file, audio_file, output_file):
    image = ImageClip(os.path.join(image_folder, image_file))
    audio = AudioFileClip(os.path.join(audio_folder, audio_file))

    # 设置图片时长与音频时长一致
    image = image.set_duration(audio.duration)

    # 应用转场特效
    in_effect, out_effect = transition_options[transition_name]
    image = out_effect(image, duration=2)

    # 读取同名的字幕文件
    subtitle_file = os.path.join(image_folder, os.path.splitext(image_file)[0] + '.txt')
    if os.path.exists(subtitle_file):
        with open(subtitle_file, 'r') as f:
            subtitle_text = f.read()
        # 设置字幕样式
        subtitle = TextClip(subtitle_text, fontsize=font_size, color=color, bg_color=bg_color)
        subtitle = subtitle.set_duration(image.duration).set_position('bottom')
        video = CompositeVideoClip([image, subtitle])
    else:
        video = image

    # 将音频添加到视频中
    video = video.set_audio(audio)

    # 保存视频
    video.write_videofile(output_file, fps=24)

def process_folder():
    for image_file in os.listdir(image_folder):
        if image_file.endswith('.png'):
            audio_file = os.path.splitext(image_file)[0] + '.mp3'
            if os.path.exists(os.path.join(audio_folder, audio_file)):
                output_file = os.path.join(output_folder, os.path.splitext(image_file)[0] + '.mp4')
                create_video(image_file, audio_file, output_file)

if st.button("开始合成"):
    process_folder()
    st.success("视频合成完成！")