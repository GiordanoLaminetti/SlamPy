============================================
Introduction
============================================

This project is a python wrapper to SLAM algorithms.
At the moment, we provide support for:

- ORB_SLAM2
- ORB_SLAM3

The installation rules can be found :ref:`here <installation>` .

-----------------
Example of usage
-----------------

in the project can be found two jupyter notebook:

- **example_usage** shows how to use ORB_SLAM2 with a sequence of the KITTI dataset

- **trajectory_example** which provides a video sequence that draws the camera trajectory and the point cloud 

it is also present an **run.py** script where, by providing a video sequence, it saves the trajectory as a .txt file for the possible argument see the :ref:`Run.py references <run_module>`   

To change the algorithm and its parameter settings see :ref:`parameters file <settings>` 

-------
Credits
-------

Our project has been developed starting from other repositories, in particular:

- Python bindings to ORB Slam are based on the `repo <https://github.com/jskinn/ORB_SLAM2-PythonBindings>`_
- ORB Slam 2 has been cloned from `the ORB_SLAM2 original repository <https://github.com/raulmur/ORB_SLAM2>`_
- ORB Slam 3 has been cloned from `the ORB_SLAM3 original repository <https://github.com/UZ-SLAMLab/ORB_SLAM3>`_

