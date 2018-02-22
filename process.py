import os
import json
from multiprocessing.dummy import Pool  # use multi-threading instead of multi-processing


def do_each_file(name_path):
    print('processing {}'.format(name_path[0]))
    with open(name_path[1], encoding='utf-8') as f:
        for line in f:
            try:
                tweet_json = json.loads(line)
            except Exception:
                print('one json cannot be loaded, in file {}'.format(name_path[1]))
            else:
                # only process those geo-tagged tweets
                if tweet_json['geo'] or tweet_json['coordinates'] or tweet_json['place']:
                    with open(os.path.join(extract_dir, '{}_extracted.txt'.format(name_path[0])), 'a', encoding='utf-8') as fw:
                        fw.write('{id}--{geo}--{cor}--{place}--{text}\n'.format(id=tweet_json['id'],
                                                                                geo=tweet_json['geo'] or ' ',
                                                                                cor=tweet_json['coordinates'] or ' ',
                                                                                place=tweet_json['place'] or ' ',
                                                                                text=tweet_json['text']))


def get_names_paths(folder):
    return ((f[:-4], os.path.join(folder, f))
            for f in os.listdir(folder)
            if f.endswith('txt'))


if __name__ == '__main__':
    root_dir = "D:\Projects\extract_geo\dataset"  # change to the directory of the tweet files
    extract_dir = os.path.join(root_dir, 'geo_extracted')  # the directory to store extracted files
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    names_files = get_names_paths(root_dir)

    pool = Pool(16)  # 16 threads in default, change to a higher number if powerful machine
    pool.map(do_each_file, names_files)
    pool.close()
    pool.join()

