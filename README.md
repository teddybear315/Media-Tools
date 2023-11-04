# Media Tools

 Media tools for reencoding TV/Movie media

 For ease of use or if having problems with compare.py running, add this project to your PATH variable and create script files along the lines of `python <install path>/<python script>.py`

 for compare please avoid the name "compare"

## Why would anyone use this?

 I frequently find media either only available in x264, not encoded with 10bit, or just having larger file sizes or a higher bitrate than needed. With a large library this tool makes it easy to format entire series or movies.

## Requirements

 FFmpeg

 Python

## Usage

### Recommended Bitrate and Quality for x265 encoding

| res             | bitrate  | qval  |
| --------------- | -------- | ----- |
| 720p            | 1-2mbps  | 16-20 |
| 1080p animation | 1-3mbps  | 20-25 |
| 1080p           | 2-4mbps  | 18-25 |
| 1440p           | 4-6mbps  | 16-23 |
| 4K              | 6-10mbps | 13-18 |

### Recommended Encoding Levels for x265 encoding

| res       | fps | level |
| --------- | --- | ----- |
| 720×480   | 40  | 3     |
| 1280×720  | 30  | 3.1   |
| 960×540   | 60  | 3.1   |
| 720×480   | 80  | 3.1   |
| 1280×720  | 60  | 4     |
| 1920×1080 | 30  | 4     |
| 1920×1080 | 60  | 4.1   |
| 3840×2160 | 30  | 5     |
| 3840×2160 | 60  | 5.1   |

## reencode.py arguments

IF USING -P AND GETTING 0 BYTE FILES REMOVE -P AND CHECK FFMPEG OUTPUT AND SET SETTINGS ACCORDINGLY

raw data passed directly to ffmpeg

capital letter in \[y/n\] default

### MetaData

| argument    | description  | raw data |
| ----------- | ------------ | -------- |
| `-m [str]`  | Movie Name   | &#9745;  |
| `-mp [str]` | Movie Path   | &#9745;  |
| `-t [str]`  | Show Title   | &#9745;  |
| `-s [int]`  | Season       | &#9745;  |
| `-y [int]`  | Release Year | &#9745;  |

### FFmpeg settings

| argument    | description                                                                               | raw data |
| ----------- | ----------------------------------------------------------------------------------------- | -------- |
| `-c [int]`  | Thread count                                                                              | &#9744;  |
| `-cp`       | Compare Filesizes after completion (please complete "ease of use" setup for this to work) | &#9744;  |
| `-gpu`      | use hevc_nvenc over libx265                                                               | &#9744;  |
| `-p`        | Pretty Output                                                                             | &#9744;  |
| `-r [Y/n]`  | Rename Files?                                                                             | &#9744;  |
| `-rp [Y/n]` | Replace Periods                                                                           | &#9744;  |

### Video

| argument                   | description                                                                                                               | raw data |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------- | -------- |
| `-sv`                      | Skip Video Encoding                                                                                                       | &#9744;  |
| `-ll`                      | Lossless conversion, used mainly for heavily compressed x264 conversion                                                   | &#9744;  |
| `-ta`                      | Tune Animation                                                                                                            | &#9744;  |
| `-lv [encoding lvl]`       | Encoding level, `4.0`:720p60/1080p30, `4.1`:1080p60, `5.0`:4k30, `5.1`:4k60                                               | &#9745;  |
| `-b [int][k/m] [int][k/m]` | Bitrate Min/Max, leave blank for automatic bitrate                                                                        | &#9745;  |
| `-10b [Y/n]`               | 10 Bit Mode                                                                                                               | &#9744;  |
| `-cq [int]`                | Constant Bitrate Quality (translates to `-rc vbr -crf [cq]` with cpu or `-rc vbr -cq [cq] -qmax [cq+3]` with gpu)         | &#9745;  |
| `--broken_artwork`         | Only use if artwork stream is broken, or you want to discard all video streams other than 0                               | &#9744;  |
| `--no_audio_lang`          | Used if srt file has language and audio doesnt, if not using external srt file dont include -l, sets audio language to -l | &#9744;  |
| `-srt [Y/n]`               | External Subtitles                                                                                                        | &#9744;  |
| `-l <eng>`                 | Subtitle Language Abbreviation for External subtitles or omitting extra subtitle streams                                  | &#9745;  |
| `-ss`                      | Skip Subtitle Encoding                                                                                                    | &#9744;  |
| `-se <encoding>`           | Change subtitle Encoding                                                                                                  | &#9745;  |
| `-a[rt] <path>`            | Specify path to art                                                                                                       | &#9745;  |
| `-o`                       | Overwrite Mode                                                                                                            | &#9744;  |
| `-mep`                     | Multiple Episodes in file used for title formatting                                                                       | &#9744;  |
| `-ep <int>`                | Episode \'E\' Index                                                                                                       | &#9744;  |
| `-ts <int>`                | Episode Title Start Index                                                                                                 | &#9744;  |
| `-te [int]`                | Index of space after Title, used to remove common metadata suffixes, 0 for no suffix                                      | &#9744;  |

### DEPRECATED/USED WITH NVENC

| argument   | description                                                          | raw data |
| ---------- | -------------------------------------------------------------------- | -------- |
| `-q [int]` | Quality (translates to `-rc vbr -cq [cq] -qmin [cq-3] -qmax [cq+3]`) | &#9745;  |
