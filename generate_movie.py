import moviepy


# Load the generated audio
audio = moviepy.AudioFileClip("output/output_audio.mp3")  # The generated audio file

# Check if the audio file exists and has content
if audio.duration == 0:
    print("❌ Audio file is empty. Please check the audio generation process.")
    exit(1)

# Create a background image (or use your own)
image_path = "assets/my_fig_1.JPG"  # Path to your background image
try:
    clip = moviepy.ImageClip(image_path) \
        .with_duration(audio.duration) \
        .with_audio(audio) \
        .with_fps(24)

    # Save the video
    video_output_path = "output/final_video.mp4"
    clip.write_videofile(video_output_path, codec="libx264", audio_codec="aac")

    print(f"✅ Video created successfully at {video_output_path}")

except Exception as e:
    print("❌ Error creating video:", e)
