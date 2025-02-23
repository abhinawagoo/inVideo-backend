from moviepy.editor import TextClip, ColorClip, CompositeVideoClip
import os

def test_video_generator():
    print("Testing basic video generation...")
    
    try:
        # Create output directory
        os.makedirs("output", exist_ok=True)
        
        # Create a simple clip
        txt_clip = TextClip("Test Video", fontsize=70, color='white')
        txt_clip = txt_clip.set_duration(5)
        
        # Create background
        bg_clip = ColorClip((1920, 1080), color=(25, 25, 25))
        bg_clip = bg_clip.set_duration(5)
        
        # Combine clips
        video = CompositeVideoClip([bg_clip, txt_clip.set_position('center')])
        
        # Write the video file
        output_path = "output/test_video.mp4"
        video.write_videofile(output_path, fps=24)
        
        print(f"Video created successfully at: {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_video_generator()