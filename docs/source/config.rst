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

---------------------------------
Drawer Params
---------------------------------
See **setting.yaml** for examples values

- **Drawer.eye.x ** determines the x view point about the origin of this scene. 
- **Drawer.eye.y ** determines the y view point about the origin of this scene.
- **Drawer.eye.z ** determines the z view point about the origin of this scene.
- **Drawer.center.x ** determines the x plane translation about the origin of this scene.
- **Drawer.center.y ** determines the y plane translation about the origin of this scene.
- **Drawer.scale_grade.x ** determines the zoom about x plane.
- **Drawer.scale_grade.y ** determines the zoom about y plane.
- **Drawer.scale_grade.z **  (float): determines the zoom about z plane.
- **Drawer.aspectratio.x** to set the x-axis aspecratio. 
- **Drawer.aspectratio.y** to set the y-axis aspecratio.
- **Drawer.aspectratio.z** to set the z-axis aspecratio. 
- **Drawer.point_size** the size of the marker point in pixel.