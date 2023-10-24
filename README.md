# Media Tools

 Media tools for reencoding TV/Movie media

## Why would anyone use this?
 I frequently find media either only available in x264, not encoded with 10bit, or just having larger file sizes or a higher bitrate than needed. With a large library this tool makes it easy to format entire series or movies.

# Requirements

 FFmpeg
 Python

# Usage

## Recommended Bitrate and Quality for x265 encoding

| res             | bitrate  | qval  |
| --------------- | -------- | ----- |
| 720p            | 1080p    | 18-20 |
| 1080p animation | 1-3mbps  | 20-25 |
| 1080p           | 2-4mbps  | 20-25 |
| 1440p           | 4-6mbps  | 20-25 |
| 4K              | 6-10mbps | 13-18 |

## reencode.py arguments

### IF USING -P AND GETTING 0 BYTE FILES REMOVE -P AND CHECK FFMPEG OUTPUT AND SET SETTINGS ACCORDINGLY

### raw data passed directly to ffmpeg

### MetaData


| argument   | description  | raw data |
| ---------- | ------------ | -------- |
| `-m [str]` | Movie Name   | &#9745;  |
| `-t [str]` | Show Title   | &#9745;  |
| `-s [int]` | Season       | &#9745;  |
| `-y [int]` | Release Year | &#9745;  |

### FFmpeg settings

| argument    | description                 | raw data |
| ----------- | --------------------------- | -------- |
| `-c [int]`  | Thread count                | &#9744;  |
| `-gpu`      | use hevc_nvenc over libx265 | &#9744;  |
| `-p`        | Pretty Output               | &#9744;  |
| `-r [Y/n]`  | Rename Files?               | &#9744;  |
| `-rp [Y/n]` | Replace Periods             | &#9744;  |

### Video

| argument                   | description                                                                                                       | raw data |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------- | -------- |
| `-sv`                      | Skip Video Encoding                                                                                               | &#9744;  |
| `-t[a/f]`                  | Tune Animation/Film                                                                                               | &#9744;  |
| `-lv [encoding lvl]`       | Encoding level, `4.0`:720p60/1080p30, `4.1`:1080p60, `5.0`:4k30, `5.1`:4k60                                       | &#9745;  |
| `-b [int][k/m] [int][k/m]` | Bitrate Min/Max, leave blank for automatic bitrate                                                                | &#9745;  |
| `-10b [Y/n]`               | 10 Bit Mode                                                                                                       | &#9744;  |
| `-cq [int]`                | Constant Bitrate Quality (translates to `-rc vbr -crf [cq]` with cpu or `-rc vbr -cq [cq] -qmax [cq+3]` with gpu) | &#9745;  |
| `-srt [Y/n]`               | External Subtitles                                                                                                | &#9744;  |
| `-l <eng>`                 | Subtitle Language Abbreviation for External subtitles or omitting extra subtitle streams                          | &#9745;  |
| `-ss`                      | Skip Subtitle Encoding                                                                                            | &#9744;  |
| `-se <encoding>`           | Change subtitle Encoding                                                                                          | &#9745;  |
| `-a[rt] <path>`            | Specify path to art                                                                                               | &#9745;  |
| `-o`                       | Overwrite Mode                                                                                                    | &#9744;  |
| `-mep`                     | Multiple Episodes in file used for title formatting                                                               | &#9744;  |
| `-ep <int>`                | Episode \'E\' Index                                                                                               | &#9744;  |
| `-ts <int>`                | Episode Title Start Index                                                                                         | &#9744;  |
| `-te [int]`                | Index of space after Title, used to remove common metadata suffixes, 0 for no suffix                              | &#9744;  |

### DEPRECATED/USED WITH NVENC

| argument   | description                                                          | raw data |
| ---------- | -------------------------------------------------------------------- | -------- |
| `-q [int]` | Quality (translates to `-rc vbr -cq [cq] -qmin [cq-3] -qmax [cq+3]`) | &#9745;  |
