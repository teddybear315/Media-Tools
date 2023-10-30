import math
import os
from sys import argv


def represents_int(s):
    try: int(s)
    except ValueError: return False
    else: return True

def default(argi):
    """
    Returns if the command line argument (sys.argv[argi]) specified should be set to default
    Returns if the command line argument (sys.argv[argi]) has another option or no successor
    :param argi: index of parameter
    :return: bool
    """
    return len(argv) < (argi + 2) or (argv[argi + 1][0] == '-' and not represents_int(argv[argi + 1]))

def yn_bool(yn: str): return yn.lower() == 'y'

def ep_pos_to_int(_str, pos):
    """Checks if each spot is int instead of trying to convert entire string, fails if supply a char

    Args:
        _str (str): episode title
        pos (int): position of 'E' supplied by user

    Returns:
        int: Episode number
    """
    try:
        return int(_str[pos]) * 10 + int(_str[pos + 1])
    except:
        return int(_str[pos])

video_formats = ["mp4", "mkv"]
show_name = movie = ""
year = season = 0
rp_check = ep_check = te_check = replace_periods = ruler_2nd = False
index_checks = ep_i = start_i = end_i = 0

for arg in range(0, len(argv)):
    if argv[arg] == "-t": show_name = argv[arg+1]
    elif argv[arg] == "-m": movie  = argv[arg + 1]
    elif argv[arg] == "-y": year = int(argv[arg+1])
    elif argv[arg] == "-s": season = int(argv[arg+1])
    elif argv[arg] == "-rp":
        rp_check = True
        replace_periods = True if default(arg) else yn_bool(argv[arg + 1])
    elif argv[arg] == "-ep":  # episode index
        ep_check = True
        index_checks += 1
        ep_i = int(argv[arg + 1])
    elif argv[arg] == "-ts":  # title start index
        index_checks += 1
        start_i = int(argv[arg + 1])
    elif argv[arg] == "-te":  # space after title index
        te_check = True
        index_checks += 1
        end_i = 0 if default(arg) else int(argv[arg + 1])
    elif argv[arg] == "-mep" and default(arg): ruler_2nd = True

cwd = os.getcwd()
current_episode=0

if not rp_check and not movie: replace_periods = yn_bool(input("Replace Periods? (y/N) "))
if not show_name and not movie: show_name = input("Show Title? ")
if not year: year = int(input("Release Year? "))
if not season and not movie: season = int(input("Season Number? "))

# ruler for getting indexes
if index_checks != 3 and not movie:
    strs = ["", "", "", "", ""]
    example_item = ""
    for _ in os.listdir(cwd):
        if _[-3:] not in video_formats: continue
        print(_[:-4])
        example_item = len(_[:-4])
        break
    for letter in range(0, example_item):
        strs[0] = strs[0] + str(math.floor(letter / 10) % 10)
        strs[1] = strs[1] + str(letter % 10)
        strs[2] = strs[2] + '-'
        strs[3] = strs[3] + str(math.floor((example_item / 10) - (letter / 10)) % 10)
        strs[4] = strs[4] + str((example_item - letter) % 10)
    for _str in strs:
        print(_str)

    # if variables not set automatically set manually
    if not ep_check:
        print("Used for files that contain multiple EPs")
        ep_i = int(input("Episode Index? ('E') (0:none)"))
        if not ep_i: ep = 1
    if not start_i:
        # print("If example file has multiple EPs, subtract 3 from helper index if Exx-xx, subtract 4 if Exx-Exx
        # or just len of characters after 1st episode # (`-xx`, `-Exx`)")
        start_i = int(input("Title Start Index? (first letter) "))
    if not te_check: end_i = int(input("Title End Index? (space after last letter, use negative under \'-\') (0:end) "))
    if not ruler_2nd and index_checks != 3:
        ruler_2nd = yn_bool(input("Does the EXAMPLE RULER contain multiple episodes in one file? (y/n)"))

for item in os.listdir(cwd):
        current_episode+=1
        print(item)
        item_path = os.path.join(cwd, item)  # Full path to the item
        # Check if the item is a video file, if not check next file
        if item[-3:] not in video_formats: continue
        item_title = item[:-4]
        file_type = item[-4:]
        ep_title = ""
        print("File:", item_title)
        nth_item = 0  # any time nth_item != 0 the current file contains multiple episodes

        if not movie:
            ep = ep_pos_to_int(item_title, ep_i + 1)
            offset = 0
            # if ep index known and "SxxExx`-`"
            if ep_i and item_title[ep_i + 3] == '-':
                try:  # convert "SxxExx-`**`" to int
                    nth_item = ep_pos_to_int(item, ep_i + 4)
                    offset = 3
                except:  # fail if common encoding: SxxExx-Exx instead of just SxxExx-xx
                    nth_item = ep_pos_to_int(item, ep_i + 5)
                    offset = 4

            # ruler_2nd means automatic offset
            # and nth_item means needed offset
            if not ruler_2nd and nth_item:
                temp_i = start_i + offset
            elif ruler_2nd and not nth_item:
                temp_i = start_i - offset
            else:
                temp_i = start_i

            if not end_i:
                ep_title = item_title[temp_i:]
            else:
                ep_title = item_title[temp_i:end_i]

            # if renaming file, set output_item
            if replace_periods: ep_title = ep_title.replace('.', ' ')
            # SHOW (YEAR) SxxExx(-xx) EPISODE TITLE
            output_item = f"{show_name} ({year}) S{season:02d}E{ep:02d}" \
                        f"{f'-{nth_item:02d}' if (item_title[ep_i + 3] == '-' and ep_i != 0) else ''} {ep_title}{file_type}"
        elif movie:
            output_item = f"{movie} ({year}){file_type}"
        else:
            output_item = item
        os.rename(os.path.join(cwd, item), os.path.join(cwd, output_item))