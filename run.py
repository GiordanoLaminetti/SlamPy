import os
import cv2
import numpy as np
import slampy
import argparse
import yaml
from tqdm import tqdm
from utils import *
from kitti_odometry import KittiEvalOdom


def run(args):
    """Run SLAM system for each frame in the dataset and save depths and poses.

    Args:
        args: command line arguments
    """
    setting_file = args.settings
    if not os.path.exists(setting_file):
        raise ValueError(f"Cannot find setting file at {setting_file}")
    if args.pose_id < -1:
        raise ValueError(f"Pose index must be -1 or >0")

    with open(args.settings) as fs:
        settings_yalm = yaml.safe_load(fs)
        print("\nAlgorithm " + settings_yalm["SLAM.alg"] + " has been set\n")

    print("Dataset selected: " + os.path.basename(args.dataset) + "\n")

    app = slampy.System(setting_file, slampy.Sensor.MONOCULAR)

    print("\n")

    # TODO: generic loader an not KITTI one

    if args.data_type == "TUM":
        image_filenames, timestamps = load_images_TUM(args.dataset, "rgb.txt")
    elif args.data_type == "KITTI_VO":
        image_filenames, timestamps = load_images_KITTI_VO(args.dataset)
    elif args.data_type == "OTHERS":
        image_filenames, timestamps = load_images_OTHERS(args.dataset)

    num_images = len(image_filenames)

    dest_depth = os.path.join(args.dest, "depth")
    dest_pose = os.path.join(args.dest, "pose")

    create_dir(dest_depth)
    create_dir(dest_pose)

    states = []
    errors = []

    with tqdm(total=num_images) as pbar:
        for idx, image_name in enumerate(image_filenames):
            # TODO: it is image loader duty to provide correct images
            # image_name = image_name.replace(".png", ".jpg")
            image = cv2.imread(image_name)
            if image is None:
                raise ValueError(f"failed to load image {image_name}")

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            state = app.process_image_mono(image, timestamps[idx])

            # NOTE: we buid a default invalid depth, in the case of system failure
            if state == slampy.State.OK:
                depth = app.get_depth()
                pose_past_frame_to_current = app.get_pose_to_target(
                    precedent_frame=args.pose_id
                )
                name = os.path.splitext(os.path.basename(image_name))[0]

                depth_path = os.path.join(dest_depth, name)
                save_depth(depth_path, depth)

                pose_path = os.path.join(dest_pose, name)
                save_pose(pose_path, pose_past_frame_to_current)

                curr_pose = app.get_pose_to_target(-1)
                if curr_pose is not None:
                    save_pose_txt(args, name, curr_pose)

                if args.is_evaluate_depth:
                    gt_file_path = os.path.join(args.gt_depth, "{}.png".format(name))
                    err = get_error(args, name, depth, gt_file_path)
                    errors.append(err)

            states.append(state)
            pbar.update(1)

        if args.is_evaluate_depth:
            mean_errors = np.array(errors).mean(0)
            save_results = os.path.join(args.dest, "results.txt")
            save_depth_err_results(save_results, "mean values", mean_errors)

    # NOTE: final dump of log.txt file
    with open(os.path.join(args.dest, "log.txt"), "w") as f:
        for i, state in enumerate(states):
            f.write(f"{i}: {state}\n")

    if args.is_evaluate_pose:
        print("Begin to evaluate predicted pose")
        evaluate_pose(args)
        eval_tool = KittiEvalOdom()
        eval_tool.eval(args)


parser = argparse.ArgumentParser(
    description="Run the SLAM system and save, at each frame, the current depth and pose"
)

parser.add_argument(
    "--dataset",
    type=str,
    default="/media/Datasets/KITTI_VO/dataset/sequences/10",
    help="path to dataset",
)
parser.add_argument(
    "--settings",
    type=str,
    default="./settings_kitty.yaml",
    help="which configuration?",
)
parser.add_argument(
    "--dest",
    type=str,
    default="./results_kitty_vo_10",
    help="where do we save artefacts?",
)
parser.add_argument(
    "--pose_id",
    type=int,
    default=-1,
    help="between which frames do you want compute the pose? If pose_id==-1, get the pose between 0->T; \
        if pose_id >0, compute the pose between T-pose_id->T \
        For instance, if pose_id=2 then compute the pose between T-2->T",
)
parser.add_argument(
    "--is_evaluate_depth",
    default=False,
    action="store_true",
    help="If set, will evalute the orb depth with the gt files ",
)

parser.add_argument(
    "--is_evaluate_pose",
    default=False,
    action="store_true",
    help="If set, will evalute the orb pose with the gt files",
)

parser.add_argument(
    "--is_bash",
    # default=True,
    action="store_true",
    help="If set, means use bash shell to evaluate",
)

parser.add_argument(
    "--data_type",
    type=str,
    help="which dataset type",
    default="KITTI_VO",
    choices=["TUM", "KITTI_VO", "KITTI", "OTHERS"],
)

parser.add_argument(
    "--gt_depth",
    type=str,
    help="the gt depth files of the dataset",
    default="/media/Datasets/KITTI_VO_SGM/10/depth",
)
# /media/Datasets/TUM/freiburg3_convert/depth

parser.add_argument(
    "--gt_pose_dir",
    type=str,
    help="each frame's gt pose file, saved as previous to current, and filename as current.npy",
    default="/media/Datasets/KITTI_VO_SGM/10/npy_pose",
)

parser.add_argument(
    "--gt_pose_txt",
    type=str,
    help="this is the gt pose file provided by kitty or tum.",
    default="/media/Datasets/KITTI_VO/dataset/poses/10.txt",
)

parser.add_argument(
    "--align",
    type=str,
    choices=["scale", "scale_7dof", "7dof", "6dof"],
    default="7dof",
    help="alignment type",
)

parser.add_argument(
    "--named", type=str, help="the names for saving pose", default="kitty_vo_10"
)


if __name__ == "__main__":

    args = parser.parse_args()
    run(args)
