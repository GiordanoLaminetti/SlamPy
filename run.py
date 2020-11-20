import os
import cv2
import numpy as np
import slampy
import argparse
from tqdm import tqdm
from utils import create_dir, save_depth, save_pose, load_images_KITTI


def run(args):
    """Run SLAM system for each frame in the dataset and save depths and poses.

    Args:
        args: command line arguments
    """
    setting_file = args.settings
    if not os.path.exists(setting_file):
        raise ValueError(f"Cannot find setting file at {setting_file}")

    app = slampy.System(setting_file, slampy.Sensor.MONOCULAR)

    # TODO: generic loader an not KITTI one
    image_filenames, timestamps = load_images_KITTI(args.dataset)
    num_images = len(image_filenames)

    dest_depth = os.path.join(args.dest, "depth")
    dest_pose = os.path.join(args.dest, "pose")

    create_dir(dest_depth)
    create_dir(dest_pose)

    states = []
    with tqdm(total=num_images) as pbar:
        for idx, image_name in enumerate(image_filenames):
            # TODO: it is image loader duty to provide correct images
            image_name = image_name.replace(".png", ".jpg")
            image = cv2.imread(image_name)
            if image is None:
                raise ValueError(f"failed to load image {image_name}")

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            state = app.process_image_mono(image, timestamps[idx])

            # NOTE: we buid a default invalid depth, in the case of system failure
            h, w = image.shape[:2]
            depth = np.full((h, w), -1, dtype=np.float32)
            if state == slampy.State.OK:
                depth = app.get_depth()

            states.append(state)

            name = os.path.splitext(os.path.basename(image_name))[0]
            depth_path = os.path.join(dest_depth, name)
            save_depth(depth_path, depth)

            # NOTE: add code to dump the pose
            pbar.update(1)

    # NOTE: final dump of log.txt file
    with open(os.path.join(args.dest, "log.txt"), "w") as f:
        for i, state in enumerate(states):
            f.write(f"{i}: {state}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the SLAM system and save, at each frame, the current depth and pose"
    )
    parser.add_argument("--dataset", type=str, required=True, help="path to dataset")
    parser.add_argument(
        "--settings", type=str, default="settings.yaml", help="which configuration?"
    )
    parser.add_argument(
        "--dest", type=str, default="results", help="where do we save artefacts?"
    )

    args = parser.parse_args()
    run(args)
