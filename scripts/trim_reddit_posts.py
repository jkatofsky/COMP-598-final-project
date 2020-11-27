import argparse
import json


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", required=True)
    parser.add_argument("data_file", nargs='+')
    
    args = parser.parse_args()
    output = args.o
    data_file = args.data_file

    line_count = 0
    json_lines = []
    for data_f in data_file:
        with open(data_f, 'r') as f:
            for line in f:
                if line_count < 1000:
                    json_lines.append(line)
                line_count += 1
    with open(output, 'w') as f:
        for line in json_lines:
            f.write(line)

if __name__ == "__main__":
    main()
