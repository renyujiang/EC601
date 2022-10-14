import sys
import time

import requests
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import tweepy
import wordcloud
import botometer
import os

from google.cloud import language_v1

import api_auth_info

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./ec602-project-2-382ab4aae677.json"

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setUI()

    def setUI(self):
        self.resize(1060, 960)
        self.center()
        self.setWindowTitle('EC601 Project 2 - Renyu Jiang')

        # set font
        font1 = QtGui.QFont()
        font1.setPointSize(16)
        font2 = QtGui.QFont()
        font2.setPointSize(15)
        font3 = QtGui.QFont()
        font3.setPointSize(10)
        font4 = QtGui.QFont()
        font4.setPointSize(12)

        # Qlabel to put profile
        self.profile = QLabel('Profile', self)
        self.profile.setScaledContents(True)
        self.profile.setGeometry(25, 25, 200, 200)
        self.profile.setStyleSheet("background-color:white; border:1px solid black;")
        self.profile.setAlignment(Qt.AlignCenter)
        self.profile.setFont(font1)

        # some Qlabels to put account info
        self.name = QLabel('Name', self)
        self.name.setGeometry(250, 25, 250, 80)
        self.name.setStyleSheet("background-color:white; border:1px solid black;")
        self.name.setAlignment(Qt.AlignCenter)
        self.name.setFont(font1)

        self.introduction = QLabel('Description', self)
        self.introduction.setGeometry(250, 120, 500, 105)
        self.introduction.setStyleSheet("background-color:white; border:1px solid black;")
        self.introduction.setAlignment(Qt.AlignCenter)
        self.introduction.setWordWrap(True)

        self.follower = QLabel('Follower', self)
        self.follower.setGeometry(525, 25, 225, 35)
        self.follower.setStyleSheet("background-color:white; border:1px solid black;")
        self.follower.setAlignment(Qt.AlignCenter)
        self.follower.setFont(font3)

        self.following = QLabel('Following', self)
        self.following.setGeometry(525, 70, 225, 35)
        self.following.setStyleSheet("background-color:white; border:1px solid black;")
        self.following.setAlignment(Qt.AlignCenter)
        self.following.setFont(font3)

        # input username
        self.username = QLineEdit('twitter', self)
        self.username.setGeometry(805, 40, 225, 80)
        self.username.setStyleSheet("background-color:white; border:1px solid black;")
        self.username.setAlignment(Qt.AlignCenter)
        self.username.setFont(font2)

        # search button
        self.search_button = QPushButton('Search', self)
        self.search_button.setGeometry(820, 135, 195, 70)
        self.search_button.setFont(font4)

        # some account details
        self.label1 = QLabel('Account Info', self)
        self.label1.setGeometry(25, 230, 1010, 50)
        # self.label1.setStyleSheet("background-color:white; border:1px solid black;")
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setFont(font4)

        self.account_details = QLabel('Account Info', self)
        self.account_details.setGeometry(25, 280, 1010, 50)
        self.account_details.setStyleSheet("background-color:white; border:1px solid black;")
        self.account_details.setAlignment(Qt.AlignCenter)
        self.account_details.setFont(font4)
        self.account_details.setWordWrap(True)

        # analyse account data
        self.label2 = QLabel('Bot Account Analysis', self)
        self.label2.setGeometry(25, 325, 1010, 50)
        # self.label2.setStyleSheet("background-color:white; border:1px solid black;")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setFont(font4)

        self.tweets_satistics_data = QLabel('Recent tweets Analysis', self)
        self.tweets_satistics_data.setGeometry(25, 375, 850, 100)
        self.tweets_satistics_data.setStyleSheet("background-color:white; border:1px solid black;")
        self.tweets_satistics_data.setAlignment(Qt.AlignCenter)
        self.tweets_satistics_data.setFont(font4)

        # switch statistic graph button
        self.switch_button = QPushButton('Switch', self)
        self.switch_button.setGeometry(885, 400, 150, 50)
        self.switch_button.setFont(font4)

        self.label3 = QLabel('Tweets Statistic Graph', self)
        self.label3.setGeometry(25, 475, 1010, 50)
        # self.label3.setStyleSheet("background-color:white; border:1px solid black;")
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setFont(font4)

        self.pic1 = QLabel('Image', self)
        self.pic1.setGeometry(25, 525, 1010, 410)
        self.pic1.setStyleSheet("background-color:white; border:1px solid black;")
        self.pic1.setAlignment(Qt.AlignCenter)
        self.pic1.setFont(font4)
        self.pic1.setWordWrap(True)

        self.userid = 783214
        # connect button to clicked event
        self.search_button.clicked.connect(self.search_button_clicked)
        self.switch_button.clicked.connect(self.switch_button_clicked)
        self.searched=False
        self.show()

    def center(self):
        this_frame = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        this_frame.moveCenter(screen_center)
        self.move(this_frame.topLeft())

    def search_button_clicked(self):
        username = self.username.text()
        try:

            # input authentication information
            auth = tweepy.OAuthHandler(api_auth_info.api_key, api_auth_info.api_secret)
            auth.set_access_token(api_auth_info.access_token, api_auth_info.access_token_secret)

            rapidapi_key = api_auth_info.rapidapi_key
            twitter_app_auth = api_auth_info.twitter_app_auth

            api = tweepy.API(auth)
            bot_analyser = botometer.Botometer(wait_on_ratelimit=True,
                                               rapidapi_key=rapidapi_key,
                                               **twitter_app_auth)
            # Basic information

            input_name = self.username.text()
            user = api.get_user(screen_name=input_name)
            # print(user)
            name = user.name
            user_id = user.id
            location = user.location
            description = user.description
            followers_count = user.followers_count
            following_count = user.friends_count
            profile_url = user.profile_image_url_https
            tweets_count = user.statuses_count
            verified = user.verified
            user_url = user.url
            protected = user.protected
            list_count = user.listed_count
            favourites_count = user.favourites_count
            language = user.lang

            profile_req = requests.get(profile_url)
            profile_ = QPixmap()
            profile_.loadFromData(profile_req.content)

            self.userid = user_id

            self.profile.setPixmap(profile_)
            self.name.setText(name)
            self.follower.setText(str(followers_count))
            self.following.setText(str(following_count))
            self.introduction.setText(description)

            today_date = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())

            account_info_text = "User id: " + str(user_id) + "   Tweets: " + str(tweets_count) + "   Favourite: " + str(
                favourites_count) + "   Location: " + location
            self.account_details.setText(account_info_text)

            bot_analysis_result = bot_analyser.check_account(user_id)

            bot_analysis_text = ''
            bot_analysis_text += 'Major Language: ' + bot_analysis_result['user']['majority_lang'] + '   Bot Score: '+str(round(bot_analysis_result['cap']['english'],3))+' (English)' +'   '+str(round(bot_analysis_result['cap']['universal'],3))+' (Universal)'
            # print(bot_analysis_result)
            bot_analysis_text+='\n'+'   Fake Follower: '+str(bot_analysis_result['raw_scores']['universal']['fake_follower'])+'   Financial: '+str(bot_analysis_result['raw_scores']['universal']['financial'])+'   Spammer: '+str(bot_analysis_result['raw_scores']['universal']['spammer'])+'   Astroturf: '+str(bot_analysis_result['raw_scores']['universal']['astroturf'])
            bot_analysis_text += '\n' + '   Other: ' + str(bot_analysis_result['raw_scores']['universal']['other'])+ '   Overall: ' + str(bot_analysis_result['raw_scores']['universal']['overall'])+ '   Self_declared: ' + str(bot_analysis_result['raw_scores']['universal']['self_declared'])
            self.tweets_satistics_data.setText(bot_analysis_text)

            recent_100_tweets_text = ''
            self.recent_10_tweets_text=''
            count=0
            tweets_100 = api.user_timeline(id=user_id, count=100)
            for i in tweets_100:
                recent_100_tweets_text += '\n' + i.text
            for i in tweets_100:
                self.recent_10_tweets_text += '\n' + i.text
                count+=1
                if count>10:
                    break
            # print(recent_100_tweets_text)
            recent_100_tweets_text = recent_100_tweets_text.replace("https", " ")
            recent_100_tweets_text = recent_100_tweets_text.replace("t.co", " ")
            recent_100_tweets_text = recent_100_tweets_text.replace("RT", " ")

            print('information refreshed, user:', username)

            w = wordcloud.WordCloud(width=1010, height=410, background_color='white', max_words=100)
            w.generate(recent_100_tweets_text)
            w.to_file('Graphs/graph_1.png')

            graph_1 = QPixmap('Graphs/graph_1.png')
            self.pic1.setPixmap(graph_1)
            self.graph_num = 1
            self.searched=True

        except Exception as e:
            print(e)

        except Exception as e:
            print(e)

    def switch_button_clicked(self):
        if self.searched:
            print('Analysing...')
        else:
            print('Please search first')
            return 0

        document = language_v1.Document(
            content=self.recent_10_tweets_text, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        client = language_v1.LanguageServiceClient()
        if self.graph_num==1:
            # Do Sentiment analysis
            sentiment = client.analyze_sentiment(
                request={"document": document}
            ).document_sentiment
            sentiment_analysis='\tRecent tweets\' sentiment analysis'
            sentiment_analysis+='\nHere are some tweets samples: '+self.recent_10_tweets_text[:175]+'...'
            sentiment_analysis+='\n\tIn recent 10 tweets, this user gets a sentiment value of '+str(round(sentiment.score,2))
            sentiment_analysis+=', which indicates that these tweets are '
            if sentiment.score>0 and sentiment.score<0.5:
                sentiment_analysis+='slightly positive.'
            elif sentiment.score>=0.5:
                sentiment_analysis += 'very positive.'
            elif sentiment.score==0:
                sentiment_analysis += 'neutral.'
            elif sentiment.score<0 and sentiment.score>-0.5:
                sentiment_analysis += 'slightly negative.'
            elif sentiment.score<=-0.5:
                sentiment_analysis += 'very negative.'
            else:
                sentiment_analysis='Program error'
            sentiment_analysis+=' And the magnitude value is '+str(round(sentiment.magnitude,2))+'.'



            sentiment_analysis+='\n\nAnalysed by Google NLP API'
            self.pic1.setText(sentiment_analysis)
            self.graph_num+=1
        elif self.graph_num==2:
            # Do Entities analysis
            entities = client.analyze_entities(
                request={"document": document}
            )
            print(entities)
            count=0
            entities_analysis_text = 'Entities_analysis_text'
            entities_analysis_text += '\nHere are some mentioned entities in recent tweets.\n'
            for i in entities.entities:
                entities_analysis_text+='\n'+str(i.name)+'  '+str( i.type_)+'  '+ str(i.salience)
                count+=1
                if count>8:
                    break
            entities_analysis_text+='\nAnalysed by Google NLP API'
            self.pic1.setText(entities_analysis_text)
            self.graph_num+=1
        elif self.graph_num==3:
            graph_1 = QPixmap('Graphs/graph_1.png')
            self.pic1.setPixmap(graph_1)
            self.graph_num = 1
        else:
            print('Software error')

        print('Analysis finished')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
