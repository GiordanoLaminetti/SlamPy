# SlamPy

this project is a wrapper for an aribtrary SLAM alogirthm in python.

for the slam algorithm is current provided :

- ORB_SLAM2
- ORB_SLAM3

## ORB_SLAM2 / ORB_SLAM3 requirement

for this algorithm you need to install the python wrapper for this two algorithm, this wrapper can be found at [ORB_SLAM2-PythonBindings](https://github.com/GiordanoLaminetti/ORB_SLAM2-PythonBindings) for ORB_SLAM2 and [ORB_SLAM3-PythonBindings](https://github.com/GiordanoLaminetti/ORB_SLAM2-PythonBindings/tree/ORBSLAM3) for ORB_SLAM3

## Example of usage with ORB_SLAM2

the jupyter notebooks **example_usage** show and example of usage with ORB_SLAM2 with a KITTI dataset, the dataset can be found at this [link](http://www.cvlibs.net/datasets/kitti/raw_data.php)

## Change the settings

to change the algorithm settings you can modify the **setitng.yaml** file in the line

> SLAM.alg:'insert here your .py file that contains the wrapper class'

you can add at the file the other params that the method needs.
to change from ORB_SLAM2 to ORB_SLAM3 you need to change only the **SLAM.alg** entry.

### ORB_SLAM2/3 params

the params needed for this 2 algorithms are:

- a vocabulary file
- a setting file with the intrisec parameters of the cameras and the other configuration params

in this repository is provided the vocabulary file and the configuration file for ORB_SLAM2/3 for the KITTI_02 camera and the TUM freiburg3 camera in the **slam_metohd/Settings** folder, but you can add your owns using as model the files currently provided.


### Docker

on dockerhub can be found a container with all the dipendences and the repository already installed. You can download it by typing 
```
docker pull giordanolaminetti/slampy:latest
```
in the repository is also provided the Dockerfile to build your own container.
to run it after the download or build, the command is
```
docker run -it -p 8888:8888 giordanolaminetti/slampy tmux
```
after the execution it will open a tumx terminal on the container.

if you want to bind the container on a specific folder in your pc, you can type 
```
docker run -it --mount type=bind,source="$(pwd)",target=/pyslam -p 8888:8888 giordanolaminetti/slampy tmux
```
and change the source directory to the directory you want to bind; the example command is run on root direcotry of the repository
