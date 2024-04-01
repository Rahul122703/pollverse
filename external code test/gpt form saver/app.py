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
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sentiment Analysis</title>
            <style>
                .result {
                    padding: 20px;
                    margin: 20px auto;
                    width: 50%;
                    text-align: center;
                    font-size: 18px;
                }
            </style>
        </head>
        <body>
            <form action="/" method="post">
                <textarea name="comment" rows="4" cols="50" placeholder="Enter your comment..."></textarea><br>
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
    '''



def map_polarity_to_color(polarity):
    normalized_polarity = (polarity + 1) / 2  
    red = int(255 * (1 - normalized_polarity))
    green = int(255 * normalized_polarity)
    return f'rgb({red}, {green}, 0)'

@app.route('/result', methods=['POST'])
def result():
    comment = request.form['comment']
    polarity = analyze_sentiment(comment)
    color = map_polarity_to_color(polarity)
    return render_template('result.html', polarity=polarity, color=color, comment=comment)

if __name__ == '__main__':
    app.run(debug=True)
