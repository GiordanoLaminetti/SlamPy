from enum import Enum
import numpy as np
import importlib
import yaml


class Sensor(Enum):
    """
    This class is used to set the type of the sensor
        Values:
            MONOCULAR
            STEREO
            MONOCULAR_IMU
            STEREO_IMU
            RGBD
    """

    MONOCULAR = 1
    STEREO = 2
    MONOCULAR_IMU = 3
    STEREO_IMU = 4
    RGBD = 5


class State(Enum):
    """This class is used to get the actual state of the tracking
    Values:
        OK
        LOST
        NOT_INITIALIZED
    """

    OK = 1
    LOST = 2
    NOT_INITIALIZED = 3
    SYSTEM_NOT_READY = 4


class System:
    """This class is a wrapper for the SLAM method in the slam_method folder,"""

    def __init__(self, params_file, sensor_type):
        """Build the wrapper

        Args:
            params_file (str): the Path to the .yaml file.
            sensor_type (Enum): the sensort type of the SLAM
        """
        # read and process the config file
        with open(params_file) as fs:
            self.params = yaml.safe_load(fs)

        module = importlib.import_module("slam_method." + self.params["SLAM.alg"])
        self.slam = module.Slam(self.params, sensor_type)
        self.pose_array = []  # is an array that contains the pose stored by the SLAM

    def process_image_mono(self, image, tframe):
        """Process an image mono.

        Note: it works only if the sensor type is MONOCULAR

        Args:
            image : ndarray of the image
            tframe (float): the timestamp when the image was capture

        Returns:
            the state of the traking in this frame

        Raises:
            Exception: if the sensor type is different from MONOCULAR
        """
        self.image_shape = image.shape
        self.slam.process_image_mono(image, tframe)
        self.image = image
        if self.get_state() == State.OK:
            self.pose_array.append(self.get_pose_to_target())
        return self.get_state()

    def process_image_stereo(self, image_left, image_right, tframe):
        """Process a stereo pair.

        Note: it works only if the sensor type is STEREO

        Args:
            image_left (ndarray) : left image as HxWx3
            image_right (ndarray) : right image as HxWx3
            tframe (float): the timestamp when the image was capture

        Returns:
            the state of the traking in this frame

        Raises:
            Exception: if the sensor type is different from STEREO
        """
        self.image_shape = image_left.shape
        self.slam.process_image_stereo(image_left, image_right, tframe)
        self.image = image_left
        if self.get_state() == State.OK:
            self.pose_array.append(self.get_pose_to_target())
        return self.get_state()

    def process_image_imu_mono(self, image, tframe, imu):
        """Process an image mono with the imu data.

        Note: it works only if the sensor type is MONOCULAR_IMU

        Args:
            image (ndarray): image as HxWx3
            tframe (float): the timestamp when the image was capture
            imu : the imu data stored in an float array in the form of [ AccX ,AccY ,AccZ, GyroX, vGyroY, vGyroZ, Timestamp]

        Returns:
            the state of the traking in this frame

        Raises:
            Exception: if the sensor type is different from MONOCULAR_IMU
        """
        self.image_shape = image.shape
        self.slam.process_image_imu_mono(image, tframe, imu)
        self.image = image
        if self.get_state() == State.OK:
            self.pose_array.append(self.get_pose_to_target())
        return self.get_state()

    def process_image_imu_stereo(self, image_left, image_right, tframe, imu):
        """Process an image stereo with the imu data.

        Note: it work only if the sensor type is STEREO_IMU

        Args:
            image_left (ndarray): left image as HxWx3
            image_right (ndarray) : right image as HxWx3
            tframe (float): the timestamp when the image was capture
            imu : the imu data stored in an float array in the form of [ AccX ,AccY ,AccZ, GyroX, vGyroY, vGyroZ, Timestamp]

        Returns:
            the state of the traking in this frame

        Raises:
            Exception: if the sensor type is different from STEREO_IMU
        """
        self.image_shape = image_left.shape
        self.slam.process_image_imu_stereo(image_left, image_right, tframe, imu)
        self.image = image_left
        if self.get_state() == State.OK:
            self.pose_array.append(self.get_pose_to_target())
        return self.get_state()

    def process_image_rgbd(self, image, tframe):
        """Process an  rgbd image.

        Note: it works only if the sensor type is RGBD

        Args:
            image (ndarray): RGBD image as HxWx4
            tframe (float): the timestamp when the image was capture

        Returns:
            the new state of the SLAM system

        Raises:
            Exception: if the sensor type is different from RGBD

        """
        self.image_shape = image.shape
        self.slam.process_image_rgbd(image, tframe)
        self.image = image
        if self.get_state() == State.OK:
            self.pose_array.append(self.get_pose_to_target())
        return self.get_state()

    def get_pose_to_target(self, precedent_frame=-1):
        """Get the pose between a previous frame X in the sequence and the current one T.

        The param `precedent_frame` allows to distinguish between different situations:
        * precedent_frame = -1:  X is the first frame of the sequence. We get the pose between 0->T
        * precedent_frame > 0 :  X is frame at (T-precedent_frame). For instance, if precedent_frame=1, it means we are computing the
        pose  (T-1) -> T.

        Args:
            precedent_frame : id of the frame to use when computing the pose between frame. Default is -1 (i.e., pose 0->T)

        Returns:
            the 4x4 pose matrix corresponding to the transormation between the precedent_frame and the current one.
            If the state is not State.OK, return None


        Examples:
            >>> slam.get_pose_to_target() # return the pose 0 -> T
            >>> slam.get_pose_to_target(precedent_frame=1) # return the pose (T-1) -> T
            >>> slam.get_pose_to_target(precedent_frame=2) # return the pose (T-2) -> T

        """
        if self.get_state() == State.OK:
            if precedent_frame <= 0:
                return self.slam.get_pose_to_target()
            else:
                # get_pose_to_target = pose 0->T
                # inv(0->T-precedent_frame) = pose T-precedent_frame to 0
                # pose T-precedent_frame->T = 0->T * (T-1 -> 0)
                return np.dot(
                    self.slam.get_pose_to_target(),
                    np.linalg.inv(self.pose_array[-precedent_frame]),
                )
        return None

    def get_pose_from_target(self):
        """Get the pose from the current frame T to the reference one 0."""
        if self.get_state() == State.OK:
            return np.linalg.inv(self.slam.get_pose_to_target())
        return None

    def get_abs_cloud(self):
        """Get the point cloud at the current frame stored in absolute coordinates.

        Return:
            an array with the 3D coordinate of the point, None if the traking is failed

        """
        if self.get_state() == State.OK:
            return self.slam.get_abs_cloud()
        return None

    def get_point_cloud(self):
        """Get the point cloud at the current frame form the wiev of the current position .

        Return:
            an array with the 3D coordinate of the point, None if the traking is failed

        """
        if self.get_state() == State.OK:
            return [cp for (cp, _) in self._get_2d_point()]
        return None

    def get_point_cloud_colored(self):
        """Get the point cloud at the current frame form the wiev of the current position with the RGB color of the point .

        Return:
            an array with the 3D coordinate of the point and the relative RGB color, None if the traking is failed

        """
        if self.get_state() == State.OK:
            return [
                [cp, self.image[point[1], point[0]]]
                for (cp, point) in self._get_2d_point()
            ]
        return None

    def get_depth(self):
        """Get the depth computed in the current image.

        Return:
            an array of the image shape with depth when it is aviable otherwise -1 , None if the traking is failed

        """
        depth = None
        if self.get_state() == State.OK:
            depth = np.ones(self.image_shape[0:2]) * -1
            for (cp, point) in self._get_2d_point():
                depth[point[1], point[0]] = cp[2]
        return depth

    def _get_2d_point(self):
        """This private method is used to compute the transormation between the absolute point to the image point

        Return:
            a np.ndarray of pairs (camera view, image point) , an empty list if the tracking is failed

        """
        points2D = []
        points = self.get_abs_cloud()
        camera_matrix = self.slam.get_camera_matrix()
        pose = self.get_pose_from_target()
        for point in points:
            point = np.append(point, [1]).reshape(4, 1)
            camera_points = np.dot(pose, point)
            if camera_points[2] >= 0:
                u = (
                    camera_matrix[0, 0] * (camera_points[0] / camera_points[2])
                    + camera_matrix[0, 2]
                )
                v = (
                    camera_matrix[1, 1] * (camera_points[1] / camera_points[2])
                    + camera_matrix[1, 2]
                )
            if int(v) in range(0, self.image_shape[0]):
                if int(u) in range(0, self.image_shape[1]):
                    points2D.append([camera_points, (int(u), int(v))])
        return points2D

    def get_camera_matrix(self):
        """Get the camera instrinsics

        Returns:
            np.ndarray with shape 3x4 containing the camera parameters.
        """
        return self.slam.get_camera_matrix()

    def get_state(self):
        """Get the current state of the SLAM system

        Returns:
            a State corresponding to the state
        """
        return self.slam.get_state()

    def shutdown(self):
        """Shutdown the SLAM system"""
        self.slam.shutdown()
        self.pose_array = []

    def reset(self):
        """Reset SLAM system"""
        self.slam.reset()
