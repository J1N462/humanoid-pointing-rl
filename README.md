# Humanoid Deictic Pointing — RL Research

Unitree G1 휴머노이드의 **가리키기(deictic pointing) 모션**을 강화학습으로 제어하고,
공학적 reward만으로는 표현하기 어려운 동작 품질을 **human preference**로 보완하며,
그 개선이 **sim-to-real** 이식 후에도 유지되는지 검증하는 연구.

> 핵심 관점: *휴머노이드 RL·제어*가 주제이며, human preference는 reward 설계의 한계를 보완하는 **도구**로 사용한다.

---

## 환경 / 스택

- **Simulation**: Isaac Sim 5.1, Isaac Lab
- **RL**: PPO (rsl_rl), AMP (skrl)
- **Robot / OS**: Unitree G1, Ubuntu 24.04, ROS2 Jazzy
- **GPU**: RTX 5070 (12GB)

---

## 연구 개요

| 단계 | 내용 |
|---|---|
| 문제의식 | 동작의 "자연스러움·표현력"은 reward 수식으로 정의하기 어렵다 — reward 설계의 한계 |
| 접근 | 가리키기를 testbed로, 정량 reward로 학습한 정책의 품질을 human preference로 보완 |
| 검증 | 개선된 정책이 실제 G1으로 이식(sim-to-real)된 후에도 유지되는지 확인 |

---

## 진행 현황

### 완료
- [x] RL 개발환경 구축 (Isaac Sim 5.1 / Isaac Lab / ROS2)
- [x] **G1 보행 baseline 학습** — `Isaac-Velocity-Flat-G1-v0`, PPO
  (mean reward −7 → 28.95, 속도 추종 0.94, 낙상률 0.36%)
- [x] **모션 모방(AMP) 학습** — `Isaac-Humanoid-AMP-Dance`, skrl (80k steps)
- [x] **가리키기 task 제작** — `manipulation/reach`를 G1으로 이식 (`Isaac-Reach-G1-v0`)
- [x] reward 정체(-2) 원인 진단 및 해결 → 위치 기반 가리키기 학습 성공

### 진행 / 예정
- [ ] **"손→목표 방향 벡터" 기반 pointing reward 설계** (핵심 다음 단계)
- [ ] human preference를 보조 reward로 결합 (preference-based RL)
- [ ] 정량 지표 vs 인간 선호도 비교 분석
- [ ] sim-to-real 이식 (실물 G1 — 시뮬/실물 모델 차이 고려)

---

## 가리키기 task 제작 요약

Isaac Lab의 `reach`(테이블 위 산업용 팔 reaching) task를 G1 휴머노이드 가리키기용으로 이식.

**주요 변경**
- 로봇: `FRANKA_PANDA_CFG` → `G1_CFG`
- end-effector: `panda_hand` → `right_palm_link`
- 제어 관절: franka 7DOF → G1 오른팔 5DOF (`right_shoulder_.*`, `right_elbow_.*`)
- 책상 제거, 하체 고정(`fix_root_link`)으로 균형 문제 분리 → 상체+팔만 학습

**디버깅으로 얻은 통찰**
- reach의 franka 전용 방향 제약(`pitch=π`)이 G1 손 축과 맞지 않아 팔이 꺾이고 reward가 −2에서 정체 → 방향 제약 제거로 해결
- reach는 "닿기(position)", pointing은 "향하기(direction)" — 본질이 다름.
  목표가 멀면 닿을 수 없으므로, **손→목표 방향 벡터** 기반 reward가 올바른 방향 (다음 단계)
- 시뮬 `G1_CFG`(손가락 포함)와 실물 G1 EDU(손목까지) 구조 차이 → sim-to-real 시 확인 필요

---

## 저장소 구조

```
g1_pointing_task/      G1 가리키기 task config (reach 이식)
  ├─ __init__.py            task 등록 (Isaac-Reach-G1-v0)
  └─ joint_pos_env_cfg.py   G1 reach/pointing 환경 설정
plot_rewards.py        학습 로그(CSV) 시각화 스크립트
*.csv                  학습 지표 데이터 (보행 baseline)
*.png                  reward 곡선 그래프
```

---

## 데모

- `g1_pointing_v1` — 방향 제약으로 팔이 꺾이던 상태 (before)
- `g1_pointing_v2` — 제약 제거 후 목표로 뻗는 상태 (after)
- G1 보행 baseline 시연 영상

*(영상 및 상세 진행 기록은 별도 공유)*
