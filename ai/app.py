from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import os

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure API keys from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

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

# Fetch YouTube video
def fetch_youtube_video(title):
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=1&q={title}&key={YOUTUBE_API_KEY}"
    response = requests.get(search_url)
    data = response.json()
    print("API Response:", data)

    try:
        if 'items' in data and len(data['items']) > 0:
            item = data['items'][0]
            video_id = item['id'].get('videoId')
            if video_id:
                video_url = f"https://www.youtube.com/embed/{video_id}"
                return video_url, item['snippet']['title'], '5 minutes'  # Hardcoded duration
    except Exception as e:
        print(f"Error fetching video: {e}")

    return None, None, None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_course', methods=['POST'])
def generate_course():
    try:
        category = request.form['category']
        topic = request.form['topic']
        level = request.form['level']
        duration = request.form['duration']
        no_of_chapters = int(request.form['no_of_chapters'])

        # Gemini Chat Session
        chat_session = model.start_chat(
            history=[{
                "role": "user",
                "parts": [
                    f"Generate a course plan in JSON format for Category: {category}, Topic: {topic}, Level: {level}, "
                    f"Duration: {duration}, NoOfChapters: {no_of_chapters}."
                ],
            }]
        )

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
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to generate course"}), 500

if __name__ == '__main__':
    app.run(debug=True)
