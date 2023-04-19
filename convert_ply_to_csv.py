import argparse
import glob
from pathlib import Path
import sys
from pyntcloud import PyntCloud
import os

parser = argparse.ArgumentParser(
                    prog = 'Ply converter',
                    description = 'This program converts all .ply files in the folder to .csv', 
                    #usage="python convert_ply_to_csv.py -f path\\to\\your\\ply\\folder -s path\\to\\savefolder", 
                    epilog="Don't forget to: pip install requirements.txt", add_help=False)
parser.add_argument("-f", dest="folder", required=True, type=str)
parser.add_argument("-s", dest="folder_to_save", required=True, type=str)
parser.add_argument('-h', action='help', default=argparse.SUPPRESS,
                    help='Show this help message and exit.')
try: 

    args = parser.parse_args()
except Exception as e:
    print(e)

def main(): 
    try:
        folder_from = args.folder
        folder_to_save =  args.folder_to_save
        csv = ".csv"
        if not Path(folder_to_save).exists(): 
            os.mkdir(folder_to_save)

        for file in glob.glob(folder_from + "*.ply"):
            cloud = PyntCloud.from_file(file)
            file_path = Path(file)
            file_name = file_path.stem
            cloud.points.to_csv(f"{folder_to_save}{file_name}{csv}", index=False)
    except Exception as e: 
        print(f"Exception occured: {e}")



if __name__ == "__main__": 
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    main()