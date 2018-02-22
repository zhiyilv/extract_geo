# extract_geo
Extract geo info from tweet corpus. Read from a folder of txt files, in which one line stores a tweet json.

The output are separate txt files that stores (tweet_id, geo, coordinates, place) in each line.

1. To run the script, python 3 should be installed already.
2. Please input the folder directory that stores all those txt files.
3. Increase or decrease the number of threads if necessary.
4. Then execute 'python process.py' in terminal (cd to the folder containing process.py or use the absolute path to it).
