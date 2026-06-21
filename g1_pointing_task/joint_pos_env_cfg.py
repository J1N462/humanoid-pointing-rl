# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import math

from isaaclab.utils import configclass

import isaaclab_tasks.manager_based.manipulation.reach.mdp as mdp
from isaaclab_tasks.manager_based.manipulation.reach.reach_env_cfg import ReachEnvCfg

##
# Pre-defined configs
##
from isaaclab_assets import G1_CFG  # isort: skip


##
# Environment configuration
##


@configclass
class G1ReachEnvCfg(ReachEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # switch robot to G1
        self.scene.robot = G1_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
        # 책상 제거 
        self.scene.table = None
        # G1 몸통 고정해서 균형 문제 제거, 상체+팔만 학습
        self.scene.robot.spawn.articulation_props.fix_root_link = True
        # override rewards
        self.rewards.end_effector_position_tracking.params["asset_cfg"].body_names = ["right_palm_link"]
        self.rewards.end_effector_position_tracking_fine_grained.params["asset_cfg"].body_names = ["right_palm_link"]
        self.rewards.end_effector_orientation_tracking.params["asset_cfg"].body_names = ["right_palm_link"]
        # 가리키기: 손 절대각도 제약 제거 (방향추종 off → 안 꺾임)
        self.rewards.end_effector_orientation_tracking.weight = 0.0

        # override actions
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot", joint_names=["right_shoulder_.*","right_elbow_.*"], scale=0.5, use_default_offset=True)
        # override command generator body
        # end-effector is along z-direction
        self.commands.ee_pose.body_name = "right_palm_link"
        self.commands.ee_pose.ranges.pitch = (math.pi, math.pi)
        # 목표 위치를 G1 팔이 닿는 앞쪽으로 조정
        self.commands.ee_pose.ranges.pos_x = (0.2, 0.45)
        self.commands.ee_pose.ranges.pos_y = (-0.35, 0.0)
        self.commands.ee_pose.ranges.pos_z = (-0.1, 0.25)

@configclass
class G1ReachEnvCfg_PLAY(G1ReachEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
