ARG base_container=ubuntu:18.04
FROM $base_container
USER root

ARG build_dependences=true

RUN if $build_dependences ; then \
				useradd -d /slampy slampy ;\
				mkdir /slampy; \
				chown -R slampy:slampy /slampy ; \
				apt-get update  && apt-get install -y git wget unzip tmux pkg-config \
																									libglew-dev python3-dev \
																									python3-pip cmake ffmpeg \
																									libgl1-mesa-dev libavcodec-dev \
																									libavutil-dev libavformat-dev \
																									libswscale-dev libavdevice-dev \
																									libdc1394-22-dev libraw1394-dev \
																									libjpeg-dev libtiff5-dev \
																									libopenexr-dev \
																									qemu gcc-aarch64-linux-gnu \
																									libboost-all-dev libpcap-dev libssl-dev; \
				python3 -mpip install numpy pyopengl Pillow pybind11 jupyter matplotlib \
															pandas pyyaml ; fi


# Pangolin installation

ARG Pangolin_Path='/slampy/Pangolin'
ARG build_dependences=true

RUN mkdir $Pangolin_Path
RUN if $build_dependences ; then \
				git clone https://github.com/stevenlovegrove/Pangolin.git $Pangolin_Path ;  \
				fi

RUN mkdir $Pangolin_Path/build
WORKDIR $Pangolin_Path/build

RUN if $build_dependences ; then \
			cd  $Pangolin_Path/build ;\
			cmake  $Pangolin_Path ;\
			make -j7; \
			make install; fi

#Eigen installation
ARG Eigen_Path='/slampy/Eigen'
ARG build_dependences=true

RUN mkdir $Eigen_Path
RUN if $build_dependences ; then \
			git clone https://gitlab.com/libeigen/eigen.git $Eigen_Path ; fi
RUN mkdir $Eigen_Path/build
WORKDIR $Eigen_Path/build
RUN if $build_dependences ; then \
			cd  $Eigen_Path/build ;\
			cmake  $Eigen_Path ;\
			make -j7; \
			make install; fi

# OpenCV installation
ARG opencv_Path='/slampy/opencv-3.4.11'
ARG opencv_contrib_Path='/slampy/opencv_contrib-3.4.11'
ARG build_dependences=true

RUN mkdir $opencv_Path
RUN if $build_dependences ; then \
				wget https://github.com/opencv/opencv/archive/3.4.11.zip ; \
				unzip 3.4.11.zip -d /slampy ;\
				rm 3.4.11.zip; \
				wget https://github.com/opencv/opencv_contrib/archive/3.4.11.zip ;\
				unzip 3.4.11.zip -d /slampy ;\
				rm 3.4.11.zip; fi

RUN cd $opencv_Path
RUN mkdir $opencv_Path/build

WORKDIR $opencv_Path/build
RUN if $build_dependences ; then \
				cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local \
        				OPENCV_EXTRA_MODULES_PATH=$opencv_contrib_Path  .. ; \
			  make -j7 ;\
				make install ; \
				pip3 install --upgrade pip ;\
				python3 -mpip install opencv-contrib-python==3.4.11.45; fi


# Orb_Slam2 installation
ARG Orb_Slam2_Path='/slampy/OrbSlam2'
ARG build_orbslam2=true

RUN mkdir $Orb_Slam2_Path
RUN if $build_orbslam2 ; then \
				git clone https://github.com/GiordanoLaminetti/ORB_SLAM2 $Orb_Slam2_Path; fi

RUN mkdir $Orb_Slam2_Path/build
WORKDIR $Orb_Slam2_Path

RUN if $build_orbslam2 ; then \
				./build.sh 2>/dev/null; \
				cd $Orb_Slam2_Path/build; fi

WORKDIR $Orb_Slam2_Path/build
RUN if $build_orbslam2 ; then \
				make install ; fi


# Orb_Slam3
ARG Orb_Slam3_Path='/slampy/OrbSlam3'
ARG build_orbslam3=true

RUN mkdir $Orb_Slam3_Path
RUN if $build_orbslam3 ; then \
				git clone https://github.com/GiordanoLaminetti/ORB_SLAM3 $Orb_Slam3_Path; fi
RUN mkdir $Orb_Slam3_Path/build

WORKDIR $Orb_Slam3_Path
RUN if $build_orbslam3 ; then \
				./build.sh 2>/dev/null ; fi

WORKDIR $Orb_Slam3_Path/build
RUN if $build_orbslam3 ; then \
				make install; fi


# OrbSlam2-python Bindings
ARG Orb_Slam2_PB_Path='/slampy/OrbSlam2-PythonBinding'
ARG build_orbslam2=true

RUN if [ ! -L "/usr/lib/x86_64-linux-gnu/libboost_python-py35.so" ]; then \
 								ln -s /usr/lib/x86_64-linux-gnu/libboost_python-py36.so \
								/usr/lib/x86_64-linux-gnu/libboost_python-py35.so ; fi
RUN	apt-get update ; apt-get -y install libeigen3-dev
RUN if [ ! -L "/usr/local/include/Eigen" ]; then\
			ln -s /usr/include/eigen3/Eigen /usr/local/include/Eigen ; fi
RUN mkdir $Orb_Slam2_PB_Path
RUN if $build_orbslam2 ; then \
				git clone https://github.com/GiordanoLaminetti/ORB_SLAM2-PythonBindings.git \
						$Orb_Slam2_PB_Path ; fi

RUN mkdir $Orb_Slam2_PB_Path/build
WORKDIR $Orb_Slam2_PB_Path/build

RUN if $build_orbslam2 ; then \
				cmake .. ;\
				make -j7 ;\
				make install ;\
				ln -s /usr/local/lib/python3.5/dist-packages/orbslam2.so \
         			/usr/local/lib/python3.6/dist-packages/orbslam2.so ; fi

# OrbSlam3-python Bindings
ARG Orb_Slam3_PB_Path='/slampy/OrbSlam3-PythonBinding'
ARG build_orbslam3=true

RUN mkdir $Orb_Slam3_PB_Path
RUN if $build_orbslam3 ; then \
				git clone -b ORBSLAM3 https://github.com/GiordanoLaminetti/ORB_SLAM2-PythonBindings.git \
						$Orb_Slam3_PB_Path ; fi

RUN mkdir $Orb_Slam3_PB_Path/build
WORKDIR $Orb_Slam3_PB_Path/build

RUN if $build_orbslam3 ; then \
				cmake .. ;\
				make -j7 ;\
				make install ;\
				ln -s /usr/local/lib/python3.5/dist-packages/orbslam3.so \
         			/usr/local/lib/python3.6/dist-packages/ ;fi

#remove all the folder
WORKDIR /slampy
RUN rm -rf /slampy/*
RUN ldconfig
#change user
USER slampy
COPY . /slampy/slampy
WORKDIR /slampy/slampy
EXPOSE 8888

