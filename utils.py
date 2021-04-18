from datetime import datetime
import time
import numpy as np
import os
import glob
import cv2
from PIL import Image


def load_images_KITTI(path_to_sequence):
    """Return the sequence of the images found in the path and the corrispondent timestamp

    Args:
        path_to_sequence : the sequence in witch we can found the image sequences

    Returns :
        two array : one contains the sequence of the image filename and the second the timestamp in whitch they are acquired

    """
    timestamps = []
    t0 = None
    with open(os.path.join(path_to_sequence, "timestamps.txt")) as times_file:
        for line in times_file:
            if len(line) > 0:
                line = line[:-4]
                if t0 is None:
                    t0 = datetime.strptime(line, "%Y-%m-%d %H:%M:%S.%f")
                t1 = datetime.strptime(line, "%Y-%m-%d %H:%M:%S.%f")
                difference = t1 - t0
                timestamps.append(
                    difference.seconds + difference.microseconds / 1000000
                )

    return [
        os.path.join(path_to_sequence, "data", str(idx).zfill(10) + ".png")
        for idx in range(len(timestamps))
    ], timestamps


def load_images_TUM(path_to_sequence, file_name):
    """Return the sequence of the images found in the path and the corrispondent timestamp

    Args:
        path_to_sequence : the sequence in witch we can found the image sequences

    Returns:
        two array : one contains the sequence of the image filename and the second the timestamp in whitch they are acquired

    """
    timestamps = []
    rgb_filenames = []
    with open(os.path.join(path_to_sequence, file_name)) as times_file:
        for line in times_file:
            if len(line) > 0 and not line.startswith("#"):
                t, rgb = line.rstrip().split(" ")[0:2]
                rgb_filenames.append(rgb)
                timestamps.append(float(t))

    return [os.path.join(path_to_sequence, name) for name in rgb_filenames], timestamps


def compute_errors(gt, pred):
    """Computation of error metrics (abs rel,sq rel, rmse, rmse log) between predicted and ground truth depths
    From https://github.com/mrharicot/monodepth

    Args:
        gt : an array with the ground truth values
        pred : an array with the predicted values

    Returns:
        abs_rel,sq_rel,rmse,rmse_log : the error

    """
    """Computation of error metrics between predicted and ground truth depths
    """
    thresh = np.maximum((gt / pred), (pred / gt))
    a1 = (thresh < 1.25).mean()
    a2 = (thresh < 1.25 ** 2).mean()
    a3 = (thresh < 1.25 ** 3).mean()

    rmse = (gt - pred) ** 2
    rmse = np.sqrt(rmse.mean())

    rmse_log = (np.log(gt) - np.log(pred)) ** 2
    rmse_log = np.sqrt(rmse_log.mean())

    abs_rel = np.mean(np.abs(gt - pred) / gt)

    sq_rel = np.mean(((gt - pred) ** 2) / gt)

    return abs_rel, sq_rel, rmse, rmse_log, a1, a2, a3


def convert_scale(points, gt_depth):
    """convert the scale of the predictions to the gt

    Args:
        points: the predictions depth
        gt_filename: the gt references filename

    Returns: the ratio between the predictions and the gt
    """
    depth_SLAM = np.array(
        [gt_depth[int(img_point[1]), int(img_point[0])] for (_, img_point) in points]
    )
    depth_SLAM_mask = depth_SLAM > 0
    depth_SLAM = depth_SLAM[depth_SLAM_mask]
    cp = np.array([cp[2] for (cp, _) in points])
    cp = cp[depth_SLAM_mask]
    return np.median(depth_SLAM) / np.median(cp)


def get_error_TUM(points, gt_filename):
    """Get the realtive gt from it's filename and convert the scale of the predictions in order to compute the error

    Args:
        points: the predictions depth
        gt_filename: the gt references filename

    Returns:
        the error computed on this examples
    """
    gt_depth = read_depth_TUM(gt_filename)
    if points is not None:
        ratio = convert_scale(points, gt_depth)
        depth = []
        gt = []
        for (cp, img_point) in points:
            depth_converted = cp[2] * ratio
            if gt_depth[int(img_point[1]), int(img_point[0])] > 0:
                depth.append(depth_converted)
                gt.append(gt_depth[int(img_point[1]), int(img_point[0])])
        depth = np.array(depth)
        gt = np.array(gt)
        return compute_errors(gt, depth)


def get_error_KITTI(points, gt_filename):
    """Get the realtive gt from it's filename and convert the scale of the predictions in order to compute the error

    Args:
        points: the predictions depth
        gt_filename: the gt references filename

    Returns:
        the error computed on this examples
    """
    gt_depth = read_depth_KITTI(gt_filename)
    if points is not None:
        ratio = convert_scale(points, gt_depth)
        depth = []
        gt = []
        for (cp, img_point) in points:
            depth_converted = cp[2] * ratio
            if gt_depth[int(img_point[1]), int(img_point[0])] > 0:
                depth.append(depth_converted)
                gt.append(gt_depth[int(img_point[1]), int(img_point[0])])
        depth = np.array(depth)
        gt = np.array(gt)
        return compute_errors(gt, depth)


def read_depth_KITTI(filename):
    """loads depth map D from png file and returns it as a numpy array,"""
    depth_png = np.array(Image.open(filename), dtype=int)
    # make sure we have a proper 16bit depth map here.. not 8bit!
    assert np.max(depth_png) > 255

    depth = depth_png.astype(np.float) / 256.0
    depth[depth_png == 0] = -1.0
    return depth


def read_depth_TUM(filename):
    """loads depth map D from png file and returns it as a numpy array,"""
    depth_png = np.array(Image.open(filename), dtype=int)
    # make sure we have a proper 16bit depth map here.. not 8bit!
    assert np.max(depth_png) > 255

    depth = (depth_png.astype(np.float) / 256) / 5000.0
    return depth


def create_dir(directory):
    """Create a directory if not exists
    Args:
        directory: directory to create
    Returns:
        None, but it creates a new folder if not exists
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_depth(dest, depth):
    """Save depth as 16 bit png file

    Args:
        dest: path to new 16 bit png image wiht depth, w/o exension
        depth: depth to save, as ndarray HxW

    Returns:
        None, but a new 16 bit png image will be saved at dest
    """
    cv2.imwrite(f"{dest}.png", (depth * 256).astype(np.uint16))


def save_pose(dest, pose):
    """Save pose as npy file

    Args:
        dest: path to new npy file wiht pose, w/o exension
        pose: ndarray with 4x4 pose matrix (as R|t in homogeneous notation)

    Returns:
        None, but it creates a new npy file with the pose
    """

    np.save(f"{dest}.npy", pose)


def save_pose_txt(args, name, pose):
    """Save pose as txt file

    Args:
        dir: directory of pose.txt
        name: frame name or id
        pose: ndarray with 4x4 pose matrix (as R|t in homogeneous notation)

    Returns:
        None, but it creates a new npy file with the pose
    """
    pose_file_path = os.path.join(args.dest, "pose.txt")
    fp = open(pose_file_path, "a")
    pose34 = pose[:3]
    fp.write(name)
    for row in pose34:
        fp.write(" ")
        fp.write(" ".join(str(round(i, 10)) for i in row))
    # fp.write('\n')
    fp.write("\n")
    fp.close()


def save_pose_and_times_txt(args, name, pose):
    """Save pose and time in two different txt files."""

    time_file_path = os.path.join(args.dest, "times.txt")
    pose_file_path = os.path.join(args.dest, "pose.txt")
    fd = open(time_file_path, "a")
    fp = open(pose_file_path, "a")
    pose34 = pose[:3]
    fd.write(name)
    fd.write("\n")
    fd.close()
    line = ""
    for row in pose34:
        line += " ".join(str(round(i, 10)) for i in row)
        line += " "
    line = line[:-1]
    line += "\n"
    fp.write(line)
    # fp.write('\n')
    fp.close()


def evaluate_pose(args):
    """Evaluate odometry on the KITTI dataset"""
    orb_pose_dir = os.path.join(args.dest, "pose")
    pred_poses = []
    gt_local_poses = []
    ates = []
    for count, dir_name in enumerate(sorted(os.listdir(orb_pose_dir))):
        fileId = os.path.splitext(dir_name)[0]
        id = fileId.zfill(6)
        pose_file = os.path.join(orb_pose_dir, "{}.npy".format(id))
        pred_poses.append(np.load(pose_file))

        gt_pose_file = os.path.join(args.gt_pose_dir, "{}.npy".format(id))
        gt_local_poses.append(np.load(gt_pose_file))

    num_frames = len(gt_local_poses)
    track_length = 5
    for i in range(0, num_frames - track_length - 1):
        if i == num_frames - track_length - 2:
            print("break")
        local_xyzs = np.array(dump_xyz(pred_poses[i : i + track_length - 1]))
        gt_local_xyzs = np.array(dump_xyz(gt_local_poses[i : i + track_length - 1]))
        ates.append(compute_ate(gt_local_xyzs, local_xyzs))

    print(
        "\n   Trajectory error: {:0.3f}, std: {:0.3f}\n".format(
            np.mean(ates), np.std(ates)
        )
    )


# from https://github.com/tinghuiz/SfMLearner
def dump_xyz(source_to_target_transformations):
    xyzs = []
    cam_to_world = np.eye(4)
    xyzs.append(cam_to_world[:3, 3])
    for source_to_target_transformation in source_to_target_transformations:
        cam_to_world = np.dot(cam_to_world, source_to_target_transformation)
        xyzs.append(cam_to_world[:3, 3])
    return xyzs


# from https://github.com/tinghuiz/SfMLearner
def compute_ate(gtruth_xyz, pred_xyz_o):

    # Make sure that the first matched frames align (no need for rotational alignment as
    # all the predicted/ground-truth snippets have been converted to use the same coordinate
    # system with the first frame of the snippet being the origin).
    offset = gtruth_xyz[0] - pred_xyz_o[0]
    pred_xyz = pred_xyz_o + offset[None, :]

    # Optimize the scaling factor
    scale = np.sum(gtruth_xyz * pred_xyz) / (np.sum(pred_xyz ** 2) + 0.00001)
    alignment_error = pred_xyz * scale - gtruth_xyz
    rmse = np.sqrt(np.sum(alignment_error ** 2)) / gtruth_xyz.shape[0]
    return rmse


def save_depth_err_results(file_path, filename, err):
    f = open(file_path, "a+")
    print("----------------------------------------------")
    print("image id:{}".format(filename))
    print(
        "\n  "
        + ("{:>8} | " * 7).format(
            "abs_rel", "sq_rel", "rmse", "rmse_log", "a1", "a2", "a3"
        )
    )
    print(("&{: 8.3f}  " * 7).format(*err) + "\\\\")

    f.writelines("----------------------------------------------\n")
    f.writelines("image id:{}".format(filename))
    f.writelines(
        "\n  "
        + ("{:>8} | " * 7).format(
            "abs_rel", "sq_rel", "rmse", "rmse_log", "a1", "a2", "a3"
        )
    )
    f.writelines("\n")
    f.writelines(("&{: 8.3f}  " * 7).format(*err) + "\\\\")
    f.writelines("\n")
    return


def get_error(args, filename, points, gt_filename):
    """Get the realtive gt from it's filename and convert the scale of the predictions in order to compute the error

    Args:
        points: the predictions depth
        gt_filename: the gt references filename

    Returns:
        the error computed on this examples
    """
    MIN_DEPTH = 1e-3
    if args.data_type == "KITTI_VO":
        MAX_DEPTH = 100
        gt_depth = cv2.imread(gt_filename, -1) / 256
        if gt_depth is None:
            print("gt path err {}".gt_filename)
            return None
    elif args.data_type == "TUM":
        MAX_DEPTH = 10
        gt_depth = (cv2.imread(gt_filename, -1) / 256) / 5000.0
        if gt_depth is None:
            print("gt path err {}".gt_filename)
            return None
    else:
        print("Error data type {}".format(args.data_type))
        return
    pred_depth = points

    mask_pred = pred_depth > 0
    mask_gt = gt_depth > 0
    mask = (mask_pred) & (mask_gt)
    gt_depth = gt_depth[mask]
    pred_depth = pred_depth[mask]

    ratio = np.median(gt_depth) / np.median(pred_depth)
    pred_depth *= ratio

    pred_depth[pred_depth < MIN_DEPTH] = MIN_DEPTH
    pred_depth[pred_depth > MAX_DEPTH] = MAX_DEPTH
    err = compute_errors(gt_depth, pred_depth)

    save_results = os.path.join(args.dest, "results.txt")
    save_depth_err_results(save_results, filename, err)

    return err


def load_images_KITTI_VO(path_to_sequence):
    """Return the sequence of the images found in the path and the corrispondent timestamp

    Args:
        path_to_sequence : the sequence in witch we can found the image sequences

    Returns :
        two array : one contains the sequence of the image filename and the second the timestamp in whitch they are acquired

    """
    timestamps = []
    t0 = None
    with open(os.path.join(path_to_sequence, "times.txt")) as times_file:
        for line in times_file:
            if len(line) > 0:
                timestamps.append(float(line))
    return [
        os.path.join(path_to_sequence, "data", str(idx).zfill(6) + ".png")
        for idx in range(len(timestamps))
    ], timestamps


def load_images_TUM(path_to_sequence, file_name):
    """Return the sequence of the images found in the path and the corrispondent timestamp

    Args:
        path_to_sequence : the sequence in witch we can found the image sequences

    Returns:
        two array : one contains the sequence of the image filename and the second the timestamp in whitch they are acquired

    """
    timestamps = []
    rgb_filenames = []
    with open(os.path.join(path_to_sequence, file_name)) as times_file:
        for line in times_file:
            if len(line) > 0 and not line.startswith("#"):
                t, rgb = line.rstrip().split(" ")[0:2]
                rgb_filenames.append(rgb)
                timestamps.append(float(t))

    return [os.path.join(path_to_sequence, name) for name in rgb_filenames], timestamps


def load_images_OTHERS(path_to_sequence):

    """Return the sequence of the images found in the path and the corrispondent timestamp

    Args:
        path_to_sequence : the sequence in witch we can found the image sequences

    Returns :
        two array : one contains the sequence of the image filename and the second the timestamp in whitch they are acquired

    Inside of path_to_sequence must be: +data
                                           xxxxxxxx.png
                                           xxxxxxxy.png
                                           ....
                                        -times.txt
    where times.txt simply contains timestamps of every frame

    """

    timestamps = []
    framenames = []

    with open(os.path.join(path_to_sequence, "times.txt")) as times_file:
        for line in times_file:
            if len(line) > 0 and not line.startswith("#"):
                timestamps.append(float(line))

    for framename in sorted(os.listdir(os.path.join(path_to_sequence, "data"))):
        if framename.endswith(".png"):
            framenames.append(framename)

    return [
        os.path.join(path_to_sequence, "data", name) for name in framenames
    ], timestamps


def load_images_TUM_VI(path_to_sequence):

    """This loader is created for Visual Inertial TUM datasets. Format of such datasets is:
    path_to_sequence/mav0/cam0/+data/xxxx.png
                              /-times.txt
    """
    timestamps = []
    framenames = []

    with open(os.path.join(path_to_sequence, "mav0/cam0/times.txt")) as times_file:
        for line in times_file:
            if len(line) > 0 and not line.startswith("#"):
                framenames.append(line.split()[0] + ".png")
                timestamps.append(float(line.split()[1]))

    return [
        os.path.join(path_to_sequence, "mav0/cam0/data", name) for name in framenames
    ], timestamps


def load_images_EuRoC(path_to_sequence):

    """This loader is created for Visual Inertial EuRoC datasets. Format of such datasets is:
    path_to_sequence/mav0/cam0/+data/xxxx.png
                              /-times.txt
    """
    timestamps = []
    framenames = []

    with open(os.path.join(path_to_sequence, "mav0/cam0/data.csv")) as times_file:
        for line in times_file:
            if len(line) > 0 and not line.startswith("#"):
                framenames.append(line.split(",")[1].rstrip())
                timestamps.append(float(line.split(",")[0]) * 1e-9)

    return [
        os.path.join(path_to_sequence, "mav0/cam0/data", name) for name in framenames
    ], timestamps


def load_IMU_datas_TUM_VI(path_to_sequence):
    timestamp = []
    gyro_data = []
    acc_data = []
    with open(os.path.join(path_to_sequence, "mav0/imu0/data.csv")) as imu_file:
        for line in imu_file:
            if len(line) > 0 and not line.startswith("#"):
                imu_line = line.split(",")
                timestamp.append(float(imu_line[0]) * 1e-9)
                gyro_data.append(
                    [float(imu_line[1]), float(imu_line[2]), float(imu_line[3])]
                )
                acc_data.append(
                    [float(imu_line[4]), float(imu_line[5]), float(imu_line[6])]
                )

    return acc_data, gyro_data, timestamp
