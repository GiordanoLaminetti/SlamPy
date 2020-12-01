data="/media/Datasets/KITTI_VO/dataset/sequences/10"
settings="./settings_kitty.yaml"
save_path="./results_kitty_vo_10"
poseid=-1
type="KITTI_VO"
gt_depth_path="/media/Datasets/KITTI_VO_SGM/10/depth"
gt_pose_dir="/media/Datasets/KITTI_VO_SGM/10/npy_pose"
#gt_pose_dir="/media/Datasets/KITTI_VO_SGM/npy_depth"
gt_pose_txt="/media/Datasets/KITTI_VO/dataset/poses/10.txt"
names_to_plot="kitty_vo_10"


python run.py	--dataset $data \
				--settings $settings \
				--dest $save_path  \
				--pose_id $poseid \
                                --data_type $type \
                                --gt_depth $gt_depth_path\
                                --gt_pose_dir $gt_pose_dir\
                                --gt_pose_txt $gt_pose_txt\
                                --named $names_to_plot\
				--is_evalute_depth  \
				--is_evalute_pose  \
                                --is_bash \
				$extras
