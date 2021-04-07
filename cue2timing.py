import sys
import os
import time
from pathlib import Path
from cueparser import CueSheet
from datetime import datetime

def write_timing_file(timings):
    out = "a.out"
    out = Path(sys.argv[1]).stem + ".txt"
    print(out)
    lines = []
    for idx, time in enumerate(timings):
        lines.append(f"{time}\t{time}\t{idx+1}\n")
    with open(out, "w") as f:
        f.writelines(lines)

def convert_time(timestamps):
    converted = []
    for timestamp in timestamps:
        sum = 0
        min = timestamp.minute
        sum += min * 60
        sum += timestamp.second
        sum += timestamp.microsecond / 1_000_000
        converted.append(f"{sum:.6f}")
    return converted

def convert_file(cuefile):
    if not os.path.isfile(cuefile):
        print("Error: argument needs to be a file")
        return
    cuesheet = CueSheet()
    cuesheet.setOutputFormat("%title%", "%offset%")
    with open(cuefile, "r") as f:
        cuesheet.setData(f.read())
    cuesheet.parse()
    timestamps = []
    for track in cuesheet.tracks:
        timestamps.append(datetime.strptime(str(track), "%M:%S:%f"))
    converted = convert_time(timestamps)
    write_timing_file(converted)

def main():
    if len(sys.argv) < 2:
        print("Error: need to supply a file argument")
        return
    cuefile = sys.argv[1]
    convert_file(cuefile)

if __name__ == "__main__":
    main()