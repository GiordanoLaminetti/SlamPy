=======================
Docker Container
=======================

.. _docker_container:


We provide a container on dockerhub, where all the dipendences and the repository are already installed.

-------------------------
Download docker container
-------------------------
On docker hub there are 4 containers with a different tagname :

- ``base`` the base container in which only the dipendences are installed
- ``orbslam2`` a container with only installed the ORB_SLAM2 library
- ``orbslam3`` a container with only installed the ORB_SLAM3 library
- ``latest`` a container with installed all the library

for downloading the container you can type ::

    docker pull giordanolaminetti/slampy:tagname


with the addiction of ``-focal`` after ``tagname`` you can download the builds with ubuntu 20.04 (focal fossa), by default the docker are built over ubuntu 18.04::

  docker pull giordanolaminetti/slampy:latest-focal

with the addiction of ``-ros-noetic`` after ``tagname`` you can download the ubuntu 20.04 (focal fossa) with ros noetic already installed ::

  docker pull giordanolaminetti/slampy:latest-focal

----------------------
Build docker container
----------------------
you can also build your own container, with the shell in the root path, typing this command ::

    docker build . -t slampy [--build-args arg=value]*

you can change the image name by replacing ``slampy`` with the desired image name, the ``build args `` can be:


- ``base_container`` (String) you can change the base container, by default it is ``ubuntu:18.04``, it can also be used to install multiple algorithm
- ``build_dependences`` (Bool) build and install the dependences packages (pangolin, Eigen, Opencv, Python3.8, ...) default ``true``
- ``build_orbslam2`` (Bool) build and install ORB_SLAM2 and the Python wrapper  default ``true``
- ``build_orbslam3`` (Bool) build and install ORB_SLAM3 and the Python wrapper  default ``true``

For example if you want to build only the ORB_SLAM2 package from the base you can type ::

    docker build . -t slampy:orbslam2 --build-arg build_dependences=false --build-arg build_orbslam3=false --build-arg base_container=giordanolaminetti/slampy:base

For example if you want to install only ORB_SLAM2 and ORB_SLAM3 you can type ::

    docker build . -t slampy:orbslam2+3 --build-arg build_dependences=false --build-arg build_orbslam2=false --build-arg base_container=giordanolaminetti/slampy:orbslam2

----------------
Run docker image
----------------

When the image is ready, you can create a new container running: ::

    NAME="orb"
    DATAPATH="/PATH/TO/KITTI/DATE/DRIVE_SYNC_FOLDER/"
    IMAGE_NAME="giordanolaminetti/slampy"
    TAG="latest"
    sudo docker run -it \
                    --name $NAME \
                    --mount type=bind,source="$(pwd)",target=/slampy/slampy \
                    -v $DATAPATH:"/slampy/slampy/Dataset":ro \
                    -p 8888:8888 --rm\
                    $IMAGE_NAME:$TAG /bin/bash


Doing so, the created container contains both the code and the Dataset (in read-only mode to prevent wrong behaviours)

You can have a test with the `jupyter` example running: ::

    jupyter notebook --ip 0.0.0.0

after the close connection it will remove the container, if you want to preserve it then remove the  ``-rm `` options
