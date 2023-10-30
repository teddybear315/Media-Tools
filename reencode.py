import math
import os
import subprocess
from sys import argv

# Get the current working directory
cwd = os.getcwd()
debug = ["-h", "--help", "-help"] in argv or "-debug" in argv
if not debug:
    try:
        os.mkdir("Reencode")
    except:
        print("Couldnt make folder")

def represents_int(s):
    try: int(s)
    except ValueError: return False
    else: return True

def default(argi):
    """
    Returns if the command line argument (sys.argv[argi]) specified should be set to default
    Returns if the command line argument (sys.argv[argi]) has another option or no successor

    Args:
        argi (int): position of argument in argv

    Returns:
        bool: if using default value
    """
    return len(argv) < (argi + 2) or (argv[argi + 1][0] == '-' and not represents_int(argv[argi + 1]))


def yn_bool(yn: str): return yn.lower() == 'y'


video_formats = ["mp4", "mkv"]
rename = show = overwrite_mode = movie = art_path = lang = movie_path = str_subtitlemapping = ""
q = cq = -1
fflvl = "4.1"
subenc = "copy"
year = season = subtitle_input = ep_i = start_i = end_i = index_checks = ep = 0
ruler_2nd = pretty = external_subtitles = replace_periods = skip_subtitles = skip_reencode = has_art = b10_mode = tune_animation = gpu = broken_artwork = lossless = False
ep_check = te_check = bit_check = rp_check = ss_check = sr_check = es_check = rn_check = b10_check = ov_check = False
bitrate = ("0", "0")

help_bitrate = """Recommended Bitrate and Quality for x265 encoding
res\tbitrate\tq val
720p\t1-2mbps\t18-20
1080p\t1-3mbps\t20-25\tanimation
1080p\t2-4mbps\t20-25
1440p\t4-6mbps\t20-25
2160p\t6-10mbps\t13-18"""

help_message = """[Y/n] defaults to capital letter
IF USING -P YOU 0 BYTE FILES REMOVE -P AND CHECK FFMPEG OUTPUT AND SET SETTINGS ACCORDINGLY
MetaData:
-m  [str]   : Movie Name, passed directly to ffmpeg
-mp [str]   : Movie Path, passed directly to ffmpeg
-t  [str]   : Show Title, passed directly to ffmpeg
-s  [int]   : Season, passed directly to ffmpeg
-y  [int]   : Release Year, passed directly to ffmpeg

FFMPEG:
-c   [#]	    : Thread count
-gpu		    : use hevc_nvenc over libx265
-p              : Pretty Output
-r   [Y/n]      : Rename Files?
-rp  [Y/n]      : Replace Periods

Video:
-sv                 : Skip Video Encoding
-ll                 : Lossless conversion, used mainly for heavily compressed x264 conversion
-ta                 : Tune Animation
-lv  [encoding lvl] : Encoding level, 4.0:720p60/1080p30, 4.1:1080p60, 5.0:4k30, 5.1:4k60, passed directly to ffmpeg
-b   [int]k [int]m  : Bitrate Min/Max, leave blank for automatic bitrate, passed directly to ffmpeg
-10b [Y/n]          : 10 Bit Mode
-cq  [int]          : Constant Bitrate Quality (translates to "-rc vbr -crf [cq]" with cpu or "-rc vbr -cq [cq] -qmax [cq+3]" with gpu), passed directly to ffmpeg
--broken_artwork    : Only use if artwork stream is broken, or you want to discard all video streams other than 0

-srt [Y/n]          : External Subtitles
-l  <eng>           : Subtitle Language Abbreviation for External subtitles, passed directly to ffmpeg
-ss                 : Skip Subtitle Encoding
-se <encoding>      : Change subtitle Encoding, passed directly to ffmpeg
-a[rt] <path>       : Specify path to art, passed directly to ffmpeg
-o                  : Overwrite Mode
-mep                : Multiple Episodes in file used for title formatting
-ep <int>           : Episode \'E\' Index
-ts <int>           : Episode Title Start Index
-te [int]           : Index of space after Title

DEPRECATED/USED WITH NVENC
-q   [int]          : Quality (translates to "-rc vbr -cq [cq] -qmin [cq-3] -qmax [cq+3]"), passed directly to ffmpeg"""

# loop through environment args and set variables accordingly
for arg in range(0, len(argv)):
    if argv[arg] in ["-h", "--help", "-help"] or len(argv) <= 1:
        if len(argv) > (arg + 1) and argv[arg + 1] in ["bitrate", "b", "-b", "-q", "-cq", "cq", "q"]:
            print(help_bitrate)
        else: print("add -b -q or -cq to get bitrate and quality recommendations based on content\n")
        print(help_message)
        exit(0)
    elif argv[arg] == "--broken_artwork": broken_artwork = True
    elif argv[arg] == "-ta": tune_animation = True
    elif argv[arg] == "-gpu": gpu  = True
    elif argv[arg] == "-p": pretty = True
    elif argv[arg] == "-s": season = int(argv[arg + 1])
    elif argv[arg] == "-t": show   = argv[arg + 1]
    elif argv[arg] == "-m": movie  = argv[arg + 1]
    elif argv[arg] == "-y": year   = int(argv[arg + 1])
    elif argv[arg] == "-ss": ss_check = skip_subtitles = True
    elif argv[arg] == "-sv": sr_check = skip_reencode = True
    elif argv[arg] == "-ll": lossless = True
    elif argv[arg] == "-mp": movie_path = argv[arg + 1]
    elif argv[arg] == "-r":  # rename boolean
        rn_check = True
        rename = True if default(arg) else yn_bool(argv[arg + 1])
    elif argv[arg] == "-rp":  # replace periods
        rp_check = True
        replace_periods = True if default(arg) else yn_bool(argv[arg + 1])
    elif argv[arg] == "-srt":  # external subtitles
        ss_check = es_check = True
        external_subtitles = True if default(arg) else yn_bool(argv[arg + 1])
    elif argv[arg] == "-l":
        if default(arg):
            print("Error: no default for -l")
            exit()
        lang = argv[arg + 1]
    elif argv[arg] == "-se":
        if default(arg):
            print("Error: no default for -se")
            exit()
        subenc = argv[arg + 1]
    elif argv[arg] in ["-a", "-art"]:
        if default(arg):
            print("Error: no default for -art")
            exit()
        has_art = True
        art_path = argv[arg + 1]
    elif argv[arg] == "-b":  # bitrate of encoding
        bit_check = True
        if default(arg): bitrate = ("AUTO", "AUTO")
        if len(argv) >= (arg + 2) and not default(arg) and not default(arg+1):  # included maximum
            bitrate = (argv[arg + 1], argv[arg + 2])
        else:
            bitrate = (argv[arg + 1], "AUTO")
    elif argv[arg] == "-q": q = int(argv[arg + 1])
    elif argv[arg] == "-cq": cq = int(argv[arg + 1])
    elif argv[arg] == "-lv": fflvl = "5.1" if default(arg) else argv[arg + 1]
    elif argv[arg] == "-10b":  # 10 bit mode
        b10_check = True
        b10_mode = True if default(arg) else yn_bool(argv[arg + 1])
    elif argv[arg] == "-o":  # overwrite mode
        ov_check = True
        overwrite_mode = 'y' if default(arg) else argv[arg + 1][0]
    elif argv[arg] == "-ep":  # episode index
        ep_check = rn_check = rename = True
        index_checks += 1
        ep_i = int(argv[arg + 1])
    elif argv[arg] == "-ts":  # title start index
        rn_check = rename = True
        index_checks += 1
        start_i = int(argv[arg + 1])
    elif argv[arg] == "-te":  # space after title index
        te_check = rn_check = rename = True
        index_checks += 1
        end_i = 0 if default(arg) else int(argv[arg + 1])
    elif argv[arg] == "-mep" and default(arg):
        ruler_2nd = True

# if variables not set automatically set manually
# if not sr_check: skip_reencode = (input("Copy Video instead of Reencode? (y/N)").lower()=='y')
if not bit_check and not skip_reencode and not (cq or q):
    bitrate = (input("Target Bitrate? "), input("Max Bitrate? (0 for CBR) "))
    if bitrate[1] == '0': bitrate = ('0', "AUTO")
if not ((q or cq) or skip_reencode or bitrate[0].lower() == "auto" or bitrate[1].lower() == "auto"):
    cq = int(input("Target Quality? -crf (1-51) "))

if not b10_check and not skip_reencode: b10_mode = yn_bool(input("10b Encoding? (y/N) "))

if not rn_check: rename = yn_bool(input("Rename? (y/N) "))
rename_decision = rn_check and rename
if not rp_check and rename_decision and not movie: replace_periods = yn_bool(input("Replace Periods? (y/N) "))
if rename_decision:
    if not show and not movie: show = input("Show Title? ")
    if not year: year = int(input("Release Year? "))
    if not season and not movie: season = int(input("Season Number? "))
if not es_check and not skip_subtitles:
    external_subtitles = yn_bool(input("External Subtitles? (y/N) "))
    if external_subtitles: lang = input("Language code (before .srt extension, default eng) ")

# ruler for getting indexes
if index_checks != 3 and rename_decision and not movie:
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


# Loop through each item in the directory
for item in os.listdir(cwd):
    if movie_path and movie: item = movie_path
    item_path = os.path.join(cwd, item)  # Full path to the item
    # Check if the item is a video file, if not check next file
    if item[-3:] not in video_formats: continue
    item_title = item[:-4]
    ep_title = ""
    print("File:", item_title)
    nth_item = 0  # any time nth_item != 0 the current file contains multiple episodes

    if rename_decision and not movie:
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
        output_item = f"{show} ({year}) S{season:02d}E{ep:02d}" \
                      f"{f'-{nth_item:02d}' if (item_title[ep_i + 3] == '-' and ep_i != 0) else ''} {ep_title}"
    elif movie and rename_decision:
        output_item = f"{movie} ({year})"
    else:
        output_item = item_title
    print(f"Reencoding {item} to {output_item}.mp4 ...")

    str_loglevel = ' -loglevel quiet -stats' if pretty else ''
    str_overwrite = ' -' + overwrite_mode if ov_check else ''
    str_tune = f" -tune animation"

    cmd = f"ffmpeg{str_loglevel}{str_overwrite} -hide_banner {'-hwaccel auto' if gpu else ''} -i \"./{item}\""

    if has_art: cmd = f"{cmd} -i \"{art_path}\" -map 1 -c:v:1 copy {art_path[-3:]} -disposition:v:1 attatched_pic"
    if external_subtitles:
        cmd = f"{cmd} -i \"./{item_title}{'.'+lang if lang else ''}.srt\""
        str_subtitlemapping = f" -map {'2' if has_art else '1'}"
    if skip_reencode:
        cmd = f"{cmd} -map 0:v{str_subtitlemapping} -gpu 0 -c:v:0 copy"
    else:
        str_profile = f"main{'10' if b10_mode else ''}"
        str_maxbitrate = (" -maxrate " + bitrate[1]) if bitrate[1].lower() != 'auto' else f' -maxrate {bitrate[0]}'
        if gpu: str_bitmode = "p010le" if b10_mode else "yuv420p"
        else:   str_bitmode = f"yuv420p{'10le' if b10_mode else ''}"

        cmd = f"{cmd} -map 0:v{':0'if broken_artwork else ''}{str_subtitlemapping} -c:v:0 {'hevc_nvenc' if gpu else 'libx265'}" \
              f" -profile:v {str_profile} -level {fflvl} -preset {'p6' if gpu else 'fast'} -pix_fmt {str_bitmode}"
        if not lossless:
            if bitrate[0].lower() != "auto":
                cmd = f"{cmd} -b:v {bitrate[0]}{str_maxbitrate}"
                if bitrate[1][-1].lower() == 'k': cmd = f"{cmd} -bufsize {int(bitrate[1][:-1])+1000}K"
                elif bitrate[1][-1].lower() == 'm': cmd = f"{cmd} -bufsize {int(bitrate[1][:-1])+1}M"
            if q > 0 and gpu: # -gpu -q
                cmd = f"{cmd} -rc vbr -qp {q} -qmin {q - 3} -qmax {q + 3}"
            elif q > 0 and not gpu:
                cmd = f"{cmd} -rc vbr -crf {q}"
            elif cq > 0 and gpu: # -gpu -cq
                cmd = f"{cmd} -rc vbr -qp {cq} -qmax {cq + 3}"
            elif cq > 0 and not gpu: # -c -cq
                cmd = f"{cmd} -rc vbr -crf {cq}"
            elif bitrate[1].lower() == "auto" and cq+q <= 0: # -b [int]
                cmd = f"{cmd} -rc cbr{' -qp -1' if gpu else ''}"
            # elif gpu: # -gpu
            #     cmd = f"{cmd} -rc vbr -qp 18 -qmax 20"
            # else:
            #     cmd = f"{cmd} -rc vbr -crf 20"
            cmd = f"{cmd}{str_tune if tune_animation else ''} -aq-mode 2"
        else: cmd = f"{cmd} -x265-params lossless=1"
        
        if lang:
            cmd = f"{cmd} -map 0:a:m:language:{lang} -c:a copy"
        else:
            cmd = f"{cmd} -map 0:a -c:a copy"

    if not skip_subtitles:
        if not lang:
            cmd = f"{cmd}{' -map 0:s' if not str_subtitlemapping else ''} -c:s {subenc}"
        elif not external_subtitles:
            cmd = f"{cmd} -map 0:s:m:language:{lang}"
        else:
            cmd = f"{cmd} -metadata:s:s:0 language={lang if lang else 'eng'} -c:s {subenc}"

    if ep_title: cmd = f"{cmd} -metadata title=\"{ep_title}\""
    elif movie:  cmd = f"{cmd} -metadata title=\"{movie}\""
    if show:     cmd = f"{cmd} -metadata show=\"{show}\""
    if season:   cmd = f"{cmd} -metadata season={season}"
    if ep:       cmd = f"{cmd} -metadata episode={ep}"
    if year:     cmd = f"{cmd} -metadata year={year}"

    cmd = f"{cmd} -f mp4 \"{os.getcwd()}/Reencode/{output_item}.mp4\""
    print(cmd)
    if not debug:
        subprocess.call(cmd)

    # if relying on ep to be accurate
    if not ep_i and rename_decision:
        if nth_item:
            ep = nth_item + 1
        else:
            ep = ep + 1
    if movie: break

if "-cp" in argv:
    subprocess.call(f"python {os.path.dirname(os.path.abspath(__file__))}/compare.py")