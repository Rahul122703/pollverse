import json
import requests
class Subcomment:
    def _init_(self, body, upvote, downvote, user_id, comment_id, date, anonymous, color, intensity):
        self.body = body
        self.upvote = upvote
        self.downvote = downvote
        self.user_id = user_id
        self.comment_id = comment_id
        self.date = date
        self.anonymous = anonymous
        self.color = color
        self.intensity = intensity

# JSON data
json_data = '''
{
    "replies": [
        {
            "body": "Phones are a major distraction in classrooms and hinder the learning process. #Distraction #Learning",
            "upvote": "10",
            "downvote": "20",
            "user_id": "5",
            "comment_id": 11,
            "date": "15:27 08/04/2024",
            "anonymous": 1,
            "color": "#f21800",
            "intensity": 0
        },
        {
            "body": "Allowing phones in classrooms promotes cheating and dishonesty among students. #Cheating #Honesty",
            "upvote": "8",
            "downvote": "15",
            "user_id": "6",
            "comment_id": 11,
            "date": "15:27 08/04/2024",
            "anonymous": 0,
            "color": "#f21800",
            "intensity": 0
        },
        {
            "body": "Phones can disrupt the classroom environment and decrease student focus. #Disruption #Focus",
            "upvote": "7",
            "downvote": "18",
            "user_id": "7",
            "comment_id": 11,
            "date": "15:27 08/04/2024",
            "anonymous": 1,
            "color": "#f21800",
            "intensity": 0
        },
        {
            "body": "Phones in class can lead to social comparison and feelings of inadequacy among students. #SocialComparison #Inadequacy",
            "upvote": "5",
            "downvote": "12",
            "user_id": "8",
            "comment_id": 11,
            "date": "15:27 08/04/2024",
            "anonymous": 0,
            "color": "#f21800",
            "intensity": 0
        },
        {
            "body": "Phones may disrupt teacher-student interaction and hinder effective communication. #Interaction #Communication",
            "upvote": "6",
            "downvote": "10",
            "user_id": "9",
            "comment_id": 11,
            "date": "15:27 08/04/2024",
            "anonymous": 1,
            "color": "#f21800",
            "intensity": 0
        },
        {
            "body": "Phones can serve as valuable learning tools, providing access to educational apps and resources. #LearningTools #Resources",
            "upvote": "25",
            "downvote": "5",
            "user_id": "10",
            "comment_id": 11,
            "date": "15:27 08/04/2024",
            "anonymous": 0,
            "color": "#00f200",
            "intensity": 0
        },
        {
            "body": "Phones enable quick access to information, facilitating research and enhancing learning efficiency. #AccessToInformation #Efficiency",
            "upvote": "20",
            "downvote": "3",
            "user_id": "11",
            "comment_id": 11,
            "date": "15:27 08/04/2024",
            "anonymous": 1,
            "color": "#00f200",
            "intensity": 0
        },
        {
            "body": "Integrating phones into lessons can make learning more engaging and interactive for students. #Engagement #Interactivity",
            "upvote": "18",
            "downvote": "7",
            "user_id": "12",
            "comment_id": 11,
            "date": "15:27 08/04/2024",
            "anonymous": 0,
            "color": "#00f200",
            "intensity": 0
        },
        {
            "body": "Phones allow for personalized learning experiences tailored to individual student needs. #Personalization #StudentNeeds",
            "upvote": "15",
            "downvote": "6",
            "user_id": "13",
            "comment_id": 11,
            "date": "15:27 08/04/2024",
            "anonymous": 1,
            "color": "#00f200",
            "intensity": 0
        },
        {
            "body": "While phones can be useful, strict guidelines are necessary to prevent misuse and distractions. #Guidelines #Prevention",
            "upvote": "12",
            "downvote": "8",
            "user_id": "14",
            "comment_id": 11,
            "date": "15:27 08/04/2024",
            "anonymous": 0,
            "color": "#596061",
            "intensity": 0
        }
    ]
}
'''
website_link = 'https://pollverse-w0d9.onrender.com'

data = json.loads(json_data)

for reply in data['replies']:
    
    add_reply_api_end_point = f"{website_link}/add_reply?body={reply['body']}&comment_id={int(reply['comment_id'])}&date={reply['date']}&anonymous={int(reply['anonymous'])}&color={reply['color']}&intensity={int(reply['intensity'])}"
    response = requests.post(add_reply_api_end_point)

    if response.status_code == 200:
        print("Data posted successfully.")
    else:
        print("Error:", response.status_code)
    # new_reply = Subcomment(
    #     body=reply['body'],
    #     upvote=int(reply['upvote']),
    #     downvote=int(reply['downvote']),
    #     user_id=int(reply['user_id']),
    #     comment_id=int(reply['comment_id']),
    #     date=reply['date'],
    #     anonymous=int(reply['anonymous']),
    #     color=reply['color'],
    #     intensity=int(reply['intensity'])
    # )
    # print(vars(new_reply))  