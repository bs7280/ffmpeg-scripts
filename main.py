from doctest import OutputChecker
import subprocess
import argparse
import os
from collections import Counter

def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def seconds_to_hhmmss(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def screenshot_at_time(video_path, seconds, out_fname='frames/frame.png'):
    formatted_time = seconds_to_hhmmss(seconds)
    print(formatted_time)
    print(f"Getting screenshot from: {video_path}")
    # frames/frame{i:03}.png'
    run_cmd(f'ffmpeg.exe -i "{video_path}" -ss {formatted_time} -vframes 1 -y f{out_fname}')

def make_gif(video_path, out_filename):
    cmd_video_seconds = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{video_path}"'
    video_length = run_cmd(cmd_video_seconds)
    video_length = float(video_length.stdout.strip())

    # Remove existing frames
    run_cmd("rm frames/*")

    #for i,s in enumerate(range(10, int(video_length), int(video_length/15))):
    #    formatted_time = seconds_to_hhmmss(s)
    #    print(formatted_time)

    #    print(f"Getting screenshot from: {video_path}")
   #     run_cmd(f'ffmpeg.exe -i "{video_path}" -ss {formatted_time} -vframes 1 -y frames/frame{i:03}.png')
    
    seconds = int(30 * video_length / 15)
    _cmd = f"""ffmpeg -i "{video_path}" -vf "select='not(mod(n,{seconds}))',setpts='N/(30*TB)'" -s 1280x720 -f image2 frames/frame%03d.png"""
    print(_cmd)
    run_cmd(_cmd)

    # Create parent folder if it does not exist
    create_parent_folders(out_filename)
    os.path.join(out_filename)
    cmd_make_gif = f'magick convert -delay 40 -loop 0 frames/frame*.png {out_filename}'
    run_cmd(cmd_make_gif)

def find_videos_in_folder(folder_path):
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv']  # Add more extensions as needed
    video_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            _, extension = os.path.splitext(file)
            if extension.lower() in video_extensions:
                video_files.append(os.path.abspath(os.path.join(root, file)))

    return video_files

def create_parent_folders(path):
    parent_folder = os.path.dirname(path)

    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)

### Argparser entrypoints

def process_file(filename, out_filename):
    # Add your logic for processing a single file here
    print(f"Processing file: {filename} ")
    print(f"Saving to: {out_filename}")

    make_gif(filename, out_filename)    

def process_folder(folder, output_folder):
    # Add your logic for processing a folder here
    print(f"Processing folder: {folder}")
    
    if not os.path.isdir(output_folder):
        raise ValueError("Output path must be a directory when processing a folder of videos")

    video_paths = find_videos_in_folder(folder)

    for video in video_paths[3:]:
        base_name = os.path.basename(video)
        print(f"Starting {base_name}")
        #filename, ext = os.path.splitext(base_name)

        out_filename = base_name.replace(' ', '_')

        out_filepath = os.path.join(output_folder, out_filename)

        make_gif(video, out_filepath)

def main():
    parser = argparse.ArgumentParser(description="Process files or folders.")
    parser.add_argument("command", choices=["gif"], help="Specify the command to execute.")
    parser.add_argument("target", help="Specify the target file or folder.")
    parser.add_argument("-o", "--output", required=True, help="Specify the output file.")

    args = parser.parse_args()

    if args.command == "gif":
        target_path = os.path.abspath(args.target)
        output_path = os.path.abspath(args.output)

        if os.path.isfile(target_path):
            process_file(target_path, output_path)
        elif os.path.isdir(target_path):
            process_folder(target_path, output_path)
        else:
            print(f"Error: {target_path} is neither a file nor a folder.")

if __name__ == "__main__":
    main()

    
    #

