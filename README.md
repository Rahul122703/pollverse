# PollVerse - Sentiment Analyzer Web-App

![PollVerse Banner](https://example.com/banner.png)

Hosted Link: [discussly.onrender.com](https://discussly.onrender.com)

## Description
PollVerse is a sentiment analyzer web-app designed to analyze the sentiment of discussion threads. The app allows users to create and participate in anonymous polls, initiate discussions, and observe sentiment analysis over time.

## Features
- **Anonymous Poll Creation**: Logged-in users can anonymously create polls on various topics of interest.
- **Discussion Threads**: Users can initiate and participate in discussion threads related to the polls.
- **Sentiment Analysis**: The system employs sentiment analysis to analyze the sentiments expressed in the comments.
- **User Authentication**: Enables user registration, login, and account management with a forgot password system that uses OTP.
- **User Profiles**: Each user has a profile page displaying their activity.
- **Responsive Interface**: Offers a smooth user experience on different device sizes.
- **Database Connectivity**: Manages all user data, polls, and discussion threads in an SQL database.
- **REST API**: Provides a REST API with API key authentication for `GET` requests.

---

## Getting Started

### Prerequisites
Ensure that you have Python and pip installed on your machine.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/pollverse.git
   cd pollverse
2. Install Libraries and Run 
  ```bash
   pip install -r requirements.txt
   flask run
