# app/services/video_generator.py

from moviepy.editor import TextClip, ImageClip, ColorClip, CompositeVideoClip, concatenate_videoclips
from moviepy.video.fx.resize import resize
import os
import numpy as np
from PIL import Image
from PIL.Image import Resampling

class VideoGenerator:
    def __init__(self):
        self.output_dir = "output"
        self.width = 1920
        self.height = 1080
        self.duration = {
            'intro': 5,
            'screenshot': 6,
            'feature': 4,
            'text': 4
        }
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, content: dict) -> str:
        """Main method to generate the video"""
        try:
            clips = []
            
            # Use default values if content is missing
            title = content.get('title', 'Website Preview').strip()
            description = content.get('description', 'Explore our website').strip()
            
            # Create intro
            intro = self._create_intro(title, description)
            clips.append(intro)
            
            # Add screenshots if available
            if content.get('screenshots', {}).get('full'):
                showcase = self._create_website_showcase(content['screenshots']['full'])
                clips.append(showcase)
            
            # Add outro
            outro = self._create_outro()
            clips.append(outro)
            
            # Combine clips and create video
            final_video = concatenate_videoclips(clips)
            output_path = os.path.join(self.output_dir, f"promo_{abs(hash(title))}.mp4")
            
            # Write video file
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio=False
            )
            
            return output_path
            
        except Exception as e:
            print(f"Error details: {str(e)}")
            raise Exception(f"Error generating video: {str(e)}")

    def _create_intro(self, title: str, description: str) -> CompositeVideoClip:
        """Create intro clip with title and description"""
        # Create background
        bg = ColorClip((self.width, self.height), color=(25, 25, 25))
        bg = bg.set_duration(self.duration['intro'])
        
        # Create title clip
        title_clip = (TextClip(
            txt=title,
            fontsize=70,
            color='white',
            size=(self.width-200, None),
            method='caption'
        ).set_position(('center', self.height//3))
         .set_duration(self.duration['intro']))
        
        # Create description clip
        desc_clip = (TextClip(
            txt=description,
            fontsize=40,
            color='white',
            size=(self.width-400, None),
            method='caption'
        ).set_position(('center', self.height//2 + 100))
         .set_duration(self.duration['intro']))
        
        return CompositeVideoClip([bg, title_clip, desc_clip])

    def _create_website_showcase(self, screenshot_path: str) -> CompositeVideoClip:
        """Create clip showing website screenshot"""
        try:
            # Create background
            bg = ColorClip((self.width, self.height), color=(15, 15, 15))
            bg = bg.set_duration(self.duration['screenshot'])
            
            # Load and process screenshot
            img = Image.open(screenshot_path)
            # Resize image while maintaining aspect ratio
            img = self._resize_image(img, self.width-100)
            img_clip = ImageClip(np.array(img))
            
            # Position and set duration
            img_clip = img_clip.set_position('center')
            img_clip = img_clip.set_duration(self.duration['screenshot'])
            
            return CompositeVideoClip([bg, img_clip])
            
        except Exception as e:
            print(f"Error creating showcase: {str(e)}")
            return None

    def _resize_image(self, img, target_width: int) -> Image:
        """Resize image maintaining aspect ratio"""
        ratio = target_width / float(img.size[0])
        target_height = int(float(img.size[1]) * float(ratio))
        return img.resize((target_width, target_height), Resampling.LANCZOS)

    def _create_outro(self) -> CompositeVideoClip:
        """Create outro clip"""
        bg = ColorClip((self.width, self.height), color=(25, 25, 25))
        bg = bg.set_duration(5)
        
        text_clip = (TextClip(
            txt="Visit our website to learn more",
            fontsize=60,
            color='white',
            method='caption'
        ).set_position('center')
         .set_duration(5))
        
        return CompositeVideoClip([bg, text_clip])