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
text = "Aapke drishtikon par upasthiti neetiyon ke prati vichaarshil hai. Main chhatra sangathan aur bhagidari sunischit karne ke mahatva ko samajhta hoon, lekin aapka tippani deta hai ki shiksha settings mein sahanubhooti aur lachilapan ki avashyakta hai. Yeh mahatvapurn hai ki chhatron ke samne vibhinn chunautiyon ko manyata di jaye jo unki upasthiti par prabhav daal sakti hain, aur kathin neetiyon se tanav ko badha sakti hain aur shiksha ko badhit kar sakti hain. Samjhane aur samarthan pradan karke, sansthan ek aur sankranti shiksha vaatavaran bana sakte hain jahan chhatra mulyankan aur safalta ke liye mahsus karte hain. Dhanyavad ki aapne is mahatvapurn charcha ko prerit kiya hai ki hum chhatron ki samagr kalyan ki samarthan mein kaise behtar saksham ho sakte hain jabki shiksha manakon ko banaye rakhte hain."

# API URL
api_url = 'https://api.api-ninjas.com/v1/sentiment?text={}'.format(text)

# Make API request
response = requests.get(api_url, headers={'X-Api-Key': '9No6wnmZqzRC/NRH0VvxHA==QRYgA94Njvme77Wg'})

# Check if the request was successful
if response.status_code == requests.codes.ok:
    data = response.json()
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
