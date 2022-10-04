import sys
import time

import requests
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import tweepy
import wordcloud

api_key = "xxxxxxxxxxxxxxxxxxxxxxx"
api_secret = "xxxxxxxxxxxxxxxxxxxxxxx"
access_token = "xxxxxxxxxxxxxxxxxxxxxxx"
access_token_secret = "xxxxxxxxxxxxxxxxxxxxxxx"
bearer_token = "xxxxxxxxxxxxxxxxxxxxxxx"


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
        self.label1 = QLabel('Account Details', self)
        self.label1.setGeometry(25, 230, 1010, 50)
        # self.label1.setStyleSheet("background-color:white; border:1px solid black;")
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setFont(font4)

        self.account_details = QLabel('Account Details', self)
        self.account_details.setGeometry(25, 280, 1010, 100)
        self.account_details.setStyleSheet("background-color:white; border:1px solid black;")
        self.account_details.setAlignment(Qt.AlignCenter)
        self.account_details.setFont(font4)
        self.account_details.setWordWrap(True)

        # analyse account data
        self.label2 = QLabel('Tweets statistic', self)
        self.label2.setGeometry(25, 375, 1010, 50)
        # self.label2.setStyleSheet("background-color:white; border:1px solid black;")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setFont(font4)

        self.tweets_satistics_data = QLabel('Recent tweets statistic', self)
        self.tweets_satistics_data.setGeometry(25, 425, 850, 50)
        self.tweets_satistics_data.setStyleSheet("background-color:white; border:1px solid black;")
        self.tweets_satistics_data.setAlignment(Qt.AlignCenter)
        self.tweets_satistics_data.setFont(font4)

        # follow button
        self.follow_button = QPushButton('Follow', self)
        self.follow_button.setGeometry(885, 425, 150, 50)
        self.follow_button.setFont(font4)

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

        self.userid=783214
        # connect button to clicked event
        self.search_button.clicked.connect(self.search_button_clicked)
        self.follow_button.clicked.connect(self.follow_button_clicked)

        # self.button_open_camera = QPushButton(u'打开相机')
        # self.button_open_camera.ser
        self.show()

    def center(self):
        this_frame = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        this_frame.moveCenter(screen_center)
        self.move(this_frame.topLeft())

    def search_button_clicked(self):
        username = self.username.text()
        try:
            client = tweepy.Client(consumer_key=api_key, consumer_secret=api_secret, access_token=access_token,
                                   access_token_secret=access_token_secret, bearer_token=bearer_token, return_type=dict)
            account_info = client.get_user(username=username,
                                           user_fields='public_metrics,description,profile_image_url,verified,protected,location,url')
            name_ = account_info['data']['name']
            user_id = account_info['data']['id']
            public_metrics = account_info['data']['public_metrics']
            followers_count = public_metrics['followers_count']
            following_count = public_metrics['following_count']
            tweets_count = public_metrics['tweet_count']
            introduction_ = account_info['data']['description']
            profile_url = account_info['data']['profile_image_url']
            list_count = public_metrics['listed_count']
            user_url = account_info['data']['url']
            protected = account_info['data']['protected']
            if 'location' in account_info['data']:
                location = account_info['data']['location']
            else:
                location = 'Unknown'

            profile_req = requests.get(profile_url)
            profile_ = QPixmap()
            profile_.loadFromData(profile_req.content)

            self.userid=user_id

            self.profile.setPixmap(profile_)
            self.name.setText(name_)
            self.follower.setText(str(followers_count))
            self.following.setText(str(following_count))
            self.introduction.setText(introduction_)

            today_date = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
            tmp = client.get_users_tweets(id=user_id, max_results=100, start_time=today_date)
            if tmp['meta']['result_count'] != 0:
                today_tweets = tmp['data']
                today_tweets_count = 0
                for i in today_tweets:
                    today_tweets_count += 1
            else:
                today_tweets_count = 0
            tweet_statistics = "Total Tweets: " + str(tweets_count) + "      Tweets Today: " + str(today_tweets_count)
            self.tweets_satistics_data.setText(tweet_statistics)

            recent_100_tweets_text=''
            tmp2=client.get_users_tweets(id=user_id,max_results=100)
            for i in range(len(tmp2['data'])):
                recent_100_tweets_text+=tmp2['data'][i]['text']
            #print(recent_100_tweets_text)
            recent_100_tweets_text=recent_100_tweets_text.replace("https"," ")
            account_detail_text = "User id: " + str(user_id) + "   List Count: " + str(
                list_count)+"   Location: "+location + "\nAccount Protect Statu: " + str(protected) + "   User's Profile Url: " + user_url
            self.account_details.setText(account_detail_text)

            print('information refreshed,', account_info)

            w = wordcloud.WordCloud(width=1010,height=410,background_color='white',max_words=100)
            w.generate(recent_100_tweets_text)
            w.to_file('graph_1.png')

            graph_1=QPixmap('graph_1.png')
            self.pic1.setPixmap(graph_1)

        except Exception as e:
            print(e)

    def follow_button_clicked(self):
        try:
            client = tweepy.Client(bearer_token=bearer_token, return_type=dict)
            if self.follow_button.text()== 'Follow':
                client.follow(target_user_id =self.userid, user_auth = False)
                self.follow_button.setText('Unfollow')
            elif self.follow_button.text()== 'Unfollow':
                client.follow(target_user_id =self.userid, user_auth = False)
                self.follow_button.setText('Follow')

        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
