import os
import json
import gzip
import sys


if __name__ == '__main__':
    print('This test script will try to extract 2 pieces of geo information as a test.\n')

    # the directory of one tweet file
    try:
        file_dir = sys.argv[1]
    except IndexError:
        file_dir = input('Please input the absolute path to one gz file, '
                         'the first one in the current folder if not provided :\n')
        if not file_dir:  # set the test file as the first gz file in the current folder
            for i in os.listdir(os.getcwd()):
                if i.endswith('.gz'):
                    file_dir = i
                    break
            else:  # no valid file in current folder
                raise ValueError('Please input a valid path or put the script in the right folder')

    # the folder to store processed files
    try:
        extract_dir = sys.argv[2]
    except IndexError:
        extract_dir = input('Please input the absolute path to the folder storing processed files, '
                            'will create one in current folder if not provided:\n') or os.path.join(os.getcwd(),
                                                                                                   'processed')
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    file_name = os.path.basename(file_dir)
    extract_file_name = file_name[:-3] + '_extracted.gz'
    print('your input file is named {}\nthe extracted file is named {}\nit is stored in {}'.format(file_name,
                                                                                                   extract_file_name,
                                                                                                   extract_dir))
    # start testing
    piece_count = 0  # number of geo info found
    with gzip.open(file_dir, 'rt', encoding='utf-8') as f:
        for line in f:
            try:
                tweet_json = json.loads(line)  # load each json
            except Exception:
                print('one json cannot be loaded, in file {}'.format(file_name))  # skip if error
            else:
                # only process those geo-tagged tweets
                if tweet_json['geo'] or tweet_json['coordinates'] or tweet_json['place']:
                    info_to_write = [tweet_json['timestamp_ms'], tweet_json['id'], tweet_json['user']['id'],
                                     tweet_json['geo'] or ' ', tweet_json['coordinates'] or ' ',
                                     tweet_json['place'] or ' ', tweet_json['text']]
                    info_to_write = json.dumps(info_to_write)
                    info_to_write = info_to_write + '\n'
                    print(info_to_write)
                    with gzip.open(os.path.join(extract_dir, extract_file_name), 'at', encoding='utf-8') as fw:
                        fw.write(info_to_write)
                    piece_count += 1
                    if piece_count == 2:  # just extract 2 pieces of geo info
                        break
    print('Please find the file in {}'.format(extract_dir))
    print('Check whether it contains {} lines of [time,id, usr_id, geo, cor, place, text]'.format(piece_count))
    print('and note that each element will be blank if it does not exist in the json')

