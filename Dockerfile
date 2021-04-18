ARG base_container=ubuntu:18.04
FROM $base_container
USER root

ARG build_dependences=true

RUN if $build_dependences ; then \
				useradd -d /slampy slampy ;\
				mkdir /slampy; \
				chown -R slampy:slampy /slampy ; \
				apt-get update ;\
				apt-get install -y software-properties-common ;\
				add-apt-repository -y ppa:deadsnakes/ppa;\
				apt-get update  && apt-get install -y --no-install-recommends git wget unzip tmux pkg-config curl \
																									libglew-dev python3.8-dev \
																									python3-pip python3.8-venv \
																									cmake ffmpeg \
																									libgl1-mesa-dev libavcodec-dev \
																									libavutil-dev libavformat-dev \
																									libswscale-dev libavdevice-dev \
																									libdc1394-22-dev libraw1394-dev \
																									libjpeg-dev libtiff5-dev \
																									libopenexr-dev libeigen3-dev \
																									qemu gcc-aarch64-linux-gnu build-essential \
																									libboost-all-dev libpcap-dev libssl-dev g++ ;\
				ldconfig ;\
				rm -rf /var/lib/apt/lists/* && apt-get clear ;\
				python3 -mpip install numpy pyopengl Pillow pybind11 pandas  ; \
				update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1;\
				update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2;\
				python3 -mpip install poetry setuptools ; \
				mkdir /slampy/program; fi

# Pangolin installation
ARG Pangolin_Path='/slampy/program/Pangolin'
ARG build_dependences=true

RUN if $build_dependences ; then \
				mkdir $Pangolin_Path && \
				git clone https://github.com/stevenlovegrove/Pangolin.git $Pangolin_Path && \
				cd $Pangolin_Path && \
				mkdir $Pangolin_Path/build && \
				cd build && \
				cmake $Pangolin_Path && \
				make -j$(nproc) &&\
				make install ;  fi



#Eigen installation
ARG Eigen_Path='/slampy/program/Eigen'
ARG build_dependences=true

RUN if $build_dependences ; then \
			mkdir $Eigen_Path && \
			git clone https://gitlab.com/libeigen/eigen.git $Eigen_Path && \
			mkdir $Eigen_Path/build && \
			cd  $Eigen_Path/build &&\
			cmake  $Eigen_Path &&\
			make -j$(nproc) && \
			make install; fi

# OpenCV installation
ARG opencv_Path='/slampy/program/opencv-3.4.11'
ARG opencv_contrib_Path='/slampy/program/opencv_contrib-3.4.11'
ARG build_dependences=true

RUN if $build_dependences ; then \
				mkdir $opencv_Path &&\
				wget https://github.com/opencv/opencv/archive/3.4.11.zip && \
				unzip 3.4.11.zip -d /slampy/program &&\
				rm 3.4.11.zip && \
				wget https://github.com/opencv/opencv_contrib/archive/3.4.11.zip && \
				unzip 3.4.11.zip -d /slampy/program && \
				rm 3.4.11.zip && \
				cd $opencv_Path && \
				mkdir $opencv_Path/build &&\
				cd $opencv_Path/build &&\
				cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local \
        				OPENCV_EXTRA_MODULES_PATH=$opencv_contrib_Path  .. && \
			  	make -j$(nproc) &&\
				make install && \
				pip3 install --upgrade pip &&\
				python3 -mpip install opencv-contrib-python==3.4.11.45; fi


# Orb_Slam2 installation
ARG Orb_Slam2_Path='/slampy/program/OrbSlam2'
ARG build_orbslam2=true

RUN if $build_orbslam2 ; then \
				mkdir -p $Orb_Slam2_Path && \
				git clone https://github.com/GiordanoLaminetti/ORB_SLAM2 $Orb_Slam2_Path && \
				mkdir $Orb_Slam2_Path/build &&  \
				cd $Orb_Slam2_Path &&\
				./build.sh 2>/dev/null &&  \
				cd $Orb_Slam2_Path/build && \
				make install ; fi


# Orb_Slam3
ARG Orb_Slam3_Path='/slampy/program/OrbSlam3'
ARG build_orbslam3=true

RUN if $build_orbslam3 ; then \
				mkdir -p $Orb_Slam3_Path && \
				git clone https://github.com/GiordanoLaminetti/ORB_SLAM3 $Orb_Slam3_Path && \
	 			mkdir $Orb_Slam3_Path/build && \
				cd $Orb_Slam3_Path &&\
				./build.sh 2>/dev/null && \
				cd $Orb_Slam3_Path/build &&\
				make install; fi


# OrbSlam2-python Bindings
ARG Orb_Slam2_PB_Path='/slampy/program/OrbSlam2-PythonBinding'
ARG build_orbslam2=true


RUN	 if [ ! -L "/usr/local/include/Eigen" ]; then\
			ln -s /usr/include/eigen3/Eigen /usr/local/include/Eigen ; fi

RUN if $build_orbslam2 ; then \
				mkdir -p $Orb_Slam2_PB_Path && \
				git clone https://github.com/GiordanoLaminetti/ORB_SLAM2-PythonBindings.git \
						$Orb_Slam2_PB_Path && \
				mkdir $Orb_Slam2_PB_Path/build && \
				cd $Orb_Slam2_PB_Path/build && \
				cmake $Orb_Slam2_PB_Path &&\
				make -j$(nproc) &&\
				make install; fi

# OrbSlam3-python Bindings
ARG Orb_Slam3_PB_Path='/slampy/program/OrbSlam3-PythonBinding'
ARG build_orbslam3=true

RUN mkdir $Orb_Slam3_PB_Path
RUN if $build_orbslam3 ; then \
				mkdir -p $Orb_Slam3_PB_Path && \
				git clone -b ORBSLAM3 https://github.com/GiordanoLaminetti/ORB_SLAM2-PythonBindings.git \
						$Orb_Slam3_PB_Path &&\
				mkdir $Orb_Slam3_PB_Path/build && \
				cd $Orb_Slam3_PB_Path/build && \
				cmake .. &&\
				make -j$(nproc) &&\
				make install ;fi

#remove all the folder
WORKDIR /slampy
RUN rm -rf /slampy/program && ldconfig

#change user
USER slampy

COPY . /slampy/slampy
WORKDIR /slampy/slampy

RUN poetry config virtualenvs.create false && poetry install --no-root
ENV PATH /slampy/.local/bin:$PATH
RUN jupyter nbextension enable --py widgetsnbextension && jupyter nbextension enable --py plotlywidget

EXPOSE 8888
