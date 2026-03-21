import os
import asyncio
import edge_tts
from moviepy.editor import ImageClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Use dynamic temporary directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "videos")
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate_audio(text: str, output_path: str):
    """Generate TTS audio using edge-tts (free)."""
    voice = "en-IN-PrabhatNeural" # Indian English male voice
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def generate_background_image(title: str, output_path: str):
    """Create a dark, simple background with the article headline using Pillow."""
    width, height = 1080, 1920  # Shorts / Reels format
    img = Image.new('RGB', (width, height), color=(15, 23, 42)) # Slate 900
    
    draw = ImageDraw.Draw(img)
    # Simple text wrapping
    words = title.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        if len(" ".join(current_line)) > 20: 
            lines.append(" ".join(current_line))
            current_line = []
    if current_line:
        lines.append(" ".join(current_line))
        
    y_text = height // 2 - (len(lines) * 60) // 2
    
    # Try using default font if no specific font available
    # Actually just drawing text with default is tiny, loop to scale it up manually
    try:
        font = ImageFont.truetype("Arial", 60)
    except IOError:
        font = ImageFont.load_default()
        
    for line in lines:
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        w = right - left
        draw.text(((width - w) / 2, y_text), line, font=font, fill=(212, 175, 55)) # Gold color
        y_text += 80
        
    # Draw NewsET logo
    draw.text((80, 80), "NewsET", fill=(255, 255, 255), font=font)
    
    img.save(output_path)

def generate_video_script(title: str, content: str) -> str:
    """Generate a 40-50 second script using Gemini."""
    if not GEMINI_API_KEY:
         return f"Here is a quick update on {title}. {content[:200]}"
         
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        Act as a professional financial news anchor. 
        Write a short, punchy 40-second script summarizing this news for a short-form video (TikTok/Reels format).
        DO NOT include any stage directions, sound effects, or visual cues. ONLY return the spoken text.
        Make it engaging, starting with a hook.

        Title: {title}
        Content: {content[:1500]}
        """
        response = model.generate_content(prompt)
        return response.text.replace("*", "").strip()
    except Exception as e:
        print(f"Error generating script: {e}")
        return f"Brief update on {title}: {content[:200]}"

async def create_video_summary(article_id: str, title: str, content: str) -> str:
    """
    Orchestrates the video generation pipeline.
    Returns the relative path to the generated video.
    """
    video_filename = f"{article_id}_summary.mp4"
    final_output_path = os.path.join(OUTPUT_DIR, video_filename)
    
    if os.path.exists(final_output_path):
        return f"/static/videos/{video_filename}"
        
    # 1. Generate Script
    print("Generating script...")
    script = generate_video_script(title, content)
    
    # Paths for temp files
    audio_path = os.path.join(OUTPUT_DIR, f"{article_id}_tts.mp3")
    image_path = os.path.join(OUTPUT_DIR, f"{article_id}_bg.jpg")
    
    try:
        # 2. Generate Audio
        print("Generating TTS audio...")
        await generate_audio(script, audio_path)
        
        # 3. Generate Image
        print("Generating background image...")
        generate_background_image(title, image_path)
        
        # 4. Combine into Video
        print("Assembling video...")
        audio = AudioFileClip(audio_path)
        image = ImageClip(image_path).set_duration(audio.duration)
        video = image.set_audio(audio)
        
        # Write file with low fps to be fast
        video.write_videofile(
            final_output_path, 
            fps=1, 
            codec="libx264", 
            audio_codec="aac",
            logger=None # Suppress verbose output
        )
        
        # Cleanup
        audio.close()
        video.close()
        os.remove(audio_path)
        os.remove(image_path)
        
        return f"/static/videos/{video_filename}"
    except Exception as e:
        print(f"Video generation skipped/failed: {e}")
        raise e
