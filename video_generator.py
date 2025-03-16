import os
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import (
    VideoFileClip, ImageClip, AudioFileClip, TextClip, CompositeVideoClip, CompositeAudioClip
)

#PIL (Pillow) → To process images.
#gTTS → To convert text to speech.
#moviepy → To edit and create videos.
def add_text_to_image(image_path, text, output_image_path):
    
    image = Image.open(image_path)
    

    draw = ImageDraw.Draw(image)
    

    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        font = ImageFont.load_default()
    

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]  
    text_height = bbox[3] - bbox[1]  

    
    position = ((image.width - text_width) // 2, (image.height - text_height) // 2)
    
    
    draw.text(position, text, fill="white", font=font)
    

    image.save(output_image_path)


def apply_grayscale(image_path, output_image_gray_path):
    image = Image.open(image_path)
    
    grayscale_image = image.convert("L")
    grayscale_image.save(output_image_gray_path)


def generate_voiceover(text, output_audio_path):
    tts = gTTS(text)
    tts.save(output_audio_path)


def create_video_from_image(image_path, voiceover_path, background_music_path, output_video_path, duration=5):

    clip = ImageClip(image_path, duration=duration)
    
    
    audio = AudioFileClip(voiceover_path)
    
    
    background_music = AudioFileClip(background_music_path)
    
    
    combined_audio = audio.volumex(1)  
    background_music = background_music.volumex(0.3)  
    
    
    final_audio = CompositeAudioClip([combined_audio, background_music.set_duration(clip.duration)])
    

    clip = clip.set_audio(final_audio)
    
    clip.write_videofile(output_video_path, codec="libx264", fps=24)


def add_captions_to_video(video_path, captions, output_video_with_captions_path):
    clip = VideoFileClip(video_path)
    txt_clip = TextClip(captions, fontsize=24, color='white', bg_color='black', font='Arial', size=clip.size)
    txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(clip.duration)
    
    final_clip = CompositeVideoClip([clip, txt_clip])
    final_clip.write_videofile(output_video_with_captions_path, codec="libx264", fps=24)

def main():
    
    image_path = r"C:\Users\rawia\Downloads\360_F_573073449_eDX3JwNWr3dQmP5fidnxqLP8AGuqzQYO.jpg"  
    text = "I am a Python Speaking Cool Bunny , Do you have any carrots?"  
    output_image_path = r"C:\Users\rawia\Downloads\output_image_with_text.jpg"  
    output_image_gray_path = r"C:\Users\rawia\Downloads\output_image_gray.jpg"  
    output_audio_path = r"C:\Users\rawia\Downloads\ttsMP3_com_VoiceText.mp3"  
    output_video_path = r"C:\Users\rawia\Downloads\output_video12.mp4" 
    output_video_with_captions_path = r"C:\Users\rawia\Downloads\output_video_with_captions.mp4"  
    background_music_path = r"C:\Users\rawia\Downloads\zen-garden-310599.mp3"
    
    add_text_to_image(image_path, text, output_image_path)
    
    apply_grayscale(output_image_path, output_image_gray_path)
    
    generate_voiceover(text, output_audio_path)
    
    create_video_from_image(output_image_gray_path, output_audio_path, background_music_path, output_video_path)
    
    captions = "This is a test caption!"
    add_captions_to_video(output_video_path, captions, output_video_with_captions_path)

    print("✅ Video created successfully!")

if __name__ == "__main__":
    main()
