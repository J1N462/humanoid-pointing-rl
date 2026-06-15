# Humanoid Gait Transition — RL Research

Unitree G1 휴머노이드의 보행 시작(gait initiation)과 정지(stopping) 전환 구간을
강화학습으로 학습하고, 정량 지표와 인간 선호도 비교로 평가하는 연구.

## 환경
- Isaac Sim 5.1 / Isaac Lab
- PPO (rsl_rl), AMP (skrl)
- Unitree G1, Ubuntu 24.04, ROS2 Jazzy

## 진행 현황
- [x] 개발환경 구축 (Isaac Sim / Isaac Lab)
- [x] G1 보행 baseline 학습 (Isaac-Velocity-Flat-G1-v0, PPO)
- [x] 모션 모방(AMP) 학습 실험 (Humanoid-AMP-Dance)
- [ ] 전환(stand→walk→stop) 명령 프로파일 설계
- [ ] 상체 진동 가중치 ablation
- [ ] 정량 지표 + 인간 선호도 평가

## 구조
- `plot_rewards.py` — 학습 로그 시각화
- `*.csv` — 학습 지표 데이터
