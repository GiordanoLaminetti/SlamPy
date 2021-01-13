import slampy
import numpy as np
import yaml
import plotly.graph_objects as go
import time


class TrajectoryDrawer:
    """This class is used to print a the trajectory result from the slam method in a sequence of images, it use the Plotily library """

    def __init__(
        self,
        params_file,
        width=None,
        height=None,
        drawpointcloud=True,
        useFigureWidget=True,
    ):
        """Build the Trajectory drawer

        Args:
            params_file (str): the Path to the .yaml file.
            width(int): the width of figure in pixel. Defaults to None
            height(int): the height of figure in pixel. Defaults to None
            drawpointcloud (bool): if is false the plot show only trajectory and not the point cloud. Defaults to True
            useFigureWidget (bool): use the plotily.graph_object.FigureWidget instance if false it used the plotily.graph_object.Figure
        """
        with open(params_file) as fs:
            self.params = yaml.safe_load(fs)

        self.eye_x = self.params["Drawer.eye.x"]
        self.eye_y = self.params["Drawer.eye.y"]
        self.eye_z = self.params["Drawer.eye.z"]
        self.center_x = self.params["Drawer.center.x"]
        self.center_y = self.params["Drawer.center.y"]
        self.scale_grade_x = self.params["Drawer.scale_grade.x"]
        self.scale_grade_y = self.params["Drawer.scale_grade.y"]
        self.scale_grade_z = self.params["Drawer.scale_grade.z"]
        self.point_size = self.params["Drawer.point_size"]
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
                aspectratio=dict(
                    x=self.params["Drawer.aspectratio.x"],
                    y=self.params["Drawer.aspectratio.y"],
                    z=self.params["Drawer.aspectratio.z"],
                ),
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
            pose = slampy_app.get_pose_to_target()
            depth = slampy_app.get_depth()

            if self.drawpointcloud:
                # get the colored point cloud
                points_colored = slampy_app.get_point_cloud_colored()

                # convert the camera coordinates to world coordinates
                cp, colors = zip(*points_colored)
                wp = np.array([np.dot(pose, point)[0:3] for point in cp]).reshape(-1, 3)

                # draw the point cloud
                self.figure.add_scatter3d(
                    x=wp[..., 0] * -1,
                    y=wp[..., 1] * -1,
                    z=wp[..., 2],
                    mode="markers",
                    marker=dict(
                        size=self.point_size,
                        color=colors,
                    ),
                    hoverinfo="skip",
                )

            # get the camera center in absolute coordinates
            camera_center = pose[0:3, 3].flatten()
            if self.prec_camera_center is not None:
                self.figure.add_scatter3d(
                    x=np.array([camera_center[0], self.prec_camera_center[0]]).flatten()
                    * -1,
                    y=np.array([camera_center[1], self.prec_camera_center[1]]).flatten()
                    * -1,
                    z=np.array(
                        [camera_center[2], self.prec_camera_center[2]]
                    ).flatten(),
                    marker=dict(
                        size=self.point_size * 2, color="red", symbol="diamond"
                    ),
                    line=dict(width=self.point_size, color="red"),
                    hoverinfo="skip",
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
