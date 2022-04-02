# Video Converter (ICloud Built In Transfer)

This script converts your video files (3GP, MKV, WMV, MP4, AVI) to MP4 and transfers it directly to your ICloud.
.

## Getting Started

Before starting, install the required Python packages using the requirements.txt file included.
Run this command within the folder (and I do recommend creating a virtual environment before this step):

$ pip install -r requirements.txt

The script automatically transfers the converted files to your ICloud folder, so having an Apple account it's a must.
It would be helpful to make sure you have enogh space available before running as well. Keep in mind that video files are large and the script don't previously check the amount
of space required to complete the transfer.

### Instructions

No installation necessary, the only requirements is that the script and the files to be converted necessary have to be inside the same folder.
All the video files inside that folder will be converted. Just run the script inside the folder containing the files to be converted using the command:

$ python converter.py

First thing, the script will ask your credentials to connect to the ICloud service.
It will then create an output folder to store the output files. After completing each conversion, the final file will be transferred to the ICloud.

