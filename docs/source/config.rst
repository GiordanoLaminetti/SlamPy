=======================
settings.yaml
=======================
.. _settings:

it is the configuration file and it is used to change the current algorithm and the other parameters of the algorithm.

----------------------------
change the current algorithm
----------------------------

To change the algorithm settings you can modify the **setting.yaml** file in the line ::

    SLAM.alg:'insert here your .py file that contains the wrapper class'

---------------------------------
ORB_SLAM2 and ORB_SLAM3 settings
---------------------------------

the other params for the ORB_SLAM2/3 algorithm are :

- **SLAM.vocab_path**: "Path to the ORB_SLAM2/3 vocabular file"
- **SLAM.settings_path**: "Path to the ORB_SLAM2/3 .yaml settings file"

---------------------------------
add your own settings
---------------------------------

if you add your method with :ref:`this <addmethod>` you can add in **settings.yaml** the params needed for your application execution in the form ::

    params_name : 'params_values'
