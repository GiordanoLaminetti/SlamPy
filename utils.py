from datetime import datetime
import time
import numpy as np
import os
import read_depth


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
    t0 = None
    with open(os.path.join(path_to_sequence, file_name)) as times_file:
        for line in times_file:
            if len(line) > 0 and not line.startswith("#"):
                t, rgb = line.rstrip().split(" ")[0:2]
                rgb_filenames.append(rgb)
                timestamps.append(float(t))

    return [os.path.join(path_to_sequence, name) for name in rgb_filenames], timestamps


def compute_errors(gt, pred):
    """Computation of error metrics (abs rel,sq rel, rmse, rmse log) between predicted and ground truth depths

    Args:
        gt : an array with the ground truth values
        pred : an array with the predicted values

    Returns:
        abs_rel,sq_rel,rmse,rmse_log : the error

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

    return abs_rel, sq_rel, rmse, rmse_log


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
    gt_depth = read_depth.read_depth_TUM(gt_filename)
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
    gt_depth = read_depth.read_depth_KITTI(gt_filename)
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
