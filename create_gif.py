import os
import subprocess
import argparse

def create_gif(input_folder, output_gif, fps=10, size=None):
    """
    Create a GIF from a folder of images using FFmpeg, preserving original colors.
    
    Parameters:
    input_folder (str): Path to folder containing image sequences
    output_gif (str): Path for output GIF file
    fps (int): Frames per second for the output GIF
    size (str): Optional size parameter (e.g., '640x480'). If None, original size is kept
    """
    # Ensure input folder exists
    if not os.path.exists(input_folder):
        raise ValueError(f"Input folder '{input_folder}' does not exist")
    
    # Build the FFmpeg command
    command = [
        'ffmpeg',
        '-y',  # Overwrite output file if it exists
        '-f', 'image2',  # Force image2 format
        '-framerate', str(fps),
        '-i', os.path.join(input_folder, '%*.jpg')  # Input pattern for numbered images
    ]
    
    # Add size parameter if specified
    if size:
        command.extend(['-s', size])
    
    # Add output options without color palette generation
    command.extend([
        '-gifflags', '+transdiff',  # Use transparency optimization
        '-filter:v', 'fps=fps=' + str(fps),  # Ensure consistent frame rate
        output_gif
    ])
    
    try:
        # Run FFmpeg command
        subprocess.run(command, check=True, capture_output=True)
        print(f"Successfully created GIF: {output_gif}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating GIF: {e.stderr.decode()}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a GIF from a folder of images using FFmpeg')
    parser.add_argument('input_folder', help='Path to folder containing image sequences')
    parser.add_argument('output_gif', help='Path for output GIF file')
    parser.add_argument('--fps', type=int, default=10, help='Frames per second (default: 10)')
    parser.add_argument('--size', help='Output size in format WxH (e.g., 640x480)')
    
    args = parser.parse_args()
    
    create_gif(
        input_folder=args.input_folder,
        output_gif=args.output_gif,
        fps=args.fps,
        size=args.size
    )