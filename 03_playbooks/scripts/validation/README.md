# `building_audit.py` 실제 AI 건물 검증 기록

> 작성: 2026-09-27 · 대상 스크립트: [`../building_audit.py`](../building_audit.py) · 원자료: [`raw/`](raw/) · 재현 도구: [`tools/`](tools/)

## 1. 왜 했나

처음 만든 `building_audit.py`(v1)는 직접 만든 상자형 집으로만 테스트했습니다. 사용자 요청("네트워크 정책 때문에 안 되는 건 빼고 2번만")에 따라
**실제 AI가 만든 건물**에 돌려서 오탐(멀쩡한데 문제라고 함)과 미탐(문제를 못 잡음)을 재고, 원인을 일반 규칙으로 고쳤습니다.
기준은 "사람이 설계한 건물처럼 말이 되는가(백룸처럼 기묘하지 않은가)"입니다.

## 2. 검사한 장면 — 실제 AI 생성 건물 9개

| 장면 | 만든 AI | 형식 | 이 장면이 까다로운 점 |
|---|---|---|---|
| Realsee 재구성 공간 1개 | GPT-6 Astra (Codex에서 Blender 직접 조작) | 원본 `.blend` ([realsee-astra-blender](https://github.com/realsee-developer/realsee-astra-blender), Git LFS) | 실제 사무·쇼룸 공간 재구성. 벽 44개가 조각조각, 문틀·걸레받이 등 마감재 80여 개, 90° 열린 문, 문짝 없는 출입구, 오픈 셀 격자 천장, 외부 지면 없음 |
| house-3d Fable 판 4개 스타일 | Claude Fable 5.1 | three.js 앱 → GLB → Blender ([house-3d](https://github.com/hahaliu1029/house-3d) `fable/`) | 같은 110 m² 아파트 평면(방 10곳). **벽 전체가 메시 1개**, 모든 것이 `house/floors/openings` 그룹 아래, 커튼이 창 오브젝트에 포함, 베이창(飘窗), 3.6 m 유리 미닫이 |
| house-3d GPT-6 판 4개 스타일 | GPT-6 | three.js 앱 → GLB → Blender (같은 저장소 `gpt6/`) | 같은 평면. **이름이 전부 중국어**, 벽·창틀·유리를 **재질별로 합침**(모든 창이 오브젝트 1개), 열린 채 구멍 옆에 겹쳐 둔 미닫이 문짝 |

- house-3d는 두 AI가 **같은 평면도**로 만든 결과라, 같은 규칙으로 두 AI의 결과물을 비교할 수 있습니다.
- Fable 판은 앱 데이터에 있는 열림부 종류(door/window/arch)를 glTF extras → Blender 커스텀 속성 `obj["role"]`로 넘겼습니다(스크립트가 공식 지원하는 방식). GPT-6 판은 이름만으로 판정했습니다.
- 렌더 이미지는 저장소에 넣지 않았습니다(Realsee는 코드만 MIT이고 사진 텍스처 권리는 별도, house-3d는 Apache-2.0이지만 입력 평면도 권리는 별도). 아래 도구로 누구나 다시 만들 수 있습니다.

## 3. 결과 — 전후 비교

| 장면 | v1 (원래) | v2 첫 실행 | **최종** | 백룸 위험도 |
|---|---|---|---|---|
| Realsee × Astra | 오류 18 · 경고 10 (방 6, 위험도 high) | 오류 3 · 경고 7 | **오류 0 · 경고 1** | medium (이유는 아래) |
| Fable 현대식 | 오류 0 · 경고 0 — **방·문·창을 하나도 못 알아봄(조용한 실패)** | 오류 35 · 경고 43 | **오류 0 · 경고 8** | low |
| Fable 프렌치 / 이탈리안 / 송 | (같은 구조) | — | 오류 1 / 0 / 0 · 경고 6 / 8 / 8 | low |
| GPT-6 현대식 | 오류 0 · 경고 0 — **방 0개 인식(조용한 실패)** | 오류 7 · 경고 21 | **오류 0 · 경고 8** | low |
| GPT-6 프렌치 / 이탈리안 / 송 | (같은 구조) | — | 오류 0 · 경고 9 / 8 / 8 | low |

- 최종 인식 결과: Realsee 방 5·문 4 / Fable 방 10·문 9·창 9 / GPT-6 방 9·문 8·창 10 — 원본 앱 데이터(`fable/src/plan.js`, `gpt6/src/layout.js`)와 방 연결, 창턱 높이(욕실 1.5 m, 침실 0.9 m, 베이창 0.45~0.55 m, 주방 1.0 m 등)가 일치합니다.
- 검사 시간: Realsee(오브젝트 약 1,000개) 약 90~100초, house-3d 1~5초.
- 원자료: `raw/realsee_astra_v1.json`(v1), `raw/realsee_astra_v2.json`, `raw/house3d_{fable,gpt6}_{style}.json`, v1이 house-3d를 못 알아본 결과 `raw/house3d_{fable,gpt6}_modern_v1.json`.

## 4. 남은 지적은 진짜인가 — 하나씩 확인

좌표 확인, 레이 측정, 평면도 렌더(`tools/render_plan.py`), 원본 앱 데이터 대조로 확인했습니다.

| 장면 | 남은 지적 | 확인 결과 |
|---|---|---|
| Realsee | 거실 `windowless_room` | **맞음.** 창 오브젝트가 없고, 거실 끝 '풍경'은 사진 패널(재질 `PhotoGraphicStation8`), 유리 미닫이는 방 안 벽감 칸막이. 위험도 medium은 "창 없는 거실 + 복도 면적 40%" 때문이며 사무 공간이라 의도일 수 있음 |
| Fable 4종 | 다다미방 문 `door_narrow` | **맞음.** 1.2 m 양개 유리문 바로 앞 0.16 m에 책상이 문 폭의 절반을 막고, 남은 0.53 m 틈 0.68 m 앞에 의자. 송 스타일은 발코니 미닫이 앞 라운지 의자로 1건 더 |
| Fable 프렌치 | 주욕실 문 `door_blocked` (오류) | **맞음.** 문을 들어서면 0.5 m 안에서 변기와 세면대 사이가 0.43 m. 이탈리안 판은 변기가 17 cm 더 떨어져 있어 경고만 나옴 |
| Fable 4종 | 동쪽 벽 창 `window_misaligned` 0.29 m | **맞음(가벼운 설계 불일치).** 같은 외벽에서 욕실 창 윗선 2.2 m, 침실 창 윗선 2.5 m (`plan.js` 창턱+높이) |
| Fable·GPT-6 | `door_clearance` (욕실 변기·세면대, 현관 벤치, 협탁 등) | **그럴듯함(약한 경고).** 문 여는 방향을 모르므로 "여닫이라면 부딪힘"으로 표시 |
| GPT-6 4종 | 발코니 옆창 `window_awkward_sill` 0.17 m | **맞음.** `layout.js`의 설계값이 창턱 0.18 m |
| GPT-6 4종 | 주방 창 `window_blocked` 40% | **맞음.** 창턱 0.87 m가 조리대(약 0.9 m)보다 낮아 조리대·수전이 창 아래쪽을 가림. 프렌치 스타일은 발코니 낮은 수납장이 옆창 26%를 가리는 것 1건 더 |
| GPT-6 4종 | 공용 욕실 미닫이 `door_narrow` | 그럴듯함. 문 안쪽 가까이 변기 |

**백룸 오경보는 한 건도 없었습니다**(9개 장면 모두 low 또는 설명 가능한 medium).

## 5. 고친 오탐·미탐과 원인 (모두 일반 규칙으로 고침)

| # | 증상 | 원인 | 고친 방식 | 회귀 테스트 |
|---|---|---|---|---|
| 1 | 문짝 없는 출입구·아치로 이어진 방을 "밀폐된 방"으로 | 문 오브젝트만 연결로 봄 | 방 바닥 가장자리에서 벽 쪽으로 레이를 쏴 출입구·통로·창 구멍을 형상으로 찾음 | 기존 테스트 |
| 2 | 90° 열려 옆벽에 붙은 문짝 → "양쪽이 같은 방" | 겹치는 부피로 벽을 고름 | 후보마다 **실제 구멍**을 찾고 "문짝 폭과 맞고 문짝과 붙은 구멍"을 고름. 문짝 끝(경첩)에서 직각으로 이어지는 가설 추가 | `test_merged_walls_in_container_groups` |
| 3 | 인방(LINTEL)·문틀(FRAME)·걸레받이를 가구로 | 이름 규칙 부족 | 마감재 역할(trim), 인방·헤더·소핏은 벽 | 실제 장면 |
| 4 | 아래는 벽·위는 안쪽으로 물러난 계단식 벽 → "유리 없는 창 구멍" | 레이 시작점이 윗벽 뒤 | 더 안쪽에서 다시 쏨 | `test_stepped_bay_wall_is_not_a_hole` |
| 5 | 바 의자가 "벽을 보고 앉음" | 앞면 = 로컬 -Y 규약, 이 장면은 회전이 정점에 박힘 | 등받이(높은 부분) 반대쪽을 앞면으로 | 실제 장면 |
| 6 | 격자 천장 위 설비 공간 틈 → "벽이 천장에 안 닿음" (렌더로 안 보임 확인) | 가는 막대 수백 개인 격자 천장을 천장으로 못 봄 | `…Ceiling_Grid`·baffle·louver 인식, 벽 옆 0.4 m 안 **가장 가까운 천장 면**으로 판단 | `test_open_grid_ceiling_hides_plenum` |
| 7 | 연기 감지기 부품 `IntakePillar`를 기둥으로 | 이름만 봄 | 높이 1 m 미만 '기둥'은 소품 | 실제 장면 |
| 8 | 바·게임룸·촬영실 "창 없는 방" | 모든 방에 창을 요구 | 창 없어도 자연스러운 실내 공간 유형(interior) | 실제 장면 |
| 9 | 벽 전체가 메시 1개 → 문 양쪽 방·문 앞 구역·창 정렬이 모두 틀어짐 (오류 35) | 벽 오브젝트의 축(집 전체의 PCA)을 문 자리의 벽 방향으로 씀 | 떨어진 조각별 분리 + **문·창 자신의 방향과 주변 벽면 법선**으로 그 자리의 벽 방향·두께를 잼 | `test_merged_walls_in_container_groups`, `test_door_without_hole_in_merged_walls` |
| 10 | GLB로 가져온 장면에서 v1이 아무것도 못 알아보고 "오류 0" | 최상위 그룹 1개 = 가구 1개로 봄 | `house/floors/openings`·방 규모 그룹은 풀어서 검사. 아무 방도 못 찾으면 `no_rooms_found` 경고 | `test_nothing_recognized_is_not_a_pass` |
| 11 | 가구 속 부품 `InnerWall`·`GoalDoor`·수납장 문을 벽·문으로 | 그룹 풀기 규칙이 자식 이름만 봄 | 방 규모(가로·세로 2.5 m 이상) 그룹만 풂 | `test_furniture_parts_named_like_structure` |
| 12 | 창턱 0 m ("어정쩡한 창턱", 가구가 창을 가림) | 창 오브젝트에 바닥까지 내려오는 커튼 포함 | 창 높이를 **실제 구멍**의 아래·위로 잼. 커튼·블라인드는 가림 가구가 아님 | `test_curtain_window_and_bay_window` |
| 13 | 베이창(飘窗) 방이 "창 없음" | 창 안쪽이 걸터앉는 턱(가구) 위라 방 바닥이 아님 | 창 안쪽에 가구·턱이 있으면 한 걸음 더 들어가 방을 찾음 | 같은 테스트 |
| 14 | 발코니 유리문만 있는 거실 "창 없음" | 유리문을 채광으로 안 셈 | 밖·발코니로 난 유리문은 창으로 셈 | `test_glazed_balcony_door_counts_as_daylight` |
| 15 | 3.6 m 유리 미닫이 "문 폭 이상", 문 앞 3.6 m 구역에 가구 다수 | 여닫이 기준을 모든 문에 적용 | 유리문 6 m까지 허용, 넓은 문은 **폭 0.6 m 통로가 하나라도 비면** 통과 | 같은 테스트 |
| 16 | 문 앞 판정이 너무 거침 | bbox 겹침만 봄 | 실제 형상 침범 + 3단계: 통로 0.6 m 막힘(오류) / 0.45~0.6 m(좁음, 경고) / 여닫이 여유 공간(경고) | `test_desk_half_blocks_door_and_wardrobe_covers_window` |
| 17 | 창 앞 수전·화분 가장자리 → "창을 가림" | 창 앞 상자에 걸치기만 해도 보고 | 창 면적을 격자로 나눠 **가려진 비율 25% 이상**만 | 같은 테스트 |
| 18 | 구멍 옆에 겹쳐 주차된 미닫이 문짝 → 구멍 폭 0.42 m | 탐색 범위가 문짝 폭 기준 | 탐색 범위 확장, 구멍은 문·창과 붙어 있어야 함 | `test_sliding_door_parked_beside_opening` |
| 19 | 바닥까지 내려온 유리문 → "창이 바닥보다 0.6 m 아래" | 구멍 세로 탐색이 바닥 아래까지 | 양옆 바닥 높이에서 멈춤 | 실제 장면 |
| 20 | `窗边绿植`(창가 화분)·`双门冰箱`(양문 냉장고)을 창·문으로 | 글자가 들어 있으면 매칭 | 한국어·중국어는 **끝 단어**로 판정, 끝 방향어(남·北)는 건너뜀 | `test_korean_chinese_names` |
| 21 | 모든 창이 오브젝트 1개(16 m × 3.6 m 창) | 재질별 합치기 | 가까운 조각끼리 묶어 창 하나씩으로 분리 | 실제 장면 |
| 22 | 집 전체 문 손잡이를 합친 `合批 · metal`이 모든 문 앞 가구로 | 흩어진 묶음을 가구 1개로 봄 | 여러 곳에 흩어진 묶음·7 m 넘는 '가구'는 마감재 | 실제 장면 |
| 23 | 현관문 옆 벽걸이 그림·스위치가 "문 앞 가구" | 벽에 붙은 얇은 물건도 셈 | 두께 10 cm 미만이고 바닥에서 뜬 물건 제외 | 실제 장면 |
| 24 | (코드 버그) 틈 확인용 검색 상자가 벽 법선이 음(−)이면 뒤집혀 주변 물체를 못 찾음 | 상자 계산 오류 | 두 끝점으로 상자 계산. 틈은 벽 양쪽 0.6 m까지 트여야 "건너편이 보임" | 실제 장면, `test_stepped_bay_wall_is_not_a_hole` |
| 25 | 구멍 없는 가짜 문이 방을 이어 줌 | 문이면 무조건 연결 | 구멍이 없으면 연결에서 제외(`opening_not_cut`) | `test_door_without_hole_in_merged_walls` |

테스트 모형을 만들다 스크립트가 **모형 쪽의 진짜 문제**를 잡은 경우도 있었습니다(방 사이 벽을 빼먹은 기존 테스트 모형, 문 앞에 놓은 침대·푸스볼 테이블). 이런 경우는 스크립트가 아니라 모형을 고쳤습니다.

## 6. 여전히 못 하는 것

- **문 여는 방향(스윙)을 모릅니다** → `door_clearance`는 "여닫이라면"이라는 약한 경고입니다.
- 벽이 메시 하나로 합쳐져 있으면 **벽 단위 검사(두께·끝 틈·천장 틈)는 건너뜁니다**(`summary.notes`에 표시). 문·창·방 검사는 됩니다.
- 실제 AI 장면 중 **다층 건물·경사 지붕·곡선 벽**은 이번에 없었습니다(합성 테스트로만 확인).
- 이름도 `role` 속성도 없으면(Plane, Cube…) 판정할 수 없습니다 → `no_rooms_found` 경고. AI에게 이름 규칙이나 `obj["role"]`을 지키게 하세요.
- 네트워크 정책으로 막힌 자료(예: 중국 npm 미러, 일부 데이터셋)는 이번 검증에서 뺐습니다.
- 아름다움(재질·조명·비례)은 판단하지 않습니다 — 4방향 검토 렌더와 사람 눈으로.

## 7. 다시 해 보기

```bash
# 0) 준비: pip bpy (Python 3.11) — ../README.md "테스트 실행" 참고
# 1) Realsee: 저장소를 받아 LFS 로 .blend 를 받은 뒤
python tools/run_audit.py -- realsee-astra-blender/artifacts/reconstruction_native.blend out/realsee.json

# 2) house-3d: 앱마다 three 만 설치 (package-lock 이 중국 미러를 가리키므로 npm ci 대신)
(cd house-3d/fable && npm install three@0.185.1 --no-save --registry=https://registry.npmjs.org)
(cd house-3d/gpt6  && npm install three@0.180.0 --no-save --registry=https://registry.npmjs.org)
node tools/export_house3d.mjs house-3d fable modern out/fable_modern.glb     # fable|gpt6 × french|italian|modern|song
python tools/import_glb.py -- out/fable_modern.glb out/fable_modern.blend
python tools/run_audit.py  -- out/fable_modern.blend out/fable_modern.json

# 3) 눈으로 확인: 평면도 렌더 (중심 x, y, 보이는 폭 m)
python tools/render_plan.py -- out/fable_modern.blend out/plan.png 4.4 -8.2 17.5
```

`tools/stubs.mjs`는 Node에서 three.js 장면 코드를 돌리기 위한 최소 브라우저 대역(가짜 캔버스·FileReader)입니다. 형상만 필요하므로 텍스처는 버립니다.
