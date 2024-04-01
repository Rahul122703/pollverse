from flask import Flask, request, render_template
from textblob import TextBlob

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comment = request.form['comment']
        polarity = analyze_sentiment(comment)
        color = map_polarity_to_color(polarity)
        return render_template('result.html', polarity=polarity, color=color, comment=comment)
    return render_template('index.html')

def analyze_sentiment(comment):
    blob = TextBlob(comment)
    polarity = blob.sentiment.polarity
    return polarity

def map_polarity_to_color(polarity):
    # Map polarity to a color gradient from green to red
    # Polarity ranges from -1 (most negative) to 1 (most positive)
    normalized_polarity = (polarity + 1) / 2  # Normalize polarity to the range [0, 1]
    # Convert normalized polarity to a color value in the range [0, 255]
    red = int(255 * (1 - normalized_polarity))
    green = int(255 * normalized_polarity)
    return f'rgb({red}, {green}, 0)'

if __name__ == '__main__':
    app.run(debug=True)
