import slampy
import numpy as np
import plotly.graph_objects as go
import time


class TrajectoryDrawer:
    """This class is used to print a the trajectory result from the slam method in a sequence of images, it use the Plotily library """

    def __init__(
        self,
        eye_x=-18.0,
        eye_y=-13.0,
        eye_z=-55.0,
        center_x=-17.0,
        center_y=-8.0,
        scale_grade_x=1.0,
        scale_grade_y=1.0,
        scale_grade_z=10.0,
        aspectratio=dict(x=50, y=50, z=100),
        width=None,
        height=None,
        point_size=2,
        drawpointcloud=True,
        useFigureWidget=True,
    ):
        """Build the Trajectory drawer
        Args:
            eye_x (float): determines the x view point about the origin of this scene. Defaults to -18.0
            eye_y (float): determines the y view point about the origin of this scene. Defaults to -13.0
            eye_z (float): determines the z view point about the origin of this scene. Defaults to -55.0
            center_x (float): determines the x plane translation about the origin of this scene. Defaults to -17.0
            center_y (float): determines the y plane translation about the origin of this scene. Defaults to -8.0
            scale_grade_x (float): determines the zoom about x plane. Defaults to 1
            scale_grade_y (float): determines the zoom about y plane. Defaults to 1
            scale_grade_z (float): determines the zoom about z plane. Defaults to 10
            aspectratio (dict): a dict in the form (x=(int), y=(int), z=(int)) to set the scene aspecratio Defaults to dict(x=50, y=50, z=100)
            width(int): the width of figure in pixel. Defaults to None
            height(int): the height of figure in pixel. Defaults to None
            point_size (int): the size of the marker point in pixel. Defauts to 2
            drawpointcloud (bool): if is false the plot show only trajectory and not the point cloud. Defaults to True
            useFigureWidget (bool): use the plotily.graph_object.FigureWidget instance if false it used the plotily.graph_object.Figure
        """
        self.eye_x = eye_x
        self.eye_y = eye_y
        self.eye_z = eye_z
        self.center_x = center_x
        self.center_y = center_y
        self.scale_grade_x = scale_grade_x
        self.scale_grade_y = scale_grade_y
        self.scale_grade_z = scale_grade_z
        self.point_size = point_size
        self.drawpointcloud = drawpointcloud
        # initialize the figure
        if useFigureWidget == True:
            self.figure = go.FigureWidget()
        else:
            self.figure = go.Figure()
        # hide the axis and change the aspect ratio
        self.figure.update_layout(
            showlegend=False,
            width=width,
            height=height,
            scene=dict(
                aspectmode="manual",
                aspectratio=aspectratio,
                xaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    visible=False,
                    autorange=False,
                ),
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    visible=False,
                    autorange=False,
                ),
                zaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    visible=False,
                    autorange=False,
                ),
            ),
        )
        self.prec_camera_center = None

    def get_figure(self):
        """Return the figure"""
        return self.figure

    def plot_trajcetory(self, slampy_app):
        """Compute the trajectory and add it to the figure
        Args:
            slampy_app (Slampy): the slampy instance used to compute the pose in the image
        """
        if slampy_app.get_state() == slampy.State.OK:
            # get the depth and pose
            pose = slampy_app.get_pose()
            depth = slampy_app.get_depth()

            if self.drawpointcloud:
                # get the colored point cloud
                points_colored = slampy_app.get_point_cloud_colored()

                # convert the camera coordinates to world coordinates
                cp, colors = zip(*points_colored)
                wp = np.array([np.dot(pose, point)[0:3] for point in cp]).reshape(-1, 3)

                # draw the point cloud
                self.figure.add_scatter3d(
                    x=wp[..., 0],
                    y=wp[..., 1] * -1,
                    z=wp[..., 2],
                    mode="markers",
                    marker=dict(
                        size=self.point_size,
                        color=colors,
                    ),
                )

            # get the camera center in absolute coordinates
            camera_center = pose[0:3, 3].flatten()
            if self.prec_camera_center is not None:
                self.figure.add_scatter3d(
                    x=np.array(
                        [camera_center[0], self.prec_camera_center[0]]
                    ).flatten(),
                    y=np.array([camera_center[1], self.prec_camera_center[1]]).flatten()
                    * -1,
                    z=np.array(
                        [camera_center[2], self.prec_camera_center[2]]
                    ).flatten(),
                    marker=dict(
                        size=self.point_size * 2, color="red", symbol="diamond"
                    ),
                    line=dict(width=self.point_size, color="red"),
                )
                self.figure.update_layout(
                    scene_camera=dict(
                        eye=dict(
                            x=self.eye_x + camera_center[0] * self.scale_grade_x,
                            y=self.eye_y + camera_center[1] * self.scale_grade_y,
                            z=self.eye_z + camera_center[2] * self.scale_grade_z,
                        ),
                        up=dict(x=0, y=1, z=0),
                        center=dict(
                            x=self.center_x + camera_center[0] * self.scale_grade_x,
                            y=self.center_y + camera_center[1] * self.scale_grade_y,
                            z=camera_center[2] * self.scale_grade_z,
                        ),
                    ),
                ),
            self.prec_camera_center = camera_center
            return self.figure.layout.scene
