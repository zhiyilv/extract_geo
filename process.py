import os
import json
from multiprocessing.dummy import Pool  # use multi-threading instead of multi-processing
import gzip
import io
import sys


# the directory of the tweet files
try:
    files_folder_dir = sys.argv[1]
except IndexError:
    files_folder_dir = input('Please input the absolute path to the folder storing gz files, '
                             'current folder in default:\n') or os.getcwd()

# the folder to store processed files
try:
    extract_dir = sys.argv[2]
except IndexError:
    extract_dir = input('Please input the absolute path to the folder storing processed files, '
                        'will create one in current folder if not provided:\n') or os.path.join(os.getcwd(), 'processed')


def do_each_file(file_name):
    if file_name.endswith('.gz'):  # must be gz file
        # file_name = os.path.basename(file_path)
        file_path = os.path.join(files_folder_dir, file_name)
        extracted_file = os.path.join(extract_dir, file_name[:-3]+'_extracted.gz')  # the path of the extracted file
        print('processing {}, the processed file is in {}'.format(file_name, extracted_file))

        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            for line in f:
                try:
                    tweet_json = json.loads(line)  # try to load each json
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
                        with gzip.open(extracted_file, 'at', encoding='utf-8') as fw:
                            fw.write(info_to_write)


if __name__ == '__main__':
    # create if extract_dir does not exist
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    file_list = os.listdir(files_folder_dir)

    pool = Pool(4)  # 4 threads in default, change to a higher number if powerful machine
    pool.map(do_each_file, file_list)
    pool.close()
    pool.join()

