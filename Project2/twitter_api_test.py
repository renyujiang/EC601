import tweepy

api_key = "xxxxxxxxxxxxxxxxxxxxxxx"
api_secret = "xxxxxxxxxxxxxxxxxxxxxxx"
access_token = "xxxxxxxxxxxxxxxxxxxxxxx"
access_token_secret = "xxxxxxxxxxxxxxxxxxxxxxx"
bearer_token = "xxxxxxxxxxxxxxxxxxxxxxx"

client = tweepy.Client(consumer_key=api_key, consumer_secret=api_secret, access_token=access_token,
                       access_token_secret=access_token_secret, bearer_token=bearer_token, return_type=dict)

# Replace with your own search query
query = 'covid -is:retweet'

# Replace the limit=1000 with the maximum number of Tweets you want
account_info = client.get_user(username='elonmusk',user_fields='public_metrics')
username=account_info['data']['name']
user_id=account_info['data']['id']
tweet=client.get_users_tweets(id=user_id)

print(account_info)
print("Username:", account_info['data']['name'])
for i in range(0,10):
    print("tweets:",tweet['data'][i]['text'])

follower=client.get_users_followers(id=user_id)
print(follower)



