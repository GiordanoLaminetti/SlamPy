# SlamPy

![Python version](https://img.shields.io/badge/python-python%203.8-brightgreen) [![Build Status](https://travis-ci.com/GiordanoLaminetti/SlamPy.svg?branch=master)](https://travis-ci.com/GiordanoLaminetti/SlamPy) [![Documentation Status](https://readthedocs.org/projects/slampy/badge/?version=latest)](https://slampy.readthedocs.io/en/latest/?badge=latest)

This project is a python wrapper to SLAM algorithms.

<p float="center">
    <img src="assets/SLAM.gif" width='100%'/>
</p>

At the moment, we provide support for:

- ORB_SLAM2
- ORB_SLAM3

## Example of usage with ORB_SLAM2

- the jupyter notebook **example_usage** shows how to use ORB_SLAM2 with a sequence of the KITTI dataset
- the jupyter notebook **trajectory_example** draw the camera trajectory and the point cloud

## Change the settings

to change the algorithm settings you can modify the **setting.yaml** file in the line

> SLAM.alg:'insert here your .py file that contains the wrapper class'

you can add at the file the other params that the method needs.
to change from ORB_SLAM2 to ORB_SLAM3 you need to change only the **SLAM.alg** entry.

<p float="center">
     <img src="assets/Trajectory.gif" width='100%' height="500" />
</p>

### ORB_SLAM2/3 params

the params needed for this 2 algorithms are:

- a vocabulary file
- a setting file with the intrinsics parameters of the cameras and other configuration params

We provided the vocabulary file and the configuration file for ORB_SLAM2/3 for the KITTI_02 camera and the TUM freiburg3 camera in the **slam_metohd/Settings** folder, but you can add your owns using as model the files currently provided.

### Docker

We provide a container on dockerhub, in which all the dipendences and the repository are already installed.

```
docker pull giordanolaminetti/slampy:tag
```

The `tag` correspond to the container you need:

- `base` correspond to a container with installed only the dependences
- `orbslam2` correspond to a container with only ORB_SLAM2 installed
- `orbslam3` correspond to a container with only ORB_SLAM2 installed
- `latest` correspond to a container with ORB_SLAM2 and ORB_SLAM3 installed

When the image is ready, you can create a new container running:

```
NAME="orb"
DATAPATH="/PATH/TO/KITTI/DATE/DRIVE_SYNC_FOLDER/"
TAG="latest"
sudo docker run -it \
                --name $NAME \
                --mount type=bind,source="$(pwd)",target=/slampy/slampy \
                -v $DATAPATH:"/slampy/slampy/Dataset":ro \
                -p 8888:8888 --rm\
                giordanolaminetti/slampy:$TAG /bin/bash
```

Doing so, the created container contains both the code and the Dataset (in read-only mode to prevent wrong behaviours)

You can have a test with the `jupyter` example running:

```
jupyter notebook --ip 0.0.0.0
```

## Credits:

Our project has been developed starting from other repositories, in particular:

- Python bindings to ORB Slam are based on the [repo](https://github.com/jskinn/ORB_SLAM2-PythonBindings)
- ORB Slam 2 has been cloned from [the original repository](https://github.com/raulmur/ORB_SLAM2)
- ORB Slam 3 has been cloned from [the original repository](https://github.com/UZ-SLAMLab/ORB_SLAM3)
