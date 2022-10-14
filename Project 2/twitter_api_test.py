import tweepy
import api_auth_info

auth = tweepy.OAuthHandler(api_auth_info.api_key, api_auth_info.api_secret)
auth.set_access_token(api_auth_info.access_token, api_auth_info.access_token_secret)

api = tweepy.API(auth)
user = api.get_user(screen_name='elonmusk')
print(user)
name = user.name
id_str = user.id_str
location = user.location
description = user.description
followers_count = user.followers_count
followings_count = user.friends_count
profile_url = user.profile_image_url_https
statuses_count=user.statuses_count
verified=user.verified
tweets=api.user_timeline(screen_name='elonmusk',count=100)
for i in tweets:
    print(i.text)
