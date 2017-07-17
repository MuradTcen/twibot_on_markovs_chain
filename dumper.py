# -*- coding: utf-8 -*-
'''
Module to get 3.2k tweet from twitter, delete links and @names and save to txt

Example:
    python3 dumper.py -n twitter -f secrets_and_tokens.json
'''


import tweepy
import json
from tweepy import OAuthHandler
import re
import argparse
get_text_from_json = (lambda x: x._json['text'])


def get_secrets_and_tokens_from_json(json_file):
    try:
        data = json.load(open(json_file))
    except:
        print("json file with consumers key, secret and access token, secret is absent at directory ")
    return data


def authorization(*args):
    auth = OAuthHandler(args[0]['consumer_key'], args[0]['consumer_secret'])
    auth.set_access_token(args[0]['access_token'], args[0]['access_secret'])
    api = tweepy.API(auth)
    return api


def write_txt(list, filename):
    with open(filename + '.txt', 'w') as f:
        f.write('\n\n'.join(list))


def cleaning_tweets(tweet):
    pattern_name_start = r'@\w* '
    pattern_name_end = r' @\w*'
    pattern_link_space_begin = r'http\w?:\/\/(www.)?\w*.\w*(\/\w*)* '
    pattern_link_space_end = r' http\w?:\/\/(www.)?\w*.\w*(\/\w*)*'
    tweet = re.sub(pattern_name_start, '', tweet)
    tweet = re.sub(pattern_name_end, '', tweet)
    tweet = re.sub(pattern_link_space_begin, '', tweet)
    result = re.sub(pattern_link_space_end, '', tweet)
    return result


def tweets_dumper(screen_name, api):
    all_tweets = []
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    all_tweets.extend(new_tweets)
    oldest = all_tweets[-1].id - 1
    while len(new_tweets) > 0:
        print('getting tweets before %s' % (oldest))
        new_tweets = api.user_timeline(
            screen_name=screen_name, count=200, max_id=oldest)
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1
        print('..%s tweets downloaded so far' % (len(all_tweets)))
    # outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in all_tweets]
    all_tweets = list(map(get_text_from_json, all_tweets))
    return all_tweets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, required=True)
    parser.add_argument('-f', '--file', type=str, required=True)
    args = parser.parse_args()
    credentials = get_secrets_and_tokens_from_json(args.file)
    api = authorization(credentials)
    tweets = tweets_dumper(args.name, api)
    tweets = list(map(cleaning_tweets, tweets))
    write_txt(tweets, args.name)


if __name__ == '__main__':
    main()
