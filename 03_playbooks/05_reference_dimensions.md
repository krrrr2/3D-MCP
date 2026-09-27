# 실측 치수·간격 기준표 (한국·미국·유럽)

> 기준일: 2026-09-27 · 에이전트가 가구·공간을 만들고 배치할 때 그대로 참조하는 mm 치수표입니다. 행마다 지역·출처·신뢰도를 달고, 출처 간 충돌과 오픈소스 시스템(Infinigen·SceneSmith·SAGE·Holodeck) 코드 값을 나란히 적었습니다. 프롬프트용 압축 블록은 10절, `scene_audit.py` 대응표는 11절에 있습니다.

## 핵심 요약

- **관계 치수가 절대값보다 중요합니다.** 식탁 상판과 의자 좌판의 차이는 250~305 mm, 카운터와 스툴 좌판의 차이는 230~305 mm, 협탁 윗면은 매트리스 윗면 ±50 mm입니다. 가구를 하나씩 따로 만들면 이 관계가 깨져 장면이 어딘가 어색해집니다(9절).
- **이름 대신 mm 값을 넘기세요.** '킹' 매트리스 폭은 한국 1600(브랜드에 따라 1670), 미국 1930, 영국 1500, EU 1600 mm입니다. '표준 방문'도 한국 900×2100(문틀), 미국 813×2032(미확인), 독일 860×1985(문짝)로 제각각입니다.
- **[한국] 지역 프리셋을 따로 두세요.** 아파트 천장고는 구축 2300, 2020년대 신축 2400~2500 mm입니다. 싱크대는 850(신규 900) mm, 상하부장 간격은 650~750 mm입니다. 미국은 조리대 914, 간격 457 mm라서 섞으면 한 주방 안에서 모순이 생깁니다.
- **검증에서 정정된 값이 있습니다.** 공동주택 공용계단은 높이 2 m를 넘으면 **2 m 이내마다** 계단참을 둡니다(원 조사의 3 m는 일반 건축물 기준). 그래서 층고 2800 mm를 직통 16단으로 만들면 안 됩니다. NKBA 식탁 뒤 여유는 813/914/1118 mm 3단계이고, "통행이 없으면 915 mm(NKBA)"는 틀린 인용입니다.
- **문은 치수 세 가지를 구분합니다.** 한국 900×2100은 문틀 기준이고 문짝은 약 60 mm 작습니다. DIN 문짝 860×1985의 벽 개구부는 약 885×2010 mm입니다. 벽 boolean에는 **개구부 치수**를 씁니다.
- **출처끼리 값이 다르면 모두 적었습니다.** 예를 들어 소파–커피테이블 간격은 인테리어 가이드 356~457, SceneSmith 300~500, Infinigen 450~600 mm입니다(8절). 권장 기본값은 여러 출처가 겹치는 구간에서 골랐습니다.
- **Infinigen 값은 "표준"이 아니라 랜덤 생성 범위입니다.** 의자 좌판 윗면이 약 0.47~0.54 m로 표준(0.43~0.48 m)보다 높습니다. 부품 구조를 참고하는 용도로만 쓰세요.
- **신뢰도의 한계:** 대부분 웹 검색 요약 두 개 이상으로 교차 확인했고, NKBA PDF·KS 원문·일부 법령 조문은 직접 열람하지 못했습니다. 냉장고, 미국 문·천장고, 암체어·콘솔, 한국 저상 침대·로우 소파는 출처가 없어 "낮음"입니다.
- **스크립트와 연결됩니다.** 이 표의 범위로 [`scene_audit.py`](scripts/README.md)의 치수 검사를 돌릴 수 있습니다. 작성 중 발견한 오탐(이름 부분 일치, 90° 회전, 암체어·스툴 규칙 부재)과 천장 관통 미검사는 스크립트에 반영해 고쳤습니다. 한국 구축 아파트는 11절처럼 `ceiling_z=2.30`과 한국 프리셋을 쓰세요.

---

## 0. 쓰는 법

### 0.1 표기

- 단위는 mm입니다. Blender(1 unit = 1 m)에 넣을 때는 1000으로 나눕니다.
- 지역: **KR** 한국, **US** 미국, **EU** 유럽 대륙, **UK** 영국, **공통** 여러 지역 출처가 일치.
- 신뢰도: **높음** 여러 출처가 일치하거나 1차 자료(법령·제조사 스펙·소스 코드) / **중간** 출처 1~2개, 커뮤니티·실무 SNS / **낮음** 출처 없는 관행값·기억치·계산값.
- 검증 표시(보완 검증 결과): ✅ 독립 확인 / 🟡 조건부 확인·세부 정정 / ❌ 반박되어 정정값 사용 / ❔ 독립 재확인 못 함(원 조사 등급 유지). 표시가 없으면 독립 검증 대상이 아니었던 값입니다.
- **코드**라고 적은 값은 오픈소스 저장소의 소스·프롬프트·설정에서 확인한 값입니다. 실측 표준이 아니라 **그 시스템이 쓰는 값**입니다.
- 약어: **NKBA** 미국 주방·욕실 협회(National Kitchen & Bath Association)의 설계 지침, **IRC** 미국 국제주거건축규약(International Residential Code), **DIN** 독일 표준, **KS** 한국산업표준, **R / T** 계단 단높이(챌면) / 단너비(디딤판).

### 0.2 시스템마다 좌표·단위 규약이 다릅니다

| 시스템 | 단위·축 | 크기 표기 | 회전 | 출처 |
|---|---|---|---|---|
| 이 저장소 스크립트 | m, Z-up, 원점 = 바닥 접점, 가구 정면 −Y | `size_wdh_m` [폭 w, 깊이 d, 높이] (가구 방향 기준) + 월드 bbox | Z 회전만 | [scripts/README](scripts/README.md) |
| Holodeck 프롬프트 | cm | [length, width, height] | 0/90/180/270° | [prompts.py](https://raw.githubusercontent.com/allenai/Holodeck/main/ai2holodeck/generation/prompts.py), [floor_objects.py](https://raw.githubusercontent.com/allenai/Holodeck/main/ai2holodeck/generation/floor_objects.py) |
| SceneSmith 툴 | m, z = 0 직립 고정 | generate_assets [w, d, h] | yaw °(반시계), local +Y가 'toward' | [furniture_tools.py](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/furniture_agents/tools/furniture_tools.py) |
| LayoutVLM | m, z-up, 원점 = 방 중심 | bbox | 0° = +X, 반시계, degree | [base_prompt.py](https://raw.githubusercontent.com/sunfanyunn/LayoutVLM/main/prompts/layoutvlm/base_prompt.py) |
| glTF 2.0 | m, +Y up, 정면 +Z, 왼쪽 +X | — | radian | [glTF 2.0 스펙](https://raw.githubusercontent.com/KhronosGroup/glTF/main/specification/2.0/Specification.adoc) |

- CAD 쪽(build123d 등)은 mm가 기본입니다. Blender로 가져올 때는 0.001배 한 뒤 스케일을 Apply합니다(08 원자료 노하우).
- LLM에게 치수를 줄 때는 매번 단위를 적고, 에이전트가 내놓는 값에도 단위를 붙이게 하세요.

### 0.3 하드 제약과 소프트 선호

배치 규칙은 둘로 나눠 솔버나 검사 단계에 넣습니다([Homes & Gardens](https://www.homesandgardens.com/interior-design/living-rooms/a-guide-to-living-room-clearances-measurements-and-spacing), [Eureka](https://eurekaergonomic.com/blogs/eureka-ergonomic-blog/dining-table-space-clearance-guide) 기반 G1 노하우).

- **하드(어기면 고친다):** 법규(계단·난간), 관통 0·부유 0, 문 앞과 주동선 최소 폭, 매트리스·문 규격.
- **소프트(범위 안에서 흔든다):** 그림 높이, 펜던트 높이, 러그 크기, TV 거리, 좌판 높이 편차.
- 출처끼리 값이 다르면 범위로 저장하고, 생성할 때 범위 안에서 조금씩 다르게 줍니다. 모든 의자를 정확히 450 mm로 만들면 오히려 CG처럼 보입니다([Sizemarker](https://www.sizemarker.com/dimensions/standard-dining-chair-dimensions)).

---

## 1. 좌석

| 항목 | 전형값 | 범위 | 지역 | 출처 | 신뢰도 |
|---|---|---|---|---|---|
| 식탁 의자 좌판 높이(바닥~좌판 윗면) | 450 | 430~480 (17~19 in) | 공통 | [Pop Maison](https://www.popmaison.com/blogs/guide/dining-chair-dimensions), [Picket & Rail](https://picketandrail.com/blogs/dining-blog/what-are-the-typical-dimensions-of-a-standard-dining-chair), [Sizemarker](https://www.sizemarker.com/dimensions/standard-dining-chair-dimensions) | 높음 |
| 식탁 의자 좌판 높이(한국 실무) | 450 | 430~460 | KR | [ideabuild(Threads)](https://www.threads.com/@ideabuild_official/post/DQ8kvc-kRe7) | 중간(단일 SNS) |
| 식탁 의자 좌판 깊이 | 430 | 406~457 | 공통 | [Picket & Rail](https://picketandrail.com/blogs/dining-blog/what-are-the-typical-dimensions-of-a-standard-dining-chair), [Eureka](https://eurekaergonomic.com/blogs/eureka-ergonomic-blog/how-to-choose-the-right-dining-chair-dimensions) | 중간 |
| 식탁 의자 좌판 폭 | 450 | 400~500 | 공통 | [asktfurniture](https://www.asktfurniture.net/post/standard-dining-chair-dimensions) (수치 직접 확인 못 함) | 낮음 |
| 식탁 의자 등받이(좌판 위) | 400 | 305~508 | 공통 | [Picket & Rail](https://picketandrail.com/blogs/dining-blog/what-are-the-typical-dimensions-of-a-standard-dining-chair), [Pop Maison](https://www.popmaison.com/blogs/guide/dining-chair-dimensions) | 중간 |
| 식탁 의자 전체 높이 | 850 | 813~965 | 공통 | [Sizemarker](https://www.sizemarker.com/dimensions/standard-dining-chair-dimensions), [Hernest](https://www.hernest.com/blog-detail/how-tall-is-a-dining-chair-b-104.html) | 중간 |
| **상판 − 좌판 높이차** | 300 | 254~305 | 공통 | [Pop Maison](https://www.popmaison.com/blogs/guide/dining-chair-dimensions), [Eureka](https://eurekaergonomic.com/blogs/eureka-ergonomic-blog/dining-table-chair-dimensions) | 높음 |
| 소파 좌판 높이 | 450 | 432~483 | 공통 | [OMHU](https://omhucph.com/blogs/inspiration/standard-sofa-dimensions), [Interior Insider](https://www.interiorinsider.com/article/sofa-dimensions-guide), [SeatUp](https://seatup.com/blog/guide-to-sofa-dimensions/) | 중간 |
| 소파 좌판 깊이 | 560 | 508~610 (딥시트 610~760) | 공통 | [Home Style Calculator](https://homestylecalculator.com/standard-sofa-dimensions/), [SeatUp](https://seatup.com/blog/guide-to-sofa-dimensions/) | 중간 |
| 3인 소파 폭 | 2130 | 1830~2440 (다른 출처 1980~2290) | 공통 | [Povison](https://www.povison.com/blog/buying-guide/standard-sofa-size-guide.html), [RoomSketch3D](https://roomsketch3d.com/help/dimensions/sofa-and-loveseat-dimensions), [Tribesigns](https://tribesigns.com/blogs/furniture-knowledge/standard-sofa-size-guide) | 높음 |
| 3인 소파 전체 깊이 | 940 | 810~1020 | 공통 | [Povison](https://www.povison.com/blog/buying-guide/standard-sofa-size-guide.html), [Rapport](https://rapportfurniture.com/blogs/rapport-furniture/sofa-dimensions-guide) | 중간 |
| 소파 전체 높이 | 840 | 760~915 | 공통 | [Povison](https://www.povison.com/blog/buying-guide/standard-sofa-size-guide.html), [Adorncroft](https://adorncroft.com/blog/sofa-size-guide/) | 중간 |
| 2인 소파(러브시트) 폭 × 깊이 | 1500 × 890 | 폭 1320~1830, 깊이 760~1020 | 공통 | [RoomSketch3D](https://roomsketch3d.com/help/dimensions/sofa-and-loveseat-dimensions), [Adorncroft](https://adorncroft.com/blog/sofa-size-guide/) | 중간 |
| 소파 팔걸이 높이 | 600 | 550~700 | 공통 | [Home Style Calculator](https://homestylecalculator.com/standard-sofa-dimensions/) ("크기와 무관하게 거의 일정"이라고만 함) | 낮음 |
| 암체어 폭 × 깊이 | 800 × 850 | 폭 710~1000, 깊이 760~1000 | 공통 | 출처 없음(관행값) | 낮음 |
| 카운터 스툴 좌판(914 조리대용) | 635 | 610~660 | US | [POLYWOOD](https://www.polywood.com/blogs/buying-guides/bar-height-vs-counter-heights-for-stools-and-tables-whats-the-difference), [Barstool Comforts](https://barstoolcomforts.com/heights/), [Rejuvenation](https://www.rejuvenation.com/pages/design-tips/how-to-choose-bar-stool-height/) | 높음 |
| 카운터 스툴 좌판(한국 850 조리대용) | 600 | 550~620 | KR | 계산값(850 − 230~300, 아래 '스툴 좌판 ~ 상판 간격' 행 기준. 직접 출처 없음) | 낮음 |
| 바 스툴 좌판(1016~1067 바 카운터용) | 740 | 711~762 | US | [POLYWOOD](https://www.polywood.com/blogs/buying-guides/bar-height-vs-counter-heights-for-stools-and-tables-whats-the-difference), [Froy](https://froy.com/blogs/tips/dining-table-height-bar-height-and-counter-height-guide) | 높음 |
| 스툴 좌판 ~ 상판 간격 | 254 | 230~305 | 공통 | [Barstool Comforts](https://barstoolcomforts.com/heights/), [Lumens](https://the-edit.lumens.com/the-guides/how-to-choose-seating-height/) | 높음 |
| 사무용 의자 좌판(조절 범위) | 450 | 400~520 | KR/US | [Sizemarker 사무용 의자](https://www.sizemarker.com/ko/dimensions/standard-office-chair-dimensions)(BIFMA 요약), [블라인드](https://www.teamblind.com/kr/post/%EC%A0%81%EC%A0%88%ED%95%9C-%EC%9D%98%EC%9E%90-%EB%86%92%EC%9D%B4%EC%97%90-%EB%8C%80%ED%95%B4-XBOhgfr2), [한국산업위생학회지](https://www.jksoeh.org/data/issue/JKSOEH/J01901/J01901002.pdf) | 중간 |
| 식탁 벤치 좌판 높이 / 깊이 | 450 / 380 | 430~480 / 330~400 | 공통 | [Pop Maison](https://www.popmaison.com/blogs/guide/dining-chair-dimensions)(높이 규칙만. 깊이는 관행값) | 낮음 |

**코드 값(참고용, 표준 아님)**

- **Infinigen ChairFactory**: width 0.4~0.5, 깊이 0.38~0.45, leg_height 0.45~0.5, back_height 0.4~0.5, 좌판 두께 0.04~0.08, 다리 두께 0.04~0.06 m. 좌판이 두께 중앙 기준으로 놓이므로 **좌판 윗면은 약 0.47~0.54 m**가 됩니다. 🟡 (값은 확인, "실측형 레퍼런스"라는 해석은 정정) — [chair.py](https://raw.githubusercontent.com/princeton-vl/infinigen/indoors-stable/infinigen/assets/objects/seating/chairs/chair.py)
- **Holodeck** 프롬프트 예시: 소파 `[200, 100, 80]` cm — [prompts.py](https://raw.githubusercontent.com/allenai/Holodeck/main/ai2holodeck/generation/prompts.py)
- 08 원자료 치트시트(원문 미확인): 팔걸이 높이(좌면 위) 180~250, 사무용 의자 좌면 약 400~510(EN 1335 계열). ❔

> **[한국]** 로우형·모듈 소파의 좌판은 더 낮은 경우가 많다고 하지만(약 380~420) 출처로 확인하지 못했습니다. 한샘·일룸·시디즈 같은 한국 제조사 스펙으로 보강해야 합니다.

---

## 2. 테이블·책상

| 항목 | 전형값 | 범위 | 지역 | 출처 | 신뢰도 |
|---|---|---|---|---|---|
| 식탁 상판 높이 | 750 | 711~762 (28~30 in) | 공통 | [Pop Maison](https://www.popmaison.com/blogs/guide/dining-chair-dimensions), [Flowyline](https://flowyline.com/blogs/for-diy-ers/standard-dining-table-dimensions-the-size-guide), [Froy](https://froy.com/blogs/tips/dining-table-height-bar-height-and-counter-height-guide) | 높음 |
| 식탁 상판 높이(한국 실무) | 750 | 720~750 | KR | [ideabuild(Threads)](https://www.threads.com/@ideabuild_official/post/DQ8kvc-kRe7) | 중간 |
| 식탁 1인당 가장자리 폭 | 610 | 610(일상) ~ 710~760(격식) | 공통 | [NEPA](https://www.nepafurniture.com/blog/home-furniture-32/dining-table-size-guide-based-on-number-of-people-414), [Retreat](https://www.retreathomefurniture.com/blogs/buying-guides/dining-table-size-guide), [Parotas](https://parotas.com/en/calculate-best-dining-table-size/) | 높음 |
| 4인 사각 식탁 길이 | 1200~1400 | — | 공통 | 계산값(1인 610 기준) | 낮음 |
| 식탁 폭(깊이 방향) | 900 | 800~1020 (한국 4인은 800 전후가 흔함) | 공통/KR | [Flowyline](https://flowyline.com/blogs/for-diy-ers/standard-dining-table-dimensions-the-size-guide)(수치 직접 확인 못 함) | 낮음 |
| 커피테이블 높이 | 430 | 406~457 | 공통 | [POLYWOOD](https://www.polywood.com/blogs/buying-guides/bar-height-vs-counter-heights-for-stools-and-tables-whats-the-difference), [Apartment Therapy](https://www.apartmenttherapy.com/living-room-layouts-the-ideal-measurements-for-everything-in-the-room-206734) | 중간 |
| 커피테이블 길이 | 소파 길이 × 0.67 | × 0.5~0.67 | 공통 | [Apartment Therapy](https://www.apartmenttherapy.com/living-room-layouts-the-ideal-measurements-for-everything-in-the-room-206734)(직접 확인 못 함) | 낮음 |
| 사이드테이블(소파 옆) 높이 | 600 | 500~660 (팔걸이 ±50) | 공통 | [Hernest](https://www.hernest.com/blog-detail/side-table-vs-nightstand-b-91.html) | 낮음 |
| 사무용 책상 높이 | 720 | 700~740 | KR | [KS G 4203 목록(KSSN)](https://www.kssn.net/search/stddetail.do?itemNo=K001010111402), [대한인간공학회 2009](https://www.esk.or.kr/conference/2009_fall/pdf/14_5.pdf), [Todaysppc](http://m.todaysppc.com/renewal/view.php?id=free&page=11&page_num=15&category=&sn=off&ss=on&sc=on&keyword=&prev_no=&select_arrange=headnum&desc=asc&no=479576) | 중간(KS 원문은 유료·미열람) |
| 책상 높이 | 740 | 711~762 | US | 출처 없음(관행값) | 낮음 |
| 책상 깊이 | 700 | 600~800 (모니터를 쓰면 700 이상이 흔함) | KR/공통 | 출처 없음 | 낮음 |
| 콘솔 테이블 높이 / 깊이 | 800 / 350 | 760~910 / 250~450 | 공통 | 출처 없음 | 낮음 |
| 바 테이블·바 카운터 높이 | 1060 | 1016~1067 (40~42 in) | US | [POLYWOOD](https://www.polywood.com/blogs/buying-guides/bar-height-vs-counter-heights-for-stools-and-tables-whats-the-difference), [Moruxo](https://moruxo.com/blog/counter-height-table-bar-height-table-table-height) | 높음 |
| 카운터 좌석 무릎 공간(NKBA) | 상판 762 → 457 / 914 → 381 / 1067 → 305 | 좌석당 폭 610 | US | [Lily Ann](https://www.lilyanncabinets.com/cabinet-articles/kitchen-island-overhang/), [NKBA 지침 사본](https://www.ivocabinets.com/wp-content/uploads/2024/06/NKBA-Kitchen-Planning-Guidelines.pdf), [NKBA pre-2023](https://nkba-ps.com/images/downloads/Awards/nkba_kitchen_planning_guidelines_pre_2023.pdf) | 중간~높음 ✅ |
| 아일랜드 폭 / 좌석 다리 공간(한국 실무) | 700 이상 / 250 | — | KR | [ideabuild(Threads)](https://www.threads.com/@ideabuild_official/post/DQ8kvc-kRe7) | 낮음(단일 SNS) |

**코드 값(참고용, 랜덤 생성 범위)**

- **Infinigen 식탁**: 높이 0.65~0.85, 폭 0.91~1.16, 길이 1.4~2.8, 상판 두께 0.03~0.06, straight 다리 직경 0.05~0.07 m, stretcher는 다리 높이의 0.2~0.6 위치 — [dining_table.py](https://raw.githubusercontent.com/princeton-vl/infinigen/indoors-stable/infinigen/assets/objects/tables/dining_table.py) ✅(값 확인)
- **Infinigen 책상**: 높이 N(0.73, 0.05)를 0.6~0.83으로 자름, 폭 N(1.0, 0.1), 깊이 N(0.6, 0.05), 상판 두께 0.01~0.03 m — [simple_desk.py](https://raw.githubusercontent.com/princeton-vl/infinigen/indoors-stable/infinigen/assets/objects/shelves/simple_desk.py) ✅
- 학생용은 [KS G 2010](https://standard.go.kr/KSCI/standardIntro/getStandardSearchView.do?menuId=919&topMenuId=502&upperMenuId=503&ksNo=KSG2010&tmprKsNo=KSG2010&reformNo=29) 규격이 있지만 수치는 확인하지 못했습니다(미확인).

---

## 3. 침대·매트리스

### 3.1 매트리스 폭 × 길이 (mm)

| 등급 | KR | US | EU | UK |
|---|---|---|---|---|
| 싱글 | **S 1000×2000** (브랜드별 ±50) | **Twin 965×1905** | **Single 900×2000** (800~1000) | Single 900×1900 |
| 슈퍼싱글 / Twin XL / Small Double | **SS 1100×2000** (한국 1인 침대에서 가장 흔함) | Twin XL 965×2032 | — | Small Double 1200×1900 |
| 더블 / Full | D 1400×2000 (폭 1350~1400, 한국에선 드묾) | **Full 1372×1905** | **Double 1400×2000** | Double 1350×1900 |
| 퀸 | **Q 1500×2000** ✅ | **Queen 1524×2032** | — | — |
| 킹 | **K 1600×2000**(표준표) 🟡 브랜드 1600~1670 × 2000~2075 | **King 1930×2032** | **King 1600×2000** | King 1500×2000 |
| 라지킹 / 캘리포니아킹 / 슈퍼킹 | **LK 1800×2000**(표준표) 🟡 브랜드 1700~1800 × 2000~2075 | **Cal King 1829×2134** | **Super/Grand King 1800×2000** | **Super King 1800×2000** |

굵은 글씨는 신뢰도 높음, 나머지는 중간입니다.

- **KR 출처**: [브런치](https://brunch.co.kr/@phapark/59), [슬립퍼](https://sleeper.co.kr/magazine/01-bed-size-guide/bed-size-guide.html), [3boon1](https://blog.3boon1.com/mattress-size-guide), [로다니즘](https://rodanism.co.kr/%EB%A7%A4%ED%8A%B8%EB%A6%AC%EC%8A%A4-%EC%82%AC%EC%9D%B4%EC%A6%88-%EC%B4%9D-%EC%A0%95%EB%A6%AC-%EC%8A%88%ED%8D%BC%EC%8B%B1%EA%B8%80ss-%ED%80%B8%EC%82%AC%EC%9D%B4%EC%A6%88q-%EB%93%B1/), [모아모앙](https://shop.moamoang.co.kr/%EC%B9%A8%EB%8C%80-%EB%A7%A4%ED%8A%B8%EB%A6%AC%EC%8A%A4-%EC%82%AC%EC%9D%B4%EC%A6%88/), [마홀른](https://maholn.com/blog/?bmode=view&idx=23711323), [policyoh](https://policyoh.com/%EC%B9%A8%EB%8C%80-%EB%A7%A4%ED%8A%B8%EB%A6%AC%EC%8A%A4-%EC%82%AC%EC%9D%B4%EC%A6%88%ED%95%9C%EA%B5%AD-%EB%AF%B8%EA%B5%AD-%ED%94%84%EB%9E%91%EC%8A%A4-%EC%82%AC%EC%9D%B4%EC%A6%88-%EA%B7%9C%EA%B2%A9/), [더슬립](http://thesleep.kr/144/?bmode=view&idx=655266). 검증: [퀸 6개사 공통(소비자가만드는신문)](https://www.consumernews.co.kr/news/articleView.html?idxno=713641), [킹·라지킹 업체별 차이(같은 매체)](https://www.consumernews.co.kr/news/articleView.html?idxno=520936), [컨슈머리서치](https://www.consumerresearch.co.kr/news/articleView.html?idxno=462951).
- **US/EU/UK 출처**: [T3](https://www.t3.com/features/mattress-size-guide), [TechRadar](https://www.techradar.com/health-fitness/mattresses/mattress-sizes-uk-vs-us-vs-eu), [Turmerry](https://www.turmerry.com/blogs/dreamerry/international-mattress-size-guide), [Nectar](https://www.nectarsleep.com/posts/international-mattress-sizes-guide), [Bed in a Box](https://www.bedinabox.com/blogs/news/european-vs-united-states-mattress-size-comparison-guide), [Global Size Chart](https://globalsizechart.com/tools/home/mattress-size-chart), [Odd Mattress](https://oddmattress.co.uk/all-mattresses/mattress-size-guide/).
- **[한국] K·LK는 업체마다 다릅니다.** 에이스침대 킹은 1670×2075, 시몬스는 킹이 없고 라지킹이 1700 또는 1800×2075, 한샘·현대리바트는 라지킹을 취급하지 않았습니다(검증 시점 보도). 브랜드를 정하지 않았을 때만 1600/1800×2000을 기본값으로 씁니다. Q 1500×2000은 조사한 6개사(한샘, 현대리바트, 에이스, 에몬스, 시몬스, 까사미아)가 모두 같습니다.
- 키 180 cm 이상이면 길이 2100 옵션을 권장합니다([슬립퍼](https://sleeper.co.kr/magazine/01-bed-size-guide/bed-size-guide.html), [더슬립](http://thesleep.kr/144/?bmode=view&idx=655266)).
- 위 값은 **매트리스** 치수입니다. 프레임 외곽 치수는 이번 자료에 없으니 제품 스펙을 확인하세요.
- UK 싱글·더블 계열은 EU보다 100 mm 짧고, UK King 폭은 US Queen에 가깝습니다([TechRadar](https://www.techradar.com/health-fitness/mattresses/mattress-sizes-uk-vs-us-vs-eu)).

**코드 값**: Infinigen 침대 프레임 폭 1.4~2.4, 길이 2.0~2.4, 다리 높이 0.2~0.6, 헤드보드 0.5~1.3 m(랜덤 범위) — [bedframe.py](https://raw.githubusercontent.com/princeton-vl/infinigen/indoors-stable/infinigen/assets/objects/seating/bedframe.py) ✅

### 3.2 침대 높이·협탁

| 항목 | 전형값 | 범위 | 지역 | 출처 | 신뢰도 |
|---|---|---|---|---|---|
| 바닥 ~ 매트리스 윗면 | 635 | 500~760 (약 25 in) | US | [Froy](https://froy.com/blogs/tips/how-tall-should-a-nightstand-be-the-nightstand-height-guide), [Dimensions.com](https://www.dimensions.com/collection/bedside-tables-nightstands) | 중간 |
| 바닥 ~ 매트리스 윗면(저상형) | — | 약 400~550 | KR | 출처 없음 | 낮음 ❔ |
| 협탁 높이 | 650 | 610~710 | 공통 | [Dimensions.com](https://www.dimensions.com/collection/bedside-tables-nightstands), [Wayfair](https://www.wayfair.com/sca/ideas-and-advice/guides/nightstand-dimensions-how-to-choose-the-right-nightstand-size-for-your-bedroom-T12031), [Froy](https://froy.com/blogs/tips/how-tall-should-a-nightstand-be-the-nightstand-height-guide) | 높음 |
| 협탁 윗면 vs 매트리스 윗면 | 같게 | ±50 | 공통 | [Froy](https://froy.com/blogs/tips/how-tall-should-a-nightstand-be-the-nightstand-height-guide) | 높음 |

침대 옆 통로는 6.3절을 보세요. 08 원자료 치트시트는 매트리스 윗면을 500~650으로 적었습니다(원문 미확인).

---

## 4. 수납·주방

### 4.1 주방 — 한국/미국 프리셋

| 항목 | KR | US | 출처 | 신뢰도(KR / US) |
|---|---|---|---|---|
| 조리대(싱크대) 높이 | **850** (신축·리모델링은 900도 씀. 흔한 휴리스틱: 키 ÷ 2 + 50) | **914** (36 in = 캐비닛 876 + 상판 38) | KR: [치호건축사사무소](https://chiho.co.kr/blogroom/%EC%A3%BC%EB%B0%A9-%EC%8B%B1%ED%81%AC%EB%8C%80-%EB%86%92%EC%9D%B4%EC%99%80-%EB%8F%99%EC%84%A0-%EC%84%A4%EA%B3%84-%ED%82%A4%EB%B3%84-%EC%B5%9C%EC%A0%81-%EC%B9%98%EC%88%98-%EA%B3%B5%EA%B0%9C-%EC%A3%BC%EB%B0%A9%EC%84%A4%EA%B3%84), [LX Z:IN](https://www.lxzin.com/styling/style-guide/detail/5596), [ideabuild](https://www.threads.com/@ideabuild_official/post/DQ8kvc-kRe7) / US: [CRD](https://www.crddesignbuild.com/blog/kitchen-dimensions-code-requirements-nkba-guidelines/), [Allure](https://www.allurekitchencabinet.com/blog/7-base-cabinet-sizes-standard-height-depth-width), [DesignMax](https://designmaxofficial.com/kitchen-cabinet-dimensions-guide/) | 높음 ❔ / 높음 |
| 상판 깊이 | 600 (실무는 650 이상 권장. 출처 간 이견) | 635~648 (하부장 610) | KR: [ideabuild](https://www.threads.com/@ideabuild_official/post/DQ8kvc-kRe7), [LX Z:IN 싱크대](https://www.lxzin.com/styling/style-guide/detail/647) / US: [Allure](https://www.allurekitchencabinet.com/blog/7-base-cabinet-sizes-standard-height-depth-width), [Slabwise](https://slabwise.com/guides/how-deep-are-countertops) | 중간 / 높음 |
| 상하부장 간격(조리대 ~ 상부장 하단) | 700 (650~750) | 457 (457~508) | KR: [LX Z:IN](https://www.lxzin.com/styling/style-guide/detail/5596), [ideabuild](https://www.threads.com/@ideabuild_official/post/DQ8kvc-kRe7), [뽐뿌](https://m.ppomppu.co.kr/new/bbs_view.php?id=interior&no=10642) / US: [CRD](https://www.crddesignbuild.com/blog/kitchen-dimensions-code-requirements-nkba-guidelines/), [DMB](https://www.dmbbuildersinc.com/standard-kitchen-dimensions/) | 중간 / 높음 |
| 바닥 ~ 상부장 하단 | 1550 (1500~1600, 파생값) | 1372 (1372~1448) | KR: [LX Z:IN](https://www.lxzin.com/styling/style-guide/detail/5596) / US: [WC Supply](https://www.thewcsupply.com/pages/kitchen-design-guidelines-standard-clearances), [TC Wholesale](https://tcwholesalecabinetry.com/blog/wall-cabinet-sizes-types) | 중간 / 높음 |
| 상부장 본체 높이 | 750 (700~900, 천장고에 맞춰 조정) | 762 / 914 / 1067 (30/36/42 in 규격) | KR: [LX Z:IN](https://www.lxzin.com/styling/style-guide/detail/5596), [블라인드](https://www.teamblind.com/kr/post/%EB%AC%B4%EB%AA%B0%EB%94%A9-%EC%A3%BC%EB%B0%A9-%EC%83%81%EB%B6%80%EC%9E%A5%EA%B3%BC-%EC%B2%9C%EC%9E%A5-%EB%86%92%EC%9D%B4-%EB%AC%B8%EC%9D%98-1qzVjCGh) / US: [TC Wholesale](https://tcwholesalecabinetry.com/blog/wall-cabinet-sizes-types) | 중간 / 낮음 |
| 상부장 깊이 | 350 (300~350) | 305 (305~381) | KR: [ideabuild](https://www.threads.com/@ideabuild_official/post/DQ8kvc-kRe7) / US: [TC Wholesale](https://tcwholesalecabinetry.com/blog/wall-cabinet-sizes-types), [DesignMax](https://designmaxofficial.com/kitchen-cabinet-dimensions-guide/) | 중간 / 중간 |
| 수직 모듈 합계 | 850 + 700 + 750 = **2300** (2300~2400) | — | [LX Z:IN](https://www.lxzin.com/styling/style-guide/detail/5596) | 중간 |
| 작업 통로 | 900 이상(실무) | 1067(1인) / 1219(다인) | KR: [ideabuild](https://www.threads.com/@ideabuild_official/post/DQ8kvc-kRe7) / US: [CRD](https://www.crddesignbuild.com/blog/kitchen-dimensions-code-requirements-nkba-guidelines/), [NKBA PDF](https://media.nkba.org/uploads/2022/05/Kitchen-Planning-Guidelines.pdf), [Mod Cabinetry](https://www.modcabinetry.com/nkba-guideline/) | 중간 / 높음 ❔ |
| 워크 트라이앵글(싱크·레인지·냉장고) | — | 3변 합 ≤ 7925, 각 변 1219~2743 | [CRD](https://www.crddesignbuild.com/blog/kitchen-dimensions-code-requirements-nkba-guidelines/), [Wikipedia](https://en.wikipedia.org/wiki/Kitchen_work_triangle) | — / 높음 ❔ |

- **[한국]** 천장이 더 높으면 상부장만 늘립니다(LX Z:IN 원리). 예: 천장 2400이면 850 + 700 + 850.
- EU 조리대 높이 900~910은 08 원자료 치트시트 값이고 원문을 확인하지 못했습니다(낮음).
- **코드 값**: Archimesh 주방 기본값은 하부장 깊이 0.59, 높이 0.70, 걸레받이 0.16(그만큼 캐비닛을 올림), 상판 두께 0.02, 상판 돌출 0.03, 판 두께 0.018 m라서 **상판 윗면이 약 0.88 m**입니다. 상부장은 깊이 0.35 m, 바닥에서 1.5 m에 놓입니다 — [achm_kitchen_maker.py](https://raw.githubusercontent.com/blender/blender-addons/main/archimesh/achm_kitchen_maker.py) ✅. Infinigen 주방 캐비닛은 측판 0.02, 하단 0.06 m — [kitchen_cabinet.py](https://raw.githubusercontent.com/princeton-vl/infinigen/indoors-stable/infinigen/assets/objects/shelves/kitchen_cabinet.py).
- 08 원자료 치트시트(원문 미확인): 하부장 깊이 580~600, 걸레받이 100~150.

### 4.2 수납가구

| 항목 | 전형값 | 범위·변형 | 지역 | 출처 | 신뢰도 |
|---|---|---|---|---|---|
| IKEA BILLY 깊이 | 280 | 유리문 버전 300 | 공통 | [IKEA US](https://www.ikea.com/us/en/p/billy-bookcase-white-50522040/), [IKEA GB](https://www.ikea.com/gb/en/p/billy-bookcase-white-80263832/), [IKEA 유리문](https://www.ikea.com/us/en/p/billy-bookcase-with-glass-doors-dark-blue-20323805/), [Dimensions.com](https://www.dimensions.com/element/ikea-billy-bookcases) | 높음 ✅ |
| IKEA BILLY 폭 / 높이 | 400·800 / 1060·2020·2370 | — | 공통 | [BILLY 시리즈](https://www.ikea.com/us/en/cat/billy-series-28102/), [IKEA US](https://www.ikea.com/us/en/p/billy-bookcase-white-90522043/), [IKEA GB 조합](https://www.ikea.com/gb/en/p/billy-bookcase-white-s89017827/), [Wikipedia](https://en.wikipedia.org/wiki/IKEA_Billy) | 높음 ✅ |
| 일반 책장 깊이 | 280 | 250~350 | 공통 | [itemfits BILLY](https://itemfits.com/dimensions/ikea/ikea-billy) | 중간 |
| 책장 선반 간격(수직) | 300 | 250~350 (대형 도서 350~400) | 공통 | 출처 없음 | 낮음 |
| IKEA PAX 깊이 | 580 | 350 프레임도 있음 | 공통 | [itemfits PAX](https://itemfits.com/dimensions/ikea/ikea-pax), [IKEA GB 안내](https://www.ikea.com/gb/en/customer-service/knowledge/articles/4dc0cd26-geg1-487c-gee0-43g399373g9f.html), [IKEA US PAX 2](https://www.ikea.com/us/en/p/pax-2-wardrobe-frames-white-s19556396/) | 높음 🟡 |
| IKEA PAX 폭 / 높이 | 500·750·1000 / 2010·2360 | — | 공통 | [itemfits PAX](https://itemfits.com/dimensions/ikea/ikea-pax), [The Happy Housie](https://www.thehappyhousie.com/making-sense-of-ikea-pax-how-to-choose-the-right-pax-configuration-for-your-space/) | 높음 ✅ |
| 일반 옷장 깊이 | 600 | 550~650 (행거를 쓰면 약 600) | 공통 | [itemfits PAX](https://itemfits.com/dimensions/ikea/ikea-pax) | 중간 |
| 판재 두께 | 18 | 18~25 | 공통 | Archimesh board 0.018(코드). 상한 25는 08 원자료(원문 미확인) | 중간 |

- **[한국] PAX 2360은 구축 천장고 2300에 들어가지 않습니다.** 2010 모델이나 맞춤 붙박이장을 쓰세요. 신축 2400 이상이면 들어갑니다. 한국 붙박이장은 깊이가 600을 넘기도 합니다(미확인).
- 2026년 IKEA 미국 사이트는 제품명을 'PAX 2 wardrobe frames'로 표기합니다. SKU를 인용할 때 확인하세요.
- 대량생산 가구는 범위의 평균보다 **실제 SKU 치수**를 쓰는 편이 더 그럴듯합니다(G1 노하우).
- 08 원자료 치트시트(원문 미확인, 낮음): 옷봉 높이 1600~1800, 18 mm 판의 무지지 스팬 800 이하, 뒤판 3~6, 문·서랍 틈 2~3.

### 4.3 가전 (출처 없음, 반드시 제조사 스펙 확인)

| 항목 | 폭 / 높이 / 깊이 | 지역 | 신뢰도 |
|---|---|---|---|
| 냉장고(미국 표준형) | 762~914 / 1676~1778 / 737~889 | US | 낮음 ❔(검색으로 확인 못 한 일반 지식) |
| 냉장고(한국 양문형·4도어) | 약 910 / 약 1800~1850 / 약 900~930(도어 포함) | KR | 낮음 ❔(삼성·LG 스펙 확인 필요) |

---

## 5. 건축 요소

### 5.1 천장·층고·벽

| 항목 | 전형값 | 범위 | 지역 | 출처 | 신뢰도 |
|---|---|---|---|---|---|
| 아파트 천장고(반자높이) | 2300 (구축·표준 설계) | 2020년대 신축 2400~2500, 고급 단지는 그 이상 | KR | [한국PM](https://hkpm.co.kr/%EC%9D%BC%EB%B0%98%EC%A0%81%EC%9D%B8-%EC%95%84%ED%8C%8C%ED%8A%B8-%EC%B8%B5%EA%B3%A0%EC%99%80-%EC%B2%9C%EC%9E%A5%EA%B3%A0-%EA%B8%B0%EC%A4%80%EA%B3%BC-%EC%9D%98%EB%AF%B8-%EA%B4%80%EA%B3%84/), [아파트관리신문](http://www.aptn.co.kr/news/articleView.html?idxno=49567), [sanerang](https://sanerang.com/entry/%EC%95%84%ED%8C%8C%ED%8A%B8-%EC%B2%9C%EC%9E%A5%EB%86%92%EC%9D%B4-23m-%EB%B0%98%EC%9E%90%EB%86%92%EC%9D%B4). 신축 추세: [서울경제TV](https://www.sentv.co.kr/article/view/sentv202209140082), [뉴스스페이스](https://www.newsspace.kr/news/article.html?no=5411) | 높음 🟡 |
| 거실 우물천장 | 천장고 + 50~100 | — | KR | G1 노하우([한국PM](https://hkpm.co.kr/%EC%9D%BC%EB%B0%98%EC%A0%81%EC%9D%B8-%EC%95%84%ED%8C%8C%ED%8A%B8-%EC%B8%B5%EA%B3%A0%EC%99%80-%EC%B2%9C%EC%9E%A5%EA%B3%A0-%EA%B8%B0%EC%A4%80%EA%B3%BC-%EC%9D%98%EB%AF%B8-%EA%B4%80%EA%B3%84/)) | 중간 |
| 층고(슬래브 ~ 슬래브) | 2800 | 2800~2850. 층간소음 대책으로 슬래브를 250 mm로 두껍게 한 신축은 2900 이상 | KR | [한국PM](https://hkpm.co.kr/%EC%9D%BC%EB%B0%98%EC%A0%81%EC%9D%B8-%EC%95%84%ED%8C%8C%ED%8A%B8-%EC%B8%B5%EA%B3%A0%EC%99%80-%EC%B2%9C%EC%9E%A5%EA%B3%A0-%EA%B8%B0%EC%A4%80%EA%B3%BC-%EC%9D%98%EB%AF%B8-%EA%B4%80%EA%B3%84/), [a-ha](https://www.a-ha.io/questions/41a27d6d5c2dfadb88b54e89959b5c12), [ramowa](https://ramowa.com/%EC%95%84%ED%8C%8C%ED%8A%B8-%ED%95%9C-%EC%B8%B5-%EB%86%92%EC%9D%B4-%EC%B8%B5%EA%B3%A0-vs-%EC%B2%9C%EC%9E%A5%EA%B3%A0-%EC%B0%A8%EC%9D%B4%EB%8A%94/) | 중간 🟡 |
| 천장고 | 2438 (8 ft) | 2440~2740 | US | 원자료 관행값(URL 없음) | 낮음 |
| 천장고 | — | 2500~2700 | EU | 원자료 관행값(URL 없음) | 낮음 |
| 외벽 콘크리트 구조체 | 200 | 단열·마감을 더하면 300 이상 | KR | [클리앙](https://www.clien.net/service/board/kin/12725939), [a-ha](https://www.a-ha.io/questions/4c62435ef5f74961bcce64ed41912ed3), [PGR21](https://www.pgr21.com/qna/180303) | 중간 |
| 내력벽(내벽) | 180 | 150~200 (180 이상이면 내력벽일 가능성이 큼) | KR | [AJD](https://www.ajd.co.kr/contents/basic-tip/detail/%EB%82%B4%EB%A0%A5%EB%B2%BD_%EB%B9%84%EB%82%B4%EB%A0%A5%EB%B2%BD_%EA%B5%AC%EB%B6%84_%EB%B0%A9%EB%B2%95%EA%B3%BC_%EC%B0%A8%EC%9D%B4%EF%BD%9C%EB%8F%84%EB%A9%B4%C2%B7%EB%91%90%EA%BB%98%EB%A1%9C_%EC%B2%A0%EA%B1%B0_%EA%B0%80%EB%8A%A5_%EC%97%AC%EB%B6%80_%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0-72255), [클리앙](https://www.clien.net/service/board/kin/12725939) | 중간 |
| 비내력 칸막이 / 욕실 벽 | 100 / 150 | — | KR | [AJD](https://www.ajd.co.kr/contents/basic-tip/detail/%EB%82%B4%EB%A0%A5%EB%B2%BD_%EB%B9%84%EB%82%B4%EB%A0%A5%EB%B2%BD_%EA%B5%AC%EB%B6%84_%EB%B0%A9%EB%B2%95%EA%B3%BC_%EC%B0%A8%EC%9D%B4%EF%BD%9C%EB%8F%84%EB%A9%B4%C2%B7%EB%91%90%EA%BB%98%EB%A1%9C_%EC%B2%A0%EA%B1%B0_%EA%B0%80%EB%8A%A5_%EC%97%AC%EB%B6%80_%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0-72255) | 중간 |
| 목조 스터드 벽(2×4 + 양면 석고보드) | 114 | 114~165 (2×6 외벽) | US | 출처 없음 | 낮음 |

> **[한국] 천장고가 틀리면 전부 어긋납니다.** 문(2100), 주방 모듈(합계 2300), 펜던트 높이, 붙박이장까지 비율이 달라져 "한국 집 같지 않은" 인상을 줍니다. 장면을 시작할 때 **구축(2300)인지 신축(2400~2500)인지** 먼저 정하세요. 신축 기준이면 미국 2438과의 차이는 크지 않습니다(검증 의견).

### 5.2 문·창

| 항목 | 전형값 | 범위·변형 | 지역 | 출처 | 신뢰도 |
|---|---|---|---|---|---|
| 방문(여닫이) — **문틀 기준** | 900×2100 | 규격 700×2000 / 800×2100 / 900×2100 / 1000×2100. 가장 많이 쓰는 폭은 900·1000 | KR | [다음카페 건재정보](https://m.cafe.daum.net/retirecountry/GbzJ/5?q=D_KkJLW6NS9QQ0), [다음카페 설창고](https://m.cafe.daum.net/sulchango/AsM/151?svc=cafeapi), [지식로그](https://www.jisiklog.com/qa/14210770), [a-ha](https://a-ha.io/questions/4e22c54b42b8110980a1018e203ab0cb) | 중간 🟡 |
| 방문 문짝 | 문틀 폭 − 약 60 (900 → 약 840) | 문짝 두께 35, 문틀 두께(벽 방향) 110 | KR | [다음카페 설창고](https://m.cafe.daum.net/sulchango/AsM/151?svc=cafeapi), [다음카페 건재정보](https://m.cafe.daum.net/retirecountry/GbzJ/5?q=D_KkJLW6NS9QQ0) | 중간 🟡 |
| 욕실문(문틀 기준) | 700×2000 | ~800×2100. 욕실·창고문은 (700~800)×(1800~2100) | KR | [다음카페 건재정보](https://m.cafe.daum.net/retirecountry/GbzJ/5?q=D_KkJLW6NS9QQ0), [다음카페 설창고](https://m.cafe.daum.net/sulchango/AsM/151?svc=cafeapi) | 중간 ✅ |
| 현관문(아파트) | 1000×2100 | 900~1100 × 2100 (가전이 커지면서 1100이 늘어나는 추세) | KR | [APRO](https://aprodoor.com/front-door-sizes/), [창호자재](http://www.changhojajae.com/m/product.html?branduid=729803) | 중간 |
| 실내문 | 813×2032 (32×80 in) | 폭 610~914. 현관문은 보통 914×2032 | US | 출처 없음(일반 지식) | 낮음 |
| 실내문 문짝(DIN 18101) | 860×1985 (가장 흔함) | 폭 610·735·860·985·1110 / 높이 1985·2110 | EU(DE) | [BauNetz Wissen](https://www.baunetzwissen.de/fenster-und-tueren/fachwissen/konstruktion-funktion/tuerblattgroessen-nach-din-18101-155263), [MVK](https://mvk-kuechen-und-raumdesign.de/innentueren-ratgeber/tuermasse-innentueren/), [steel-interior](https://www.steel-interior.de/tuermasse-nach-din/), [Westag](https://www.westag.de/de/westag-tueren/ratgeber/blog/tuermasse-und-tuerzargemasse-nach-din-1/) | 높음 ✅ |
| DIN 건축 규격 / 벽 개구부 | 문짝 + 약 15 (875×2000) / 약 885×2010 | — | EU(DE) | 같은 출처 | 높음 ✅ |
| 침실 창대 높이 | 900 | 800~1000. 거실 발코니 창은 바닥부터 시작하는 경우가 많음 | KR | 출처 없음(관행값) | 낮음 |
| 비상탈출창(EERO) 개구부 하단 | ≤ 1118 (44 in) | — | US(IRC R310) | [Routt County](https://www.co.routt.co.us/DocumentCenter/View/15206), [Shape Products](https://shapeproducts.com/wp-content/uploads/2021/01/Manual_EgressCode.pdf), [Window Well Experts](https://windowwellexperts.com/egress-codes/) | 높음 ✅ |

- **벽 boolean에는 개구부 치수를 씁니다.** 한국은 문틀 외곽 치수로 벽을 뚫고, 문짝 메시는 약 60 mm 작게 만듭니다. DIN은 문짝 860×1985이면 개구부 약 885×2010입니다.
- **코드 값**: Archimesh 문 기본값 1.0×2.1 m, 문틀 두께 0.08 m — [achm_door_maker.py](https://raw.githubusercontent.com/blender/blender-addons/main/archimesh/achm_door_maker.py). Holodeck 문 폭 single 1 m / double 2 m — [prompts.py](https://raw.githubusercontent.com/allenai/Holodeck/main/ai2holodeck/generation/prompts.py).

### 5.3 계단·난간

| 항목 | 값 | 지역·근거 | 출처 | 신뢰도 |
|---|---|---|---|---|
| 단높이(챌면) | ≤ 180 | KR 공동주택 공용계단(주택건설기준 등에 관한 규정 제16조) | [국가법령정보센터](https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=268503), [마이다스캐드](https://www.midascad.com/cad_archive/buildingact-4), [04noti](https://04noti.com/%EA%B3%84%EB%8B%A8-%EC%84%B8%EB%B6%80-%EC%84%A4%EC%B9%98%EA%B8%B0%EC%A4%80-%EB%8B%A8%EB%84%88%EB%B9%84-%EB%8B%A8%EB%86%92%EC%9D%B4-%EA%B3%84%EB%8B%A8%EB%84%88%EB%B9%84/) | 높음 ✅ |
| 단너비(디딤판) | ≥ 260 | 같음 | 같음. 돌음계단 측정 기준은 [법제처 해석(CaseNote)](https://casenote.kr/%EB%B2%95%EC%A0%9C%EC%B2%98/18-0465-d5162f) | 높음 ✅ |
| 공용계단 유효폭 | ≥ 1200 | 같음 | [국가법령정보센터](https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=268503) | 높음 ✅ |
| 계단참(공동주택) | 높이 2000을 넘는 계단은 **2000 이내마다**, 너비 ≥ 1200(유효폭 이상). 세대 내 계단 제외 | KR 주택건설기준 제16조 | [국가법령정보센터](https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=268503), [qnaqc](https://qnaqc.co.kr/%EC%98%A5%EC%83%81-%EC%8A%B9%EA%B0%95%EA%B8%B0-%EA%B8%B0%EA%B3%84%EC%8B%A4-%EA%B3%84%EB%8B%A8%EC%9D%80-%EC%A3%BC%ED%83%9D%EA%B1%B4%EC%84%A4%EA%B8%B0%EC%A4%80-%EB%93%B1%EC%97%90-%EA%B4%80%ED%95%9C/), [지평 뉴스레터](https://www.jipyong.com/origin/newsletter/real_estate/41_202003/download/law_download_02.pdf) | 높음 ❌(원 조사 3000을 정정) |
| 계단참(일반 건축물) | 높이 3000 이내마다, 유효너비 ≥ 1200 | KR 건축물의 피난·방화구조 등의 기준에 관한 규칙 제15조 | [국가법령정보센터](https://www.law.go.kr/LSW/lsLinkCommonInfo.do?lspttninfSeq=124056&chrClsCd=010202), [04noti](https://04noti.com/%EA%B3%84%EB%8B%A8-%EC%84%B8%EB%B6%80-%EC%84%A4%EC%B9%98%EA%B8%B0%EC%A4%80-%EB%8B%A8%EB%84%88%EB%B9%84-%EB%8B%A8%EB%86%92%EC%9D%B4-%EA%B3%84%EB%8B%A8%EB%84%88%EB%B9%84/) | 높음 |
| 난간 설치 의무 | 높이 1000을 넘는 계단·계단참 양옆(벽 포함) | KR 피난·방화규칙 제15조 | [국가법령정보센터](https://www.law.go.kr/LSW/lsLinkCommonInfo.do?lspttninfSeq=124056&chrClsCd=010202), [bigcase](https://bigcase.ai/law/%EA%B1%B4%EC%B6%95%EB%AC%BC%EC%9D%98%ED%94%BC%EB%82%9C%C2%B7%EB%B0%A9%ED%99%94%EA%B5%AC%EC%A1%B0%EB%93%B1%EC%9D%98%EA%B8%B0%EC%A4%80%EC%97%90%EA%B4%80%ED%95%9C%EA%B7%9C%EC%B9%99/%EC%A0%9C15%EC%A1%B0?refDate=20100211) | 높음 ✅ |
| 유효높이(머리 위 여유) | ≥ 2100 (계단 바닥 마감면 ~ 상부 구조체 하부 마감면) | KR 피난·방화규칙 제15조 | [국가법령정보센터](https://www.law.go.kr/LSW/lsLinkCommonInfo.do?lspttninfSeq=124056&chrClsCd=010202), [04noti](https://04noti.com/%EA%B3%84%EB%8B%A8-%EC%84%B8%EB%B6%80-%EC%84%A4%EC%B9%98%EA%B8%B0%EC%A4%80-%EB%8B%A8%EB%84%88%EB%B9%84-%EB%8B%A8%EB%86%92%EC%9D%B4-%EA%B3%84%EB%8B%A8%EB%84%88%EB%B9%84/) | 높음 🟡 |
| 손잡이 높이 | 850 | KR | 수치를 확인한 출처 없음 | 낮음 ❔(미확인) |
| 난간 높이 | ≥ 1200(바닥 마감면 기준). 내부 계단·계단 중간 난간처럼 위험이 적은 곳은 ≥ 900 | KR 주택건설기준 제18조 | [국가법령정보센터 제18조](https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EC%A3%BC%ED%83%9D%EA%B1%B4%EC%84%A4%EA%B8%B0%EC%A4%80%20%EB%93%B1%EC%97%90%20%EA%B4%80%ED%95%9C%20%EA%B7%9C%EC%A0%95/%EC%A0%9C18%EC%A1%B0), [kuk34](https://kuk34.com/%EA%B3%84%EB%8B%A8-%EB%82%9C%EA%B0%84-%EA%B7%9C%EC%A0%95-3%EA%B0%9C-%EB%B2%95%EB%A0%B9-%EB%B9%84%EA%B5%90/) | 높음 ✅ |
| 난간 간살 간격 | 안목 ≤ 100 | KR 주택건설기준 제18조 | 같음 | 높음 ✅ |
| 단높이 | ≤ 197 (7¾ in) | US IRC R311 | [Essex CT 2015 IRC](https://www.essexct.gov/DocumentCenter/View/449/Residential-Stairways-and-Ramps-2015-Irc-Handout-PDF), [Building Code Trainer](https://buildingcodetrainer.com/residential-stair-code/), [TradeMaster](https://trademastercalc.com/reference/irc-stair-code) | 높음 ❔ |
| 디딤판 | ≥ 254 (10 in, 챌면 코 있음) / 코가 없으면 ≥ 279 | US IRC | [Essex CT](https://www.essexct.gov/DocumentCenter/View/449/Residential-Stairways-and-Ramps-2015-Irc-Handout-PDF), [build-construct](https://build-construct.com/building/building-tips/residential-stair-code-requirements-riser-height-tread-depth-width-and-headroom/) | 높음 ❔ |
| 머리 위 여유 | ≥ 2032 (6'8") | US IRC | [TradeMaster](https://trademastercalc.com/reference/irc-stair-code), [NY DOS](https://dos.ny.gov/system/files/documents/2019/10/tb-1005-rcnys-residential-exit-doors-stairs-and.pdf) | 높음 ❔ |
| 손잡이 높이 | 864~965 (34~38 in, 디딤판 코 연결선 기준). 챌면 4개 이상이면 최소 한쪽 필수 | US IRC R311.7.8 | [ICC IRC 2018](https://codes.iccsafe.org/s/IRC2018P4/chapter-3-building-planning/IRC2018P4-Ch03-SecR311.7.8), [Koffler](https://kofflersales.com/blog/handrail-height-guide-code-requirements/), [Viewrail](https://resources.viewrail.com/code-compliance/railing-code/maximum-and-minimum-handrail-heights) | 높음 ✅ |
| 가드(추락방지 난간) | ≥ 914 (36 in). 계단 개방면에서 손잡이를 겸하면 864~965 허용. 상업용 IBC 42 in은 미확인 | US IRC R312 | [Routt County](https://www.co.routt.co.us/DocumentCenter/View/15199), [Cheney 2021 IRC](https://www.cityofcheney.org/DocumentCenter/View/2876/Railings---2021-IRC), [Deck & Rail Supply](https://deckandrailsupply.com/blogs/railings/guard-vs-handrail-irc-code-requirements) | 높음 ✅ |
| 쾌적 공식(Blondel) | 2R + T = 620~640 | 공통 | [FreeCAD ArchStairs](https://raw.githubusercontent.com/FreeCAD/FreeCAD/main/src/Mod/BIM/ArchStairs.py)(코드 설명문) | 높음 ✅ |

- 세대 안의 계단(복층 등)은 공동주택 기준표의 적용 범위가 다르다는 법제처 해석이 있습니다([법제처](https://www.moleg.go.kr/lawinfo/nwLwAnInfo.mo?mid=a10106020000&cs_seq=40746)).
- 공동주택이라도 기계실·물탱크실 계단은 3 m 간격 예외가 적용됩니다([qnaqc](https://qnaqc.co.kr/%EC%98%A5%EC%83%81-%EC%8A%B9%EA%B0%95%EA%B8%B0-%EA%B8%B0%EA%B3%84%EC%8B%A4-%EA%B3%84%EB%8B%A8%EC%9D%80-%EC%A3%BC%ED%83%9D%EA%B1%B4%EC%84%A4%EA%B8%B0%EC%A4%80-%EB%93%B1%EC%97%90-%EA%B4%80%ED%95%9C/)). 프리셋을 `KR_apartment: landing_every ≤ 2000`, `KR_general: landing_every ≤ 3000`으로 나누세요.
- IRC 단높이·디딤판·머리 위 여유(❔)는 널리 알려진 값이라 원 조사 등급을 유지했지만, 보완 검증에서 독립 확인하지는 못했습니다.
- **코드 값**: Archimesh 계단 기본값은 단높이 0.14, 단너비 0.30, 디딤판 두께 0.03 m입니다 — [achm_stairs_maker.py](https://raw.githubusercontent.com/blender/blender-addons/main/archimesh/achm_stairs_maker.py). 2R + T = 580이라 Blondel 범위보다 낮은, 완만한 계단입니다(계산값).

### 5.4 콘센트·스위치

| 항목 | 전형값 | 범위 | 지역 | 출처 | 신뢰도 |
|---|---|---|---|---|---|
| 콘센트(일반 벽면, 중심) | 300 | 250~400 | KR | [sunnysunnyday](https://sunnysunnyday.com/entry/%EC%8B%B1%ED%81%AC%EB%8C%80-%EC%95%9E%EC%97%90-%EC%BD%98%EC%84%BC%ED%8A%B8%EA%B0%80-%EC%9E%88%EB%8D%98-%ED%98%84%EC%9E%A5%EC%9D%84-%EC%9D%B4%EC%96%B4%EB%B0%9B%EA%B3%A0-%EB%82%98%EC%84%9C-%EC%A0%95%EB%A6%AC%ED%95%9C-%EC%BD%98%EC%84%BC%ED%8A%B8%C2%B7%EC%8A%A4%EC%9C%84%EC%B9%98-%EC%9C%84%EC%B9%98-%EC%84%A4%EA%B3%84-%EA%B0%80%EC%9D%B4%EB%93%9C-%EA%B3%B5%EA%B0%84%EB%B3%84-%EC%BD%98%EC%84%BC%ED%8A%B8-%EB%86%92%EC%9D%B4-%EC%8A%A4%EC%9C%84%EC%B9%98-%EB%B0%B0%EC%B9%98-%ED%9A%8C%EB%A1%9C-%EB%B6%84%EB%A6%AC-%EA%B8%B0%EC%A4%80), [딘소디자인](https://dinsodesign.com/bbs/board.php?bo_table=process&wr_id=1517) | 낮음 |
| 콘센트(침대 옆 협탁용) | 650 | 600~700 | KR | [sunnysunnyday](https://sunnysunnyday.com/entry/%EC%8B%B1%ED%81%AC%EB%8C%80-%EC%95%9E%EC%97%90-%EC%BD%98%EC%84%BC%ED%8A%B8%EA%B0%80-%EC%9E%88%EB%8D%98-%ED%98%84%EC%9E%A5%EC%9D%84-%EC%9D%B4%EC%96%B4%EB%B0%9B%EA%B3%A0-%EB%82%98%EC%84%9C-%EC%A0%95%EB%A6%AC%ED%95%9C-%EC%BD%98%EC%84%BC%ED%8A%B8%C2%B7%EC%8A%A4%EC%9C%84%EC%B9%98-%EC%9C%84%EC%B9%98-%EC%84%A4%EA%B3%84-%EA%B0%80%EC%9D%B4%EB%93%9C-%EA%B3%B5%EA%B0%84%EB%B3%84-%EC%BD%98%EC%84%BC%ED%8A%B8-%EB%86%92%EC%9D%B4-%EC%8A%A4%EC%9C%84%EC%B9%98-%EB%B0%B0%EC%B9%98-%ED%9A%8C%EB%A1%9C-%EB%B6%84%EB%A6%AC-%EA%B8%B0%EC%A4%80) | 중간 |
| 콘센트(책상 위 사용) | 850 | 800~900 | KR | 같음 | 중간 |
| 조명 스위치(중심) | 1200 | 1100~1250 | KR | 같음(합성 요약 수준) | 낮음 |
| 콘센트(바닥 ~ 박스 하단) / 스위치(중심) | 305~406 / 1219 (48 in) | — | US | [TaskRabbit](https://www.taskrabbit.com/blog/standard-outlet-height/), [Angi](https://www.angi.com/articles/light-switch-outlet-height.htm), [HomeGuide](https://homeguide.com/articles/standard-light-switch-and-outlet-heights), [ExpertCE](https://expertce.com/learn-articles/nec-rough-in-heights-outlets-switches/) | 중간 ✅(관행. NEC는 주거용 스위치 높이를 법으로 정하지 않음) |

미국 콘센트는 박스 **하단**까지, 스위치는 **중심**까지 잰 값입니다. 측정 기준이 다르니 섞지 마세요.

---

## 6. 동선·간격

아래 간격은 모두 **가구 모서리 사이의 평면 거리**입니다. 이 저장소의 `placement_utils.xy_clearance()`가 같은 방식(두 유닛 AABB 사이 XY 최소 거리)으로 잽니다.

### 6.1 거실

| 항목 | 전형값 | 범위 | 지역 | 출처 | 신뢰도 |
|---|---|---|---|---|---|
| 주 통행로(좌석 그룹 주변) | 910 | 760~910 (30~36 in) | 공통 | [Homes & Gardens](https://www.homesandgardens.com/interior-design/living-rooms/a-guide-to-living-room-clearances-measurements-and-spacing), [Apartment Therapy](https://www.apartmenttherapy.com/living-room-layouts-the-ideal-measurements-for-everything-in-the-room-206734), [Keck](https://keckfurniture.com/blog/living-room-layout-rules-traffic-flow-conversation-zones-and-tv-placement/) | 높음 |
| 소파 앞면 ~ 커피테이블 모서리 | 400 | 356~457 (14~18 in) | 공통 | [Homes & Gardens](https://www.homesandgardens.com/interior-design/living-rooms/a-guide-to-living-room-clearances-measurements-and-spacing), [Apartment Therapy](https://www.apartmenttherapy.com/living-room-layouts-the-ideal-measurements-for-everything-in-the-room-206734), [VBU](https://vbufurniture.com/blogs/furniture-buying-guide/stationary-anchors-sofa) | 높음 |
| TV 시청거리(배수) | 대각선 × 1.5~2.5 | 4K는 더 가까워도 됨 | 공통 | [Keck](https://keckfurniture.com/blog/living-room-layout-rules-traffic-flow-conversation-zones-and-tv-placement/), [Wehomz](https://wehomzfurn.com/blogs/decoration-ideas/optimizing-your-living-room-the-ultimate-guide-to-sofa-and-tv-layouts-by-wehomz) | 중간 |
| TV 55형 거리 | 2400 | 2130~2740 (7~9 ft) | 공통 | [Keck](https://keckfurniture.com/blog/living-room-layout-rules-traffic-flow-conversation-zones-and-tv-placement/), [Planner 5D](https://planner5d.com/blog/living-room-furniture-layout/) | 중간 |
| TV 65형 거리 | 2750 | 2440~3050 (8~10 ft) | 공통 | [Keck](https://keckfurniture.com/blog/living-room-layout-rules-traffic-flow-conversation-zones-and-tv-placement/) | 중간 |
| TV 거리(시야각 기준) | 16:9에서 30° → 대각선 × 1.63, 36° → × 1.34, 40° → × 1.20 | 55형 약 1.7~2.3 m, 65형 약 2.0~2.7 m | 공통 | 계산값. THX(약 36~40°)·SMPTE(약 30°) 원문 미확인 | 낮음 ❔ |
| TV 화면 중심 높이 | 1050 | 950~1150 | 공통 | 파생값(소파 좌판 + 앉은 눈높이). 출처 없음 | 낮음 |
| 러그: 소파 양끝 바깥 여유 | ≥ 150 | 모든 좌석의 앞다리 2개 이상이 러그 위 | 공통 | [Homes & Gardens](https://www.homesandgardens.com/interior-design/living-rooms/a-guide-to-living-room-clearances-measurements-and-spacing), [Toparredi](https://www.toparredi.com/en/living-room-layout-dimensions-spacing-guide) | 중간 |
| 러그 ~ 벽 여백 | 450 | 최소 150, 작은 방 305~457, 큰 방 610 | 공통 | [Homes & Gardens](https://www.homesandgardens.com/interior-design/living-rooms/a-guide-to-living-room-clearances-measurements-and-spacing), [Anabei](https://anabei.com/blogs/tips-tricks/living-room-furniture-ideas-easy-layouts-that-actually-work) | 중간 |

### 6.2 식사·주방

| 항목 | 전형값 | 범위 | 지역 | 출처 | 신뢰도 |
|---|---|---|---|---|---|
| 식탁 모서리 ~ 벽(의자 빼기) | 915 | ≥ 915 (36 in) | 공통 | [Eureka](https://eurekaergonomic.com/blogs/eureka-ergonomic-blog/dining-table-space-clearance-guide), [Homary](https://www.homary.com/tips-and-ideas/article/how-much-space-around-a-dining-table-the-complete-clearance-guide-513.html), [NEPA](https://www.nepafurniture.com/blog/home-furniture-32/how-much-space-is-needed-around-a-dining-table-416) | 높음 |
| 식탁·카운터 뒤 여유(NKBA 3단계) | 뒤로 지나가는 사람 없음 **813** / 비켜 지나감 **914** / 걸어서 지나감 **1118** | — | US | [CRD](https://www.crddesignbuild.com/blog/kitchen-dimensions-code-requirements-nkba-guidelines/), [NKBA 지침 사본](https://newcreationsaustin.com/wp-content/uploads/2019/05/nkba-planning-guidelines.pdf), [Simply Cabinetry](https://www.simplycabinetry.com/design-guidelines-nkba) | 높음 🟡("통행 없으면 915"는 틀림) |
| 앉은 사람 뒤로 통행 | 1118 | 1067~1219 | US | [Lamon Luther](https://www.lamonluther.com/resources/table-size-space-guidelines/), [Enkle](https://enkledesigns.com/how-much-room-do-you-need-around-a-dining-table/) | 중간 |
| 의자를 빼는 데 필요한 거리 | 510 | 460~610 | 공통 | [Sicotas](https://sicotas.com/blogs/blogs-sicotas-brand-story/minimum-space-around-dining-table), [Actu](https://actufurniture.com/blogs/buying-guides/how-much-space-do-you-need-around-a-dining-table) | 중간 |
| 식탁 아래 러그: 식탁 모서리 밖 확장 | 610 | 600~760 | 공통 | 출처 없음(관행값) | 낮음 |
| 펜던트: 식탁 상판 ~ 조명 하단 | 810 | 760~860 (일부 출처 760~915) | 공통 | [Fenchel Shades](https://www.fenchelshades.com/blog/post/pendant-lights-over-dining-table-height-standard-measurements-and-placement-guide-2026-usa), [Artika](https://artika.com/blogs/inspiration/complete-pendant-height-spacing-guide), [City Lights SF](https://citylightssf.com/blogs/city-lights-insights/how-high-to-hang-dining-room-pendant-lights) | 높음 |
| 다등 펜던트 중심 간격 | 660 | 610~760, 최대 915 | 공통 | [2Modern](https://www.2modern.com/blogs/modern-how-to/how-far-apart-should-pendant-lights-be), [Kouboo](https://www.kouboo.com/blogs/news/essential-guide-to-pendant-lighting-sizing-spacing-more) | 중간 |
| 펜던트·샹들리에 폭 상한 | 식탁 폭 − 610 (양쪽 305씩) | 다등은 식탁 길이의 약 2/3에 걸치고, 식탁 끝에서 150~300 안쪽 | 공통 | [Horne](https://shophorne.com/blogs/journal/styling-guide-what-size-pendant-light-should-i-hang-in-the-dining-room), [Schoolhouse](https://schoolhouse.com/blogs/how-to/choose-the-right-size-chandelier-or-pendant) | 중간 |

주방 작업 통로와 워크 트라이앵글은 4.1절에 있습니다.

> **[한국]** 천장고 2300에서 식탁 750 + 810이면 조명 하단은 바닥에서 약 1560, 늘어뜨린 길이는 약 740입니다(계산값).

### 6.3 침실·작업 공간

| 항목 | 전형값 | 범위 | 지역 | 출처 | 신뢰도 |
|---|---|---|---|---|---|
| 침대 옆 통로 | 600 | 최소 600, 쾌적 750~900 | 공통 | 출처 없음(관행값) | 낮음 |
| 책상 앞 의자 이동 여유(책상 모서리 ~ 뒤쪽 장애물) | 900 | 760~1000 | 공통 | 출처 없음(관행값) | 낮음 |

### 6.4 벽 장식 높이

| 항목 | 전형값 | 범위 | 지역 | 출처 | 신뢰도 |
|---|---|---|---|---|---|
| 그림·액자 중심(바닥 기준) | 1450 (57 in) | 1450~1520 (57~60 in) | 공통 | [AS Hanging](https://www.ashanging.com/en_us/help/what-is-the-rule-of-57), [Park West Gallery](https://www.parkwestgallery.com/blog/3-simple-rules-for-hanging-art/), [Fab Art](https://www.fab-art.co/blogs/news/the-57-inch-rule-perfect-art-hanging-height-explained), [Modern Memory](https://www.modernmemorydesign.com/blogs/news/how-high-to-hang-pictures-the-ultimate-gallery-standard-guide-2026) | 높음 |
| 소파·콘솔 위 그림 | 가구 윗면 + 150~250 | — | 공통 | G1 원자료(수치 미확인) | 낮음 ❔ |

57 in 규칙은 평균 서 있는 눈높이에 근거한 박물관 관행입니다([artacademi](https://artacademi.com/blogs/kb/ocular-ergonomics-physics-57-inch-museum-height-rule)). 가구 위에 걸 때는 가구 윗면 기준 여백을 먼저 맞추고, 천장이 아주 높은 공간은 예외입니다.

### 6.5 오픈소스 시스템에 들어 있는 배치 수치

연구·로보틱스 시뮬레이션용 시스템의 값입니다. 인테리어 관행과 다를 수 있으니 8절에서 비교하세요.

| 규칙 | 값 | 시스템 | 성격 | 출처 |
|---|---|---|---|---|
| 소파 ~ TV장 | 2~3 m | Infinigen `hinge(2,3)` | 소프트(최소화 비용) | [home.py v1.16.0](https://raw.githubusercontent.com/princeton-vl/infinigen/v1.16.0/infinigen_examples/constraints/home.py) |
| 커피테이블 ~ 소파 | 0.45~0.6 m | Infinigen `hinge(0.45, 0.6)` | 소프트 | 같음 |
| 사이드테이블 ~ 벽 | 0.3 m 이내 | Infinigen `hinge(0, 0.3)`, weight 10 | 소프트 | 같음 |
| 소파 벽 마진 | 0.1~0.3 m | Infinigen `StableAgainst(..., margin=uniform(0.1, 0.3))` | 관계 제약 | 같음 |
| 조명 간 최소 간격 | ≥ 1 m | Infinigen `min_distance_internal(lights) >= 1` | **하드** | 같음 |
| 소파가 TV를 향함 | `focus_score < 0.5` | Infinigen | **하드** | 같음 |
| 러그 간 최소 간격 / 벽 장식 바닥 높이 | 1 m / 0.6 m 초과 | Infinigen | 조건 | 같음 |
| 천장등 밀도 | hinge(0.08, 0.15) / m² | Infinigen | 소프트 | 같음 |
| 식탁당 의자 / 방 채움 정도(fullness) | 3~6개 / 0.6~0.9 | Infinigen | 조건 | 같음(원 조사) |
| 커피테이블 ~ 소파 | 0.3~0.5 m | SceneSmith 가구 designer | 프롬프트 규칙 | [designer_agent.yaml](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/furniture_agent/designer_agent.yaml) |
| 주동선 | 0.7~1.0 m | SceneSmith | 프롬프트 규칙 | 같음 |
| 카운터 뒤 여유 | 0.5~0.7 m | SceneSmith | 프롬프트 규칙 | 같음 |
| 무관한 물체 사이 | ≥ 0.2 m (충돌 해소 1단계 "넉넉한 간격부터 시도") | SceneSmith | 프롬프트 규칙 | 같음 |
| 그림·거울 중심 높이 | 1.4~1.7 m (대형 작품 1.2~1.5, 선반 1.2~1.8, 시계 1.5~1.8) | SceneSmith 벽 designer | 프롬프트 규칙 | [wall designer_agent.yaml](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/wall_agent/designer_agent.yaml) |
| 가구 위 벽걸이 | 가구 윗면 + 0.2~0.4 m, 그룹 간격 0.1~0.3 m | SceneSmith 벽 designer | 프롬프트 규칙 | 같음 |
| 스냅 | 0.01 m씩 전진, 부딪히면 한 스텝 후퇴, 마진 0.01 m | SceneSmith | 툴 | [base_furniture_agent.yaml](https://raw.githubusercontent.com/nepfaff/scenesmith/main/configurations/furniture_agent/base_furniture_agent.yaml), [snapping_helpers.py](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/furniture_agents/tools/snapping_helpers.py) |
| 자연 노이즈 | 가구 XY σ 0.03 m·yaw σ 1° / 소품 XY σ 0.01 m·yaw σ 3° | SceneSmith | 설정 | 같음, [base_manipuland_agent.yaml](https://raw.githubusercontent.com/nepfaff/scenesmith/main/configurations/manipuland_agent/base_manipuland_agent.yaml) |
| 관통 판정 / 가구 바닥 관통 허용 | 1 mm / 0.05 m | SceneSmith | 설정 | [base_furniture_agent.yaml](https://raw.githubusercontent.com/nepfaff/scenesmith/main/configurations/furniture_agent/base_furniture_agent.yaml) |
| 소품 넘어짐 판정 | 45° 이상 기울거나 1 m 이상 이동 | SceneSmith | 설정 | [base_manipuland_agent.yaml](https://raw.githubusercontent.com/nepfaff/scenesmith/main/configurations/manipuland_agent/base_manipuland_agent.yaml) |
| 가구 점유율 | 30~40% | SAGE | 프롬프트 규칙 | [object_placement_planner.py](https://raw.githubusercontent.com/NVlabs/sage/main/server/objects/object_placement_planner.py) |
| 주요 가구 사이 동선 | 60~90 cm | SAGE | 프롬프트 규칙 | 같음 |
| 문 회전 여유 | 약 90 cm (프롬프트). 솔버는 문 폭 × 문 폭 정사각형만 막고 개구부 깊이는 50 cm. 창 앞 여유는 계산하지 않음 | SAGE | 프롬프트 / 솔버 | 같음 |
| 충돌 패딩 | bbox 가로·세로 전체 + 3.5 cm(한쪽 약 1.75 cm), DFS grid 20 | SAGE | 솔버 | 같음 |
| 벽걸이 가장자리 마진 | 0.1 m | SAGE | 솔버 | 같음 |
| near / far | 50~150 cm / 150 cm 이상 | Holodeck(SAGE 프롬프트도 같음) | 어휘 정의 | [prompts.py](https://raw.githubusercontent.com/allenai/Holodeck/main/ai2holodeck/generation/prompts.py) |
| 방 크기 | 한 변 3~8 m, 최대 48 m² | Holodeck | 프롬프트 규칙 | 같음 |
| 같은 종류 벽걸이 | 같은 높이 | Holodeck | 프롬프트 규칙 | 같음 |
| 제약 가중치 | global 1.0, relative·direction·alignment 0.5, distance 1.8 | Holodeck DFS | 솔버 | [floor_objects.py](https://raw.githubusercontent.com/allenai/Holodeck/main/ai2holodeck/generation/floor_objects.py) |
| 관통 검사 임계 | 0.02 m | Vibe3DScene `SCENE_AGENT_PENETRATION_THRESHOLD_M` | 설정 | [configuration.md](https://raw.githubusercontent.com/3DSceneAgent/Vibe3DScene/main/docs/reference/configuration.md) |

- Infinigen v1 제약 코드(`home.py`)는 main 브랜치에서 빠졌습니다. **v1.16.0 태그**를 봐야 합니다.
- SceneSmith 가구 바닥 관통 허용 0.05 m는 시뮬레이션용입니다. 렌더용 장면에서는 `scene_audit.py` 기본값(5 mm)처럼 엄격하게 잡으세요.

---

## 7. 인체 치수

| 항목 | 전형값 | 범위 | 지역 | 출처 | 신뢰도 |
|---|---|---|---|---|---|
| 성인 남성 평균 키 | 1725 | 20~69세 | KR | [사이즈코리아 8차](https://sizekorea2022.kr/8th_results/), [산업통상부 보도](https://www.motir.go.kr/kor/article/ATCL8764a1224/155118041/view), [아주경제](https://www.ajunews.com/view/20220330111158866) | 높음 ✅ |
| 성인 여성 평균 키 | 1596 | 20~69세 | KR | [사이즈코리아 8차](https://sizekorea2022.kr/8th_results/), [뉴시스](https://mobile.newsis.com/view.html?ar_id=NISX20220330_0001813471), [서울신문](https://seoul.co.kr/news/newsView.php?id=20220330500111) | 높음 ✅ |
| 성인 평균 키 남 / 여 | 약 1753 / 약 1613 | — | US | 출처 없음(CDC 계열 기억치) | 낮음 |
| 서 있는 눈높이 | 키 × 약 0.93 (KR 남 약 1600, 여 약 1480) | 1450~1600 | KR/공통 | [artacademi](https://artacademi.com/blogs/kb/ocular-ergonomics-physics-57-inch-museum-height-rule)(57 in 근거), 비율 0.93은 기억치 | 낮음 |
| 앉은 눈높이(식탁 의자) | 1150 | 1100~1250 | 공통 | 파생값(좌판 450 + 앉은 눈높이) | 낮음 |
| 앉은 눈높이(소파) | 1050 | 1000~1100 | 공통 | 파생값 | 낮음 |
| 오금 높이(좌판 높이를 정함) | 400~450 | — | 공통 | 08 원자료 치트시트 | 낮음 ❔(한국 여성 평균보다 높을 수 있음) |
| 엉덩이 ~ 오금 길이(좌판 깊이를 정함) | 450~500 | — | 공통 | 08 원자료 치트시트 | 낮음 ❔ |

- 사이즈코리아 제8차: 2020~2021년 측정, 2022-03 발표, 20~69세 6,839명, 430개 항목(직접 측정 137, 3D 293). 눈높이·어깨높이·팔 도달거리 같은 세부 항목은 사이트에서 직접 받아야 하며 이번 조사에서는 얻지 못했습니다.
- **스케일 더미**: 한국 남 1725 / 여 1596 mm 실루엣을 장면에 임시로 두고 렌더 전에 숨기면, 가구 스케일 오류를 눈으로도 bbox 비교로도 바로 잡을 수 있습니다(G1 노하우).

---

## 8. 출처 간 충돌 한눈에 (권장 기본값)

| 항목 | 값 A | 값 B | 값 C(코드 포함) | 권장 기본값 |
|---|---|---|---|---|
| 식탁 높이 | 가이드 711~762 | 한국 실무 720~750 | Infinigen 650~850(랜덤) | **750** (KR은 720~750 안에서) |
| 식탁 의자 좌판 | 가이드 430~480 | 한국 실무 430~460 | Infinigen 좌판 윗면 약 470~540 | **450** (Infinigen은 좌판 두께 중앙 배치 때문에 높음) |
| 책상 높이 | KR 720(KS 관행) | US 711~762 | Infinigen N(730, 50), 600~830 | **KR 720 / US 740** |
| 조리대 | KR 850 / 신규 900 | US 914 | Archimesh 약 880, EU 900~910(미확인) | **지역 프리셋** |
| 상하부장 간격 | KR 650~750 | US 457~508 | Archimesh: 상부장 하단 1500 − 상판 880 ≈ 620(계산) | **지역 프리셋** |
| 소파 ~ 커피테이블 | 가이드 356~457 | SceneSmith 300~500 | Infinigen 450~600 | **400** (350~450) |
| 주동선 | 가이드 760~910 | SceneSmith 700~1000 / SAGE 600~900(주요 가구 사이) | 09 원 조사 업계값 900~1200, 최소 750(미확인) | **하드 ≥ 760, 기본 900** |
| 식탁 뒤 | NKBA 813 / 914 / 1118 | 가구 가이드 915(벽까지, 의자 빼기) | 09 원 조사 900 / 1100~1200(미확인) | **벽까지 915, 뒤로 걸어 지나가면 1118** |
| TV 거리 | 유통 가이드 대각선 × 1.5~2.5 | 시야각 계산 × 1.20~1.63(원문 미확인) | Infinigen 소파~TV장 2~3 m | **55형 2.4 m, 65형 2.75 m**(Keck 전형값). 몰입형이면 시야각 기준 |
| 그림 중심 높이 | 57 in = 1450 | 60 in = 1520 | SceneSmith 1400~1700 | **1450** (±50) |
| 가구 위 벽걸이 | G1 가구 윗면 + 150~250(미확인) | SceneSmith + 200~400 | — | **+200~250** (두 출처가 겹치는 구간) |
| 펜던트 높이(상판 위) | 760~860 | 일부 760~915 | 09 원 조사 750~900(미확인) | **810** |
| 침대 옆 통로 | G1 최소 600, 쾌적 750~900(관행) | 09 원 조사 600~900, 발치 ≥ 900(미확인) | — | **최소 600, 기본 750** |
| 러그 ~ 벽 여백 | 최소 150 / 작은 방 305~457 / 큰 방 610 | 09 원 조사 300~450(미확인) | Infinigen 러그끼리 1 m | **450** |
| 식탁 아래 러그 | G1 식탁 밖 600~760(관행) | 09 원 조사 사방 ≥ 600(미확인) | — | **610** |
| 공동주택 계단참 | 원 조사 3000 ❌ | 검증 2000(주택건설기준 제16조) | 일반 건축물 3000(피난·방화규칙 제15조) | **용도별로 분리** |
| 문 | KR 900×2100(문틀) | US 813×2032(미확인) | DIN 문짝 860×1985 / Archimesh 1000×2100 / Holodeck single 1000 | **지역 프리셋 + 개구부 치수로 boolean** |
| KR 천장고 | 구축 2300 | 신축 2400~2500 | US 2438(미확인) | **연식별 프리셋** |
| K 매트리스 | KR 표준표 1600×2000 | 에이스 1670×2075 | US King 1930×2032 / UK King 1500×2000 | **브랜드를 안 정했으면 1600×2000** |
| 계단 치수 | KR R ≤ 180, T ≥ 260 | IRC R ≤ 197, T ≥ 254 | Archimesh R 140, T 300(2R+T = 580) | **법규 안에서 2R+T = 620~640** |
| 인체 더미 | KR 남 1725 / 여 1596 | 08 원자료 1750 더미 | US 1753 / 1613(미확인) | **한국 장면은 KR 값** |

---

## 9. 관계식과 계산 예

| 관계 | 식 | 출처 |
|---|---|---|
| 식탁 ↔ 의자 | 좌판 = 상판 − 250~305 | [Pop Maison](https://www.popmaison.com/blogs/guide/dining-chair-dimensions), [Eureka](https://eurekaergonomic.com/blogs/eureka-ergonomic-blog/dining-table-chair-dimensions) |
| 카운터 ↔ 스툴 | 좌판 = 카운터 − 230~305 (보통 254) | [Barstool Comforts](https://barstoolcomforts.com/heights/), [Lumens](https://the-edit.lumens.com/the-guides/how-to-choose-seating-height/) |
| 침대 ↔ 협탁 | 협탁 윗면 = 매트리스 윗면 ± 50 | [Froy](https://froy.com/blogs/tips/how-tall-should-a-nightstand-be-the-nightstand-height-guide) |
| 소파 ↔ 커피테이블 | 높이 = 소파 좌판 − 0~50, 길이 = 소파 × 0.5~0.67 | [Apartment Therapy](https://www.apartmenttherapy.com/living-room-layouts-the-ideal-measurements-for-everything-in-the-room-206734) |
| 소파 ↔ 사이드테이블 | 높이 = 팔걸이 ± 50 | [Hernest](https://www.hernest.com/blog-detail/side-table-vs-nightstand-b-91.html) |
| 식탁 ↔ 펜던트 | 조명 하단 = 상판 + 760~860, 조명 폭 ≤ 식탁 폭 − 610 | [Fenchel Shades](https://www.fenchelshades.com/blog/post/pendant-lights-over-dining-table-height-standard-measurements-and-placement-guide-2026-usa), [Horne](https://shophorne.com/blogs/journal/styling-guide-what-size-pendant-light-should-i-hang-in-the-dining-room) |
| 식탁 인원 | 한 변 길이 ≈ 그 변 인원 × 610 | [NEPA](https://www.nepafurniture.com/blog/home-furniture-32/dining-table-size-guide-based-on-number-of-people-414) |
| 계단 | 단수 n = ⌈층고 ÷ 단높이 상한⌉, R = 층고 ÷ n, T = 630 − 2R (620~640) | [FreeCAD ArchStairs](https://raw.githubusercontent.com/FreeCAD/FreeCAD/main/src/Mod/BIM/ArchStairs.py) + 5.3절 법규 |
| KR 주방 벽면 | 하부장 + 미드웨이 + 상부장 = 천장고 | [LX Z:IN](https://www.lxzin.com/styling/style-guide/detail/5596) |
| KR 싱크대(사용자 맞춤) | 키 ÷ 2 + 50 | [치호건축사사무소](https://chiho.co.kr/blogroom/%EC%A3%BC%EB%B0%A9-%EC%8B%B1%ED%81%AC%EB%8C%80-%EB%86%92%EC%9D%B4%EC%99%80-%EB%8F%99%EC%84%A0-%EC%84%A4%EA%B3%84-%ED%82%A4%EB%B3%84-%EC%B5%9C%EC%A0%81-%EC%B9%98%EC%88%98-%EA%B3%B5%EA%B0%9C-%EC%A3%BC%EB%B0%A9%EC%84%A4%EA%B3%84) |
| TV 거리 | 대각선(mm) × 1.20~1.63(시야각 40~30°) 또는 × 1.5~2.5(유통 가이드) | [Keck](https://keckfurniture.com/blog/living-room-layout-rules-traffic-flow-conversation-zones-and-tv-placement/) + 계산 |

**계산 예 (한국 구축 아파트, 천장고 2300)**

1. **식탁 세트**: 식탁 750 → 의자 좌판 = 750 − 305~250 = 445~500, 표준 범위(430~480)와 겹치는 450~470에서 고릅니다. 4인 식탁은 1400×800 전후.
2. **아일랜드 스툴**: 조리대 850 → 좌판 850 − 254 ≈ 596, 580~600으로 둡니다.
3. **주방 벽면**: 850 + 700 + 750 = 2300. 신축 2400이면 850 + 700 + 850.
4. **펜던트**: 750 + 810 = 1560(조명 하단), 천장에서 약 740 늘어뜨림.
5. **공용계단(층고 2800)**: n = ⌈2800 ÷ 180⌉ = 16, R = 175, T = 630 − 350 = 280(≥ 260 통과). 높이 2 m를 넘으므로 **8단(1400) + 계단참(너비 ≥ 1200) + 8단**으로 나눕니다. 직통 16단은 위법입니다.
6. **55형 TV**: 대각선 1397 mm → 시야각 기준 약 1.7~2.3 m, 유통 가이드 기준 2.1~3.5 m. 기본값 2.4 m, 화면 중심 약 1050.
7. **저상형 침대 협탁**: 매트리스 윗면이 500이면 협탁 윗면 450~550.

---

## 10. 압축 치수 블록 (에이전트 프롬프트에 붙여 넣기)

`CLAUDE.md`/`AGENTS.md`나 작업 프롬프트에 그대로 붙이세요. 한국 기본값이고, 다른 지역이면 REGION을 바꾸고 해당 줄을 씁니다.

```text
# DIMENSIONS (mm, Z-up, 1 BU = 1 m → ÷1000). REGION=KR 기본. 이름("킹","표준 문") 대신 mm로 지정. 추측 금지.
[관계식-최우선] 좌판=상판−250~305 | 스툴좌판=카운터−230~305 | 협탁윗면=매트리스윗면±50
  커피테이블=소파좌판−0~50 | 사이드테이블≈팔걸이±50 | 펜던트하단=식탁상판+760~860 | 계단 2R+T=620~640
[좌석] 식탁의자 좌판450(430~480) 깊이430(406~457) 폭400~500 전체850(813~965)
  소파 좌판450(432~483) 좌판깊이560(508~610) 3인2130×940×840 2인1500×890 팔걸이550~700
  카운터스툴 KR600(550~620)/US635(610~660) | 바스툴740(711~762) | 사무의자 좌판400~520
[테이블] 식탁 KR720~750/US711~762, 1인폭610, 폭800~1000 | 책상 KR720/US740, 깊이600~800
  커피테이블406~457(길이=소파×0.5~0.67) | 사이드500~660 | 콘솔760~910 | 바1016~1067
[매트리스 W×L] KR S1000 SS1100 D1400 Q1500 ×2000 | K1600(~1670)×2000(~2075) LK1800(1700~1800)
  US Twin965×1905 Full1372×1905 Queen1524×2032 King1930×2032 CalKing1829×2134
  EU 900/1400/1600/1800×2000 | UK S900×1900 D1350×1900 K1500×2000 SK1800×2000
  매트리스윗면 US635(500~760), KR저상형400~550(미확인) | 협탁610~710 | 매트리스≠프레임
[주방 KR] 조리대850(신규900) 상판깊이600~650 상하부장간격650~750 상부장깊이300~350 통로≥900
  벽면 850+700+750=2300(천장이 높으면 상부장만 늘림)
[주방 US] 조리대914 캐비닛깊이610 상판635~648 간격457 상부장하단1372 깊이305 통로1067(1인)/1219
  트라이앵글 합≤7925 각변1219~2743 | 카운터좌석 무릎공간 762→457 914→381 1067→305, 좌석폭610
[수납] 책장깊이250~350(BILLY280, H1060/2020/2370) 선반간격250~350 | 옷장깊이550~650(PAX580/350, H2010/2360)
[건축 KR] 천장 구축2300/신축2400~2500, 층고2800~2850 | 방문 문틀900×2100(문짝−60, 두께35, 문틀110)
  욕실문 문틀700~800×2000~2100 | 현관1000×2100 | 벽 외벽200 내력180 칸막이100
  공용계단 R≤180 T≥260 폭≥1200, 높이2000 넘으면 2000 이내마다 계단참(≥1200), 유효높이≥2100
  난간≥1200(내부≥900) 간살≤100 | 콘센트300 협탁옆650 책상위850 스위치1200 | 침실창대≈900(미확인)
[건축 US/EU] 천장2438(미확인) 문813×2032(미확인) | IRC R≤197 T≥254 머리위≥2032 손잡이864~965 가드≥914
  DIN 문짝860×1985 → 벽개구부≈885×2010 | 벽 boolean은 항상 개구부(문틀 외곽) 치수
[동선] 주동선≥760(기본900) | 소파–커피테이블350~450 | 식탁–벽≥915, 뒤로 걸어 지나가면1118
  의자빼기460~610 | 침대옆≥600(기본750) | 책상뒤760~1000 | 문 스윙 영역 비우기(≈문폭×문폭)
  TV거리 55형≈2400(대각선×1.2~2.5), 화면중심≈1000~1100
  그림중심1450(~1520), 가구 위는 가구윗면+200~250 | 펜던트간격610~760 | 러그: 소파양끝+150↑, 벽여백450
[인체] KR 남1725 여1596 | 선 눈높이≈키×0.93 | 스케일 더미를 두고 렌더 전에 숨김
[규칙] 하드: 관통0·부유0·문/동선 막힘0·계단법규 | 소프트(그림·펜던트·러그·TV)는 범위 안에서
  같은 가구를 반복하면 범위 안에서 조금씩 다르게 | 한 장면에서 지역 프리셋을 섞지 말 것
```

---

## 11. `scene_audit.py` 규칙과의 대응

[`scene_audit.py`](scripts/scene_audit.py)의 `DEFAULT_SIZE_RULES`는 이 문서를 근거로 한 "명백한 오류" 탐지용 넓은 범위입니다. 이 문서 작성 과정에서 나온 오탐 제안(이름 부분 일치, 90° 회전, 암체어·스툴·콘솔·바 테이블 규칙 부재, 천장 관통 미검사)은 **2026-09-27 스크립트에 반영했고 테스트를 통과했습니다**(Blender 4.2.23 LTS·5.0.1).

- **치수 측정**: 유닛(최상위 부모) 전체를 **가구 자체 방향 기준**으로 잽니다. `w` = 수평 긴 변, `d` = 수평 짧은 변, `z` = 높이. 옆벽에 붙인 소파·침대·문도, 30°처럼 비스듬히 놓은 가구도 오탐하지 않습니다. 의자·스툴의 `z`는 좌판이 아니라 등받이까지 포함한 전체 높이입니다.
- **이름 매칭**: CamelCase·구분자를 단어로 나눈 뒤 **단어 단위로** 맞춥니다(`DiningTable` → `dining_table` 규칙). `turntable`·`indoor_plant`는 매칭되지 않고, `door_handle`·`table_lamp`·`desk_lamp`처럼 부속품 단어가 뒤에 붙으면 규칙을 적용하지 않습니다.
- **구조물·천장**: 이름의 마지막 핵심 단어가 `floor`·`ground`·`wall`·`ceiling`·`terrain`이면 구조물입니다(`floor_lamp`·`wall_shelf`는 가구). 가구가 벽·천장을 뚫으면 관통으로 잡고, `ceiling_z`를 주면 천장 위로 나간 유닛을 `above_ceiling`으로 표시합니다.
- **컬렉션 범위와 박힘**: 방 내부와 건물 외관을 한 장면에 둘 때는 `audit_scene(ceiling_z=2.30, collection="Room")`처럼 컬렉션을 지정해 천장 규칙을 방 유닛에만 적용합니다(받침면·관통 상대는 장면 전체). 바닥이나 슬래브에 파고든 가구는 '떠 있음'이 아니라 `sunk_into:<상대>=<깊이>m`으로 보고됩니다.

| 키 | 기본 범위(m) | 이 표의 근거 |
|---|---|---|
| `dining_table` | z 0.68~0.80 | 711~762, KR 720~750 |
| `coffee_table` | z 0.30~0.55 | 406~457, 소파 좌판 − 0~50 |
| `console_table` | z 0.70~0.95 | 760~910 (낮음) |
| `bar_table` | z 0.95~1.12 | 1016~1067 |
| `bedside_table`, `nightstand` | z 0.40~0.80 | 610~710, 매트리스 윗면 ±50, KR 저상형 |
| `desk` | z 0.68~0.80 | KR 700~740, US 711~762 |
| `table` | z 0.35~0.80 | 사이드 500~660 등 |
| `bar_stool` | z 0.68~1.30 | 좌판 711~762 + 등받이 최대 508 |
| `counter_stool` | z 0.50~1.20 | 좌판 550~660 (+등받이) |
| `stool` | z 0.40~0.85 | — |
| `armchair` | z 0.60~1.10, w·d 0.60~1.10 | 폭 710~1000, 깊이 760~1000 |
| `chair` | z 0.70~1.20, w·d 0.35~0.80 | 식탁 의자 전체 813~965, 좌판 폭 400~500 |
| `sofa` | z 0.60~1.10, w 1.20~3.50, d 0.70~1.20 | 높이 760~915, 폭 1320~2440, 깊이 760~1020 |
| `bed` | z 0.30~1.40, w 1.85~2.45, d 0.80~2.30 | 매트리스 길이 1900~2134, 폭 800(EU 싱글)~1930 |
| `wardrobe` | z 1.60~2.45, d 0.33~0.70 | PAX 깊이 350/580, 높이 2010/2360 |
| `bookshelf`, `bookcase` | z 0.70~2.40, d 0.20~0.45 | BILLY 280(유리문 300), 1060/2020/2370 |
| `door` | z 1.80~2.50, w 0.60~1.20 | KR 문틀 2000~2100, 욕실·창고 1800~ |
| `double_door` | z 1.95~2.50 | — |
| `bar_counter` | z 0.98~1.10 | 1016~1067 |
| `counter` | z 0.84~0.96 | KR 850~900, US 914 |

**한국 구축 아파트 점검 예 (파일을 고치지 않고 `size_rules`·`ceiling_z`로 넘기기)**

```python
from scene_audit import audit_scene, DEFAULT_SIZE_RULES
KR_SIZE_RULES = {
    **DEFAULT_SIZE_RULES,
    "dining_table": {"z": [0.70, 0.78]},    # KR 720~750
    "desk": {"z": [0.68, 0.78]},            # KR 700~740
    "counter": {"z": [0.84, 0.92]},         # KR 850 (신규 900)
    "door": {"z": [1.80, 2.20], "w": [0.60, 1.10]},  # KR 문틀 2000~2100, 욕실·창고 1800~
    "wardrobe": {"z": [1.60, 2.30], "d": [0.33, 0.70]},
}
report = audit_scene(floor_z=0.0, ceiling_z=2.30, size_rules=KR_SIZE_RULES)  # 신축이면 ceiling_z=2.40~2.50
```

- 에이전트에게 **영어 snake_case 이름에 종류 단어를 넣게** 하세요(`sofa_3seat`, `bedside_table_L`). 한국어 이름은 인식하지 않습니다([templates/CLAUDE.md](templates/CLAUDE.md)).
- 가구 이름을 `..._wall`로 끝내면 구조물로 분류되니 피하세요(`wall_shelf`는 가구로 인식).

---

## 흔한 실수와 해결

| 실수 | 증상 | 해결 |
|---|---|---|
| '킹 침대', '표준 문'처럼 이름으로 지시 | 지역이 섞여 폭이 300 mm 이상 달라짐 | mm로 지정: `bed={region:'KR', mattress_mm:[1600,2000]}` |
| 한 장면에 KR·US 값을 섞음 | 850 조리대에 457 간격 → 상부장이 너무 낮아 보임 | 장면마다 지역 프리셋 하나만 |
| 문짝 치수로 벽을 뚫음 | 문틀이 벽에 파묻히거나 틈이 생김 | 벽은 개구부(문틀 외곽)로, 문짝은 약 60 mm 작게 |
| 층고를 직통 계단으로 | 공동주택 기준 위반, 비현실적 | 높이 2 m 이내마다 계단참(8단 + 참 + 8단) |
| 한국 장면에 미국식 천장고를 기본값으로 | 문·상부장·펜던트 비율이 어긋남 | 구축 2300 / 신축 2400~2500 중 하나를 명시 |
| PAX 2360을 구축 아파트에 | 천장 관통 | 2010 모델이나 맞춤장. `audit_scene(ceiling_z=2.30)`으로 검출 |
| Infinigen 샘플 범위를 표준으로 씀 | 좌판 윗면 470~540 → 식탁과 무릎 간격 부족 | 표준 430~480, 관계식으로 검증 |
| 좌판 높이와 전체 높이를 혼동 | `chair` 규칙의 z는 등받이까지 포함 | 좌판은 부품(`chair_seat`) 윗면으로 따로 잼 |
| 큐브 크기 계산 실수 | `primitive_cube_add`의 size와 scale을 섞어 쓰면 치수가 절반·두 배로 틀어짐 | size·scale 규칙을 하나로 고정하고 만든 뒤 bbox로 확인([ProfRino Assembly Skill](https://github.com/ProfRino/Blender-MCP-Assembly-Skill)은 size=2 규칙을 둠) |
| mm·cm·m 혼동 | 100배·1000배 크기 오류 | Holodeck cm, CAD mm, Blender m. 단위를 매번 명시하고 가져온 뒤 스케일 Apply |
| 모든 가구를 평균값으로 | CG처럼 보임 | 범위 안에서 조금씩 다르게 |
| 월드 x·y 치수로 가구 크기를 판단 | 옆벽에 붙인 소파·침대·문의 폭·깊이가 바뀌어 보임 | 가구 방향 기준 폭·깊이로 비교(`scene_audit`의 `size_wdh_m`이 이렇게 잼) |
| NKBA "통행 없으면 915" 인용 | 필요 이상으로 넓은 여유 | 813(통행 없음) / 914(비켜 지나감) / 1118(걸어서 지나감) |
| TV 거리 기준을 섞음 | 너무 멀거나 가까움 | 시야각 기준과 유통 가이드 기준 중 하나로 통일 |

---

## 관련 문서

- [오브젝트·가구·조형물 모델링](../02_guides/07_modeling_objects_furniture_sculpture.md): 부품 스펙 JSON, 부재 두께, 실패 모드
- [배치·레이아웃](../02_guides/08_scene_layout_placement.md): 관계 제약 + 솔버, 충돌·부유 검사, 한국 프리셋(6절)
- [에이전트 워크플로·프롬프팅](../02_guides/09_agent_workflow_prompting.md): 치수표를 컨텍스트에 넣는 방법
- [텍스처링·재질](../02_guides/05_texturing_materials.md): 실측 치수와 텍스처 스케일 맞추기
- [라이팅·렌더·아트디렉션](../02_guides/06_lighting_rendering_art_direction.md): 카메라 높이·눈높이
- [학술 연구](../02_guides/11_research_papers.md): Holodeck, SceneSmith, SAGE, Infinigen
- [보조 스크립트](scripts/README.md): `scene_audit.py`, `placement_utils.py`, `review_views.py`, `building_audit.py`(문·창·방·계단의 건축 상식 검사)
- [품질 체크리스트](04_quality_checklists.md) · [프롬프트 템플릿](03_prompt_templates.md) · [AAA 제작 플레이북](02_aaa_production_playbook.md)
- [프로젝트 규칙 템플릿](templates/CLAUDE.md) · [Claude Code 스킬 템플릿](templates/skills/blender-aaa-scene/SKILL.md)
- [한국어 자료 모음](../04_case_studies/02_korean_resources.md)
- [조사 방법·신뢰도 정책](../01_research/research_method.md) · [교차검증 로그](../01_research/verification_log.md) · [출처 카탈로그](../01_research/sources_catalog.md)

## 원자료

- [`01_research/raw/G1_dimensions.gap.json`](../01_research/raw/G1_dimensions.gap.json): 치수 136행, 법규·표준 항목, 노하우, 공백 목록
- [`01_research/raw/G1_dimensions.verify.json`](../01_research/raw/G1_dimensions.verify.json): 23개 주장 독립 검증(계단참 정정, NKBA 3단계, 매트리스 K/LK, 문틀/문짝/개구부 등)
- [`01_research/raw/08_modeling-objects.research.json`](../01_research/raw/08_modeling-objects.research.json): Infinigen·Archimesh·FreeCAD·Holodeck 코드 값, 치수 치트시트
- [`01_research/raw/08_modeling-objects.verify.json`](../01_research/raw/08_modeling-objects.verify.json): Infinigen 좌판 높이 해석 정정, 신뢰도 낮은 출처 목록
- [`01_research/raw/09_scene-layout.research.json`](../01_research/raw/09_scene-layout.research.json): SceneSmith·SAGE·Holodeck·Infinigen 배치 수치
- [`01_research/raw/09_scene-layout.verify.json`](../01_research/raw/09_scene-layout.verify.json): SAGE 솔버 실제 값, Infinigen 커피테이블 hinge(0.45, 0.6), SceneSmith 설정 확인
