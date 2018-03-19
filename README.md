# extract_geo
Extract geo info from tweet corpus. Read from a folder of gz files, in which one line stores a tweet json.

The output are separate gz files that stores (tweet_time, tweet_id, user_id, geo, coordinates, place, text) in each line.

**Requirements**:
1. To run the script, python 3 should be installed already.
2. Increase or decrease the number of threads (4 in default) in the process.py if necessary.

**How to use**:

Execute 'script.py [arg1] [arg2]' in terminal (cd to the script folder or use its absolute path).
* arg1 is the folder directory that contains all gz files
* arg2 is the folder directory to store the processed files
* If not input, the script will ask again or set to the default.

**Example**:
>python process.py D:\tweet_data\gz_files D:\tweet_data\processed

You can run the test.py first to check whether it can produce the right file.

