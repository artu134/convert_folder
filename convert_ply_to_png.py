import os
import argparse
import pyvista as pv
import numpy as np
from PIL import Image


def remove_background(image, threshold=80):
    image = image.convert("RGBA")  # Ensure the image is in RGBA mode
    image_array = np.array(image)
    
    r, g, b, a = np.rollaxis(image_array, axis=-1)
    mask = (r >= threshold) & (g >= threshold) & (b >= threshold)
    image_array[~mask, 3] = 0

    return Image.fromarray(image_array)


def crop_center(image, roi_size):
    width, height = image.size
    left = (width - roi_size[0]) // 2
    top = (height - roi_size[1]) // 2
    right = (width + roi_size[0]) // 2
    bottom = (height + roi_size[1]) // 2

    return image.crop((left, top, right, bottom))



def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Convert PLY files to grayscale 3D model images")
    parser.add_argument("input_dir", help="Directory containing PLY files")
    parser.add_argument("output_dir", help="Directory to save grayscale 3D model images")
    parser.add_argument("-r", "--resolution", default=512, type=int, help="Output image resolution (default: 512)")
    parser.add_argument("-t", "--threshold", default=75, type=int, help="Background removal threshold (default: 75)")
    parser.add_argument("--roi_width", default=200, type=int, help="ROI width (default: 200)")
    parser.add_argument("--roi_height", default=200, type=int, help="ROI height (default: 200)")
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Load each PLY file in the input directory and save a grayscale 3D model image
    for filename in os.listdir(args.input_dir):
        if filename.endswith(".ply"):
            # Load PLY file into PyVista point cloud object
            pcd = pv.read(os.path.join(args.input_dir, filename))

            # Convert point cloud to grayscale 3D model image
            plotter = pv.Plotter(off_screen=True)
            plotter.add_mesh(pcd, color="white", render_points_as_spheres=True, point_size=2)
            plotter.camera_position = [(0, 0, 10), (0, 0, 0), (0, 1, 0)]
           # plotter.show(auto_close=False)
            output_file = os.path.join(args.output_dir, os.path.splitext(filename)[0] + ".png")
            plotter.screenshot(output_file, return_img=False)

           # Convert image to grayscale
            image = Image.open(output_file).convert("L")

            # Remove background
            image = remove_background(image, args.threshold)

            # Add ROI
            roi_size = (args.roi_width, args.roi_height)
            image = crop_center(image, roi_size)

            # Save processed image
            image.save(output_file)

if __name__ == "__main__":
    main()
