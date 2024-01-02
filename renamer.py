import sys
import os
import re

path_arg = sys.argv[1]
sub_type = sys.argv[2]


def main():
    pattern_subs = ".*S[0-9][0-9].*E[0-9][0-9].*" + sub_type + "$"
    pattern_mov = ".*S[0-9][0-9].*E[0-9][0-9].*[^" + sub_type + "]$"

    movies = []
    subs = []

    for filename in os.listdir(path_arg):
        if re.match(pattern_subs, filename, re.IGNORECASE):
            # print("Sub found: " + filename)
            subs.append(filename)
        elif re.match(pattern_mov, filename, re.IGNORECASE):
            # print("Movie found: " + filename)
            movies.append(filename)
        else:
            print("File ignored: " + filename)

    sub_map = {}
    for sub in subs:
        sub_num = extract_season_episode(sub)
        if sub_map.get(sub_num) is None:
            sub_map[sub_num] = [sub]
        else:
            sub_map[sub_num].append(sub)
    movie_map = {}
    for movie in movies:
        movie_num = extract_season_episode(movie)
        movie_map[movie] = sub_map.get(movie_num)

    for (k, v) in movie_map.items():
        print(str(k) + " : " + str(v))

    for (k, v) in movie_map.items():
        if len(v) <= 1:
            for sub in v:
                new_str = path_arg + "/" + k[0:-4] + ".srt"
                new_sub = path_arg + "/" + sub
                print("Renaming \"" + new_sub + "\" to \"'" + new_str + "\"")
                os.rename(new_sub, new_str)
        else:
            counter = 0
            for sub in v:
                new_str = path_arg + "/" + k[0:-4] + "_" + str(counter) + ".srt"
                new_sub = path_arg + "/" + sub
                print("Renaming \"" + new_sub + "\" to \"" + new_str + "\"")
                os.rename(new_sub, new_str)
                counter += 1


def extract_season_episode(filename):
    match = re.search(r'S(\d+)E(\d+)', filename)
    if match:
        return int(match.group(1)), int(match.group(2))  # Season, Episode
    return 0, 0  # Default if no match


main()
