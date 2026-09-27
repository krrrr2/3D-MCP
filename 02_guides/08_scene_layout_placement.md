# 배치·레이아웃 가이드: 관계 제약, 솔버, 검증 루프

> 기준일: 2026-09-27 · LLM에게 좌표를 직접 찍게 하지 말고, **LLM은 관계 제약 → 솔버는 좌표 → 스크립트는 충돌·부유·동선 검사 → VLM은 top-down과 4뷰 렌더 채점**으로 역할을 나누세요. 2024~2026년 연구와 오픈소스 구현이 모두 이 구조로 모였습니다.

## 핵심 요약

- **좌표를 LLM이 직접 쓰면 충돌이 많이 납니다.** SceneReVis 저자들이 측정한 비교표(침실·거실 평균)에서 충돌률은 LayoutGPT(LLM 직접 좌표) 40.8%, LayoutVLM 36.8%, Holodeck(LLM 제약 + DFS 솔버) 12.7%, SceneReVis(렌더→평가→수정 루프 + 물리 보상 RL) 4.5%였습니다([SceneReVis 프로젝트 페이지](https://raw.githubusercontent.com/SceneReVis/SceneReVis.github.io/main/index.html)). 경쟁 논문이 잰 값이라 절대 수치보다 **경향**으로 읽으세요.
- **현재 합의된 구조는 4단계입니다.** ① LLM이 오브젝트 목록과 관계 제약(against_wall, facing, distance, on_top_of…)을 JSON으로 작성 → ② 솔버(DFS·MILP·gradient·simulated annealing)가 좌표를 풂 → ③ 충돌·부유·경계·동선·물리 안정성 검사 → ④ top-down 정사영과 측면 렌더를 VLM이 루브릭으로 채점. 수정 지시는 다시 ① 또는 ②로 돌아갑니다.
- **MCP로 이 구조를 직접 구현한 공개 사례**는 NVIDIA SAGE입니다. `server/layout.py`가 FastMCP로 `generate_room_layout`, `place_objects_in_room` 등을 노출하고, 배치는 Holodeck식 제약 + DFS(grid_size=20) + Shapely 충돌 검사로 풉니다([SAGE](https://github.com/NVlabs/sage)). 가장 완성도 높은 "에이전트 + 툴 + 비평" 레퍼런스는 SceneSmith(MIT)이고, 프롬프트 YAML이 그대로 실무 규칙집입니다([SceneSmith](https://github.com/nepfaff/scenesmith)).
- **배치 실패의 절반은 에셋 정규화 문제입니다.** 단위 m, 원점은 바닥 중앙, 정면 축 통일(Blender는 -Y, glTF 원본은 +Z), 회전·스케일 적용, 균일 스케일만 사용. Holodeck issue #92(정면 정렬), LayoutVLM issue #9(스케일·회전), I-Design의 `+π` 보정이 모두 여기서 나옵니다.
- **실무 레시피**: 에셋 정규화 → 초점·기능 그룹·동선 먼저 → 앵커 가구부터 계층 배치(바닥 → 벽걸이 → 천장 → 소품) → 객체당 제약 3~5개 → 솔버 → `scene_audit.py`로 관통·부유 검사 → 소품은 rigid body로 안착 → 4뷰 렌더 채점. 종료 조건은 SceneSmith 설정처럼 "6개 항목 모두 9점 이상이면 종료, 최대 3라운드, 점수가 떨어지면 체크포인트로 롤백"을 씁니다.
- **이 저장소의 테스트된 스크립트를 쓰세요.** [`placement_utils.py`](../03_playbooks/scripts/README.md)(바닥 스냅, 표면 위 올리기, 벽 붙이기, 바라보기, 간격 규칙 검사), `scene_audit.py`(관통·부유·박힘·천장 돌출·치수 JSON 리포트), `review_views.py`(위·정면·측면·3/4 검토 렌더), `building_audit.py`(문·창·방 연결·동선·계단의 건축 상식 검사와 백룸 위험도). Blender 4.2.23 LTS·5.0.1에서 테스트를 통과했습니다. 이 문서의 솔버·안착·산포 예제 코드도 같은 두 버전에서 실행해 확인했습니다.
- **수치 규칙은 출처마다 다릅니다.** 소파–커피테이블 간격만 해도 SceneSmith 0.3~0.5 m, Infinigen 0.45~0.6 m, 인테리어 가이드 356~457 mm입니다. 범위로 주고, 법규·최소 통로 같은 **하드 제약**과 디자인 관행인 **소프트 선호**를 나눠서 넣으세요.
- **[한국 사용자]** 한국 아파트는 천장고 2300 mm(구축) 또는 2400~2500 mm(최근 신축), 방문 900×2100 mm(문틀 기준), 매트리스 Q 1500×2000 mm입니다. 'King' 같은 이름 대신 mm 값을 넘기세요. SceneSmith·SceneAssistant가 쓰는 **Hunyuan3D-2 로컬 생성은 한국이 라이선스 적용 지역에서 빠져 있습니다.** Geometry Nodes 코드는 노드·소켓을 이름이 아니라 type·identifier로 찾아야 한국어 UI에서도 깨지지 않습니다.
- **야외·환경은 좌표가 아니라 산포 파라미터를 LLM에게 맡기세요.** Distribute Points on Faces의 Poisson Disk(Distance Min으로 최소 간격 보장) + 밀도 마스크(길·건물 주변 0) + 3·5·7개 클러스터 + 전경·중경·배경 밀도 차등이 기본입니다.
- **배치 품질을 공개 점수로 검증한 AAA급 AI+MCP 사례는 찾지 못했습니다.** 연구 시스템은 대부분 로보틱스 시뮬레이션용이라 조명·재질 미감은 따로 보강해야 합니다([조명·렌더 가이드](06_lighting_rendering_art_direction.md)).

---

## 1. 왜 LLM이 좌표를 직접 찍으면 실패하나

### 1.1 연구 수치: 충돌률·경계 이탈률 비교

SceneReVis 프로젝트 페이지의 비교표입니다(침실+거실 평균, 저자 측정). 수치는 1차 검증에서 원문과 일치함을 확인했습니다.

| 방법 | 좌표를 누가 정하나 | 경계 이탈 | 충돌 | 품질(0~10) |
|---|---|---|---|---|
| [LayoutGPT](https://github.com/weixi-feng/LayoutGPT) (NeurIPS 2023) | LLM이 few-shot 예시를 보고 직접 좌표 출력 | 24.7% | **40.8%** | 7.5 |
| [ReSpace](https://github.com/GradientSpaces/respace) (ICLR 2026) | 파인튜닝한 LLM이 편집 명령 출력 | 13.1% | 41.1% | — |
| [DiffuScene](https://github.com/tangjiapeng/DiffuScene) (CVPR 2024) | 확산 모델 | 37.1% | 37.7% | — |
| [LayoutVLM](https://github.com/sunfanyunn/LayoutVLM) (CVPR 2025) | VLM 초기값 + 미분 가능 최적화 | 12.9% | 36.8% | 7.7 |
| [I-Design](https://github.com/atcelen/IDesign) (ECCV 2024) | 멀티에이전트 scene graph + 백트래킹 | 16.7% | 16.2% | 7.8 |
| [Holodeck](https://github.com/allenai/Holodeck) (CVPR 2024) | LLM 관계 제약 + DFS 솔버 | 12.7% | **12.7%** | 7.8 |
| [SceneReVis](https://github.com/Runder-sun/SceneReVis) (2026-02) | 7B VLM, 렌더→평가→수정 반복 + 물리 보상 RL | **2.0%** | **4.5%** | 8.8 |

다른 벤치마크에서 나온 참고값:

- **SceneSmith**(저장소 설명상 ICML 2026 Spotlight): 기존 방법보다 객체 3~6배, 객체 간 충돌 0, 물리 시뮬레이션 후 96% 안정, 사용자 205명 연구에서 기준선 대비 평균 사실감 승률 92%·프롬프트 충실도 91%(논문 저자 자체 보고, [프로젝트 페이지](https://raw.githubusercontent.com/scenesmith/scenesmith.github.io/main/index.html)). arXiv 요약에는 충돌 "2% 미만"으로 적혀 있어([arXiv 2602.09153](https://arxiv.org/abs/2602.09153)) 두 표현을 함께 적습니다.
- **LayoutVLM 자체 논문**: 11개 방 유형 평균 PSA(Physically-Grounded Semantic Alignment, 물리적으로 타당하면서 지시와 맞는 정도) 58.8로 I-Design보다 40.8점 높고, 사용자 평가 순위도 LayoutGPT·Holodeck보다 좋았습니다([arXiv 2412.02193](https://arxiv.org/html/2412.02193), 검색 요약 기준, 신뢰도 중간). 지표에 따라 순위가 바뀝니다.
- **BlenderGym**: GPT-4o의 배치(Placement) 과제 광도 손실이 11.89로 사람(0.423)의 약 28배였습니다([BlenderGym](https://blendergym.github.io/), 보완 조사, 독립 재검증 없음).

**읽는 법**

1. LLM 직접 좌표(LayoutGPT)와 학습형 생성(DiffuScene, ReSpace)은 충돌이 37~41%입니다.
2. 충돌을 **하드 조건으로 막는** 솔버(Holodeck DFS, I-Design 백트래킹)는 12~16%로 떨어집니다.
3. LayoutVLM은 최적화를 쓰는데도 이 표에서는 36.8%였습니다. 충돌이 손실 함수의 한 항(soft)일 뿐이라 완전히 막히지 않기 때문으로 보입니다. 그러니 "솔버를 쓴다"보다 **"충돌을 하드 조건으로 막고, 배치 후 따로 검사한다"**가 핵심입니다.
4. 가장 낮은 값은 렌더→평가→수정 루프와 물리 검사를 합친 시스템(SceneReVis, SceneSmith)에서 나왔습니다.
5. 모두 저자·경쟁자 측정이고 GPT-4o 세대 결과가 많습니다. GPT-6 Astra, Claude Fable 5.1, Opus 5.5로 배치 과제를 비교한 자료는 **찾지 못했습니다(미확인)**.

### 1.2 LLM이 좌표를 쓸 때 반복되는 오류

| 오류 | 원인 | 구조적 해결 |
|---|---|---|
| 서로 겹침·벽 관통 | 좌표를 머릿속으로만 계산, 크기를 모름 | 솔버의 하드 충돌 조건 + BVH 검사 |
| 떠 있거나 바닥에 박힘 | LLM이 준 z값은 거의 항상 틀림. `location`은 원점 위치일 뿐 | z는 레이캐스트·bbox로 계산(`snap_to_floor`, `drop_to_surface`) |
| 180°·90° 방향 오류 | yaw 부호와 "0°가 어느 쪽인가" 규약이 섞임(LayoutVLM 0°=+X, Blender 정면=-Y) | 규약을 한 곳에 고정하고 facing은 공식으로 계산 |
| 크기 오류 | 에셋 스케일 정규화 누락 | 실측 m 기준 균일 스케일 + 메타데이터 |
| 문·동선 막힘 | 배치 후에 동선을 생각함 | 금지 영역(keep-out)을 먼저 깔고 배치 |
| '대기실' 배치(가구가 벽을 따라 흩어짐) | 초점·그룹 개념 없음 | 초점과 기능 그룹을 먼저 정의 |

---

## 2. 수렴된 구조: 4단계 루프

```
 ┌─────────────────────────────┐   ┌──────────────────────┐   ┌──────────────────────────┐   ┌──────────────────────────────┐
 │ ① LLM: 오브젝트 목록        │ → │ ② 솔버: x, y, yaw    │ → │ ③ 기하·물리 검사          │ → │ ④ VLM 비평                    │
 │   + 관계 제약(JSON)         │   │   (DFS/MILP/gradient/ │   │   충돌·부유·경계·동선·안정 │   │   top-down 정사영 + 측면 4뷰  │
 │   + 초점·그룹·동선          │   │    annealing)         │   │   (숫자로 판정)            │   │   루브릭 0~10점 + 수정 지시   │
 └─────────────────────────────┘   └──────────────────────┘   └──────────────────────────┘   └──────────────────────────────┘
          ↑                                                                                              │
          └──────────────── 수정: 제약 추가·삭제, 객체 교체·삭제 (점수 하락 시 체크포인트 롤백) ─────────────┘
```

| 단계 | 담당 | 출력 | 이 저장소에서 쓸 것 | 참고 구현 |
|---|---|---|---|---|
| ① 계획 | LLM(추론이 강한 모델) | 객체·치수·관계 제약 JSON | [프롬프트 템플릿](../03_playbooks/03_prompt_templates.md), 4.4절 JSON 예시 | Holodeck `prompts.py`, SAGE planner, LayoutVLM 제약 API |
| ② 좌표 | 솔버(결정적 코드) | (x, y, yaw) | 4.4절 격자 DFS 스케치, `placement_utils.py` | Holodeck DFS, LayoutVLM Adam, Infinigen annealing |
| ③ 검사 | 스크립트 | 위반 목록 JSON | `scene_audit.py`, `check_clearances()` | SceneSmith `check_physics`, SceneEval 기하 지표 4종 |
| ④ 비평 | VLM(시각이 강한 모델) | 항목별 점수 + (object_id, 문제, 이동 벡터) | `review_views.py` | SceneSmith critic, SceneReVis, LayoutVLM 좌표 마크 오버레이 |

**③을 ④보다 먼저 두는 이유**: VLM은 원근 이미지에서 거리를 잘 못 읽고 관통을 놓칩니다. Vibe3DScene이 VLM 시각 검사 위에 형상 관통 검사를 따로 붙인 것도 이 때문입니다. 숫자로 잡을 수 있는 것은 숫자로 먼저 잡고, VLM에게는 미감·의도·그룹 구성만 묻습니다.

---

## 3. 공개 구현 비교

### 3.1 에이전트·솔버 시스템

| 시스템 | 좌표 결정 | 검증 | Blender 연동 | MCP | 코드·라이선스 | 요구 사항 | 실무에서 가져올 것 |
|---|---|---|---|---|---|---|---|
| [Holodeck](https://github.com/allenai/Holodeck) (CVPR 2024) | LLM(gpt-4o-2024-05-13) 제약 + DFS(권장)/MILP. 회전 0/90/180/270°, 제약 가중치 global 1.0·relative/direction/alignment 0.5·distance 1.8 | Shapely 2D 충돌 | 없음(AI2-THOR/Unity 2020.3.25f1) | 없음 | Apache-2.0 | OpenAI API | 제약 어휘와 프롬프트 지침([prompts.py](https://raw.githubusercontent.com/allenai/Holodeck/main/ai2holodeck/generation/prompts.py)), DFS 로직([floor_objects.py](https://raw.githubusercontent.com/allenai/Holodeck/main/ai2holodeck/generation/floor_objects.py)) |
| [LayoutVLM](https://github.com/sunfanyunn/LayoutVLM) (CVPR 2025) | VLM(gpt-4o, 보조 gpt-4o-mini)이 그룹별 제약 프로그램 작성 → Adam(lr 0.01, ExponentialLR γ 0.96, 400 iter, 겹침 IoU×1000, 제약×100, 100 iter마다 방 경계 투영). trust-constr·dual_annealing 대안 | 렌더에 좌표 마크·이름 오버레이 | 렌더 스크립트만 | 없음 | **LICENSE 없음(미표기)** | Rotated_IoU CUDA 확장 빌드 | 제약 API 7종(MCP 툴 설계 템플릿), 좌표 오버레이 렌더([grad_solver.py](https://raw.githubusercontent.com/sunfanyunn/LayoutVLM/main/src/layoutvlm/grad_solver.py)) |
| [Infinigen Indoors](https://github.com/princeton-vl/infinigen) (CVPR 2024) | Python 제약 언어 + simulated annealing(추가·삭제·포즈·재할당·교환 move) | 하드 제약 + 비용항 | **Blender 네이티브**(.blend 출력) | 없음 | BSD-3 | 단일 방 coarse 단계 CPU 약 8~13분 | 제약 DSL의 모범([home.py v1.16.0](https://raw.githubusercontent.com/princeton-vl/infinigen/v1.16.0/infinigen_examples/constraints/home.py)). **v1.16.0 태그를 checkout할 것**(아래 주의) |
| [I-Design](https://github.com/atcelen/IDesign) (ECCV 2024) | 디자이너·건축가·엔지니어 에이전트 scene graph → 백트래킹 | GPT-V 렌더 채점 | `place_in_blender.py`로 glb import·배치 | 없음 | 라이선스 미표기 | GPT-4 계열 | Blender 배치 절차. 단 `+π` 보정과 비균일 스케일은 따라 하지 말 것 |
| [SceneWeaver](https://github.com/Scene-Weaver/SceneWeaver) (NeurIPS 2025) | reason-act-reflect 에이전트가 생성기들을 툴로 조합 | 자체 평가·수정 | Infinigen Blender 소켓 서버(`--socket`), UI에서 실시간 확인 | 소켓 브리지(blender-mcp와 같은 구조) | BSD-3 | `bpy==3.6.0` 고정, AzureOpenAI 기본 | 생성기 여러 개를 툴로 묶는 설계 |
| [SceneSmith](https://github.com/nepfaff/scenesmith) (ICML 2026 Spotlight, 저장소 설명 기준. README bibtex는 arXiv) | 5단계(평면도→가구→벽걸이→천장→소품), 단계마다 planner·designer·critic. 가구는 `add_furniture_to_scene_tool(asset_id, x, y, yaw°)`로 z=0 직립 배치 | `check_physics`(VHACD, 관통 임계 1 mm), `check_facing_tool`, `check_reachability`, 5초 물리 시뮬레이션 | Blender `house.blend` 출력, EEVEE Next 렌더 | 자체 툴 호출(MCP 아님) | **MIT** | 전체 파이프라인 GPU 45GB 이상 권장(L40S 테스트), OpenAI API(설정상 gpt-5.2) | 설정값·루브릭·종료/롤백 규칙 전체(4.8·4.9절) |
| [SAGE](https://github.com/NVlabs/sage) (arXiv 2602.10116, 큐레이션 목록상 CVPR 2026) | LLM이 객체당 Holodeck식 제약 4~5개 → DFS(grid_size=20, 시간 제한 max(300, n×60)초) | Shapely bbox 충돌(가로·세로 전체 치수에 +3.5 cm, 한쪽 약 1.75 cm), 소품은 후보 150개 샘플링 + physics critic | 언급 없음(USD/Isaac 중심) | **FastMCP 서버** | Apache-2.0(구성요소별 별도) | Slurm, Isaac Sim, 자체 모델 서버 | MCP 툴 설계와 배치 알고리즘([layout.py](https://raw.githubusercontent.com/NVlabs/sage/main/server/layout.py), [object_placement_planner.py](https://raw.githubusercontent.com/NVlabs/sage/main/server/objects/object_placement_planner.py)) |
| [SceneReVis](https://github.com/Runder-sun/SceneReVis) (arXiv 2602.09432) | 7B 모델(Qwen2.5-VL 기반, SFT + GRPO)이 add/move/rotate/scale/replace/remove 6개 원자 연산 호출 | overhead + diagonal 2뷰 렌더, voxel 물리(충돌·경계), VLM 0~10 채점 | Blender 4.0.2 렌더 | 없음 | MIT(코드·데이터·가중치) | 3D-FUTURE(승인 필요) | "2뷰 렌더 + 루브릭 + 원자 연산" 루프 |
| [HSM](https://github.com/3dlg-hcvc/hsm) (3DV 2026) / [SMC](https://github.com/3dlg-hcvc/smc) (3DV 2025) | 방→가구→소품 계층, 반복 배치 패턴(모티프)을 프로그램으로 | support region | SMC는 Blender 3.6 LTS에서 예시 작성 | 없음 | MIT | HSM: 씬당 약 $0.80·약 10분, HSSD 약 72GB(HF 라이선스 동의 필요) | 식탁 세팅·책장·욕실 소품을 `place_row`·`place_stack`·`place_grid` 같은 모티프 함수로 |
| [Code-as-Room](https://github.com/YxuanAr/Code-as-Room) (arXiv 2605.18451) | top-down 방 이미지 한 장 → 13단계(0~12, 8~9는 옵션) → Blender 코드 | — | Blender 3.6+/4.x | 없음 | Apache-2.0 | 초기 코드 | 사용자가 평면 스케치를 주는 워크플로의 근거 |
| [R³L](https://github.com/Neal2020GitHub/R3L) (ICML 2026) | 상대 관계로부터 레이아웃 추론(retriever/planner/solver), Holodeck·LayoutVLM 기반 | — | — | 없음 | MIT | 초기 코드 | 관계 → 좌표 분리 구조 |
| [VIGA](https://github.com/Fugtemypt123/VIGA) (arXiv 2601.11109) | Generator(씬 프로그램 작성)와 Verifier(다시점 렌더 비교)가 번갈아 동작 | 다시점 렌더 비교 | Blender 코드 에이전트, BlenderBench 공개 | 없음 | MIT | — | "레퍼런스 이미지 → Blender 씬 재현" 루프(1차 조사 누락 → 검증에서 추가) |

**주의 사항 (검증에서 나온 정정)**

- **Infinigen**: 최신 릴리스는 v2.0.0a2 알파(procfunc 기반 전면 재작성)이고, 2.0은 "간단한 실내 배치만 있는 preview"입니다([Infinigen2.md](https://raw.githubusercontent.com/princeton-vl/infinigen/main/docs/source/Infinigen2.md)). main 브랜치에서는 v1 Indoors 코드(`generate_indoors.py`, `constraints/home.py`)가 **삭제됐는데** main의 HelloRoom 문서는 여전히 v1 명령을 안내합니다. v1 제약 솔버를 쓰려면 `git checkout v1.16.0`을 하세요. 외부 에셋(Objaverse 등)은 v1.8.0부터 공식 가이드([StaticAssets.md](https://raw.githubusercontent.com/princeton-vl/infinigen/v1.16.0/docs/StaticAssets.md))로 배치 시스템에 넣을 수 있습니다. 전체 씬 내보내기는 USDC만 되고 재질은 Albedo·Roughness·Normal·Metallic만 베이크됩니다.
- **SAGE**: "문 회전반경 약 90 cm"는 LLM 프롬프트 문구일 뿐입니다. 실제 솔버는 문 앞을 "문 폭 × 문 폭" 정사각형(개구부는 깊이 50 cm)으로 막고, 창문은 벽 두께 정도의 얇은 띠만 장애물로 넣습니다. 창 앞 여유는 계산하지 않습니다. Claude 호출 코드(`claude-sonnet-4-20250514`)는 OpenAI 호환 엔드포인트를 거칩니다. 커밋 1개짜리 코드 공개(416 stars)라 유지보수 신호는 약합니다.
- **SceneSmith**: 롤백은 **자동이 아닙니다.** planner 프롬프트가 임계를 넘으면 `reset_scene_to_checkpoint()` 호출을 "강하게 고려하라"고 지시할 뿐입니다. 가구가 바닥에 5 cm까지 박히는 것을 허용하는 `floor_penetration_tolerance_m 0.05` 설정도 있습니다.
- **Holodeck**: README 실행 명령은 `python holodeck/main.py`인데 실제 패키지 폴더는 `ai2holodeck/`입니다. issue #94(2026-05)는 한 사용자의 네트워크 문제 보고라서 "데이터 호스팅 중단"의 증거는 아닙니다([#94](https://github.com/allenai/Holodeck/issues/94)).
- **SceneAssistant**([저장소](https://github.com/ROUJINN/SceneAssistant))는 라이선스가 없고 커밋 3개이며, 기본 VLM(Gemini 3 Flash Preview)을 제3자 API 중계 플랫폼으로 호출합니다. 재현성·데이터 보안 문제로 근거로 쓰지 않았습니다(미검증 주장). 스텝별 렌더 로그 구조(`scene.json` + `step_i_state.json`)만 체크포인트 설계 참고용입니다.

### 3.2 Blender MCP 쪽 도구

| 도구 | 배치 관련 기능 | 라이선스 | 비고 |
|---|---|---|---|
| [Vibe3DScene](https://github.com/3DSceneAgent/Vibe3DScene) | LangGraph 에이전트 + **자체** MCP 서버·Blender 애드온. VLM 시각 검사 위에 관통 검사 옵션(`SCENE_AGENT_ENABLE_PENETRATION_VERIFY=true`, 기본 임계 `SCENE_AGENT_PENETRATION_THRESHOLD_M=0.02`) | Apache-2.0 | ahujasid Blender-MCP는 감사 목록에만 있고 런타임 의존성이 아닙니다([차이 설명](https://raw.githubusercontent.com/3DSceneAgent/Vibe3DScene/main/docs/differ_from_blendermcp+cc.md)). LLM은 `VLM_PROVIDER`로 openai/anthropic/gemini/qwen 선택([설정 문서](https://raw.githubusercontent.com/3DSceneAgent/Vibe3DScene/main/docs/reference/configuration.md)). 3D 생성기(Rodin/Tripo/TRELLIS2/Hunyuan)는 동시에 하나만. Python 3.11+, Blender 3.6+, Node 18+, Redis 권장. 93 stars |
| [blend-ai](https://github.com/HoldMyBeer-gg/blend-ai) | Transforms(snap), Objects(origin), Physics(rigid body, bake), OpenGL 렌더 피드백 | **AGPL-3.0-or-later** | README 기준 186 tool/27 모듈(저장소 About의 175는 옛 수치). Blender 4.2+ Extension(5.1 테스트). `execute_code` 대신 전용 툴을 쓰게 하면 실패가 국소화됨. 상용 통합 시 AGPL 주의 |
| [MCP for Blender](https://github.com/ahujasid/mcp-for-blender)(ahujasid, 구 blender-mcp) | 배치 전용 툴(스냅·충돌·물리) **없음** → `execute_blender_code`로 직접 구현 | MIT | 2026-09-16 개명 공지([#366](https://github.com/ahujasid/blender-mcp/issues/366)). README가 "복잡한 작업은 작은 단계로 나눠라"라고 경고. 소켓 타임아웃 180초 |
| 공식 Blender Lab 서버 | 코드 실행·스크린샷 | GPL-3.0-or-later | Blender 5.1+ 전용. 배치 전용 툴 없음. 자세한 비교는 [Blender MCP 가이드](02_blender_mcp.md) |
| 이 저장소 스크립트 | 스냅·표면 올리기·벽 붙이기·바라보기·간격 검사·관통/부유/박힘 리포트·4뷰 렌더, 건물·방의 문·창·동선 상식 검사(`building_audit.py`) | 저장소 포함 | 어느 서버에서나 `execute_blender_code` 또는 헤드리스로 동작([사용법](../03_playbooks/scripts/README.md)) |

### 3.3 학습형 모델·기타 연구

- **3D-FRONT 학습형**: [ATISS](https://github.com/nv-tlabs/ATISS)(NeurIPS 2021, autoregressive), [DiffuScene](https://github.com/tangjiapeng/DiffuScene)(CVPR 2024, diffusion), [PhyScene](https://github.com/PhyScene/PhyScene)(CVPR 2024, 충돌·경계·도달성 guidance). 빠르고 통계적으로 자연스럽지만 학습한 방 유형과 3D-FUTURE 카테고리 밖으로는 약하고 open-vocabulary가 아닙니다. 에이전트의 "초기 배치 제안기"로 쓰는 것이 현실적입니다(SceneWeaver 방식).
- **파인튜닝 LLM**: ReSpace(LICENSE 없음, add/remove/swap 편집), [OptiScene](https://github.com/PolySummit/OptiScene)(MIT, 가중치 'coming soon'), [MesaTask](https://github.com/InternRobotics/MesaTask)(탁상 씬. **LICENSE 파일은 MIT, README는 Apache로 서로 모순** → LICENSE 파일 우선), [NaLA](https://github.com/adamcwan/NaLA-code)(MIT, 체크포인트 미공개), [DirectLayout](https://github.com/rxjfighting/DirectLayout)(LICENSE 없음). 상용 프론티어 모델 + MCP로 작업한다면 코드를 쓰기보다 아이디어만 가져오세요: ReSpace의 편집 명령 분해, MesaTask의 "관계 추론 → scene graph → 좌표" 3단계 체인, DirectLayout의 "top-down(BEV) 먼저 → 높이 lifting" 순서.
- **[InstructScene](https://github.com/chenguolin/InstructScene)**(ICLR 2024 spotlight): scene graph를 먼저 만들고 레이아웃을 뒤에 푸는 2단계 구조의 대표 예. SceneEval이 공식 지원하는 기준선입니다.
- **Global-Local Tree Search**([TreeSearchGen](https://github.com/dw-dengwei/TreeSearchGen), CVPR 2025): VLM에게 원시 좌표 대신 top-down 격자 지도(가구 0.3 m, 소품 0.1 m 칸)를 보여 주고 칸을 고르게 합니다. VLM 공간 추론을 돕는 표현 방식으로 참고할 만합니다(신뢰도 중간).
- **2026 워치리스트**(큐레이션 목록 [Awesome-3D-Scene-Generation](https://github.com/hzxie/Awesome-3D-Scene-Generation)의 표기 기준, 학회 표기는 "목록상 표기"로만 읽을 것): Scenethesis, HOG-Layout, SceneOrchestra(툴 호출 궤적 일괄 예측), SpatialGrammar(실내 생성용 DSL), ScenePilot(grow-and-repair), MANSION(다층 건물). 이번 조사에서 대부분 방법·코드를 확인하지 못했습니다. 실무에 바로 쓸 수 있는 공개 코드는 SceneSmith, SAGE, SceneReVis, Code-as-Room 정도입니다.

### 3.4 평가 도구

| 도구 | 내용 | 실무 활용 |
|---|---|---|
| [SceneEval](https://github.com/3dlg-hcvc/SceneEval) (WACV 2026 Oral, MIT) | 지표 10종. VLM 없이: Collision, Navigability, Out of Bounds, Opening Clearance(v1.1, 2025-10-27 추가). VLM(GPT-4o 기본): Object Count, Attribute, Obj-Obj Relationship, Obj-Architecture Relationship, Support, Accessibility. SceneEval-500 | 10개 지표를 **에이전트의 셀프 체크리스트**로 그대로 씀. 기하 4종은 스크립트, 나머지 6종은 VLM이 판정 |
| [BlenderGym](https://github.com/richard-guyunqi/BlenderGym-Open) (CVPR 2025 Highlight, LICENSE 없음) | `--task placement` 포함. README 기준 VLM 20종 이상 지원(공개 리더보드에 결과가 오른 VLM 시스템은 13개) | 모델 후보(Claude/GPT/Gemini)의 Blender 배치 편집 능력을 직접 비교할 때 |

### 3.5 데이터셋·에셋 라이선스 주의

- **3D-FRONT/3D-FUTURE**, **[HSSD](https://github.com/3dlg-hcvc/hssd)**(211개 씬, 18,656개 객체)의 상업 이용 조건은 이번 조사에서 원문을 확인하지 못했습니다. 상업 프로젝트에 쓰기 전에 반드시 약관을 확인하세요. HSSD는 Hugging Face에서 라이선스 동의가 필요합니다.
- **3D-FUTURE 호스팅 변화(2026-09)**: [ReSpace README](https://raw.githubusercontent.com/GradientSpaces/respace/main/README.md)는 Alibaba Tianchi가 3D-FUTURE를 내렸을 가능성과 Kaggle 미러를 안내합니다. ATISS·DiffuScene·PhyScene·LayoutGPT·ReSpace·SceneReVis 등 3D-FRONT 계열 도구의 재현성에 영향을 줍니다.
- **Objaverse**([objathor](https://github.com/allenai/objathor) 변환 코드는 Apache-2.0)는 객체마다 CC 라이선스가 다릅니다.
- **[한국 사용자]** Tencent Hunyuan3D 계열 오픈웨이트 라이선스(2.0/2.1/Omni/Part 등)는 적용 지역에서 EU·영국·대한민국을 제외하고 출력물 사용도 제한합니다. 한국에서 SceneSmith(Hunyuan3D-2 옵션)나 SceneAssistant(Hunyuan3D-2)의 로컬 생성 경로를 쓰는 것은 라이선스 범위 밖입니다. SceneSmith는 SAM3D 생성이나 HSSD/Objaverse 검색으로 대체하세요. 자세한 내용은 [라이선스 가이드](10_assets_pipeline_licensing.md)를 보세요.

---

## 4. 실무 레시피: Blender + MCP로 방 하나 배치하기

전체 흐름과 각 단계의 통과 조건입니다.

| 단계 | 할 일 | 통과 조건 |
|---|---|---|
| 0 | 방 스펙: 치수, 천장고, 문·창 위치, 지역 프리셋, 금지 영역 | 방 폴리곤과 keep-out 목록 확정 |
| 1 | 에셋 정규화 | 모든 에셋: m 단위, 원점 바닥 중앙, 정면 -Y, 스케일 (1,1,1) |
| 2 | 초점·기능 그룹·주동선 정의 | 초점 1개, 그룹마다 앵커 지정 |
| 3 | 계층 순서와 객체당 제약 3~5개 작성 | 뒤 객체는 앞 객체에만 의존(DAG) |
| 4 | 솔버로 좌표 계산 | 모든 객체 배치, 비용 임계 이하 |
| 5 | Blender에 적용하고 스냅 | 바닥·벽 접촉 오차 5 mm 이내 |
| 6 | 기하 검사 | 관통 0, 의도치 않은 부유 0, 간격 규칙 위반 0 |
| 7 | 소품: 받침면 위 배치 + rigid body 안착 | 1 m 이상 이동·45° 이상 기울어진 소품 0 |
| 8 | 자연 노이즈 | "쇼룸"이면 생략 |
| 9 | 4뷰 렌더 + VLM 채점 | 6개 항목 모두 9점 이상, 또는 3라운드 도달 |
| 10 | 단계마다 체크포인트 저장 | 점수 하락 시 되돌릴 파일 존재 |

### 4.0 방 스펙과 금지 영역

- 방 치수, 천장고, 문·창 위치를 m로 적습니다. 한국 아파트라면 구축 2300 mm, 최근 신축 2400~2500 mm를 기본값으로 둡니다(6.3절).
- **금지 영역을 가구보다 먼저 깝니다.** SAGE 프롬프트는 문 회전 약 90 cm와 주요 가구 사이 60~90 cm 동선을 규칙으로 두고, SceneEval도 Opening Clearance와 Navigability를 독립 지표로 둡니다. 나중에 동선을 확보하려 하면 전체를 다시 배치해야 합니다.
- 조사에서 제안된 예: 문 앞 0.9×0.9 m, 창 앞 깊이 0.6 m, 주동선 폭 0.9 m 띠를 방 폴리곤에서 빼서 배치 가능 영역을 만듭니다. 배치 후에는 5 cm 격자 점유 지도(occupancy map)를 만들고, 반경 0.25~0.3 m 원판(사람 몸 크기)이 지나갈 수 있는 칸을 BFS(너비 우선 탐색)로 이어 보면 "모든 방 입구와 주요 가구 앞에 도달 가능한가"를 숫자로 확인할 수 있습니다.

### 4.1 에셋 정규화 (배치 품질의 절반)

```python
# execute_blender_code 로 실행: 가져온 에셋 하나를 배치용으로 정규화
import bpy
from mathutils import Vector

def normalize_asset(obj, target_max_m=None):
    """회전·스케일 적용 → 원점을 bbox 바닥 중앙으로 → (선택) 최대 축 기준 균일 스케일."""
    bpy.context.view_layer.objects.active = obj
    for o in bpy.context.selected_objects:
        o.select_set(False)
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    bpy.context.scene.cursor.location = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, mn.z))
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    if target_max_m:
        s = target_max_m / max(mx - mn)            # 비균일 스케일 금지: 한 값으로만 맞춘다
        obj.scale = (s, s, s)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj["front_axis"] = "-Y"                        # 메타데이터: 솔버·LLM에 같이 넘긴다
    obj["size_m"] = [round(v, 3) for v in obj.dimensions]
```

- **정면을 -Y로 먼저 돌린 뒤 실행하세요.** 회전을 적용(`transform_apply`)하면 그 자세가 메쉬에 굳습니다. 비스듬한 상태로 적용하면 bbox가 커지고 솔버가 보는 크기도 틀어집니다(위 함수는 Blender 4.2.23·5.0.1에서 원점이 bbox 바닥 중앙에 오는 것을 확인).
- **정면 축 규약**: glTF 2.0 스펙은 +Y가 위, 에셋 정면이 +Z, 왼쪽이 +X입니다([glTF 스펙](https://raw.githubusercontent.com/KhronosGroup/glTF/main/specification/2.0/Specification.adoc)). Blender는 Z-up이고 Front 뷰가 -Y 쪽에서 보므로, glTF를 가져오면 원본 +Z 정면이 Blender -Y 정면이 됩니다. 이 저장소 스크립트도 **정면 = -Y**를 가정합니다.
- **규약이 서로 다른 곳**: LayoutVLM은 0°가 +X를 보고 반시계가 +(degree), 방 중심이 원점, 바닥 물체 z = bbox 높이/2입니다([base_prompt.py](https://raw.githubusercontent.com/sunfanyunn/LayoutVLM/main/prompts/layoutvlm/base_prompt.py)). SceneSmith는 local +Y를 'toward'로, 에셋을 +Y forward/Z up으로 정규화합니다. 외부 솔버를 쓰면 이 오프셋을 **한 곳(변환 함수 하나)**에서만 관리하세요.
- **생성형·Objaverse 에셋은 정면 규약을 안 따르는 경우가 많습니다.** 4방향 렌더를 VLM에게 보여 주고 "서랍·좌석·화면이 보이는 뷰"를 고르게 해서 정면을 판별합니다.
- **실측 치수로 맞춥니다.** 기준은 [실측 치수표](../03_playbooks/05_reference_dimensions.md)입니다. 크기가 틀린 채로 배치하면 간격 규칙이 전부 어긋납니다. 대량생산 가구는 실제 제품 치수(예: IKEA BILLY 깊이 280 mm, PAX 깊이 580 mm 또는 350 mm 프레임)를 쓰면 더 그럴듯합니다([PAX 치수](https://itemfits.com/dimensions/ikea/ikea-pax)).
- 모델링 단계의 정규화 규칙은 [오브젝트·가구 모델링 가이드](07_modeling_objects_furniture_sculpture.md), 생성 에셋 후처리는 [AI 3D 생성 가이드](04_ai_3d_generation.md)를 보세요.

### 4.2 초점·기능 그룹·동선을 먼저 정하기

초점이 없으면 가구가 벽을 따라 흩어진 "대기실" 배치가 됩니다. Infinigen은 `focus_score`(소파가 TV를 향함)와 `angle_alignment_cost`(커피테이블 정면을 소파에 정렬)로 시선 방향을 최적화하고, SceneSmith critic은 "대화 영역 일관성"과 "관련 가구의 스케일 매칭(책상–의자 높이)"을 평가합니다([critic 프롬프트](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/furniture_agent/stateful_critic_agent.yaml)).

```text
[계획 프롬프트]
방: 4.2 × 3.6 m, 천장 2.3 m(한국 구축 아파트), 문은 남쪽 벽 서쪽 끝(x 0.2~1.1 m), 동쪽 벽은 바닥까지 내려오는 발코니 창(y 0.8~2.8 m).
1) 이 방의 초점 1개(TV 벽 / 창 전망 / 벽난로)를 정하라.
2) 기능 그룹(대화, 독서, 식사, 작업, 수면)을 정의하고 그룹마다 앵커 1개와 멤버를 나열하라.
3) 문→발코니 주동선과 금지 영역(문 앞 0.9×0.9 m, 창 앞 0.6 m)을 먼저 적어라.
4) 그다음에 아래 JSON 스키마로 objects와 relations를 작성하라. 좌표(x, y, z)는 쓰지 마라.
   - 크기는 실측 m [폭, 깊이, 높이]. 이름은 영어 소문자(sofa, tv_stand ...).
   - 제약 어휘는 against_wall, wall_center, facing, in_front_of, center_aligned, distance(min,max) 만 쓴다.
   - 앵커는 벽 관련 제약만, 뒤에 나오는 객체는 앞에 나온 객체에만 의존한다. 객체당 제약 3~5개.
```

### 4.3 계층 순서와 제약 작성 규칙

- **순서**: 평면도 → 러그 → 앵커 가구(소파, 침대, 식탁) → 큰 가구 → 작은 가구 → 벽걸이 → 천장 → 표면 위 소품. SceneSmith(5단계), HSM(방→가구→소품), SAGE(바닥/벽/물체 위 3분류)가 공통으로 채택했습니다. 단계마다 필요한 검사가 다릅니다(바닥은 2D 충돌, 벽은 벽면 2D 격자, 소품은 받침면 + 물리).
- **거실 예시 순서**: 러그 → 소파(벽에 붙임, 초점 벽 맞은편) → TV장(맞은편 벽 중앙) → 커피테이블 → 암체어 → 사이드테이블 → 플로어 램프 → 벽 그림 → 천장 조명 → 소품.
- **Holodeck 프롬프트 지침**: 앵커는 global 제약만, 큰 것부터, 뒤에 놓는 것은 앞의 것에만 의존, 같은 종류는 정렬, edge 우선, 의자는 around. near는 50~150 cm, far는 150 cm 이상으로 수치를 못박았습니다.
- **객체당 제약 3~5개**: SAGE 프롬프트는 "객체당 4~5개 제약이 planner를 크게 돕는다"고 적었고, LayoutVLM은 객체마다 위치 제약과 방향 제약을 최소 1개씩 요구합니다.
- **제약 어휘는 7~10개로 제한하고 수치로 정의합니다.** 어휘가 모호하면 모델마다 다르게 해석합니다. 조사에서 제안된 세트: `against_wall(obj, wall, gap=0.02)`, `facing(obj, target)`, `next_to(obj, target, gap)`, `on_top_of(obj, support)`, `centered_on(obj, target)`, `aligned(obj, target, axis)`, `distance(obj, target, min, max)`, `in_corner(obj, corner)`, `clear_zone(obj, side, depth)`. LayoutVLM의 7종(`on_top_of`, `against_wall`, `distance_constraint(min,max,weight)`, `align_with`, `point_towards`, `align_x`, `align_y`)도 좋은 템플릿입니다.
- **few-shot 레퍼런스**: LayoutGPT는 비슷한 방 예시를 in-context로 붙이는 효과를 보였습니다. 사용자의 무드보드나 top-down 평면 스케치를 첨부하고 "그룹 구성과 동선은 유지하되 방 치수 4.2×3.6 m에 맞춰 relations JSON을 작성하라"고 지시하세요. SceneSmith 디자이너도 레퍼런스 이미지가 있으면 "개념을 가져오되 실제 방에 맞게 변형하라"고 지시합니다([initial instruction](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/furniture_agent/designer_initial_instruction.yaml)).

### 4.4 제약 JSON과 솔버

**제약 JSON 예시** (한국 구축 아파트 거실, 아래 솔버로 그대로 풀립니다)

```json
{
  "units": "m",
  "room": {
    "size": [4.2, 3.6], "ceiling": 2.3, "region": "KR",
    "doors": [{"wall": "S", "x": [0.2, 1.1]}],
    "windows": [{"wall": "E", "y": [0.8, 2.8], "sill": 0.0}],
    "keep_out": [[0.2, 0.0, 1.1, 0.9], [3.6, 0.8, 4.2, 2.8]]
  },
  "focal_point": "tv_stand",
  "groups": {"conversation": ["sofa", "coffee_table", "armchair", "tv_stand"], "reading": ["armchair", "floor_lamp"]},
  "objects": [
    {"id": "sofa", "size": [2.13, 0.94, 0.84], "front": "-Y",
     "relations": [["against_wall", "N"], ["wall_center", "N"]]},
    {"id": "tv_stand", "size": [1.8, 0.45, 0.5], "front": "-Y",
     "relations": [["against_wall", "S"], ["center_aligned", "sofa"], ["facing", "sofa"], ["distance", "sofa", 2.0, 3.0]]},
    {"id": "coffee_table", "size": [1.2, 0.6, 0.43], "front": "-Y",
     "relations": [["in_front_of", "sofa"], ["center_aligned", "sofa"], ["distance", "sofa", 0.35, 0.45]]},
    {"id": "armchair", "size": [0.8, 0.85, 0.8], "front": "-Y",
     "relations": [["against_wall", "W"], ["facing", "coffee_table"], ["distance", "coffee_table", 0.4, 0.8]]},
    {"id": "side_table", "size": [0.45, 0.45, 0.6], "front": "-Y",
     "relations": [["against_wall", "N"], ["distance", "sofa", 0.03, 0.1]]},
    {"id": "floor_lamp", "size": [0.35, 0.35, 1.6], "front": "-Y",
     "relations": [["against_wall", "W"], ["distance", "armchair", 0.05, 0.3]]}
  ]
}
```

- `keep_out`은 [x0, y0, x1, y1] 사각형입니다(문 앞 0.9×0.9 m, 발코니 창 앞 0.6 m).
- `distance`는 **가장자리 사이 최단 거리**입니다. 소파–TV장 2.0~3.0 m는 Infinigen의 hinge(2, 3), 소파–커피테이블 0.35~0.45 m는 SceneSmith(0.3~0.5)와 인테리어 가이드(356~457 mm)가 겹치는 구간입니다.
- 치수는 3인 소파 폭 약 2130 mm·깊이 약 940 mm·높이 약 840 mm, 커피테이블 높이 406~457 mm 같은 기준값에서 골랐습니다([실측 치수표](../03_playbooks/05_reference_dimensions.md)). 암체어·사이드테이블 치수는 출처로 확인하지 못한 관행값입니다.

**솔버 선택**

| 방식 | 언제 | 구현 |
|---|---|---|
| 구성형(constructive) | 객체 10개 이하, 관계가 단순한 방 | `placement_utils`의 `place_against_wall`·`place_next_to`·`face_towards`를 순서대로 호출 |
| 격자 DFS + 백트래킹 | 객체 5~30개 방(대부분의 실내) | 아래 스케치, Holodeck `floor_objects.py`, SAGE planner |
| 미분 최적화 | 자유 회전, 연속 좌표가 필요할 때 | LayoutVLM(Adam) 또는 scipy. **충돌은 하드 검사로 따로** |
| simulated annealing | 절차적 대량 생성, 추가·삭제까지 탐색 | Infinigen v1.16.0 |

<details>
<summary><b>격자 DFS 솔버 스케치</b> (순수 Python, 약 90줄, 위 JSON으로 실행 확인. 저장소 테스트 스크립트는 아님)</summary>

```python
# grid_solver.py — 관계 제약 JSON → (x, y, yaw) 를 푸는 최소 격자 DFS 솔버 (순수 Python, Blender 불필요)
# 규약: 방 바닥 x∈[0,W], y∈[0,D], 단위 m. yaw(도) 0이면 앞면이 -Y, 90이면 +X, 180이면 +Y, 270이면 -X.
# distance/gap은 모두 "가장자리 사이 최단 거리(m)".
import json, math

FRONT = {0: (0, -1), 90: (1, 0), 180: (0, 1), 270: (-1, 0)}
WALL_YAW = {"S": 180, "N": 0, "W": 90, "E": 270}          # 벽에 등을 붙이면 앞면이 방 안쪽을 봄

def rect(o, x, y, yaw):
    w, d = o["size"][0], o["size"][1]
    if yaw in (90, 270):
        w, d = d, w
    return (x - w / 2, y - d / 2, x + w / 2, y + d / 2)

def gap(a, b):
    dx = max(0.0, max(a[0], b[0]) - min(a[2], b[2]))
    dy = max(0.0, max(a[1], b[1]) - min(a[3], b[3]))
    return math.hypot(dx, dy)

def overlaps(a, b, pad):
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad

def wall_gap(r, wall, W, D):
    return {"S": r[1], "N": D - r[3], "W": r[0], "E": W - r[2]}[wall]

def cost(o, x, y, yaw, placed, W, D):
    r, c = rect(o, x, y, yaw), 0.0
    for rel in o.get("relations", []):
        kind, args = rel[0], rel[1:]
        if kind == "against_wall":
            c += 10 * abs(wall_gap(r, args[0], W, D) - 0.02) + (5 if yaw != WALL_YAW[args[0]] else 0)
        elif kind == "wall_center":                       # 벽의 가운데(앵커 가구용, Holodeck의 global: middle)
            c += abs(x - W / 2) if args[0] in ("N", "S") else abs(y - D / 2)
        elif kind in ("distance", "facing", "in_front_of", "center_aligned") and args[0] not in placed:
            continue  # 아직 안 놓인 대상은 건너뜀(순서 = 의존성)
        elif kind == "distance":
            t = placed[args[0]]; g = gap(r, t["rect"]); lo, hi = args[1], args[2]
            c += 5 * (max(0, lo - g) + max(0, g - hi))
        elif kind == "facing":
            t = placed[args[0]]; tx, ty = t["xy"]; fx, fy = FRONT[yaw]
            n = math.hypot(tx - x, ty - y) or 1e-9
            c += 3 * (1 - (fx * (tx - x) + fy * (ty - y)) / n)
        elif kind == "in_front_of":                       # 대상의 앞면 쪽에 있어야 함
            t = placed[args[0]]; tx, ty = t["xy"]; fx, fy = FRONT[t["yaw"]]
            c += 0 if fx * (x - tx) + fy * (y - ty) > 0 else 5
        elif kind == "center_aligned":                    # 대상의 좌우 중심선에 맞춤
            t = placed[args[0]]; tx, ty = t["xy"]; fx, fy = FRONT[t["yaw"]]
            c += 3 * abs(-fy * (x - tx) + fx * (y - ty))
    return c

def solve(scene, step=0.05, pad=0.02, top_k=6):
    W, D = scene["room"]["size"]
    keep_out = [tuple(z) for z in scene["room"].get("keep_out", [])]   # (x0, y0, x1, y1): 문 스윙, 창 앞, 동선
    objs = scene["objects"]
    def candidates(o, placed):
        out = []
        for yaw in (0, 90, 180, 270):
            for i in range(int(W / step) + 1):
                for j in range(int(D / step) + 1):
                    x, y = i * step, j * step
                    r = rect(o, x, y, yaw)
                    if r[0] < 0 or r[1] < 0 or r[2] > W or r[3] > D:
                        continue
                    if o.get("collide", True):
                        if any(overlaps(r, p["rect"], pad) for p in placed.values() if p["collide"]):
                            continue
                        if any(overlaps(r, z, 0) for z in keep_out):
                            continue
                    out.append((cost(o, x, y, yaw, placed, W, D), x, y, yaw, r))
        out.sort(key=lambda t: t[0])
        return out[:top_k]
    def dfs(k, placed):
        if k == len(objs):
            return placed
        o = objs[k]
        for c, x, y, yaw, r in candidates(o, placed):
            if c > o.get("max_cost", 1.0):               # 제약을 너무 많이 어기면 이 후보는 버림
                break
            placed[o["id"]] = {"xy": (x, y), "yaw": yaw, "rect": r, "cost": c, "collide": o.get("collide", True)}
            if dfs(k + 1, placed):
                return placed
            del placed[o["id"]]                          # 백트래킹
        return None
    res = dfs(0, {})
    if res is None:
        return None
    return {k: {"x": round(v["xy"][0], 3), "y": round(v["xy"][1], 3), "yaw_deg": v["yaw"], "cost": round(v["cost"], 3)}
            for k, v in res.items()}

if __name__ == "__main__":
    import sys
    scene = json.load(open(sys.argv[1], encoding="utf-8"))
    print(json.dumps(solve(scene), ensure_ascii=False, indent=1))
```

위 JSON의 결과(약 0.25초): sofa (2.10, 3.10, 0°), tv_stand (2.10, 0.25, 180°), coffee_table (2.10, 1.90, 0°), armchair (0.45, 1.90, 90°), side_table (0.75, 3.35, 0°), floor_lamp (0.20, 1.10, 90°). 소파–커피테이블 0.43 m, 소파–TV장 2.155 m, 커피테이블–TV장 1.125 m로 규칙을 모두 만족합니다.

- `null`이 나오면 제약끼리 충돌한 것입니다. 첫 시험에서 `wall_center` 없이 돌리자 소파가 왼쪽 끝에 붙어 TV장이 문 금지 영역과 겹쳤고, 해가 없었습니다. 앵커의 위치(벽 가운데/모서리)를 먼저 고정하는 이유입니다.
- 한계: 회전 90° 단위(Holodeck과 같음), 2D 사각형 충돌, 벽은 N/S/E/W 직사각형 방만. 비정형 방이나 자유 회전이 필요하면 Shapely 폴리곤·gradient 방식으로 바꾸세요.

</details>

### 4.5 Blender에 적용하고 스냅하기

```python
# execute_blender_code 로 실행 (에셋 이름 = JSON의 id, 원점 = 바닥 중앙, 정면 = -Y 로 정규화된 상태)
import sys, math, json, bpy
sys.path.append(r"C:\path\to\3D-MCP\03_playbooks\scripts")   # 이 저장소를 받은 위치
import importlib, placement_utils as pu; importlib.reload(pu)

layout = json.loads(LAYOUT_JSON)          # 솔버 출력 문자열
for oid, p in layout.items():
    o = bpy.data.objects[oid]
    o.location.x, o.location.y = p["x"], p["y"]
    o.rotation_euler.z = math.radians(p["yaw_deg"])
    pu.snap_to_floor(o, 0.0)              # z는 LLM이 아니라 bbox로 계산

lamp = bpy.data.objects["table_lamp"]     # 표면 위 소품: xy만 맞추고 아래 표면으로 떨어뜨림
lamp.location.x, lamp.location.y = layout["side_table"]["x"], layout["side_table"]["y"]
print(pu.drop_to_surface(lamp))           # → 'side_table' (받침 오브젝트 이름)
```

- Blender의 `rotation_euler.z`는 위에서 볼 때 반시계가 +입니다. 앞면이 -Y인 에셋을 target 쪽으로 돌리는 yaw는 `atan2(dx, -dy)`이고, `pu.face_towards()`가 쓰는 `atan2(dy, dx) + 90°`와 같은 값입니다(앞의 식은 검증 에이전트가 수학적으로 확인, 두 식이 같은 결과를 내는 것은 이 문서 작성 중 Blender에서 확인).
- **벽에 딱 붙이기**: SceneSmith의 `snap_to_object`는 방향을 정한 뒤 0.01 m씩 전진하다 충돌하면 한 스텝 물러나 0.01 m 마진을 남깁니다([snapping_helpers.py](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/furniture_agents/tools/snapping_helpers.py)). 부동소수점 오차로 생기는 관통과 틈을 같이 막습니다. `pu.place_against_wall(obj, wall_y, gap=0.02)`는 +Y 쪽 벽 기준입니다.
- **SceneSmith의 방향 분류**: A(대상을 향함, 예: 의자 → 테이블, orientation='toward'), B(기능적 정면이 방 안쪽, 예: 서랍장·옷장·가전, 'away'), C(대칭). 시각 판단 대신 `check_facing_tool`로 검증하게 강제합니다([designer 프롬프트](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/furniture_agent/designer_agent.yaml)).

```python
# 방향 검증: 정면(-Y) 벡터와 target 방향의 내적 > 0.9 이면 통과
from mathutils import Vector
def check_facing(obj, target, thresh=0.9):
    f = (obj.matrix_world.to_3x3() @ Vector((0, -1, 0))).to_2d().normalized()
    d = (target.matrix_world.translation - obj.matrix_world.translation).to_2d().normalized()
    return f.dot(d) > thresh
```

### 4.6 기하 검사: 관통·부유·간격

```python
import importlib, scene_audit, placement_utils as pu
importlib.reload(scene_audit)
rep = scene_audit.audit_scene(floor_z=0.0, ceiling_z=2.30)   # 방 JSON의 천장 2.3 m(한국 구축). 기본 치수 규칙에 armchair 등이 이미 들어 있음
print(rep["summary"])                    # interpenetrating_pairs 가 0 이어야 함
print([(u["name"], u["issues"]) for u in rep["units"] if u["issues"]])
print(pu.check_clearances([              # (A, B, 최소 m, 최대 m 또는 None)
    ("sofa", "coffee_table", 0.35, 0.50),
    ("coffee_table", "tv_stand", 0.90, None),   # 주동선
    ("armchair", "coffee_table", 0.40, 0.80),
]))
```

- 위 코드를 4.4절 솔버 결과(암체어 90° 회전 포함)로 만든 상자 장면에 돌리면 관통 0쌍, 치수·부유·천장 경고 0건, 간격 위반 `[]`이 나옵니다(Blender 4.2.23 LTS·5.0.1에서 확인. 재질·UV 경고는 블록아웃이라 제외).
- `scene_audit.py`는 부모 기준 "유닛"마다 월드 좌표 BVH(면을 빠르게 찾는 공간 트리)를 만들어 **바운딩박스가 겹치는 쌍만** 면 교차를 검사합니다. 테이블 아래로 들어간 의자(bbox만 겹침)는 관통으로 잡지 않습니다. 벽·천장 메시가 있으면 가구–벽·천장 관통도 잡습니다(구조물끼리는 제외).
- **치수 규칙은 가구 방향 기준입니다.** 루트의 Z 회전을 되돌려 폭 w(수평 긴 변)·깊이 d·높이 z를 재므로 90°나 30° 돌린 소파·암체어도 오탐하지 않습니다. 이름은 단어 단위로 맞춰서 `armchair`는 `chair` 규칙에 걸리지 않고, `table_lamp`·`door_handle`처럼 부속품 단어가 뒤에 붙으면 규칙을 적용하지 않습니다.
- **박힘과 천장**: 바닥이나 다른 가구 속으로 파고든 유닛은 '떠 있음'이 아니라 `below_floor`·`sunk_into:<상대>=<깊이>m`으로 나오고, `ceiling_z`보다 위로 나간 유닛은 `above_ceiling`으로 나옵니다. 방 내부와 건물 외관을 한 장면에 두면 `collection="Room"`처럼 컬렉션을 지정해 천장 규칙을 방 유닛에만 적용하세요.
- **API 함정 두 가지**: `BVHTree.FromObject()`는 **오브젝트 로컬 좌표** 트리라서 두 오브젝트를 그대로 비교하면 틀립니다. 월드 변환한 정점으로 `FromPolygons`/`FromBMesh`를 만드세요. `overlap()`은 표면 교차만 잡아서 **한 물체가 다른 물체 안에 완전히 들어간 경우를 놓칩니다.** AABB(축 정렬 바운딩박스) 겹침 깊이를 함께 보세요([mathutils_bvhtree.cc](https://raw.githubusercontent.com/blender/blender/main/source/blender/python/mathutils/mathutils_bvhtree.cc)). `Scene.ray_cast(depsgraph, origin, direction, distance)`는 월드 공간 evaluated geometry를 대상으로 합니다([rna_scene_api.cc](https://raw.githubusercontent.com/blender/blender/main/source/blender/makesrna/intern/rna_scene_api.cc)).
- **임계값 참고**: SceneSmith는 관통 임계 1 mm(VHACD 충돌), 충돌 해소 1단계로 무관한 물체 간 world bounds 0.2 m부터 시도, SAGE는 bbox 전체 치수에 +3.5 cm, Vibe3DScene은 관통 기본 임계 0.02 m입니다. 이 저장소 `scene_audit.py`의 기본 접촉·관통 허용 오차는 5 mm입니다.
- **고폴리 에셋**은 decimate한 프록시로 검사하세요. 느려서 MCP 소켓 타임아웃(ahujasid 180초)에 걸립니다.
- **벽걸이·천장등은 `floating_or_wall_mounted`로 나옵니다.** 의도한 것인지 확인하고, 벽 쪽은 벽과의 거리로 따로 검증하세요.
- 결과는 `[(a, b, 침투 깊이)]` 같은 짧은 텍스트로 LLM에 돌려주세요. 전체 JSON을 매번 넣으면 컨텍스트가 빨리 찹니다.

### 4.7 소품: 받침면 + rigid body 안착

쌓기·기대기처럼 자연스러운 접촉은 솔버보다 물리가 잘 만듭니다. SceneSmith는 소품을 5초(dt 0.001) 시뮬레이션해 안정성을 보고, 45° 이상 기울면 "넘어짐", 1 m 이상 움직이면 실패로 봅니다([manipuland 설정](https://raw.githubusercontent.com/nepfaff/scenesmith/main/configurations/manipuland_agent/base_manipuland_agent.yaml)). SAGE는 받침 위 후보 150개를 샘플링한 뒤 physics critic으로 거릅니다.

```python
# 소품을 2~5 cm 띄워 두고 실행. Blender 4.2.23 LTS / 5.0.1 에서 실행 확인.
import bpy, math
from mathutils import Vector

def settle(props, supports, frames=120, max_move=1.0, max_tilt_deg=45.0):
    """props를 rigid body로 떨어뜨려 안착시키고 최종 변환을 굳힌다. 실패 목록을 반환."""
    scene = bpy.context.scene
    if scene.rigidbody_world is None:
        bpy.ops.rigidbody.world_add()
    scene.rigidbody_world.point_cache.frame_start = 1
    scene.rigidbody_world.point_cache.frame_end = frames
    def add_rb(o, kind, shape):
        with bpy.context.temp_override(object=o, active_object=o, selected_objects=[o]):
            bpy.ops.rigidbody.object_add(type=kind)
        o.rigid_body.collision_shape = shape
        o.rigid_body.use_margin = True              # 기본 여백(0.04 m) 때문에 약 4 cm 떠서 멈추는 것을 막음
        o.rigid_body.collision_margin = 0.001
    for o in supports:
        add_rb(o, 'PASSIVE', 'MESH')
    for o in props:
        add_rb(o, 'ACTIVE', 'CONVEX_HULL')          # 오목한 그릇·컵 안쪽까지 필요하면 'MESH'
    start = {o.name: o.matrix_world.copy() for o in props}
    for f in range(1, frames + 1):                  # 순서대로 진행해야 캐시가 계산됨
        scene.frame_set(f)
    final = {o.name: o.matrix_world.copy() for o in props}
    for o in props + supports:                      # rigid body 제거 후 최종 변환을 그대로 적용
        with bpy.context.temp_override(object=o, active_object=o, selected_objects=[o]):
            bpy.ops.rigidbody.object_remove()
    scene.frame_set(1)
    failed = []
    for o in props:
        o.matrix_world = final[o.name]
        moved = (final[o.name].translation - start[o.name].translation).length
        up = final[o.name].to_3x3() @ Vector((0, 0, 1))
        tilt = math.degrees(math.acos(max(-1.0, min(1.0, up.normalized().z))))
        if moved > max_move or tilt > max_tilt_deg:  # SceneSmith 기준: 1 m 이상 이동 또는 45° 이상 기울면 실패
            failed.append((o.name, round(moved, 3), round(tilt, 1)))
    bpy.ops.rigidbody.world_remove()
    return failed

O = bpy.data.objects
print(settle([O["book_0"], O["book_1"], O["cup"]], [O["floor"], O["side_table"]]))
```

- **실측으로 확인한 함정**: rigid body의 기본 충돌 여백은 0.04 m입니다. 그대로 두면 책·컵이 받침면 위 약 4 cm에 떠서 멈춥니다(테스트에서 0.6399 m, 받침면 0.600 m). `use_margin=True`, `collision_margin=0.001`로 바꾸자 0.6019 m로 붙었고 `scene_audit.py`의 부유 경고도 사라졌습니다.
- 이 함수는 끝에 rigid body world를 지웁니다. 다른 물리 시뮬레이션이 있는 씬이면 사본에서 실행하세요.
- 안착 결과를 적용하지 않고 **안정성 검증만** 하려면: 60프레임 시뮬레이션 뒤 2 cm 이상 움직였거나 5° 이상 돌아간 객체를 "불안정" 목록으로 돌려주고, 원래 변환으로 복원합니다(조사에서 제안된 예시값).
- 연산자 방식을 원하면 `bpy.ops.rigidbody.bake_to_keyframes(frame_start=1, frame_end=120)` 후 마지막 프레임 값을 쓰거나 `visual_transform_apply()`를 쓸 수 있습니다([rigidbody.py](https://raw.githubusercontent.com/blender/blender/main/scripts/startup/bl_operators/rigidbody.py)).
- **반복되는 소품 배치**(식탁 세팅, 책장, 욕실 소품)는 HSM/SMC처럼 `place_row(n, spacing)`, `place_stack(n)`, `place_grid()` 같은 모티프 함수로 만들어 MCP 툴로 노출하면 안정적입니다.

### 4.8 자연 노이즈: 기계적 정렬감 없애기

완벽하게 정렬된 배치는 CG처럼 보이고, 무작위 회전은 "혼돈"으로 보입니다(SceneSmith critic의 CHAOS DETECTION 항목). SceneSmith Natural 프로파일 값([가구 설정](https://raw.githubusercontent.com/nepfaff/scenesmith/main/configurations/furniture_agent/base_furniture_agent.yaml)):

| 대상 | 위치 σ | yaw σ |
|---|---|---|
| 가구 | 0.03 m | 1° |
| 소품 | 0.01 m | 3° |

- planner는 첫 단계에서 프롬프트 키워드로 배치 스타일을 고릅니다('lived-in'이면 natural, 'showroom'이면 perfect). 쇼룸·제품 샷이면 노이즈를 끄세요.
- 조사에서 제안된 실무 예: 벽붙이 가구는 yaw를 90° 단위로 스냅한 뒤 ±1°, 자유 배치 의자는 15° 단위 + ±3°, 소품은 5 mm 격자 + ±3~8°. 식탁 의자 일부를 5~10 cm 빼 두면 "사용 중" 느낌이 납니다.
- **노이즈를 준 뒤에는 4.6절 검사를 다시 돌리세요.** 노이즈로 관통이 새로 생길 수 있습니다.

### 4.9 4뷰 렌더와 VLM 채점, 종료·롤백 규칙

```python
import bpy
from review_views import render_review_views
# GUI(MCP)에서는 Workbench가 가장 빠름. 헤드리스·GPU 없는 서버는 CYCLES.
# '//review/'처럼 .blend 기준 상대 경로를 줘도 됨(함수 안에서 bpy.path.abspath로 바꾼 뒤 폴더를 만듦).
# .blend를 저장하지 않은 새 파일이면 Blender 프로세스의 작업 폴더 아래 review/에 생기므로 먼저 저장해 둘 것
paths = render_review_views("//review/", engine="BLENDER_WORKBENCH", res=1024)
# → top.png(위 정사영), front.png, side.png, persp.png. 오브젝트마다 다른 색이라 겹침·간격이 잘 보임
```

- **왜 top-down인가**: VLM은 원근 뷰만 보면 거리를 잘 못 읽습니다. SceneSmith는 top 1024² + 측면 4뷰 512²(top_plus_sides)를 쓰고 "top-down 뷰가 좌표 읽기에 최적"이라고 적었습니다. LayoutVLM은 렌더에 좌표 마크와 에셋 이름을 오버레이하고, SceneReVis는 overhead + diagonal 2뷰를 씁니다.
- **효과를 더 올리려면**: top 렌더에 0.5 m 격자와 오브젝트 ID 라벨을 얹으세요(얇은 emission 선 평면이나 PIL 후처리). `review_views.py`에는 이 기능이 없습니다. 대신 `scene_audit.py`의 `units[].name`·`bbox_min`·`bbox_max`를 이미지와 함께 넘기면 VLM이 이름과 위치를 대조할 수 있습니다.
- 스크린샷 토큰과 이미지 20장 제한은 [Blender MCP 가이드 9.4절](02_blender_mcp.md)을 보세요. 검토 렌더는 800~1024 px로 충분합니다.

**SceneSmith 비평 루브릭과 종료·롤백 규칙** (설정값은 1차 검증에서 YAML과 일치 확인)

| 항목 | 값 |
|---|---|
| 채점 항목 (0~10) | Realism, Functionality, Layout, Completeness, Prompt Following, Reachability |
| 조기 종료 | 6개 항목 **모두 9점 이상**(`early_finish_min_score 9`) |
| 최대 라운드 | 3(`max_critique_rounds`), 소품 단계는 2 |
| 중단 | 같은 문제가 2회 이상 반복되면 |
| 롤백 | 한 항목이 **2점 이상** 떨어지거나 총점이 **1점 이상** 떨어지면 체크포인트로(자동이 아니라 planner 판단) |
| 물리 페널티 | 충돌이 남아 있으면 Realism 최대 4점 |
| 모델 설정 | designer·critic reasoning high, planner low, vision_detail high(설정상 gpt-5.2) |

```text
[비평 프롬프트]
아래 top-down(정사영)과 측면 이미지, 그리고 scene_audit 요약을 보고 6개 항목
(Realism, Functionality, Layout, Completeness, Prompt Following, Reachability)을 0~10점으로 채점하라.
- scene_audit의 interpenetrations 가 비어 있지 않으면 Realism ≤ 4.
- 문제마다 (object_id, 문제, 구체적 수정: 이동 벡터 [dx, dy] m 또는 회전 °)로 출력하라. 좌표를 새로 지어내지 말고 변화량만 적어라.
- 초점과 대화 그룹이 성립하는지, 문·창 앞과 주동선이 비어 있는지, 관련 가구의 높이가 맞는지(책상–의자) 확인하라.
- 균일하게 깔린 잡동사니, 이유 없이 막힌 문·창, 모든 가구가 벽에만 붙은 배치는 감점하라.
```

**DONE 조건을 하드 규칙으로** 넣으세요. SceneSmith 디자이너 지시문은 "check_physics로 충돌 0을 확인하기 전에는 끝내면 안 되고, 해결 못 하는 충돌은 객체를 삭제하는 편이 낫다"고 적었고, SAGE 프롬프트는 떠 있는 물체, 바닥 과밀, 비정상 크기, 충돌, 방향 오류, 벽에서 떨어진 소파를 금지 목록으로 둡니다.

```text
DONE 조건: interpenetrations == [] AND 의도치 않은 floating == [] AND keep_out 침범 == []
AND 주동선 ≥ 0.9 m AND 비평 6개 항목 ≥ 9 (또는 3라운드 도달).
(방이 여러 개인 건물이면) AND building_audit summary.errors == 0 AND liminal_risk != "high".
하나라도 위반하면 DONE을 선언하지 말고 수정하거나 해당 객체를 삭제하라.
```

### 4.10 체크포인트와 롤백

- 단계(평면도·가구·벽걸이·천장·소품)가 끝날 때마다 사본을 저장합니다. SceneSmith의 `reset_scene_to_checkpoint` 패턴입니다.

  ```python
  import bpy, os
  d = bpy.path.abspath('//checkpoints/')      # 작업 .blend를 먼저 저장해 둘 것
  os.makedirs(d, exist_ok=True)                # 폴더가 없으면 저장이 "No such file or directory"로 실패(4.2.23·5.0.1에서 확인)
  bpy.ops.wm.save_as_mainfile(filepath=os.path.join(d, '02_furniture.blend'), copy=True)
  ```

  ahujasid 서버의 safe mode(`BLENDER_MCP_SAFE_MODE=1`)는 `os.makedirs` 같은 직접 파일 I/O를 막으므로(bpy 렌더·저장은 허용) 폴더를 미리 만들어 두거나 헤드리스로 실행하세요.
- ahujasid 애드온은 `undo_push`를 호출하지 않고, Claude Code의 `/rewind`는 Blender 상태를 되돌리지 못합니다. 롤백은 저장해 둔 파일로만 믿을 수 있습니다([Blender MCP 가이드 9.6절](02_blender_mcp.md)).
- 롤백 기준은 4.9절 표(한 항목 −2점 또는 총점 −1점)를 씁니다. 되돌린 뒤에는 같은 수정을 반복하지 않게 "이전 시도와 실패 이유"를 프롬프트에 남기세요.

---

## 5. MCP 툴을 직접 설계할 때

한 번 호출에 객체 1~3개만 다루는 **원자적 툴**로 쪼개세요. 긴 `execute_blender_code`는 타임아웃·부분 실패가 잦고(2026년 ahujasid 이슈에 타임아웃 사례 다수), 툴이 작을수록 실패가 국소화됩니다.

| 권장 툴 (조사 제안) | 역할 | 대응하는 공개 구현 |
|---|---|---|
| `get_room_state()` → JSON | 객체 id·타입·위치·회전·치수·부모 | SceneReVis·SceneAssistant의 상태 JSON |
| `add_asset(asset_id, x, y, yaw)` | z=0 직립 배치 | SceneSmith `add_furniture_to_scene_tool` |
| `move(id, x, y, yaw)` / `remove(id)` / `rescale(id, s)` | 균일 스케일만 | SceneSmith move/remove/rescale(uniform), SceneReVis 6개 원자 연산 |
| `snap(id, target, mode)` | toward/away, 0.01 m 스텝 | SceneSmith `snap_to_object_tool` |
| `drop_to_surface(id)` | 받침면 위로 | 이 저장소 `pu.drop_to_surface` |
| `check_scene()` → {collisions, floating, out_of_bounds, blocked_openings, walkway_min} | SceneEval 기하 지표 4종 | SceneSmith `check_physics`·`check_reachability`, `scene_audit.py` |
| `render_topdown()` / `render_views()` → PNG | 비평용 | `review_views.py` |
| `checkpoint(name)` / `rollback(name)` | 단계 저장 | SceneSmith `reset_scene_to_checkpoint` |

- **SAGE의 실제 MCP 툴**(1차 검증에서 코드 확인): `generate_room_layout`, `get_current_layout`, `clear_layout`, `get_room_details`, `list_rooms`, `get_layout_from_json`, `place_objects_in_room`, `move_one_object_with_condition_in_room`, `get_room_information`, `get_layout_save_dir`, `robot_task_feasibility_correction_for_room`, `parse_robot_policy_requirements_for_scene_generation`. 배치의 핵심은 `place_objects_in_room`과 `move_one_object_with_condition_in_room`입니다. README에는 툴 문서가 없어 코드를 직접 읽어야 합니다.
- 툴 이름과 설명에 **규약(단위 m, yaw는 도·반시계, 정면 -Y)**을 적으세요. 모델마다 해석이 달라지는 것을 막습니다.
- 프롬프트 규칙 파일([CLAUDE.md 템플릿](../03_playbooks/templates/CLAUDE.md), [스킬 템플릿](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md))에 "좌표는 솔버, LLM은 관계만", "DONE 조건", "이름은 영어"를 넣어 두면 세션이 바뀌어도 유지됩니다.

**어떤 모델을 어디에 쓸까** (배치 전용 비교 자료는 없음, 미확인)

- 계획(관계 제약 작성)은 추론이 강한 모델, 비평은 시각이 강한 모델에 맡기세요. Anthropic은 Opus 5.5를 "vision과 computer use에 가장 좋은 Opus"라고 소개합니다. GPT-6 Astra를 Codex에서 쓰면 기본 reasoning이 low이므로 effort를 명시하세요. SceneSmith 설정도 designer·critic은 high, planner는 low입니다.
- 모델 비교와 비용은 [모델 가이드](01_ai_models_and_clients.md)를 보세요. 대부분 개인 테스트(n=1)라 절대 순위로 쓰지 마세요.

---

## 6. 인테리어 수치 규칙 (출처별 병기)

### 6.1 오픈소스 시스템에 박혀 있는 값

| 규칙 | 값 | 출처 | 성격 |
|---|---|---|---|
| 소파–TV장 거리 | 2~3 m | Infinigen `hinge(2,3)` | 소프트(비용 최소화) |
| 사이드테이블–벽 | 0.3 m 이내 | Infinigen `hinge(0,0.3)`, weight 10 | 소프트 |
| 소파 벽 마진 | 0.1~0.3 m | Infinigen `StableAgainst(cu.back, cu.walltags, margin=uniform(0.1,0.3))` | 관계 제약(margin은 무작위 샘플) |
| 조명 간 최소 간격 | 1 m 이상 | Infinigen `min_distance_internal(lights) >= 1` | **하드** |
| 소파가 TV를 향함 | `focus_score < 0.5` | Infinigen | **하드** |
| 러그끼리 최소 간격 | 1 m | Infinigen | 조건(하드/소프트 구분 미확인) |
| 벽 장식 바닥 높이 | 0.6 m 초과 | Infinigen | 조건(하드/소프트 구분 미확인) |
| 천장등 밀도 | hinge(0.08, 0.15)/m² | Infinigen | 소프트 |
| 커피테이블–소파 | **0.45~0.6 m** | Infinigen `hinge(0.45, 0.6)` | 소프트 |
| 커피테이블–소파 | **0.3~0.5 m** | SceneSmith designer 프롬프트 | 프롬프트 규칙 |
| 주동선 | 0.7~1.0 m | SceneSmith | 프롬프트 규칙 |
| 카운터 뒤 | 0.5~0.7 m | SceneSmith | 프롬프트 규칙 |
| 무관한 물체 간 | 0.2 m 이상 | SceneSmith (충돌 해소 1단계의 "넉넉한 간격부터 시도" 맥락) | 프롬프트 규칙 |
| 그림·거울 중심 높이 | 1.4~1.7 m (대형 작품 1.2~1.5, 선반 1.2~1.8, 시계 1.5~1.8) | SceneSmith [wall designer](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/wall_agent/designer_agent.yaml) | 프롬프트 규칙 |
| 가구 위 벽걸이 | 가구 상단 위 20~40 cm, 그룹 간격 0.1~0.3 m | SceneSmith wall designer | 프롬프트 규칙 |
| 가구 점유율 | 30~40% | SAGE 프롬프트 | 프롬프트 규칙 |
| 주요 가구 사이 동선 | 60~90 cm | SAGE 프롬프트 | 프롬프트 규칙 |
| 문 회전 여유 | 약 90 cm | SAGE 프롬프트(솔버는 문 폭×문 폭 정사각형) | 프롬프트 규칙 |
| near / far | 50~150 cm / 150 cm 이상 | Holodeck(SAGE 프롬프트에도 같은 정의) | 어휘 정의 |
| 같은 종류 벽걸이 | 같은 높이 | Holodeck | 프롬프트 규칙 |

Infinigen 값은 [home.py v1.16.0](https://raw.githubusercontent.com/princeton-vl/infinigen/v1.16.0/infinigen_examples/constraints/home.py)에서 확인했습니다. 소프트 비용항과 하드 제약이 섞여 있으니 가져올 때 구분하세요.

### 6.2 인테리어 가이드·표준 값 (G1 보완 조사)

| 항목 | 값 | 출처 | 신뢰도·비고 |
|---|---|---|---|
| 거실 주 통행로 | 760~910 mm (30~36 in) | [Homes & Gardens](https://www.homesandgardens.com/interior-design/living-rooms/a-guide-to-living-room-clearances-measurements-and-spacing), [Apartment Therapy](https://www.apartmenttherapy.com/living-room-layouts-the-ideal-measurements-for-everything-in-the-room-206734), [Keck](https://keckfurniture.com/blog/living-room-layout-rules-traffic-flow-conversation-zones-and-tv-placement/) | 높음 |
| 소파 앞면–커피테이블 | 356~457 mm (14~18 in) | Homes & Gardens, Apartment Therapy | 높음 |
| 커피테이블 높이 | 406~457 mm, 소파 좌판과 같거나 25~50 mm 낮게 | Apartment Therapy | 중간 |
| 커피테이블 길이 | 소파 길이의 약 1/2~2/3 | Apartment Therapy | 낮음(관행) |
| TV 시청거리 | 대각선의 1.5~2.5배(유통·인테리어 가이드). 55형 2.13~2.74 m, 65형 2.44~3.05 m | Keck | 중간 |
| TV 시청거리(시야각 기준) | 16:9에서 30° → 약 1.63배, 36° → 약 1.34배, 40° → 약 1.20배(65형 × 1.2~1.6 ≈ 1.98~2.64 m) | 산술은 맞지만 THX·SMPTE 원문 **미확인** | 보조 기준 |
| 벽 그림 중심 | 1450 mm (57 in). 일부 1520 mm (60 in) | [Rule of 57](https://www.ashanging.com/en_us/help/what-is-the-rule-of-57) | 높음. 가구 위에서는 가구 상단 기준 여백 우선 |
| 식탁 가장자리–벽 | 915 mm 이상(의자 빼기) | [Eureka](https://eurekaergonomic.com/blogs/eureka-ergonomic-blog/dining-table-space-clearance-guide) | 높음 |
| 식탁 뒤 여유 (NKBA 3단계) | 지나가는 사람 없음 **813 mm(32 in)** / 비켜 지나감 914 mm(36 in) / 걸어서 지나감 1118 mm(44 in) | [NKBA 지침 사본](https://newcreationsaustin.com/wp-content/uploads/2019/05/nkba-planning-guidelines.pdf), [CRD 요약](https://www.crddesignbuild.com/blog/kitchen-dimensions-code-requirements-nkba-guidelines/) | **정정됨**: "통행 없으면 915 mm(NKBA)"는 틀림 |
| 의자 빼는 거리 | 460~610 mm | [Sicotas](https://sicotas.com/blogs/blogs-sicotas-brand-story/minimum-space-around-dining-table) | 중간 |
| 식탁 1인당 폭 | 610 mm(일상), 710~760 mm(격식) | [NEPA](https://www.nepafurniture.com/blog/home-furniture-32/dining-table-size-guide-based-on-number-of-people-414) | 높음 |
| 펜던트(식탁 위) | 상판~조명 하단 760~860 mm(일부 760~915) | [Fenchel Shades](https://www.fenchelshades.com/blog/post/pendant-lights-over-dining-table-height-standard-measurements-and-placement-guide-2026-usa) | 높음. 한국 천장고 2300이면 바닥 기준 약 1550~1600 mm(계산값) |
| 다등 펜던트 간격 | 중심 간 610~760 mm, 최대 915 mm | [2Modern](https://www.2modern.com/blogs/modern-how-to/how-far-apart-should-pendant-lights-be) | 중간 |
| 협탁 높이 | 매트리스 상단 ±50 mm | [Froy](https://froy.com/blogs/tips/how-tall-should-a-nightstand-be-the-nightstand-height-guide) | 높음 |
| 침대 옆 통로 | 최소 600, 쾌적 750~900 mm | 출처 없음 | 낮음(관행) |
| 러그(거실) | 소파 양끝 바깥으로 150 mm 이상, 모든 좌석 앞다리 2개가 러그 위 | Homes & Gardens, [Toparredi](https://www.toparredi.com/en/living-room-layout-dimensions-spacing-guide) | 중간 |
| 러그–벽 여백 | 최소 150, 작은 방 305~457, 큰 방 610 mm | Homes & Gardens | 중간 |
| 러그(식탁 아래) | 식탁 모서리 바깥 600~760 mm | 출처 없음 | 낮음(관행) |
| 주방 작업 통로 | 1인 1067 mm / 다인 1219 mm (NKBA) | CRD 요약 | 독립 재검증 안 됨 |
| 워크 트라이앵글 | 3변 합 7925 mm 이하, 각 변 1219~2743 mm | CRD 요약 | 독립 재검증 안 됨 |

**하드 제약과 소프트 선호로 나눠서 넣으세요.** 법규·최소 통로(예: 주동선 ≥ 760 mm, 선호 910; 식탁–벽 ≥ 915; 한국 계단 단높이 ≤ 180 mm)는 솔버의 하드 조건이나 검사 assert로, 그림 높이(1450 ± 50 mm)나 펜던트 높이(760~860 mm)는 비용항으로 넣습니다. 출처끼리 값이 다르면 **범위를 저장하고 범위 안에서 약간씩 흩뜨리세요.** 모든 의자가 정확히 450 mm면 오히려 CG처럼 보입니다.

### 6.3 [한국 사용자] 한국 프리셋

| 항목 | 한국 값 | 비교 | 비고 |
|---|---|---|---|
| 아파트 천장고 | 구축 2300 mm, 최근 신축 2400~2500 mm | 미국 2438 mm(8 ft) | 연식별 프리셋. 층고 2800~2850 mm([한국PM](https://hkpm.co.kr/%EC%9D%BC%EB%B0%98%EC%A0%81%EC%9D%B8-%EC%95%84%ED%8C%8C%ED%8A%B8-%EC%B8%B5%EA%B3%A0%EC%99%80-%EC%B2%9C%EC%9E%A5%EA%B3%A0-%EA%B8%B0%EC%A4%80%EA%B3%BC-%EC%9D%98%EB%AF%B8-%EA%B4%80%EA%B3%84/), 신축 추세 [서울경제TV](https://www.sentv.co.kr/article/view/sentv202209140082)) |
| 방문 | 900×2100 mm(가장 많이 쓰는 폭 900·1000) | 미국 813×2032 mm(관행값, 출처 미확인) | **문틀 기준 치수**. 문짝은 약 60 mm 작음. 벽 boolean에는 개구부(문틀 외곽) 치수를 씀 |
| 욕실문 | 700×2000 ~ 800×2100 mm | — | 문틀 기준 |
| 매트리스 Q | 1500×2000 mm (조사 6개사 공통) | 미국 Queen 1524×2032 | [소비자가만드는신문](https://www.consumernews.co.kr/news/articleView.html?idxno=713641) |
| 매트리스 K / LK | K 1600~1670 × 2000~2075, LK 1700~1800 × 2000~2075 mm | 미국 King 1930×2032 | 업체마다 다름([에이스 킹 1670×2075 등](https://www.consumernews.co.kr/news/articleView.html?idxno=520936)). 브랜드 미지정 시 1600/1800×2000 |
| 싱크대 높이 | 850 mm(신축·리모델링은 900도) | 미국 914 mm | 상하부장 간격 650~750 mm(미국 457 mm) |
| 주방 수직 모듈 | 하부장 850 + 미드웨이 약 700 + 상부장 약 750 ≈ 2300 mm | — | [LX Z:IN](https://www.lxzin.com/styling/style-guide/detail/5596) |
| 주방 통로 | 900 mm 이상(실무) | NKBA 1067 mm | [한국 실무 SNS](https://www.threads.com/@ideabuild_official/post/DQ8kvc-kRe7), 신뢰도 중간 |
| 거실 창 | 발코니 창이 바닥부터 시작하는 경우가 많음(관행, 출처 미확인) | 침실 창대 약 900 mm(미확인) | 창 앞을 keep-out으로 |
| 공동주택 공용계단 | 단높이 ≤ 180 mm, 단너비 ≥ 260 mm, **높이 2 m를 넘으면 2 m 이내마다 계단참(너비 120 cm 이상)** | IRC 단높이 ≤ 197 mm | **정정됨**: "3 m마다"는 일반 건축물 기준. 층고 2800 mm 직통 16단은 위법 → 8단 + 참 + 8단 |

- **IKEA PAX 높이 2360 mm는 구축 천장고 2300 mm에 들어가지 않습니다.** 2010 mm 모델이나 맞춤 붙박이장을 쓰세요(신축 2400 mm 이상이면 들어감).
- **이름 대신 mm 값을 넘기세요.** 'King'은 한국 1600, 미국 1930, 영국 1500, EU 1600 mm 폭으로 모두 다릅니다. 예: `bed={region:'KR', mattress_mm:[1500,2000]}`.
- 전체 표는 [실측 치수 기준표](../03_playbooks/05_reference_dimensions.md)에 있습니다.

---

## 7. 야외·환경 산포

### 7.1 원칙

- **수천 개 인스턴스를 LLM이 좌표로 찍는 것은 불가능합니다.** LLM은 산포 **파라미터**(최소 간격, 밀도, 마스크, 스케일 범위, 시드)만 조정하게 하세요. 비파괴적이고 결과가 안정적입니다.
- **Distribute Points on Faces**(Geometry Nodes): 입력 Mesh, Selection, Distance Min(기본 0), Density Max(기본 10), Density(기본 10), Density Factor(0~1, 기본 1), Seed. 모드는 Random과 **Poisson Disk**(최소 간격 보장). 출력 Points, Normal, Rotation([소스](https://raw.githubusercontent.com/blender/blender/main/source/blender/nodes/geometry/nodes/node_geo_distribute_points_on_faces.cc), 기본값은 검증에서 확인). Instance on Points와 조합합니다.

### 7.2 구성 규칙

| 요소 | 규칙 | 근거·신뢰도 |
|---|---|---|
| 최소 간격(Distance Min) | 큰 나무 3~6 m, 관목 1~2 m, 바위 0.5~2 m | 실무 경험치(미검증) |
| 밀도 마스크 | 길·건물 주변은 Selection 또는 Density Factor 0, 거리 기반 falloff | 조사 제안 |
| 정렬 | 나무는 월드 Z, 바위·풀은 표면 Normal + 약간의 틸트 | 조사 제안 |
| 변주 | 균일 스케일 0.8~1.2, Z 회전 0~360° | 조사 제안 |
| 바위 | Normal 정렬 + 표면에 10~20% 묻기 | 조사 제안 |
| 클러스터 | 3·5·7개 단위, 크기 비 1 : 0.6 : 0.3 | 조사 제안 |
| 밀도 구역 | Hero(상호작용) 구역은 의도는 높게 잡음은 낮게, 중경은 스토리 클러스터, 배경은 드물게 실루엣만, 이동 경로·카메라 경로는 비움 | [blender-skills set-dressing](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/set-dressing/SKILL.md) — 약 2 KB 개인 스킬 문서라 **아트디렉션 체크리스트 수준으로만** 인용 |
| 스토리 비트 | 비트(버려진 식사, 쓰던 작업대, 급한 탈출)마다 소품 3~7개 + 마모·데칼 단서 1~2개. 균일하게 깔린 잡동사니 금지 | 같은 출처(체크리스트 수준) |
| 작업 순서 | 그레이박스로 스케일·동선 확정 → 모듈 키트는 그리드 스냅 → 반복 메쉬는 인스턴싱 → 스토리 클러스터 드레싱 | 같은 저장소 [scene-assembly](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/scene-assembly/SKILL.md) |

**숲길 예시(조사에서 제안된 구성)**: 길 커브에서 거리 attribute를 계산해 0~1.5 m는 밀도 0, 1.5~4 m는 풀·관목 고밀도(점점 감소), 4 m 이상은 나무(Distance Min 4 m). 카메라 3분할 교차점에 hero 바위 + 쓰러진 나무 클러스터(3~5개, 크기 1 : 0.6 : 0.3), 전경에 프레이밍용 잎, 배경은 저밀도 실루엣. 구도(삼분할, 전경·중경·배경 레이어)는 [조명·아트디렉션 가이드](06_lighting_rendering_art_direction.md)를 함께 보세요.

### 7.3 산포 코드 (Blender 4.2.23 LTS / 5.0.1에서 실행 확인)

길 주변을 비우는 밀도 가중치(버텍스 그룹)를 칠하고, Poisson Disk 산포 + 컬렉션 랜덤 선택 + 랜덤 Z 회전·균일 스케일을 거는 Geometry Nodes 모디파이어를 만듭니다. 40×40 m 지면, 나무 3종, Distance Min 4 m로 돌린 테스트에서 인스턴스 46개, 최소 간격 4.009 m, 길에서 가장 가까운 나무 3.12 m(비움 반경 1.5 m)였습니다.

```python
import bpy, math

def paint_density(ground, path_pts, clear=1.5, falloff=2.5, name="density"):
    """길(점 목록, 월드 좌표 Vector)에서 clear m 안은 0, 그 뒤 falloff m에 걸쳐 1까지 올라가는 밀도 가중치."""
    vg = ground.vertex_groups.get(name) or ground.vertex_groups.new(name=name)
    mw = ground.matrix_world
    for v in ground.data.vertices:
        p = mw @ v.co
        d = min((p.xy - q.xy).length for q in path_pts)
        vg.add([v.index], max(0.0, min(1.0, (d - clear) / falloff)), 'REPLACE')

def add_scatter(ground, collection, dist_min=4.0, density_max=0.08, seed=0,
                scale=(0.8, 1.2), density_attr="density", name="GN_Scatter"):
    ng = bpy.data.node_groups.new(name, 'GeometryNodeTree')
    ng.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    N, L = ng.nodes, ng.links
    by_id = lambda socks, ident: next(s for s in socks if s.identifier == ident)   # 이름 대신 identifier
    gi, go = N.new('NodeGroupInput'), N.new('NodeGroupOutput')
    dist = N.new('GeometryNodeDistributePointsOnFaces')
    dist.distribute_method = 'POISSON'                              # 최소 간격 보장
    by_id(dist.inputs, 'Distance Min').default_value = dist_min
    by_id(dist.inputs, 'Density Max').default_value = density_max
    by_id(dist.inputs, 'Seed').default_value = seed
    attr = N.new('GeometryNodeInputNamedAttribute')                  # 버텍스 그룹 = 밀도 마스크
    attr.data_type = 'FLOAT'
    by_id(attr.inputs, 'Name').default_value = density_attr
    coll = N.new('GeometryNodeCollectionInfo')
    by_id(coll.inputs, 'Collection').default_value = collection
    by_id(coll.inputs, 'Separate Children').default_value = True
    by_id(coll.inputs, 'Reset Children').default_value = True
    inst = N.new('GeometryNodeInstanceOnPoints')
    by_id(inst.inputs, 'Pick Instance').default_value = True
    r_idx = N.new('FunctionNodeRandomValue'); r_idx.data_type = 'INT'
    by_id(r_idx.inputs, 'Min_002').default_value = 0
    by_id(r_idx.inputs, 'Max_002').default_value = len(collection.objects) - 1
    by_id(r_idx.inputs, 'Seed').default_value = seed + 1
    r_rot = N.new('FunctionNodeRandomValue'); r_rot.data_type = 'FLOAT'   # Z 회전 0~360°
    by_id(r_rot.inputs, 'Min_001').default_value = 0.0
    by_id(r_rot.inputs, 'Max_001').default_value = 2 * math.pi
    by_id(r_rot.inputs, 'Seed').default_value = seed + 2
    rot = N.new('ShaderNodeCombineXYZ')
    r_scl = N.new('FunctionNodeRandomValue'); r_scl.data_type = 'FLOAT'   # 균일 스케일 0.8~1.2
    by_id(r_scl.inputs, 'Min_001').default_value = scale[0]
    by_id(r_scl.inputs, 'Max_001').default_value = scale[1]
    by_id(r_scl.inputs, 'Seed').default_value = seed + 3
    join = N.new('GeometryNodeJoinGeometry')
    L.new(gi.outputs[0], dist.inputs['Mesh'])
    L.new(by_id(attr.outputs, 'Attribute'), by_id(dist.inputs, 'Density Factor'))
    L.new(dist.outputs['Points'], inst.inputs['Points'])
    L.new(coll.outputs['Instances'], inst.inputs['Instance'])
    L.new(by_id(r_idx.outputs, 'Value_002'), by_id(inst.inputs, 'Instance Index'))
    L.new(by_id(r_rot.outputs, 'Value_001'), rot.inputs['Z'])
    L.new(rot.outputs['Vector'], by_id(inst.inputs, 'Rotation'))
    L.new(by_id(r_scl.outputs, 'Value_001'), by_id(inst.inputs, 'Scale'))
    L.new(gi.outputs[0], join.inputs[0])                              # 지면도 함께 출력
    L.new(inst.outputs['Instances'], join.inputs[0])
    L.new(join.outputs[0], go.inputs[0])
    mod = ground.modifiers.new(name, 'NODES')
    mod.node_group = ng
    return mod

# 사용: 지면은 촘촘하게 분할(예: 0.5 m 격자)해야 마스크가 부드럽다
# paint_density(bpy.data.objects["ground"], path_points, clear=1.5, falloff=2.5)
# add_scatter(bpy.data.objects["ground"], bpy.data.collections["TREES"], dist_min=4.0, seed=7)
```

- **[한국 사용자]** 노드는 `bl_idname`(type)으로 만들고 소켓은 `identifier`로 찾았습니다. Random Value 노드는 데이터 타입마다 같은 이름('Min', 'Max', 'Value')의 소켓이 여러 개라서 이름으로 찾으면 엉뚱한 소켓(비활성 벡터용)에 값이 들어갑니다. FLOAT는 `Min_001`/`Max_001`/`Value_001`, INT는 `Min_002`/`Max_002`/`Value_002`입니다(4.2.23·5.0.1 동일). 한국어 UI에서 새 노드 이름이 번역되는 문제는 [Blender MCP 가이드 12절](02_blender_mcp.md)을 보세요.
- 산포 확인: `depsgraph.object_instances`에서 `is_instance`인 항목의 `matrix_world`로 최소 간격·금지 구역 침범을 숫자로 검사할 수 있습니다. 테스트도 이 방법으로 했습니다.
- Geo-Scatter(구 Scatter5) 같은 상용 애드온은 이 위에 biome 프리셋·마스크 UI를 얹은 도구로 알려져 있지만, 버전·가격·기능은 이번 조사에서 확인하지 못했습니다(미확인).

### 7.4 게임 엔진에서 배치할 때

- 대규모 월드의 산포·폴리지·PCG는 엔진에서 조립하는 편이 낫습니다. 형태(히어로 에셋, UV, 트림시트)는 Blender에서, 배치·PCG·조명은 엔진에서 나누는 것이 조사된 사례의 공통 분업입니다([엔진 MCP 가이드](03_other_mcp_dcc_cad_engines.md)).
- per-simmons 하네스(Claude + UE 5.8 공식 MCP)의 교훈: 에디터는 게임 스레드가 하나이므로 **모든 씬 변경을 직렬로** 호출하고, PCG는 그래프 하나·볼륨 하나 단위로 순차 실행합니다. 지붕처럼 "위에 얹는" 오브젝트는 PCG 그래프 안에서 풀지 말고 기존 액터의 bounds를 조회해 좌표를 계산한 뒤 별도 액터로 배치합니다([PCG-GUIDE](https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/PCG-GUIDE.md), [REALISM-GUIDE](https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/REALISM-GUIDE.md)). 작성자 결론도 "real but raw"입니다.
- Unity는 [MCP for Unity(CoplayDev)](https://github.com/CoplayDev/unity-mcp)가 씬·게임오브젝트 제어의 기본 선택지입니다.

### 7.5 야외 배치 연구 현황

- Tencent Hunyuan [WorldClaw](https://github.com/Tencent-Hunyuan/Hunyuan3D-WorldClaw)(에이전트 오픈월드, 2026-08): 현재 저장소는 README만 있습니다. Hunyuan 계열이므로 공개되더라도 한국 적용 여부를 라이선스 원문으로 확인하세요.
- [LandCraft](https://github.com/RyuZhihao123/LandCraft_26)(조경, 코드 준비 중), GardenDesigner(목록상 CVPR 2026, **중국 장난(江南) 고전 원림**의 미학 원칙을 에이전트 체인으로 인코딩. 서울 강남이 아님), RAISECity·MajutsuCity·Yo'City(도시 스케일)는 대부분 코드가 미공개이거나 일부만 공개됐습니다.

---

## 흔한 실수와 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| 가구가 180° 뒤집혀 벽을 봄 | 에셋 정면 규약 불일치. Holodeck [#92](https://github.com/allenai/Holodeck/issues/92)(정면 정렬 의문, 무응답), I-Design `place_in_blender.py`의 `z_angle + π` 보정이 같은 문제의 흔적 | 가져올 때 정면을 -Y로 정규화하고 `front_axis` 메타데이터 저장. 규약 오프셋은 변환 함수 하나에서만 |
| 일부 가구만 크기·회전이 틀림 | 메쉬 스케일·회전 정규화 누락. LayoutVLM [#9](https://github.com/sunfanyunn/LayoutVLM/issues/9) | `transform_apply(rotation=True, scale=True)` 후 배치. `obj.dimensions`는 scale이 (1,1,1)일 때만 믿을 것 |
| 의자·소파 비율이 찌그러짐 | 목표 치수에 맞춘 **비균일 스케일**(I-Design 방식) | 최대 축 기준 균일 스케일만. 비율이 안 맞으면 에셋을 교체 |
| 물체가 떠 있거나 바닥에 박힘 | LLM이 준 z값, 원점이 바닥 중앙이 아님 | z는 `snap_to_floor`·`drop_to_surface`로 계산 |
| 90°·180° 방향 오류 | yaw 부호·0° 기준이 섞임 | 규약을 툴 설명에 명시하고 `check_facing`(내적 > 0.9)으로 검증 |
| 소품이 받침면 위 약 4 cm에 떠서 멈춤 | rigid body 기본 충돌 여백 0.04 m | `use_margin=True`, `collision_margin=0.001` (4.7절) |
| 관통 검사가 "0"인데 물체가 안에 들어가 있음 | `overlap()`은 표면 교차만 잡음 | AABB 포함·겹침 깊이 검사 병행 |
| 두 물체 BVH 비교 결과가 이상함 | `BVHTree.FromObject`는 로컬 좌표 | 월드 변환 정점으로 트리 생성(`scene_audit.py` 방식) |
| `scene_audit`이 가구를 치수 이상(`size_out_of_range`)으로 보고 | 이름에 종류 단어가 없거나 다른 단어로 지음(한국어 이름은 인식 안 함), 지역 범위가 맞지 않음. 예전 스크립트의 armchair·90° 회전 오탐은 고쳐짐(단어 단위 매칭, 가구 방향 기준 w/d/z) | 영어 snake_case 이름(`armchair_01`, `coffee_table`), 한국 장면은 [치수표](../03_playbooks/05_reference_dimensions.md) 11절 `KR_SIZE_RULES`를 `size_rules=`로 넘기기 |
| MCP 호출이 멈추거나 타임아웃 | 한 번에 너무 큰 코드(ahujasid 소켓 180초, 애드온 `exec()`는 제한 없음) | 객체 1~3개 단위의 원자적 호출. 고폴리 검사는 프록시로 |
| 가구가 벽을 따라 흩어진 "대기실" | 초점·그룹 없음 | 4.2절: 초점 → 그룹 → 동선 → 관계 순서 |
| 문 앞·창 앞이 막힘 | 배치 후 동선을 고려 | keep-out을 먼저 깔고 솔버의 하드 조건으로 |
| 너무 반듯해서 CG 같음 / 너무 흩어져 혼란스러움 | 노이즈 없음 / 무작위 회전 | SceneSmith Natural 프로파일(가구 σ 0.03 m·1°, 소품 σ 0.01 m·3°) |
| 균일하게 깔린 잡동사니 | 서사 없는 채우기 | 스토리 비트당 소품 3~7개 클러스터, 배경은 실루엣만 |
| 에이전트가 계속 고치다 더 나빠짐 | 종료·롤백 규칙 없음 | 9점 이상 종료, 최대 3라운드, −2/−1점 하락 시 체크포인트 복원(4.9절) |
| Infinigen 실내 생성 명령이 main에서 실패 | main(v2.0 알파)에서 v1 Indoors 모듈 삭제, 문서만 남음 | `git checkout v1.16.0` |
| 한국 아파트인데 어색함 | 천장고 2438·2700 mm, 미국식 매트리스·조리대 치수 | 6.3절 한국 프리셋, 이름 대신 mm |
| 한국어 UI에서 노드 코드가 깨짐 | 새 노드 이름 번역 | type·identifier로 찾기, New Data 번역 끄기 |
| 상업 프로젝트에서 데이터·생성 모델 문제 | 3D-FRONT/HSSD 약관 미확인, Hunyuan3D 한국 제외 | 3.5절, [라이선스 가이드](10_assets_pipeline_licensing.md) |

---

## 관련 문서

- [건축 상식 검사 `building_audit.py`](../03_playbooks/scripts/README.md): 문·창·방 연결·동선·계단의 비상식(백룸식 기묘함) 자동 검출
- [오브젝트·가구·조형물 모델링](07_modeling_objects_furniture_sculpture.md): 에셋 정면·원점·스케일 정규화, 부품 분해
- [에이전트 워크플로·프롬프팅](09_agent_workflow_prompting.md): 시각 피드백 루프, 스킬·CLAUDE.md, 토큰 비용
- [Blender MCP 생태계](02_blender_mcp.md): 서버 선택, 타임아웃, undo·버전 저장, 한국어 UI 문제
- [기타 DCC·게임 엔진 MCP](03_other_mcp_dcc_cad_engines.md): Unreal PCG, Unity, Godot 배치
- [AI 3D 생성](04_ai_3d_generation.md): 배치용 에셋 생성과 후처리
- [조명·렌더·아트디렉션](06_lighting_rendering_art_direction.md): 구도, 전경·중경·배경
- [에셋 파이프라인·라이선스](10_assets_pipeline_licensing.md): 데이터셋·Hunyuan3D 지역 제한
- [학술 연구](11_research_papers.md): 레이아웃 논문 주석
- [AI 모델·클라이언트](01_ai_models_and_clients.md): 계획·비평 모델 선택, 비용
- [실측 치수 기준표](../03_playbooks/05_reference_dimensions.md) · [보조 스크립트](../03_playbooks/scripts/README.md) · [AAA 제작 플레이북](../03_playbooks/02_aaa_production_playbook.md) · [프롬프트 템플릿](../03_playbooks/03_prompt_templates.md) · [품질 체크리스트](../03_playbooks/04_quality_checklists.md)
- [CLAUDE.md 템플릿](../03_playbooks/templates/CLAUDE.md) · [스킬 템플릿](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md)
- [사례 모음](../04_case_studies/01_case_studies.md) · [검증 로그](../01_research/verification_log.md) · [출처 카탈로그](../01_research/sources_catalog.md)

## 원자료

- `01_research/raw/09_scene-layout.research.json`: 배치·레이아웃 1차 조사(항목 24, 노하우 22, 사례 8, 출처 50)
- `01_research/raw/09_scene-layout.verify.json`: 독립 검증(판정 24, 항목 점검 15, 신뢰도 낮은 출처 6, 누락 항목 9)
- `01_research/raw/G1_dimensions.gap.json`: 실측 치수 보완 조사(측정값 136행)
- `01_research/raw/G1_dimensions.verify.json`: 치수 재검증(계단참 2 m 정정, NKBA 식탁 뒤 3단계 정정, 매트리스·천장고 조건 추가)
- 보조: `01_research/raw/13_research-papers.research.json`, `13_research-papers.verify.json`(SceneReVis 충돌률 비교표, SceneSmith 결과), `G6_benchmarks_models.gap.json`(LayoutVLM PSA, BlenderGym 배치 수치), `04_engine-mcp.research.json`·`04_engine-mcp.verify.json`(UE PCG 배치 교훈)
- 이 문서의 솔버·적용·안착·산포 예제 코드는 작성 시 Blender 4.2.23 LTS와 5.0.1(pip `bpy`)에서 실행해 결과를 확인했습니다(저장소 테스트 스위트에는 포함되지 않음).
