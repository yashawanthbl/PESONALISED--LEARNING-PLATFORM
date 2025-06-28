from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai
import requests

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get API keys from environment
api_key = os.getenv("GEMINI_API_KEY")
youtube_api_key = os.getenv("YOUTUBE_API_KEY")

# Configure Google Generative AI
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def fetch_youtube_video(title):
    search_url = (
        f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1"
        f"&q={title}&key={youtube_api_key}"
    )
    response = requests.get(search_url)
    data = response.json()
    print("YouTube API Response:", data)

    try:
        if 'items' in data and len(data['items']) > 0:
            item = data['items'][0]
            video_id = item['id'].get('videoId', None)
            if video_id:
                video_url = f"https://www.youtube.com/embed/{video_id}"
                return video_url, item['snippet']['title'], '5 minutes'
    except KeyError as e:
        print(f"KeyError: {e}")
    
    return None, None, None

# Homepage route
@app.route('/')
def home():
    return render_template('index.html')

# Generate course route
@app.route('/generate_course', methods=['POST'])
def generate_course():
    category = request.form['category']
    topic = request.form['topic']
    level = request.form['level']
    duration = request.form['duration']
    no_of_chapters = int(request.form['no_of_chapters'])

    chat_session = model.start_chat(history=[
        {
            "role": "user",
            "parts": [f"Generate a course plan in JSON format for Category: {category}, Topic: {topic}, Level: {level}, "
                      f"Duration: {duration}, NoOfChapters: {no_of_chapters}."]
        }
    ])
    response = chat_session.send_message("Generate the course layout.")
    course_data = response.text

    chapters = []
    for i in range(no_of_chapters):
        video_url, video_title, video_duration = fetch_youtube_video(f"{topic} Chapter {i + 1}")
        chapters.append({
            "title": f"{topic} Chapter {i + 1}",
            "duration": "30 minutes",
            "description": f"Chapter {i + 1} description for {topic}",
            "video_url": video_url,
            "video_title": video_title,
            "video_duration": video_duration,
            "code_example": "Sample code example",
            "quiz": "Sample quiz",
            "text_content": "Sample text content",
        })

    return jsonify({"chapters": chapters})

if __name__ == '__main__':
    app.run(debug=True, port=2000)
