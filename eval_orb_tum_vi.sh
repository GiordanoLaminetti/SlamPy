
#!bin/bash
data="Dataset/TUM_VI/dataset-corridor4_512_16"
settings="./settings_TUM_VI.yaml"
save_path="./results_tum_vi_corrido4"
poseid=1
type='TUM_VI'
gt_depth_path=
gt_pose_dir="/Dataset/TUM_VI/dataset-corridor4_512_16/dso/gt_imu.csv"
gt_pose_txt=
names_to_plot="TUM_VI_corridor4"


python3 run_MONO_IMU.py	--dataset $data \
				--settings $settings \
				--dest $save_path  \
				--pose_id $poseid \
                                --data_type $type \

                                --gt_pose_dir $gt_pose_dir\
                                --named $names_to_plot\
		
                                --is_bash \
				

