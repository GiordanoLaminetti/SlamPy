import orbslam3
import sys
import os.path
import numpy as np

sys.path.append("..")
from slampy import State
from slampy import Sensor


class Slam:
    def __init__(self, params, sensor_type):
        config_file = params["SLAM.settings_path"]
        vocab_file = params["SLAM.vocab_path"]

        # check the existence of the configuration file

        if not os.path.exists(config_file):
            raise FileNotFoundError(config_file + " not found")

        if not os.path.exists(vocab_file):
            raise FileNotFoundError(vocab_file + " not found")

        if sensor_type == Sensor.MONOCULAR:
            print("the input sensor select is MONOCULAR")
            self.slam = orbslam3.System(
                vocab_file, config_file, orbslam3.Sensor.MONOCULAR
            )
            self.sensor_type = sensor_type

        if sensor_type == Sensor.MONOCULAR_IMU:
            print("the input sensor select is MONOCULAR_IMU")
            self.slam = orbslam3.System(
                vocab_file, config_file, orbslam3.Sensor.IMU_MONOCULAR
            )
            self.sensor_type = sensor_type

        if sensor_type == Sensor.STEREO:
            print("the input sensor select is STEREO")
            self.slam = orbslam3.System(vocab_file, config_file, orbslam3.Sensor.STEREO)
            self.sensor_type = sensor_type

        if sensor_type == Sensor.STEREO_IMU:
            print("the input sensor select is STREO_IMU")
            self.slam = orbslam3.System(
                vocab_file, config_file, orbslam3.Sensor.IMU_STEREO
            )
            self.sensor_type = sensor_type

        if sensor_type == Sensor.RGBD:
            print("the input sensor select is RGBD")
            self.slam = orbslam3.System(vocab_file, config_file, orbslam3.Sensor.RGBD)
            self.sensor_type = sensor_type
        self.slam.set_use_viewer(False)
        self.slam.initialize()

    def process_image_mono(self, image, tframe):
        if self.sensor_type == Sensor.MONOCULAR:
            self.slam.process_image_mono(image, tframe, "0")
        else:
            raise Exception("The sensor type is not MONOCULAR")

    def process_image_stereo(self, image_left, image_right, tframe):
        if self.sensor_type == Sensor.STEREO:
            self.slam.process_image_stereo(image_left, image_right, tframe, "0")
        else:
            raise Exception("The sensor type is not STEREO")

    def process_image_imu_mono(self, image, tframe, imu):
        if self.sensor_type == Sensor.MONOCULAR_IMU:
            self.slam.process_image_imu_mono(image, tframe, "0", imu)
        else:
            raise Exception("The sensor type is not MONOCULAR_IMU")

    def process_image_imu_stereo(self, image_left, image_right, tframe, imu):
        if self.sensor_type == Sensor.STEREO_IMU:
            self.slam.process_image_imu_stereo(
                image_left, image_right, tframe, "0", imu
            )
        else:
            raise Exception("The sensor type is not STREO_IMU")

    def process_image_rgbd(self, image, tframe):
        if self.sensor_type == Sensor.RGBD:
            self.slam.process_image_rgbd(image, tframe, "0")
        else:
            raise Exception("The sensor type is not RGBD")

    def get_pose_to_target(self):
        if self.slam.get_tracking_state() == orbslam3.TrackingState.OK:
            return np.linalg.inv(self.slam.get_frame_pose())

    def get_abs_cloud(self):
        if self.slam.get_tracking_state() == orbslam3.TrackingState.OK:
            return self.slam.get_tracked_mappoints()

    def get_camera_matrix(self):
        return self.slam.get_camera_matrix()

    def get_state(self):
        if self.slam.get_tracking_state() == orbslam3.TrackingState.OK:
            return State.OK
        elif self.slam.get_tracking_state() == orbslam3.TrackingState.LOST:
            return State.LOST
        elif self.slam.get_tracking_state() == orbslam3.TrackingState.NOT_INITIALIZED:
            return State.NOT_INITIALIZED
        elif self.slam.get_tracking_state() == orbslam3.TrackingState.SYSTEM_NOT_READY:
            return State.SYSTEM_NOT_READY
        else:
            return State.LOST

    def reset(self):
        self.slam.reset()

    def shutdown(self):
        self.slam.shutdown()
