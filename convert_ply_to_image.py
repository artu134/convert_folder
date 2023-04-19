import os
import argparse
import pyntcloud
import matplotlib.pyplot as plt
import numpy as np 
import open3d as o3d

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Convert PLY files to PNG images")
    parser.add_argument("input_dir", help="Directory containing PLY files")
    parser.add_argument("output_dir", help="Directory to save PNG images")
    parser.add_argument("-f", "--format", default="png", help="Output image format (default: png)")
    parser.add_argument("-r", "--resolution", default=512, type=int, help="Output image resolution (default: 512)")
    args = parser.parse_args()

       # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Load each PLY file in the input directory and save a grayscale 3D model image
    for filename in os.listdir(args.input_dir):
        if filename.endswith(".ply"):
            # Load PLY file into Open3D point cloud object
            pcd = o3d.io.read_point_cloud(os.path.join(args.input_dir, filename))

            # Convert point cloud to grayscale 3D model image
            xyz = np.asarray(pcd.points)
            colors = np.asarray(pcd.colors)
            colors = (colors * 255).astype(np.uint8)
            image = np.zeros((args.resolution, args.resolution), dtype=np.uint8)
            for i in range(len(xyz)):
                x, y, z = xyz[i]
                r, g, b = colors[i]
                u = int((x / z + 0.5) * args.resolution)
                v = int((-y / z + 0.5) * args.resolution)
                if u >= 0 and u < args.resolution and v >= 0 and v < args.resolution:
                    image[v, u] = (r + g + b) // 3

            # Save grayscale 3D model image as PNG file
            output_file = os.path.join(args.output_dir, os.path.splitext(filename)[0] + ".png")
            image = Image.fromarray(image)
            image.save(output_file)

if __name__ == "__main__":
    main()
