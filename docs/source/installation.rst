=======================
Installation
=======================
.. _installation: 

this project require the installiation of at least one of the supported algorithm, each installation is describet in it's section.
We also provide a Docker container on DockerHub, but you can also build your own container all the instruction see :ref:`Docker container <docker_container>`. 

Install ORB_SLAM2
----------------------

for ORB_SLAM2 you need to install a modify version of the original that can be found at `ORB_SLAM2 <https://github.com/GiordanoLaminetti/ORB_SLAM2>`_ ,

after you have correctly installed the C++ version you need to install the python wrapper form here `ORB_SLAM2-PythonBindings <https://github.com/GiordanoLaminetti/ORB_SLAM2-PythonBindings>`_  


Install ORB_SLAM3
----------------------

similar to ORB_SLAM2 for ORB_SLAM3 we use a modify version of ORB_SLAM3 that can be found at `ORB_SLAM3 <https://github.com/GiordanoLaminetti/ORB_SLAM3>`_  

after you have correctly installed the C++ version you need to install the python wrapper form here `ORB_SLAM2-PythonBindings <https://github.com/GiordanoLaminetti/ORB_SLAM2-PythonBindings>`_  

Install Slampy
---------------------
you need to install poetry , the istrucntion can be found at this `link <https://python-poetry.org/docs/#installation>`_ 

after the installation of dependences you can download the repo ::
   
    git clone https://github.com/GiordanoLaminetti/SlamPy.git

enter in the root folder and type  ::

    poetry shell

this create a python venv in which install all the requirements