from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from textblob import TextBlob
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # Allows HTML + JS to access backend

API_KEY = "YOUR_YOUTUBE_API_KEY"   # 🔥 Put your API key here


def get_comments(video_id):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    comments = []

    response = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=50
    ).execute()

    for item in response.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)

    return comments


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    url = data["url"]

    # Extract video ID from URL
    if "v=" in url:
        video_id = url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1].split("?")[0]
    else:
        return jsonify({"sentiment": "Invalid URL"})

    comments = get_comments(video_id)

    if not comments:
        return jsonify({"sentiment": "Neutral"})

    polarity = 0
    for comment in comments:
        polarity += TextBlob(comment).sentiment.polarity

    avg_score = polarity / len(comments)

    if avg_score > 0.1:
        sentiment = "Positive"
    elif avg_score < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return jsonify({"sentiment": sentiment})


if __name__ == "__main__":
    app.run(debug=True)
