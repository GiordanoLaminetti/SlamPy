
#!bin/bash
data="/media/Datasets/TUM/freiburg3_convert"
settings="./settings_tum.yaml"
save_path="./results_freiburg3"
poseid=1
type='TUM'
gt_depth_path="/media/Datasets/TUM/freiburg3_convert/depth"
gt_pose_dir="/media/Datasets/TUM/freiburg3_convert/pose/npy_pose"
gt_pose_txt="/media/Datasets/TUM/freiburg3_convert/pose/tum_gt_pose.txt"
names_to_plot="freiburg3"


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

