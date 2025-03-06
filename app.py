import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from io import BytesIO
from wordcloud import WordCloud
from flask import Flask, json, jsonify, send_file, request
from flask_cors import CORS
import nltk
from nltk.corpus import stopwords

# Download stopwords globally
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Initialize Flask app
app = Flask(__name__)
CORS(app)  

# Load dataset
final_viz_data_path = "final_viz_data.csv"
df = pd.read_csv(final_viz_data_path)

# Convert timestamp to datetime
df['created_utc'] = pd.to_datetime(df['created_utc'], errors='coerce')
df.dropna(subset=['created_utc'], inplace=True)
df.set_index('created_utc', inplace=True)

# Function to return JSON response
def plot_to_json(fig):
    return jsonify(json.loads(fig.to_json()))

# Enable CORS headers in responses
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# Time Series using Plotly
@app.route('/plot/time_series')
def plot_time_series():
    df_resampled = df.resample('D').size().reset_index()
    df_resampled.columns = ['Date', 'Number of Posts']

    fig = px.line(df_resampled, x='Date', y='Number of Posts', 
                  title="📅 Time Series of Posts", markers=True)
    fig.update_traces(line=dict(color='blue', width=2))
    return plot_to_json(fig)

# Top Communities Pie Chart using Plotly
@app.route('/plot/top_communities')
def serve_top_communities():
    top_communities = df['subreddit'].value_counts().nlargest(10)
    fig = px.pie(values=top_communities.values, names=top_communities.index, 
                 title='🌍 Top 10 Contributing Communities', hole=0.3)
    return plot_to_json(fig)

# Preprocess text function: Remove stopwords, lowercase conversion
def preprocess_text(text):
    words = text.lower().split()
    return ' '.join([word for word in words if word not in stop_words])

# Word Cloud for Titles
# Word Cloud for Titles
@app.route('/plot/title_wordcloud')
def serve_title_wordcloud():
    text = ' '.join(df['title'].dropna().astype(str))  # Ensure text data is string
    text = preprocess_text(text)  # Clean text
    
    if not text.strip():  # Check if text is empty
        return jsonify({"error": "No text data available for title word cloud"}), 400
    
    wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='cool').generate(text)

    img = BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)
    return send_file(img, mimetype='image/png', as_attachment=False)

# Word Cloud for Selftext
@app.route('/plot/selftext_wordcloud')
def serve_selftext_wordcloud():
    text = ' '.join(df['selftext'].dropna().astype(str))
    text = preprocess_text(text)

    if not text.strip():  # Check if text is empty
        return jsonify({"error": "No text data available for selftext word cloud"}), 400

    wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='cool').generate(text)

    img = BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)
    return send_file(img, mimetype='image/png', as_attachment=False)

# Word Frequencies Bar Chart
@app.route('/plot/word_frequencies')
def plot_word_frequencies():
    text = ' '.join(df['title'].dropna().astype(str))  # Merge all text from 'title' column
    text = preprocess_text(text)
    
    word_counts = Counter(text.split())
    common_words = word_counts.most_common(20)  # Get top 20 words
    
    words, counts = zip(*common_words)  # Unpack words & counts
    
    fig = px.bar(x=words, y=counts, title="🔢 Top 20 Word Frequencies",
                 labels={'x': 'Words', 'y': 'Frequency'}, text_auto=True)
    fig.update_traces(marker_color='purple')

    return plot_to_json(fig)

# Flask Route for Homepage
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Visualization API!",
        "available_plots": [
            "time_series",
            "top_communities",
            "title_wordcloud",
            "selftext_wordcloud",
            "word_frequencies"
        ]
    })

# Run Flask App
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns a port dynamically
    app.run(host="0.0.0.0", port=port, debug=False)  # Debug should be False in production

