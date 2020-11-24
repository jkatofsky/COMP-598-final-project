import argparse
import csv
from random import randrange
import json

def check_duplicate_sentence(sent1, sent2):
    return sent1 == sent2

def get_random_sentences(title_file, line_num):
    post_indexes = []
    posts = []
    result_post = []
    with open(title_file, 'r') as f:
        for i, line in enumerate(f):
            flag = False
            for other in posts:
                if check_duplicate_sentence(line, other):
                    flag = True
                    break
            if flag:
                continue

            posts.append(line)

    if  len(posts) < line_num:
        return posts

    while len(post_indexes) < line_num:
        i = randrange(line_num)
        while i in post_indexes:
            i = randrange(line_num)
        
        post_indexes.append(i)
        result_post.append(posts[i][1:-2])

    return result_post
        


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    parser.add_argument("-l", help="Number of lines", default=200)
    parser.add_argument("-o", help="Output path")

    args = parser.parse_args()
    file_path, line_num, output_path = args.file_path, int(args.l), args.o

    random_lines = get_random_sentences(file_path, line_num)
    print(len(random_lines))

    if output_path is not None:
        with open(output_path, 'w') as f:
            tsv_writer = csv.writer(f, delimiter='\t')
            tsv_writer.writerow(['title', 'coding'])
            for line in random_lines:
                tsv_writer.writerow([line, ''])


if __name__ == "__main__":
    main()
