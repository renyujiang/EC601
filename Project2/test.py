import tweepy

api_key = "n73JX55UFog4RcU517YdFuqHr"
api_secret = "zEsYEc8ll1JlVyyGs4Vg2BBAL23tS85qnPvHMWhmeLzBDbhpqi"
access_token = "1575336781934993410-PVWukgkT8F0DWd8s0f0IpgthGYnV3g"
access_token_secret = "evA10qj4pHUnu7LXbdxScHM6gN8WxmLJWkmrEi5ODGjCa"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAPVthgEAAAAAD75NfB91Zo8zMENP26kanrrwTaE%3DpihnW7QZXLWHYfiAa1ejlPsugCOYu3x0l7484jOpDp1WDl8hze"

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



