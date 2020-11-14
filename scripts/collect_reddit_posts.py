import argparse
import json
import requests


def get_posts(subreddit, filtering, limit):
    all_posts = []
    pulled = 0

    while pulled < limit:
        _params = {'limit': 100}
        if pulled != 0:
            _params['after'] = all_posts[-1]['data']['name']

        posts = requests.get(f'http://api.reddit.com/r/{subreddit}/{filtering}',
        params=_params,
        headers={'User-Agent': 'mac:requests'})

        temp = posts.json()['data']['children']
        pulled += len(temp)
        all_posts.extend(temp)

    return all_posts[:limit]


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("subreddit")
    parser.add_argument("--outfile", type=str, default="data.json")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--filtering", type=str, default="hot")

    args = parser.parse_args()
    subreddit, outfile, limit, filtering = args.subreddit, args.outfile, args.limit, args.filtering

    with open(outfile, 'w') as output_fp:
        posts = get_posts(subreddit, filtering, limit)
        output_fp.writelines('\n'.join(json.dumps(post) for post in posts))


if __name__ == "__main__":
    main()