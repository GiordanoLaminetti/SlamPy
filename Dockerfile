FROM ubuntu:18.04
RUN useradd -d /pyslam pyslam
RUN apt-get update 
RUN apt-get install -y git
RUN apt-get install -y wget
RUN apt-get install -y unzip tmux
RUN apt-get install -y pkg-config 
RUN apt-get install -y libglew-dev python3-dev python3-pip
RUN apt-get install -y cmake
RUN apt-get install -y ffmpeg libgl1-mesa-dev libavcodec-dev libavutil-dev libavformat-dev libswscale-dev libavdevice-dev libdc1394-22-dev libraw1394-dev libjpeg-dev libtiff5-dev libopenexr-dev
RUN python3 -mpip install numpy pyopengl Pillow pybind11 jupyter matplotlib pandas pyyaml
RUN mkdir /pyslam
RUN chown -R pyslam:pyslam /pyslam

# Pangolin
ARG Pangolin_Path='/pyslam/Pangolin'
RUN cd /pyslam
RUN mkdir $Pangolin_Path
RUN git clone https://github.com/stevenlovegrove/Pangolin.git $Pangolin_Path
RUN cd  $Pangolin_Path
RUN mkdir  $Pangolin_Path/build
WORKDIR $Pangolin_Path/build
RUN cd  $Pangolin_Path/build
RUN cmake  $Pangolin_Path
RUN make -j7
RUN make install

#Eigen
ARG Eigen_Path='/pyslam/Eigen'
RUN cd /pyslam
RUN mkdir $Eigen_Path
RUN git clone https://gitlab.com/libeigen/eigen.git $Eigen_Path
RUN mkdir $Eigen_Path/build
RUN cd $Eigen_Path/build
WORKDIR $Eigen_Path/build
RUN cmake $Eigen_Path
RUN make install

# OpenCV
ARG opencv_Path='/pyslam/opencv-3.4.11'
ARG opencv_contrib_Path='/pyslam/opencv_contrib-3.4.11'
RUN cd /pyslam
RUN wget https://github.com/opencv/opencv/archive/3.4.11.zip
RUN unzip 3.4.11.zip -d /pyslam
RUN rm 3.4.11.zip
RUN wget https://github.com/opencv/opencv_contrib/archive/3.4.11.zip 
RUN unzip 3.4.11.zip -d /pyslam
RUN rm 3.4.11.zip
RUN cd $opencv_Path
RUN mkdir $opencv_Path/build
RUN cd $opencv_Path/build
WORKDIR $opencv_Path/build
RUN cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local \
        OPENCV_EXTRA_MODULES_PATH=$opencv_contrib_Path  ..
RUN make -j7
RUN make install

# install the python version
RUN pip3 install --upgrade pip
RUN python3 -mpip install opencv-contrib-python==3.4.11.45
RUN python3 -c 'import cv2; print(cv2.__version__)'

# Orb_Slam2
ARG Orb_Slam2_Path='/pyslam/OrbSlam2'
RUN cd /pyslam
RUN mkdir $Orb_Slam2_Path
RUN git clone https://github.com/GiordanoLaminetti/ORB_SLAM2 $Orb_Slam2_Path
WORKDIR $Orb_Slam2_Path
RUN ./build.sh
RUN cd $Orb_Slam2_Path/build
WORKDIR $Orb_Slam2_Path/build
RUN make install

# Orb_Slam3
ARG Orb_Slam3_Path='/pyslam/OrbSlam3'
RUN cd /pyslam
RUN mkdir $Orb_Slam3_Path
RUN git clone https://github.com/GiordanoLaminetti/ORB_SLAM3 $Orb_Slam3_Path
WORKDIR $Orb_Slam3_Path
RUN apt-get -y install qemu gcc-aarch64-linux-gnu
RUN apt-get -y install libboost-all-dev libpcap-dev libssl-dev
RUN ./build.sh
RUN cd $Orb_Slam3_Path/build
WORKDIR $Orb_Slam3_Path/build
RUN make install


# OrbSlam2-python Bindings
RUN which python3
ARG Orb_Slam2_PB_Path='/pyslam/OrbSlam2-PythonBinding'
RUN cd /pyslam
RUN mkdir $Orb_Slam2_PB_Path
RUN git clone https://github.com/GiordanoLaminetti/ORB_SLAM2-PythonBindings.git $Orb_Slam2_PB_Path
RUN mkdir $Orb_Slam2_PB_Path/build
WORKDIR $Orb_Slam2_PB_Path/build
RUN ln -s /usr/lib/x86_64-linux-gnu/libboost_python-py36.so \
         /usr/lib/x86_64-linux-gnu/libboost_python-py35.so
RUN apt-get -y install libeigen3-dev         
RUN ln -s /usr/include/eigen3/Eigen /usr/local/include/Eigen
RUN cmake ..
RUN make -j7
RUN make install
RUN ls /usr/local/lib/python3.6
RUN ln -s /usr/local/lib/python3.5/dist-packages/orbslam2.so \
         /usr/local/lib/python3.6/dist-packages/orbslam2.so
RUN python3 -c 'import orbslam2'

# OrbSlam3-python Bindings
RUN which python3
ARG Orb_Slam3_PB_Path='/pyslam/OrbSlam3-PythonBinding'
RUN cd /pyslam
RUN mkdir $Orb_Slam3_PB_Path
RUN ls -la
RUN git clone -b ORBSLAM3 https://github.com/GiordanoLaminetti/ORB_SLAM2-PythonBindings.git $Orb_Slam3_PB_Path
RUN mkdir $Orb_Slam3_PB_Path/build
WORKDIR $Orb_Slam3_PB_Path/build
RUN cmake ..
RUN make -j7
RUN make install
RUN ln -s /usr/local/lib/python3.5/dist-packages/orbslam3.so \
         /usr/local/lib/python3.6/dist-packages/
RUN python3 -c 'import orbslam3'

#remove all the folder
RUN rm -rf /pyslam/*
WORKDIR /pyslam
#change user
USER pyslam
COPY . /pyslam
EXPOSE 8888