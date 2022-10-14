import botometer
import api_auth_info

rapidapi_key = api_auth_info.rapidapi_key
twitter_app_auth = api_auth_info.twitter_app_auth

bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

# Check a single account by screen name
# result = bom.check_account('@twitter')
# print(result)
# Check a account by id
# result = bom.check_account(44196397)
# print(result)
# Check accounts by username
result = bom.check_account('@elonmusk')
print(result)
print(result['cap'])
print(result['display_scores'])
print(result['raw_scores'])
print(result['user'])
