import requests
import datetime

def format_time_and_date(date_time):
    return date_time.strftime("%H:%M %d/%m/%Y")

def map_polarity_to_color(polarity):
    normalized_polarity = (polarity + 1) / 2  
    red = int(255 * (1 - normalized_polarity))
    green = int(255 * normalized_polarity)
    return f'rgb({red}, {green}, 0)'

# Example text
text = "Your comment lacks substance and fails to contribute anything meaningful to the conversation. It's disappointing to see such shallow and uninformed remarks being made. I would advise you to reconsider the quality of your contributions before posting further."

# API URL
api_url = 'https://api.api-ninjas.com/v1/sentiment?text={}'.format(text)

# Make API request
response = requests.get(api_url, headers={'X-Api-Key': '9No6wnmZqzRC/NRH0VvxHA==QRYgA94Njvme77Wg'})

# Check if the request was successful
if response.status_code == requests.codes.ok:
    data = response.json()
    print(data)
    polarity = data['score']

    # Format current date and time
    date_time = datetime.datetime.now()
    formatted_date_time = format_time_and_date(date_time)

    # Map polarity to color
    color = map_polarity_to_color(polarity)

    print("Sentiment polarity:", polarity)
    print("Formatted date and time:", formatted_date_time)
    print("Mapped color:", color)
else:
    print("Error:", response.status_code, response.text)
