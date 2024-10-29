import telebot
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

# Function to add a watermark to a video
def add_watermark(input_file, output_file, watermark_text, font_size=20, color='white'):
    clip = VideoFileClip(input_file)
    text_clip = TextClip(watermark_text, fontsize=font_size, color=color)
    text_clip = text_clip.set_position(('center', 'bottom')).set_duration(clip.duration)
    video_clip_with_text = CompositeVideoClip([clip, text_clip])
    video_clip_with_text.write_videofile(output_file, audio=True, temp_audiofile='temp-audio.m4a', codec='libx264', bitrate='5000k')

# Handler for incoming video files
@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_id = message.video.file_id
    file_path = bot.download_file(bot.get_file(file_id).file_path)

    # Add your desired watermark text here
    watermark_text = "Your Watermark Text"

    output_file = "watermarked_video.mp4"
    add_watermark(file_path, output_file, watermark_text)

    with open(output_file, 'rb') as f:
        bot.send_video(message.chat.id, f)

# Start the bot
bot.polling()
