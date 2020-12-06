=======================
add you own algorithm
=======================
.. _addmethod:

you can add you own algorithm to Slampy by adding a new ``your_method_name.py`` file with the specs found below, to the ``slam_method`` folder

the file must contain a class named ``Slam`` with the method shown below ::

    import sys
    sys.path.append("..")
    from slampy import Sensor
    from slampy import State
    
    class Slam:
        def __init__(self, params, sensor_type):
           
        def process_image_mono(self, image, tframe):
           
        def process_image_stereo(self, image_left, image_right, tframe):
           
        def process_image_imu_mono(self, image, tframe, imu):
            
        def process_image_imu_stereo(self, image_left, image_right, tframe, imu): 

        def process_image_rgbd(self, image, tframe):
            
        def get_pose_to_target(self):
           
        def get_abs_cloud(self):
            
        def get_camera_matrix(self):
            
        def get_state(self):
            
        def reset(self):
            
        def shutdown(self):

----------------------
Slam class references
----------------------

In this section we describe all the methods with the parameters that you need to write in order to add your algorithm to Slampy.

You can add your own accessor method, but the method described below must be present with this signature and return the exact value as described

.. py:class:: Slam

    .. py:method:: __init__(self, params, sensor_type)

        Initialize your algorithm with the params from the settings.yaml and the sensor type
        
        :param dict params: the setting.yaml params conver to Python dictionary
        :param Pyslam.Sensor sensor_type: the type of the sensor as istance of Sensor Class


    **there are one process_image method for each of the sensor type in Sensor Class. If your algorithm hasn't one of this methods you can add an exception every time that one calls that sensor processing method**

    .. py:method:: process_image_mono(self, image , tframe)

        pass the image to the slam system and compute the tracking

        :param numpy.ndarray image: an RGB image
        :param float tframe: the timestamp in which the frame is caputred
        :raises Exception: if the Sensor is different from MONOCULAR


    .. py:method:: process_image_stereo(self, image_left,image_right , tframe)

        pass the images to the slam system and compute the tracking 

        :param numpy.ndarray image_left: an RGB image
        :param numpy.ndarray image_right: an RGB image
        :param float tframe: the timestamp in which the frame is caputred
        :raises Exception: if the Sensor is different from STEREO


    .. py:method:: process_image_imu_mono(self, image , tframe, imu)

        pass the image to the slam system and compute the tracking 

        :param numpy.ndarray image_left: an RGB image
        :param numpy.ndarray image_right: an RGB image
        :param float tframe: the timestamp in which the frame is caputred
        :param numpy.ndarray imu: the imu data imu data stored in an float array in the form of [ AccX ,AccY ,AccZ, GyroX, vGyroY, vGyroZ, Timestamp]
        :raises Exception: if the Sensor is different from MONOCULAR_IMU

    .. py:method:: process_image_imu_stereo(self, image_left, image_right , tframe, imu)

        pass the images to the slam system and compute the tracking 

        :param numpy.ndarray image_left: an RGB image
        :param numpy.ndarray image_right: an RGB image
        :param float tframe: the timestamp in which the frame is caputred
        :param numpy.ndarray imu: the imu data imu data stored in an float array in the form of [ AccX ,AccY ,AccZ, GyroX, vGyroY, vGyroZ, Timestamp]
        :raises Exception: if the Sensor is different from STEREO_IMU

    .. py:method:: process_image_rgbd(self, image , tframe)

        pass the image to the slam system and compute the tracking

        :param numpy.ndarray image: an RGBD image
        :param float tframe: the timestamp in which the frame is caputred
        :raises Exception: if the Sensor is different from RGBD


    .. py:method:: get_pose_to_target(self)

        return the pose between the references frame (usually the first frame) and the current one T.

        :return: the pose computed from the references frame to the actual ones, None if the tracking is failed 
        :rtype: a 4x4 numpy array
    
    .. py:method:: get_abs_cloud(self)

       return the point cloud at the current frame stored in absolute coordinates (coordinates from the references frame)

        :return: an array with the 3D coordinate of the point, None if the traking is failed
        :rtype: a nx3 numpy array

    .. py:method:: get_camera_matrix(self)

       return the intrinsec parameter of cameras

        :return: an array with the intrinsec parameter of cameras
        :rtype: a 4x4 numpy array  

    .. py:method:: get_state(self)

       return the current state of the tracking as istance of State Class
       
        :return: the state of the tracking
        :rtype: Slampy.State

    .. py:method:: reset(self)

       reset/initialize the slam tracking
  
    .. py:method:: shutdown(self)

       shutdown the slam algorithm
 