# AAA 라이팅·렌더·카메라·아트디렉션 가이드 (AI 에이전트용 수치 규칙)

> 기준일: 2026-09-27 · '싸구려 CG 티'는 대부분 숫자로 잡을 수 있습니다. 색관리·노출 → 스케일 → 광원 하나씩 → 재질 변화 → 베벨·마모 → 물리 카메라 → 절제된 합성 순서로 규칙을 적용하고, **실제 렌더를 파일로 저장해 눈과 수치로 확인하는 루프**를 돌리세요.

## 핵심 요약

- **순서가 품질을 결정합니다.** 레퍼런스와 카메라 구도를 먼저 고정하고(0단계), 그다음 ① 색관리·노출 ② 실측 스케일(1 unit = 1 m) ③ 검정에서 시작해 광원 하나씩 ④ 재질값의 공간적 변화 ⑤ 모든 하드엣지 베벨과 마모 ⑥ 물리 카메라(초점거리·f-stop·조리개 날) ⑦ 깨끗하게 렌더한 뒤 절제된 합성 순서로 갑니다. 한 번에 한 변수만 바꿉니다.
- **색관리는 AgX가 기본입니다.** 제품 색이 중요하면 Khronos PBR Neutral, HDR 납품이나 파이프라인 표준이면 ACES 2.0을 씁니다. Standard는 쓰지 않습니다(선형 1.0, 즉 중간 회색보다 약 2.5 stop 밝은 곳에서 바로 잘림. 실측에서 선형 1.44가 이미 255). AgX는 클리핑을 부드럽게 숨기므로(선형 4.0 → 표시 0.91) 노출은 False Color와 EXR 수치로 판정하고, 밝기는 램프가 아니라 `view_settings.exposure`로 조절합니다.
- **광원 크기 0 금지, 색은 켈빈으로.** Blender에서 bpy로 새로 만든 Point 라이트의 반경 기본값은 0이고(칼같이 딱딱한 그림자), UE 로컬 라이트의 Source Radius 기본값도 0입니다. 5.x는 `use_temperature`로 켈빈을 직접 지정하는데, 켜면 `color`가 곱해지는 틴트로 바뀌므로 흰색으로 되돌려야 합니다. 키는 카메라 축에서 20° 이상 떨어뜨리고(기본 40°·위 35°·피사체 반경 3배 거리·크기 = 반경), 필은 key:fill 3~4:1에서 시작해 레퍼런스에 맞춥니다.
- **blender-mcp에는 렌더 도구가 없습니다**([이슈 #61](https://github.com/ahujasid/blender-mcp/issues/61), not planned). 뷰포트 스크린샷은 최종 색관리·GI(전역 조명)·DOF(피사계 심도)와 다르므로, `execute_blender_code`나 헤드리스 Blender로 렌더를 **파일로 저장**해서 봐야 합니다. 이 문서의 `review_render()`는 렌더 한 번으로 표시용 PNG, 선형 EXR, False Color PNG, 수치 JSON을 남깁니다(pip bpy 5.0.1·4.2.23 LTS에서 실행 확인).
- **Blender 5.x에서 LLM이 자주 틀리는 것**: EEVEE 식별자(5.0+ `BLENDER_EEVEE`, 4.2~4.x `BLENDER_EEVEE_NEXT`), 없는 속성(`use_bloom`·`use_ssr`·`use_gtao` → AttributeError), 컴포지터(`scene.compositing_node_group`, Composite 노드 없음 → Group Output), Glare 기본 타입이 **Streaks**라는 점, 구버전 Glare 값(Size 8~9, mix -0.7)은 5.x에서 입력 불가, 멀티레이어 EXR은 `media_type`을 먼저 바꿔야 한다는 점.
- **Unreal**: Lumen은 **Static** 라이트만 지원하지 않습니다(Stationary도 GI에 반영됨. 커뮤니티 스킬의 'Movable만 반영' 주장은 틀림). 벽 두께 10 cm 이상, 작은 발광체는 Emissive Light Source, 거울끼리 비치는 장면은 반사 바운스(기본 1)를 올리고, Substrate 다층 재질은 Adaptive GBuffer로 바꿉니다. 룩뎁 중에는 자동노출을 끄고 EV100을 고정합니다. Path Tracer 문서는 diffuse Base Color를 0.8 미만으로 두라고 권합니다.
- **카메라·아트디렉션**: 기본 50 mm를 그대로 쓰지 않고(실내 24~35 mm), 눈높이 1.6~1.7 m, 건축은 수평 카메라 + shift로 수직선을 세웁니다. 한 뷰에 히어로 하나, 전경·중경·배경, 스토리 비트당 소품 3~7개와 마모 데칼 1~2개, 스케일 단서(1.8 m 인물 등)를 두고, 순흑·순백·채도 100% 픽셀은 금지합니다.
- **규칙끼리 충돌하는 곳**(필 비율, 제품 초점거리, 베벨 폭, 태양 세기 등)은 "기본값으로 시작 → 레퍼런스 사진과 비교해 조정"을 규칙으로 씁니다(8절).
- **[한국 사용자]** 한국어 UI에서는 새로 만든 노드 이름이 번역될 수 있으니 노드는 이름이 아니라 `bl_idname`·`type`으로 찾습니다(이 문서의 코드는 모두 그렇게 작성). 생성형 메시의 구워진 조명 문제 때문에 PBR 출력 모델을 권할 때, **Hunyuan3D 계열 오픈웨이트 라이선스는 대한민국을 적용 지역에서 제외**한다는 점을 함께 확인하세요. 스케일 단서로 흔히 쓰는 문 높이 2.03~2.13 m는 미국 인치 규격(80·84인치)이므로 한국 치수는 [실측 치수 기준표](../03_playbooks/05_reference_dimensions.md)를 쓰세요.
- **한계**: 독립적으로 검증된 'AAA급' AI+MCP 결과물은 찾지 못했습니다. 이 규칙들은 CG 티를 없애는 하한선이고, 최종 룩은 레퍼런스 비교와 사람의 마무리에서 나옵니다.

---

## 0. 근거 표기

이 문서의 수치는 출처 신뢰도가 다릅니다. 에이전트 규칙에 옮길 때 아래 표기를 참고하세요.

| 표기 | 뜻 |
|---|---|
| **[소스]** | Blender 공식 소스(v5.2.2 태그 또는 main)에서 확인하고 독립 검증을 통과한 값. 참고로 main 브랜치는 5.3 alpha([BKE_blender_version.h](https://raw.githubusercontent.com/blender/blender/main/source/blender/blenkernel/BKE_blender_version.h))이며, 이 문서에 쓴 항목은 검증 에이전트가 v5.2.2와 같다고 확인했습니다 |
| **[실측]** | 이 문서를 쓰면서 pip `bpy` **5.0.1**과 **4.2.23 LTS**를 헤드리스로 실행해 직접 확인한 값(2026-09-27). 5.2.2 GUI + MCP 경로에서는 실행하지 않았습니다 |
| **[UE 미러]** | Epic UE **5.7** 문서의 비공식 Markdown 미러([ue5-docs-mcp](https://github.com/CharlieCardenasToledo/ue5-docs-mcp))에서 확인한 내용. 검증 에이전트도 같은 미러로 재확인했지만 dev.epicgames.com 원문과 직접 대조하지는 못했습니다. 공식 출처로 인용하지 마세요 |
| **[스킬]** | 에이전트 스킬 저자가 정한 값(scenario-labs, cc-blender-skill, arjun988). 원문과 일치하는지는 검증했지만 업계 표준은 아닙니다. scenario의 게이트 수치 상당수는 원문에 `[added]`(저자 추가)로 표시돼 있습니다 |
| **(미검증 주장)** | [Bartindigital/blender-hyperrealism-skill](https://github.com/Bartindigital/blender-hyperrealism-skill)의 값. 튜토리얼 57개를 정리했다고 하지만 커밋 1개·스타 0이고 구버전 수치가 섞여 있어(4.3 이하 Glare, Cycles X에서 제거된 Branched Path Tracing, 4.1에서 제거된 Auto Smooth, 'HDRI strength ~1000') 검증에서 신뢰도 낮은 출처로 분류됐습니다. 아이디어와 출발점으로만 쓰세요 |
| **(보완 조사)** | 공식 문서·뉴스의 검색 요약으로 확인한 값(원문 미열람, 독립 검증 파일 없음) |
| **(신뢰도 낮음)** | 단일 출처이거나 SEO성 블로그 |

---

## 1. 적용 순서 (에이전트 파이프라인)

각 단계는 "통과 조건"을 만족해야 다음으로 갑니다. 여러 단계를 한꺼번에 바꾸면 무엇이 효과를 냈는지 알 수 없고, 에이전트가 값을 오가며 진동합니다.

| 단계 | 할 일 | 통과 조건(에이전트가 확인) | 자세히 |
|---|---|---|---|
| 0. 레퍼런스·구도 | 레퍼런스 보드(무드·팔레트·계절·복제할 특징 목록), 카메라 후보 여러 개를 렌더해 비교한 뒤 하나 고정 | 히어로가 무엇인지 한 문장으로 말할 수 있음. 카메라 고정 | 6.1, 5절 |
| 1. 색관리·노출 | AgX + Look, 작업 색공간은 프로젝트 시작 때 한 번만, 밝기는 `exposure`로 | `view_transform`이 Standard가 아님. 피사체 EV ≈ 0(중간 회색). `clip_pct` ≤ 0.5% | 3.1, 2.4 |
| 2. 스케일 | 1 unit = 1 m, 트랜스폼 적용(Ctrl+A), 스케일 기준물 배치 | [scene_audit.py](../03_playbooks/scripts/README.md) 치수 검사 통과 | 6.5, [모델링](07_modeling_objects_furniture_sculpture.md) |
| 3. 광원 하나씩 | World 0, 모든 램프 끔 → HDRI → 키 → 실용광 → 고보 순으로 추가. 하나를 조정할 때 나머지는 숨김 | 광원마다 존재 이유(켈빈·크기·거리). 카메라 축 20° 미만 키 없음. 실내에서 World 기여 < 10%(scenario 기준) | 3.3 |
| 4. 재질 변화 | roughness를 맵·노이즈로 변화, metallic 0 또는 1, albedo 범위 | roughness 맵 표준편차 > 0.01, 유전체 albedo sRGB 30~240 | 6.6, [텍스처링](05_texturing_materials.md) |
| 5. 베벨·마모 | 모든 하드엣지 마이크로 베벨, 마모·먼지·지문은 물리적 원인에 맞는 채널로 | 모든 모서리가 하이라이트를 받음 | 7절 #5, [모델링](07_modeling_objects_furniture_sculpture.md) |
| 6. 물리 카메라 | 초점거리·f-stop·조리개 날·초점 대상·모션블러 | 50 mm 기본값 그대로가 아님. DOF가 없지도, 과하지도 않음 | 5절 |
| 7. 절제된 합성 | 디노이즈 → (AO) → 색 보정 → Glare → 렌즈 효과 → 그레인 | 효과를 끈 버전과 A/B했을 때 "좋아졌는데 무엇을 했는지 안 보임" | 3.5 |
| 8. 검토 루프 | `review_render()` → 이미지 직접 확인 + 수치 게이트 → 한 변수만 수정 → 태그를 올려 재렌더 | 렌더를 직접 보지 않고 완료 보고 금지(scenario expert 규칙) | 2절 |

이 순서는 여러 스킬 문서가 공통으로 제시하는 흐름입니다. cc-blender-skill은 `block-out → camera → lighting → forms → materials → detail → render → composite → export`를 강제하고([RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill)), scenario는 단계마다 측정 게이트를 둡니다([scenario-blender-lighting-rendering](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-lighting-rendering/SKILL.md)). 구도(카메라 위치)는 조명보다 먼저 고정하고, 광학 설정(f-stop·DOF)은 6단계에서 마무리합니다. 조명은 시점에 의존하고, 프레임 밖이나 흐려질 곳에 쏟은 디테일은 낭비이기 때문입니다.

---

## 2. 렌더 품질 판단: 실제 렌더를 파일로 저장해 보기

### 2.1 왜 스크린샷으로는 안 되는가

- ahujasid **MCP for Blender**(PyPI `mcp-for-blender` 2.1.0, 2026-09-25)에는 전용 렌더 tool이 없습니다. 2025-03-18에 열린 기능 요청 [#61 'teach server to render'](https://github.com/ahujasid/blender-mcp/issues/61)은 not planned로 닫혔고, 현재 [README](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/README.md)에도 렌더 tool은 없습니다.
- `get_viewport_screenshot`은 뷰포트 기준입니다. 최종 뷰 변환·GI·DOF·컴포지터 결과와 다르고, Windows Blender + WSL 조합에서는 캡처가 실패한다는 보고(#187, not planned)도 있습니다.
- 스크린샷은 **배치·구도 확인용**으로만 쓰고, 조명·노출·재질 판단은 렌더 파일로 합니다.

### 2.2 경로별 방법

| 경로 | 렌더하는 법 | 이미지를 AI가 보는 법 | 주의 |
|---|---|---|---|
| ahujasid MCP for Blender (GUI) | `execute_blender_code`로 아래 `review_render()` 실행 | Claude Code·Codex처럼 로컬 파일을 읽을 수 있는 클라이언트에서 PNG를 읽음 | 소켓 타임아웃 180초 → 검토 렌더는 해상도 50%, 샘플 64 안팎. `BLENDER_MCP_SAFE_MODE=1`에서도 bpy를 통한 렌더·저장은 허용되지만(README), `open()`·`os` 같은 직접 파일 I/O는 막힙니다. 아래 `review_render()`는 `os.makedirs`와 `open()`(stats.json 쓰기)을 쓰므로 safe mode에서는 사전 검사에 걸릴 가능성이 큽니다(미실측). 그럴 땐 헤드리스로 돌리세요 |
| 공식 Blender Lab 서버 (Blender 5.1+) | 코드 실행 tool로 같은 함수 실행 | 서버의 화면·렌더 관련 tool은 [Blender MCP 가이드](02_blender_mcp.md) 참고 | 커뮤니티 서버와 같은 포트(9876)라 동시에 켜지 말 것 |
| 헤드리스 (Claude Code / Codex) | `blender -b scene.blend --factory-startup --python-exit-code 1 -P review.py` | 생성된 PNG를 파일 읽기 도구로 읽음 | `--python-exit-code 1`이 없으면 예외가 나도 성공으로 보임. GPU 없는 서버는 Cycles(CPU) |
| Unreal | MRQ(Movie Render Queue) 또는 Path Tracer로 스틸 출력 | 같은 방식으로 파일 읽기 | Epic 공식 플러그인 README에는 조명·포스트·렌더 전용 도구가 명시돼 있지 않음 → Python·콘솔 명령으로 우회(4.9) |

> 파일을 읽을 수 없는 클라이언트라면 차선책으로 뷰포트를 카메라 뷰 + Rendered 셰이딩으로 맞춘 뒤 스크린샷을 찍을 수 있습니다. 이 방법은 최종 렌더와 다를 수 있으니 룩 확정에는 쓰지 마세요(이 문서의 제안, 미검증).

### 2.3 `review_render()` — 렌더 1회로 PNG·EXR·False Color·수치 저장

**[실측]** pip bpy 5.0.1과 4.2.23 LTS에서 헤드리스로 실행해 확인했습니다. 원래 설정(해상도 %, 샘플, 파일 형식·`media_type`, 뷰 변환, Look)은 끝나면 되돌립니다.

```python
import bpy, os, json
import numpy as np

REC709 = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)

def _load_rgb(path):
    img = bpy.data.images.load(path, check_existing=False)
    px = np.empty(len(img.pixels), dtype=np.float32)
    img.pixels.foreach_get(px)
    bpy.data.images.remove(img)
    return px.reshape(-1, 4)[:, :3]

def review_render(out_dir, tag='v001', samples=64, percent=50):
    """렌더 1회 → {tag}_beauty.png / _linear.exr / _falsecolor.png / _stats.json"""
    scene = bpy.context.scene
    r, vs, im = scene.render, scene.view_settings, scene.render.image_settings
    if scene.camera is None:
        raise RuntimeError('scene.camera가 없습니다')
    os.makedirs(out_dir, exist_ok=True)
    p = {k: os.path.join(out_dir, f'{tag}_{k}') for k in ('beauty.png', 'linear.exr', 'falsecolor.png')}
    keep = (r.resolution_percentage, im.file_format, im.color_depth, vs.view_transform, vs.look)
    keep_media = getattr(im, 'media_type', None)       # 5.0+에만 있음
    keep_spp = scene.cycles.samples if r.engine == 'CYCLES' else None
    try:
        if keep_media is not None:
            im.media_type = 'IMAGE'                    # 멀티레이어 EXR 설정이 남아 있으면 PNG 지정이 실패
        r.resolution_percentage = percent
        if keep_spp is not None:
            scene.cycles.samples = samples
        bpy.ops.render.render()                        # 파일 없이 Render Result만 만든다
        res = bpy.data.images['Render Result']
        im.file_format, im.color_depth = 'PNG', '8'
        res.save_render(p['beauty.png'])               # 현재 뷰 변환(AgX 등)이 구워진 이미지
        im.file_format, im.color_depth = 'OPEN_EXR', '32'
        res.save_render(p['linear.exr'])               # 장면 선형값(뷰 변환 없음) → 측정용
        vs.view_transform, vs.look = 'False Color', 'None'
        im.file_format, im.color_depth = 'PNG', '8'
        res.save_render(p['falsecolor.png'])           # 다시 렌더하지 않고 뷰만 바꿔 저장
    finally:
        if keep_media is not None:
            im.media_type = keep_media                 # media_type을 먼저 되돌려야 file_format 복원 가능
        r.resolution_percentage, im.file_format, im.color_depth, vs.view_transform, vs.look = keep
        if keep_spp is not None:
            scene.cycles.samples = keep_spp
    disp, lin = _load_rgb(p['beauty.png']), _load_rgb(p['linear.exr'])
    mx, mn = disp.max(1), disp.min(1)
    sat = (mx - mn) / np.maximum(mx, 1e-6)
    lum = disp @ REC709
    lin_y = (lin @ REC709) * 2.0 ** vs.exposure            # EXR에는 뷰 exposure가 안 들어가므로 보정
    ev = np.log2(np.maximum(lin_y, 1e-6) / 0.18)           # 0 EV = 중간 회색(0.18)
    stats = {
        'clip_pct': (mx >= 0.99).mean() * 100,             # 하얗게 날아간 픽셀
        'ev_over5_pct': (ev >= 5).mean() * 100,            # False Color 빨강·흰색 구간
        'pure_black_pct': (mx <= 0.01).mean() * 100,       # 순흑
        'sat100_pct': ((sat >= 0.99) & (mx > 0.2)).mean() * 100,  # 채도 100%
        'value_range': np.percentile(lum, 98) - np.percentile(lum, 2),
        'median_ev': np.median(ev),
        'standard_clip_pct': (lin_y > 1.0).mean() * 100,   # Standard 뷰였다면 잘렸을 비율
    }
    stats = {k: round(float(v), 3) for k, v in stats.items()}
    with open(os.path.join(out_dir, f'{tag}_stats.json'), 'w') as f:
        json.dump(stats, f, indent=1)
    return p, stats

# 사용: 경로는 절대경로로. Windows면 r"C:\work\review"
# paths, stats = review_render(r"/abs/path/review", tag="v003", samples=64, percent=50)
# print(stats)   # → 이 결과와 v003_beauty.png, v003_falsecolor.png를 AI가 읽고 판정
```

- `save_render()`는 저장 시점의 뷰 설정을 적용하므로 **렌더 한 번으로 표시용과 False Color를 모두** 만들 수 있습니다. EXR은 뷰 변환이 들어가지 않은 선형값입니다([실측]).
- 백그라운드 모드에서는 `Render Result`의 픽셀을 바로 읽을 수 없어서, 파일로 저장한 뒤 `bpy.data.images.load()`로 다시 읽습니다.
- 배경을 투명(`film_transparent`)으로 두면 투명 영역이 순흑으로 집계됩니다. World를 켠 상태로 측정하세요.
- 테스트 예([실측] 5.0.1, 1 m 큐브 + 3.3절 조명 코드 그대로 + 발광 구 하나): `exposure` 0에서 `clip_pct` 3.3%·`median_ev` 3.4였고, 램프는 그대로 두고 `exposure = -2.0`만 바꾸자 `clip_pct` 0.37%·`median_ev` 1.4가 됐습니다. 남은 0.37%는 전부 발광 구였습니다(구를 숨기면 0%). 게이트에서 발광체를 빼야 하는 이유입니다.

### 2.4 수치 게이트

| 지표 | 목표 | 근거 |
|---|---|---|
| `clip_pct` (발광체·창 제외) | ≤ 0.5% | scenario 게이트 "발광체 외 클리핑 ≤ 0.5%" [스킬]. 이 함수는 발광체를 빼지 않으므로 하얀 영역이 전구·창인지 이미지로 확인 |
| `value_range` | ≥ 0.30 | scenario 게이트 [스킬]. scenario의 정확한 계산식은 확인하지 못했고, 이 함수는 표시 휘도의 2~98 퍼센타일 차이로 근사 |
| 피사체 노출 | 피사체 부분이 False Color 회색(≈ 0 EV) | 노출 기준점을 중간 회색에 두라는 원칙([Andrew Price](https://andrew-price-a9bl.squarespace.com/tutorials/secret-ingredient-photorealism), 보완 조사). `median_ev`는 배경을 포함한 참고값 |
| `pure_black_pct`, `sat100_pct` | 0에 가깝게(의도한 검은 배경 제외) | 순흑·순백·채도 100% 금지(6.6) |
| `standard_clip_pct` | 정보용 | AgX가 숨긴 하이라이트 양. 이 값이 크면 창·하늘이 Standard였다면 날아갔다는 뜻 |
| 키 방향 | 카메라 축에서 ≥ 20° | scenario: 20° 미만 frontal key는 경고 [스킬]. 3.3의 `key_angle_deg()`로 측정 |
| 실내 World 기여 | < 10% | scenario [스킬]. Light Group으로 World를 분리 렌더해 비교 |
| roughness 변화 | 맵 표준편차 > 0.01 | scenario texturing 게이트 [스킬] |
| EEVEE 파이널 | 같은 장면 Cycles 레퍼런스의 약 30% 이내 | scenario [스킬] |

scenario 스킬에는 이 밖에도 surround separation ≥ 0.10, edge merge ≤ 35%, clay form ratio ≥ 2.5 같은 형태 가독성 게이트가 있습니다(`bx_light.py`, Blender 5.2.1에서 테스트했다고 명시). 모두 툴킷 자체 정의라 업계 표준은 아닙니다.

### 2.5 False Color 색 구간 (Blender 5.0.1 실측)

균일한 발광 패치(선형 0.18 × 2^k)를 렌더해 읽은 값입니다. 정수 stop에서만 측정했으므로 경계는 그 사이 어딘가입니다. 4.x 이전 Filmic 시절 자료나 스킬 문서의 색 설명과 다를 수 있으니, 에이전트 규칙에는 아래 표를 쓰세요.

| 중간 회색 대비 | 선형값 | False Color | AgX 표시(8bit) | Standard 표시 | Khronos PBR Neutral |
|---|---|---|---|---|---|
| -10 stop 이하 | ≤ 0.0002 | 검정 | 0 | 1 | 0 |
| -9 ~ -7 | 0.0004~0.0014 | 파랑 | 0~2 | 1~5 | 0 |
| -6 ~ -5 | 0.003~0.006 | 하늘색 | 3~10 | 9~17 | 0 |
| -4 ~ -2 | 0.011~0.045 | 청록(cyan) | 20~54 | 27~60 | 2~30 |
| -1 | 0.09 | 초록빛 청록 | 82 | 85 | 64 |
| **0** | **0.18** | **회색** | 118 | 118 | 105 |
| +1 | 0.36 | 연두 | 155 | 162 | 154 |
| +2 | 0.72 | 노랑 | 184 | 220 | 214 |
| +3 ~ +4 | 1.44~2.88 | 주황 | 209~226 | **255(잘림)** | 248~253 |
| +5 ~ +6 | 5.8~11.5 | 빨강 | 240~250 | 255 | 254 |
| +7 이상 | ≥ 23 | 흰색 | 255 | 255 | 255 |

- Standard는 선형 1.0에서 잘리므로 중간 회색 기준 약 +2.5 stop 위부터 정보가 사라집니다. AgX는 +6 stop(선형 11.5)에서도 250으로 계조가 남습니다. 그래서 AgX 화면만 보면 과노출을 놓칩니다.
- scenario 스킬이 적은 "AgX에서 선형 4.0 → 0.910"도 위 표와 맞습니다(선형 2.88 → 226/255 = 0.89).

### 2.6 AI에게 보여 주고 판정받는 법

1. **검토 이미지 세트**: `beauty.png` + `falsecolor.png` + `stats.json`. 형태·배치 검토는 따로 [review_views.py](../03_playbooks/scripts/README.md)(위·정면·측면·3/4, 오브젝트별 랜덤 색)로 합니다. scenario expert 스킬은 실루엣·matcap·와이어 × 정면·측면·3/4·로우앵글 contact sheet를 강제합니다([scenario-blender-expert](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-expert/SKILL.md)).
2. **이미지 크기**: 검토용은 긴 변 약 1000px이면 충분합니다(이미지 토큰 계산은 [Blender MCP 가이드](02_blender_mcp.md)).
3. **판정 형식**: 7절의 12개 원인을 항목별로 "통과/문제(근거)"로 답하게 하고, 문제는 Blocker / Major / Minor / Note로 분류해 SHIP / SHIP WITH NOTES / NO-SHIP으로 결론 내게 합니다(arjun988 [qa-review](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/qa-review/SKILL.md) 방식).
4. **수정**: 한 번에 한 변수(조명·재질·카메라 중 하나)만 바꾸고 태그를 올려(`v004`) 다시 렌더합니다. 이전 태그와 나란히 비교합니다.
5. **최종본**: 대량·최종 렌더는 헤드리스(`blender -b`)로 돌립니다(scenario: 라이브 GUI 작업은 MCP, 최종 렌더와 검증은 headless).

**모델 선택**: 조명·렌더 판단 능력을 모델별로 비교한 벤치마크나 사례는 찾지 못했습니다. 그래서 비전 판단만 믿지 말고 위 수치 게이트를 함께 쓰는 편이 안전합니다. Anthropic은 Claude Opus 5.5를 'vision과 computer use에 가장 좋은 Opus'로 소개합니다. GPT-6 Astra를 Codex에서 쓸 때는 기본 reasoning effort가 low이므로 비평 단계의 effort를 명시하세요. 자세한 비교는 [AI 모델 가이드](01_ai_models_and_clients.md)에 있습니다.

---

## 3. Blender 5.x 설정

기준: Blender **5.2.2**(2026-09-14, 5.2 계열 LTS). 5.2.0은 2026-07-13, 5.2.1은 2026-08-24에 나왔고 4.5 LTS와 4.2 LTS도 함께 유지되고 있습니다([태그](https://github.com/blender/blender/tags)). 5.2 LTS는 2028년 7월까지 지원된다고 보도됐습니다([CG Channel](https://www.cgchannel.com/2026/07/blender-5-2-lts-is-here-discover-its-5-key-features/), 보완 조사).

### 3.1 색관리·노출

**뷰 변환 선택** — sRGB 디스플레이 뷰는 Standard, ACES 1.3, ACES 2.0, Khronos PBR Neutral, AgX, Filmic, Filmic Log, False Color, Raw입니다([config.ocio v5.2.2](https://raw.githubusercontent.com/blender/blender/v5.2.2/release/datafiles/colormanagement/config.ocio), [소스]).

| 용도 | View Transform | Look | 이유 |
|---|---|---|---|
| 포토리얼 씬(기본) | `AgX` | `AgX - Medium High Contrast` 또는 `AgX - Punchy` | 카메라에 가까운 하이라이트 롤오프. 고채도 광원이 흰색으로 자연스럽게 빠짐 |
| 제품·가구 색 일치(SKU 색, glTF·웹 뷰어와 맞추기) | `Khronos PBR Neutral` | `None` | base color 0.08~0.8 범위를 단위 흰색 조명에서 그대로 재현, 색상 이동 없음([Khronos](https://github.com/KhronosGroup/ToneMapping/tree/main/PBR_Neutral)) |
| HDR 납품, 파이프라인 표준 | `ACES 2.0` | — | Rec.2100-PQ에서 500/1000/2000/4000 nits HDR 뷰 제공 |
| 노출 판정(임시) | `False Color` | `None` | 2.5절 표 |
| 쓰지 않음 | `Standard` | — | 선형 1.0에서 바로 잘림 |

- **Look 이름은 접두사까지 정확히**: `'AgX - Punchy'`는 되지만 `'Punchy'`는 enum 오류입니다. 5.0.1의 AgX Look 목록은 `None`, `AgX - Punchy`, `AgX - Greyscale`, `AgX - Very High Contrast`, `AgX - High Contrast`, `AgX - Medium High Contrast`, `AgX - Base Contrast` 등입니다([실측]).
- **AgX와 Filmic의 범위**: "Filmic 25 stop, AgX 16.5 stop"이라는 비교는 오해입니다. config 설명문에 따르면 Filmic Log는 16.5 stop latitude와 25 stop dynamic range이고, AgX Log도 25 stop이며 같은 로그 범위(-12.47~+12.53 stop)를 씁니다. AgX가 Filmic보다 좁은 것이 아닙니다(검증 결과). AgX는 Filmic의 'Notorious Six'(고채도 색이 6개 색상으로 뭉개지는 문제)를 개선했고 Blender 4.0에서 새 씬 기본값이 됐습니다([EaryChow/AgX](https://github.com/EaryChow/AgX), [versioning_defaults.cc v4.0.0](https://raw.githubusercontent.com/blender/blender/v4.0.0/source/blender/blenloader/intern/versioning_defaults.cc)).
- **기본값 확인**: config.ocio 파일 자체의 `default_view_transform`은 Standard입니다. 새 씬이 AgX로 나오는 것은 씬 기본값 덕분입니다. 5.0.1에서는 `bpy.data.scenes.new()`로 만든 씬도 AgX였습니다([실측]). 그래도 에이전트는 렌더 전에 `view_transform`을 한 번 출력해 확인하세요.
- **색 정확도 비교**: scenario 스킬의 white furnace 측정 오차는 Khronos 3.8, AgX 27~42, Standard 33입니다[스킬].
- **HDR 뷰**: Rec.2100-PQ에는 ACES 1.3(1000/2000/4000 nits)과 ACES 2.0(500/1000/2000/4000 nits), Rec.2100-HLG에는 ACES 1.3/2.0 1000 nits만 있습니다. AgX HDR 뷰는 두 디스플레이 모두 1000 nits 하나입니다[소스].
- **작업 색공간(5.0+)**: 기본 Linear Rec.709이고 Linear Rec.2020, ACEScg를 고를 수 있습니다([5.0 색관리 릴리스 노트](https://developer.blender.org/docs/release_notes/5.0/color_management/), 보완 조사). bpy에서는 `bpy.data.colorspace.working_space`로 읽고, 바꿀 때는 `bpy.ops.wm.set_working_color_space`를 씁니다([실측] 5.0.1에 존재). 프로젝트 시작 때 한 번만 정하세요. 중간에 바꾸면 조명과 재질을 다시 맞춰야 합니다.
- **화이트 밸런스**: `view_settings.use_white_balance`, `white_balance_temperature`, `white_balance_tint`가 있습니다([실측]). 무드 조정은 알베도가 아니라 뷰·컴포지터에서 합니다.
- **밝기 조정은 `view_settings.exposure`로만**: 광량비(key:fill:rim)가 룩을 정합니다. 램프를 하나씩 스케일하면 비율이 깨지고 에이전트가 값을 오가며 진동합니다(scenario [스킬]). 노출 1 stop = 광량 2배입니다(Blender 매뉴얼, 보완 조사).

### 3.2 Cycles

**기본값**([properties.py v5.2.2](https://raw.githubusercontent.com/blender/blender/v5.2.2/intern/cycles/blender/addon/properties.py), [소스], 5.0.1 [실측]과 같음)

| 항목 | 기본값 | 판단 |
|---|---|---|
| samples / preview | 4096 / 1024 | 스틸은 adaptive로 충분히 멈춤 |
| adaptive sampling / threshold | 켜짐 / 0.01 | 프로덕션급. 유지 |
| max bounces | 12 (diffuse 4, glossy 4, transmission 12, volume 0, transparent 8) | 유리·액체·안개는 올려야 함(아래) |
| clamp indirect / direct | 10 / 0 | 파이어플라이가 있을 때만 낮춤 |
| caustics 반사·굴절 | 켜짐 | |
| denoiser | OIDN, 입력 Albedo+Normal, prefilter Accurate, quality High | 유지 |
| light tree | 켜짐 | 광원이 많은 장면에 유리 |
| path guiding | 꺼짐 | CPU 전용. 창으로 빛이 드는 실내에서 검토 |
| volume_biased | False | 기본은 null scattering(비편향, 아티팩트 적음, 노이즈 가능), True는 ray marching |
| pixel filter | Blackman-Harris 1.5 px | ([실측]) |

**장면 유형별 조정**

| 장면 | 조정 | 근거 |
|---|---|---|
| 테스트 → 파이널 | 테스트 약 100 samples → 파이널 500~1500(스틸은 4096 + adaptive 0.01 그대로 둬도 됨) | 스킬 문서 권장 |
| 창 하나로 빛이 드는 실내 | 창 크기 Area 라이트를 portal로(`light.cycles.is_portal = True`), 또는 Path Guiding(CPU). 약 250 samples + 디노이즈, 바운스 상향 | portal·guiding 속성 [실측]. 250 samples는 [ArchRender](https://www.archrender.ai/blog/interior-rendering-the-complete-guide-2026) (신뢰도 낮음) |
| 실용광(램프·전구)이 주광인 장면 | `max_bounces` ≥ 16, World 0.10~0.20, 작은 메시 전구 emission 800~3000 | [cc-blender-skill lighting](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-lighting/SKILL.md) [스킬] |
| 유리가 많음 | transmission ≥ 16 | 스킬 문서 권장 |
| 울퉁불퉁한 유리 | glossy 20~40(보통 30) | (미검증 주장) |
| 유색 액체·연기 | volume bounces 약 12 | (미검증 주장) |
| 겹친 안개 카드·알파 잎 | transparent 128까지 | (미검증 주장) |
| 겹친 판유리(창 여러 장) | Light Path의 ray depth가 10을 넘으면 Transparent로 전환(검은 구멍 방지), 추가 깊이마다 Fresnel × 0.1~0.2 | 검증 정정: "판유리 208 바운스 사례"는 렌즈 시뮬레이션 사례를 잘못 옮긴 것 |
| 파이어플라이 | clamp indirect 10 → 1~3, 또는 Filter Glossy | (미검증 주장). 0.2 같은 극단값은 쓰지 말 것 |
| 더 샤프하게 | pixel filter 1.5 → 약 1.15 | 단일 출처(신뢰도 낮음) |

**디노이저**: Cycles 기본은 Intel OIDN입니다. 최신은 v2.5.1(2026-08-18, 정수 오버플로 등 보안 수정), v2.5.0(2026-06-02, Intel XMX·AMX-FP16 성능, CUDA/HIP external semaphore, Apple M5 출력 손상 수정)입니다([OIDN releases](https://github.com/RenderKit/oidn/releases)). NVIDIA에서는 OptiX도 선택지입니다. main(5.3 alpha)에는 뷰포트 디노이저로 DLSS Ray Reconstruction이 들어갔지만 5.2.2에는 없습니다. 렌더 노이즈를 필름 그레인 대신 쓰지 마세요. 완전히 디노이즈한 뒤 그레인을 마지막에 따로 얹습니다.

**출력**: 측정·합성용 마스터는 OpenEXR(멀티레이어, half float, DWAA)로, 확인용은 PNG로 뽑습니다. PNG에는 뷰 변환이 구워집니다.
- **[실측] 5.0 함정**: 5.0.1에서는 `image_settings.file_format = 'OPEN_EXR_MULTILAYER'`가 enum 오류를 냅니다. `image_settings.media_type = 'MULTI_LAYER_IMAGE'`를 먼저 설정하면 `file_format`이 자동으로 OPEN_EXR_MULTILAYER가 됩니다. 4.2.23에는 `media_type`이 없고 `file_format`을 직접 지정합니다.

```python
im = bpy.context.scene.render.image_settings
if hasattr(im, 'media_type'):          # 5.0+
    im.media_type = 'MULTI_LAYER_IMAGE'
else:                                  # 4.x
    im.file_format = 'OPEN_EXR_MULTILAYER'
im.color_depth = '16'                  # half float
im.exr_codec = 'DWAA'
```

### 3.3 라이트

**새 라이트의 기본값**([DNA_light_types.h](https://raw.githubusercontent.com/blender/blender/main/source/blender/makesdna/DNA_light_types.h) [소스], 5.0.1 [실측])

| 속성 | 기본값 | 문제 | 규칙 |
|---|---|---|---|
| `energy` | 10 W | 대부분 장면에서 너무 어두움 | 거리 기반 공식으로 설정(아래) |
| Point/Spot `shadow_soft_size`(반경) | **0** | 칼같이 딱딱한 CG 그림자 | 0 금지. 실제 광원 크기 |
| Area `size` | 0.25 m | | 부드러움 = 크기 ÷ 거리 |
| Sun `angle` | 0.526° | 실제 태양 각지름(0.526~0.545°)과 같아 매우 선명 | 부드럽게는 2~5° |
| `temperature` / `use_temperature` | 6500 K / 꺼짐 | | 켈빈으로 지정 |
| Area `normalize` | 켜짐 | | 켜져 있으면 크기를 바꿔도 전체 광량 유지 |

- `use_temperature`를 켜면 `color`는 곱해지는 틴트가 됩니다. 켈빈만 쓰려면 `color = (1, 1, 1)`로 되돌리세요[소스]. 라이트 켈빈 속성은 5.0.1에는 있고 **4.2.23 LTS에는 없습니다**([실측]). 4.x에서는 라이트 노드에 Blackbody 노드를 연결합니다(Cycles 전용).
- 라이트 단위: Sun은 W/m²(방사 조도), Point·Spot·Area는 W(방사속)입니다. 전구 포장에 적힌 전기 W나 LED '등가 W'는 Blender W와 다릅니다([Blender 매뉴얼](https://docs.blender.org/manual/en/latest/render/lights/light_object.html), 보완 조사).

**색온도(켈빈)**

| 광원 | 켈빈 |
|---|---|
| 촛불 | 약 1500~1850 (arjun988: 1800) |
| 백열등 | 2000~2500 |
| 실용광(스탠드·펜던트) 기본 | 2700 |
| 텅스텐 | 3200 |
| 주광 / 흐린 날 | 5500 / 6500 |
| 푸른 시간대·달빛 | 약 8000 이상 |
| 네온, SF 광원(흑체 복사가 아닌 빛) | 켈빈 대신 RGB |

출처: [arjun988 lighting](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/lighting/SKILL.md)(1800/3200/5500/6500/8000K+, 원문 일치 확인), [cc-blender-skill lighting](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-lighting/SKILL.md). 야간 실내는 따뜻한 실용광(2700 K)에 차가운 하늘 필을 대비시키면 자연스럽습니다.

**실내 조도·색온도·노출 기준**(보완 조사, 조명 설계 자료)

| 상황 | 조도(lux) | EV100 = log2(lux / 2.5) | 권장 색온도 |
|---|---|---|---|
| 맑은 날 직사광 | 100,000~120,000 | 약 15 (100,000 → 15.3) | 5500 K 안팎 |
| 흐린 날 | 10,000~20,000 | 12.0~13.0 | 6500 K |
| 사무 책상 | 300~500 | 6.9~7.6 | 4000~6500 K |
| 주방 | 200~300 (조리대 300~500) | 6.3~6.9 | 3000~4000 K |
| 거실 | 150~200 (독서 300~500) | 5.9~6.3 | 2700~3000 K |
| 저녁 무드 조명 | 약 75 | 약 4.9 | 2400~2700 K |
| 달빛 | 약 0.1 | 약 -4.6 | 푸른 톤 |

- Kruithof 곡선에 따르면 조도가 낮을수록 따뜻한 색이 쾌적하게 느껴집니다(약 75 lx에서 2400~2700 K, 약 400 lx에서 3000~6000 K)([Kruithof curve](https://en.wikipedia.org/wiki/Kruithof_curve), [실내 조도 표](https://www.pranaair.com/blog/us/illuminance-levels-indoors-the-standard-lux-levels/)). 낮은 조도에 차가운 색을 쓰면 음산해 보입니다.

> **[한국 사용자]** 위 권장값은 해외 조명 설계 자료입니다. 한국 공간을 재현할 때는 실제 레퍼런스 사진의 색온도를 우선하세요.

**물리 스케일 vs 아티스틱 스케일 — 하나만 고르기**(보완 조사)

| 방식 | 태양 | 노출 | 메모 |
|---|---|---|---|
| 물리 스케일 | 약 1000 W/m² + Nishita 하늘 | Film/View exposure를 크게 낮춤 | 물리 값은 룩뎁에 지나치게 밝다는 커뮤니티 보고가 많음([Blendergrid](https://blendergrid.com/articles/cycles-physically-correct-brightness)) |
| 아티스틱 스케일 | 약 3~10 | 0 | 커뮤니티 관례(신뢰도 낮음) |

두 방식을 한 장면에 섞으면 에이전트가 조명을 추가할 때마다 밸런스가 깨집니다. hyperrealism 스킬의 'Filmic 시절 sun 100~130'은 구버전 값입니다.

**배치 기본값(키·필·림)**

| 역할 | 위치 | 크기 | 세기 | 근거 |
|---|---|---|---|---|
| Key | 카메라→피사체 축에서 **40°**, 위로 **35°**, 피사체 반경의 **3배** 거리 | 피사체 반경 | `100 × (거리/1.5)²` W | 위치·크기: scenario [스킬]. 세기 공식: cc-blender-skill [스킬] |
| Fill | 반대편, 낮게 | 키보다 크게 | 피사체에서 key:fill 약 3~4:1 | 8절 충돌 해결 |
| Rim | 뒤쪽, 위 | 작게 | 키의 약 0.2~0.5배(아래 재질별 표에서 환산) | cc-blender-skill [스킬] |
| 고정 좌표 레시피 | — | Key Area 1.0 m / Fill Area 2.0 m / Rim Spot 40° | Key 1000 W / Fill 300 W / Rim 600 W | cc-blender-skill [스킬] |

- 카메라 축에서 비추는 키(20° 미만)는 그림자가 프레임 밖으로 떨어져 형태감을 없앱니다. 3/4 키(좌 또는 우 30~45°, 위 35~45°) + 반대편 약한 바운스 + 뒤쪽 림이 기본형입니다.
- 광원 거리 = `max(피사체 크기 × 1.5, 1.0)` m 공식도 있습니다(cc-blender-skill). 피사체 크기에 비례해 거리와 에너지를 정하면 스케일이 달라도 결과가 일정합니다.
- 태양: 선명 0.5° ~ 부드러움 5°. Area: 선명 0.1 m ~ 부드러움 2.0 m(cc-blender-skill).

**재질 클래스별 key:fill:rim**([cc-blender-skill](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-lighting/SKILL.md), 원문 일치 확인)

| 금속 | 유리 | 나무 | 패브릭 | 피부 | 제품 |
|---|---|---|---|---|---|
| 4 : 1 : 2 | 3 : 1 : 1.2 (강한 림은 볼륨 틴트를 씻어냄) | 4 : 1 : 1.5 | 3 : 1 : 0.5 | 4 : 1 : 1 | 5 : 1 : 1.5 |

안경 같은 얇은 금속의 스펙큘러 플레어는 저자도 미해결로 남겼고, 탑다운 소프트박스나 크롭으로 우회합니다.

**코드: 색관리 + 켈빈 광원 배치 + 키 각도 검사** — [실측] 5.0.1·4.2.23에서 실행 확인. `subject`는 피사체 오브젝트, `scene.camera`가 있어야 합니다.

```python
import bpy, math
from mathutils import Vector, Matrix

scene = bpy.context.scene
vs = scene.view_settings
vs.view_transform = 'AgX'                    # 제품 색 정확도 우선이면 'Khronos PBR Neutral'
vs.look = 'AgX - Medium High Contrast'       # 'None', 'AgX - Punchy' 등. 'Punchy'만 쓰면 오류
vs.exposure = 0.0                            # 전체 밝기는 여기서만 조정(램프 비율 유지)

def world_bbox(obj):
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return mn, mx

def add_area_light(name, target_obj, cam_obj, az_deg, el_deg, dist_mult, size_mult,
                   kelvin, watts=None):
    """카메라→피사체 축 기준으로 방위각 az_deg, 앙각 el_deg에 Area 라이트를 둔다.
    거리 = 피사체 반경 x dist_mult, 크기 = 반경 x size_mult."""
    bpy.context.view_layer.update()         # 방금 옮긴 물체의 matrix_world 갱신(안 하면 옛 위치)
    mn, mx = world_bbox(target_obj)
    center, radius = (mn + mx) / 2, max((mx - mn).length / 2, 0.05)
    to_cam = cam_obj.matrix_world.translation - center
    to_cam.z = 0
    to_cam.normalize()
    h = Matrix.Rotation(math.radians(az_deg), 3, 'Z') @ to_cam
    d = (h * math.cos(math.radians(el_deg)) + Vector((0, 0, math.sin(math.radians(el_deg))))).normalized()
    dist = radius * dist_mult
    data = bpy.data.lights.get(name) or bpy.data.lights.new(name, 'AREA')
    data.shape, data.size = 'DISK', radius * size_mult     # 크기 0 금지: 크기가 그림자 부드러움
    if hasattr(data, 'use_temperature'):    # 5.0.1에는 있고 4.2.23 LTS에는 없음(실측)
        data.use_temperature, data.temperature = True, kelvin
        data.color = (1.0, 1.0, 1.0)        # 켈빈을 켜면 color는 곱해지는 틴트 → 흰색으로
    else:                                   # 4.x: Blackbody 노드(Cycles 전용, EEVEE는 무시)
        data.use_nodes = True
        nt = data.node_tree
        em = next(n for n in nt.nodes if n.type == 'EMISSION')
        bb = next((n for n in nt.nodes if n.type == 'BLACKBODY'), None) or nt.nodes.new('ShaderNodeBlackbody')
        bb.inputs['Temperature'].default_value = kelvin
        nt.links.new(bb.outputs['Color'], em.inputs['Color'])
    data.energy = watts if watts is not None else 100.0 * (dist / 1.5) ** 2   # cc-blender-skill 공식
    obj = bpy.data.objects.get(name) or bpy.data.objects.new(name, data)
    if obj.name not in scene.collection.objects:
        scene.collection.objects.link(obj)
    obj.location = center + d * dist
    obj.rotation_euler = (center - obj.location).to_track_quat('-Z', 'Y').to_euler()
    return obj

def key_angle_deg(cam_obj, light_obj, target_obj):
    """피사체에서 본 카메라 방향과 라이트 방향 사이 각도. 20° 미만이면 평평한 정면광."""
    bpy.context.view_layer.update()
    t = target_obj.matrix_world.translation
    a = (cam_obj.matrix_world.translation - t).normalized()
    b = (light_obj.matrix_world.translation - t).normalized()
    return math.degrees(a.angle(b))

subject, cam = bpy.data.objects['Hero'], scene.camera          # 'Hero'를 실제 피사체 이름으로
key = add_area_light('LGT_Key_Main', subject, cam, az_deg=40, el_deg=35, dist_mult=3, size_mult=1, kelvin=5600)
fill = add_area_light('LGT_Fill_Soft', subject, cam, az_deg=-60, el_deg=15, dist_mult=4, size_mult=2, kelvin=6500,
                      watts=key.data.energy / 3.5 * (4 / 3) ** 2)   # 거리 보정 후 key:fill ≈ 3.5:1
rim = add_area_light('LGT_Rim_Back', subject, cam, az_deg=160, el_deg=40, dist_mult=3, size_mult=0.5, kelvin=3200,
                     watts=key.data.energy * 0.4)                    # 림은 키의 0.2~0.5배(재질별 표)
print({o.name: round(o.data.energy, 1) for o in (key, fill, rim)},
      'key angle', round(key_angle_deg(cam, key, subject), 1))
```

- 테스트 장면(1 m 큐브)에서 키 에너지 300 W, 키 각도 41.5°가 나왔습니다([실측]). 이 값은 출발점일 뿐이고, 레퍼런스와 비교해 조정합니다.
- 필 에너지의 `(4 / 3) ** 2`는 필이 키보다 4/3배 멀리 있어서 넣은 역제곱 보정입니다(근사).

**"검정에서 시작하는 조명" 절차**
1. World 세기 0, 모든 램프 끄기.
2. HDRI(환경광·반사의 기반) → 키 → 실용광 → 고보 순으로 **하나씩** 켜고, 조정하는 램프 외에는 숨깁니다.
3. 광원마다 존재 이유를 적습니다("창 밖 하늘 6500 K, 크기 = 창"). 필을 쌓아 그림자를 없애는 것이 초보의 대표적인 티입니다. 그림자는 없애는 대상이 아니라 모양을 잡는 대상입니다.
4. 대안 조명 세트는 숨긴 컬렉션에 두고 A/B 비교합니다. 이름은 `LGT_Key_Main`, `LGT_Fill_Soft`, `LGT_Rim_Back`처럼 역할이 보이게 짓습니다([arjun988 lighting](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/lighting/SKILL.md)).

**HDRI**
- ahujasid MCP for Blender는 Poly Haven(CC0 HDRI·텍스처·모델)을 바로 불러옵니다. README는 해상도가 한 단계 오를 때마다 파일이 약 4배 커지므로 가까이 찍지 않는 에셋은 1k~2k로 받으라고 권합니다.
- HDRI strength 0.5~2.0([arjun988](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/lighting/SKILL.md) [스킬]). hyperrealism 스킬의 'HDRI strength ~1000'은 검증에서 구버전·오류 수치로 지적됐습니다.
- 배경으로 보이는 HDRI와 실제 조명 방향이 어긋나면 바로 가짜처럼 보입니다. 태양 방향과 HDRI의 해 위치를 맞추세요.

**Light Linking·Light Group**
- Light Linking은 **Object Properties > Shading > Light Linking**에 있습니다. 데이터는 Light 데이터블록이 아니라 라이트 **오브젝트**에 있습니다: `obj.light_linking.receiver_collection`, `obj.light_linking.blocker_collection`. 부모 패널의 호환 엔진에 `BLENDER_EEVEE`가 들어 있어 EEVEE에서도 씁니다([properties_object.py v5.2.2](https://raw.githubusercontent.com/blender/blender/v5.2.2/scripts/startup/bl_ui/properties_object.py) [소스], 5.0.1·4.2.23 [실측]).
- Light Group(렌더 패스)은 **Cycles 전용**입니다([cycles ui.py v5.2.2](https://raw.githubusercontent.com/blender/blender/v5.2.2/intern/cycles/blender/addon/ui.py)). `obj.lightgroup = 'key'`와 `view_layer.lightgroups.add(name='key')`로 광원을 역할별(key, fill, rim, window)로 나눠 EXR로 뽑으세요. 그러면 합성 단계에서 광량비를 다시 맞출 수 있어 전체 재렌더가 줄고, 역할별 기여도(예: World < 10%)도 수치로 확인할 수 있습니다(scenario [스킬]). EEVEE에서는 light linking이나 view layer로 대신합니다.

**고보·볼류메트릭** (미검증 주장 — [hyperrealism 01-lighting](https://raw.githubusercontent.com/Bartindigital/blender-hyperrealism-skill/main/references/01-lighting.md))
- 고보(쿠키): 광원 앞에 알파가 노이즈·컷아웃인 평면을 두고 광원에 parent합니다. 창살·나뭇잎·구름 그림자는 화면 밖 세계를 암시합니다. UE에서는 Light Function 머티리얼로 같은 효과를 냅니다.
- god ray는 World Volume이 아니라 볼륨 재질을 넣은 큐브로 만들고 밀도를 아주 낮게(약 0.2~0.3, 불빛 앰비언스 약 0.02) 둡니다. anisotropy 약 0.7. 빛줄기가 보이려면 딱딱한 가림막(창틀·고보)과 0이 아닌 광원 크기가 필요합니다.
- EEVEE 실내 헤이즈 밀도는 약 0.05(scenario [스킬]).

### 3.4 EEVEE

- **식별자**: 5.0+ `'BLENDER_EEVEE'`, 4.2~4.x `'BLENDER_EEVEE_NEXT'`[소스]. `scene.eevee.use_bloom`, `use_ssr`, `use_gtao`, `use_soft_shadows`는 RNA에 없어서 AttributeError가 납니다([rna_scene.cc](https://raw.githubusercontent.com/blender/blender/main/source/blender/makesrna/intern/rna_scene.cc), 5.0.1 [실측]). 인터넷의 구 튜토리얼과 일부 스킬(cc-blender-skill·arjun988의 rendering 스킬)이 아직 이 속성을 씁니다.
- **팩토리 기본값**(5.0.1 [실측]): 레이트레이싱 꺼짐, 레이트레이싱 해상도 1:2, Fast GI 해상도 1:2, Fast GI step 8, shadow rays 1, shadow steps 6.
- **파이널 설정**(scenario [스킬]) — [실측] 5.0.1·4.2.23에서 속성 설정 확인:

```python
v = bpy.app.version
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT' if (4, 2, 0) <= v < (5, 0, 0) else 'BLENDER_EEVEE'
e = scene.eevee
e.use_raytracing = True                         # 팩토리 기본은 꺼짐
e.ray_tracing_options.resolution_scale = '1'    # 1:1 (1/16 같은 저해상도 금지)
e.fast_gi_resolution = '2'                      # 1:2
e.fast_gi_step_count = 16
e.shadow_step_count = 12                        # 12~16
e.shadow_ray_count = 2
for L in bpy.data.lights:
    if L.type == 'AREA' or L.shadow_soft_size > 0:
        L.use_shadow_jitter = True              # 부드러운 광원의 그림자 품질
```

- 실내는 볼륨 프로브를 베이크합니다. Bloom은 컴포지터 Glare로 만듭니다(3.5).
- EEVEE는 SSS(표면하 산란), 굴절, 화면 밖 반사가 Cycles보다 약합니다. 피부·유리 히어로 샷은 Cycles를 쓰고, EEVEE로 반복 작업하더라도 **Cycles 레퍼런스 한 장**을 만들어 비교하세요. 레퍼런스가 없으면 에이전트가 EEVEE 아티팩트를 룩으로 오인합니다.
- 5.2 LTS는 인스턴스가 많은 CPU 병목 장면에서 EEVEE가 최대 2배 빨라졌습니다. 가구·소품이 많은 장면은 컬렉션 인스턴스로 구성하세요(보완 조사).

### 3.5 컴포지터·후처리

**5.x 컴포지터 구조**: `scene.node_tree`와 `scene.use_nodes` 대신 `scene.compositing_node_group`(노드 그룹)을 씁니다(5.0부터, [소스]). 5.0.1에는 **Composite 노드(`CompositorNodeComposite`)가 없고** 그룹 출력(`NodeGroupOutput`)으로 내보냅니다([실측]).

**Glare 노드**([node_composite_glare.cc v5.2.2](https://raw.githubusercontent.com/blender/blender/v5.2.2/source/blender/nodes/composite/nodes/node_composite_glare.cc) [소스], 5.0.1 [실측])

| 입력 소켓 | 기본값 | 범위·메모 |
|---|---|---|
| Type (메뉴) | **Streaks** | Bloom, Ghosts, Streaks, Fog Glow, Simple Star, Sun Beams, Kernel. bloom이 목적이면 반드시 `'Bloom'` 지정 |
| Quality (메뉴) | Medium | |
| Threshold | 1.0 | 이보다 밝은 픽셀만 번짐 |
| Smoothness | 0.1 | |
| Clamp / Maximum | 꺼짐 / 10.0 | 하이라이트 상한 |
| Strength | 1.0 | **0~1** |
| Saturation / Tint | 1.0 / 흰색 | |
| Size | 0.5 | **0~1** |
| Streaks | 4 | 1~16 |
| Iterations | 3 | 2~5 |
| Fade | 0.9 | 0.75~1 |

- 4.3 이하는 `glare_type`·`mix`(-1~1)·정수 `size`(6~9) **속성** 방식이었고(4.2.23 [실측]), 4.4부터 소켓 방식입니다. 그래서 튜토리얼과 hyperrealism 스킬의 "Fog Glow Size 8~9 두 겹을 mix -0.7로", "Ghost mix -0.96", "iterations 5~16"은 **5.x에서 입력할 수 없습니다**(검증에서 반박됨. 16은 Streaks 개수의 최대값).
- 원칙: 효과를 분명히 보이게 올렸다가, 의식되지 않을 때까지 내립니다. 컴포지팅을 끈 렌더(`render.use_compositing = False`)와 A/B 비교하세요.

**코드: 5.x Bloom** — [실측] 5.0.1에서 실행, bloom이 렌더 결과에 반영되는 것을 확인. 4.x에서는 동작하지 않습니다.

```python
import bpy
scene = bpy.context.scene

def add_bloom(strength=1.0, threshold=1.0, size=0.5):
    """Render Layers → Glare(Bloom) → Group Output. 5.0+ 전용."""
    assert bpy.app.version >= (5, 0, 0), '5.0+ 전용'
    ng = scene.compositing_node_group
    if ng is None:
        ng = bpy.data.node_groups.new('COMP_Main', 'CompositorNodeTree')
        scene.compositing_node_group = ng
    if not any(i.in_out == 'OUTPUT' for i in ng.interface.items_tree if i.item_type == 'SOCKET'):
        ng.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')
    nodes, links = ng.nodes, ng.links
    # 한국어 UI에서도 안전하게: 이름이 아니라 bl_idname으로 찾는다
    rl = next((n for n in nodes if n.bl_idname == 'CompositorNodeRLayers'), None) or nodes.new('CompositorNodeRLayers')
    out = next((n for n in nodes if n.bl_idname == 'NodeGroupOutput'), None) or nodes.new('NodeGroupOutput')
    glare = next((n for n in nodes if n.bl_idname == 'CompositorNodeGlare'), None) or nodes.new('CompositorNodeGlare')
    glare.inputs['Type'].default_value = 'Bloom'        # 기본값은 'Streaks'
    glare.inputs['Threshold'].default_value = threshold
    glare.inputs['Strength'].default_value = strength   # 0~1. 분명히 보이게 → 의식되지 않을 때까지 낮춤
    glare.inputs['Size'].default_value = size           # 0~1 (4.3 이하의 정수 Size 6~9 아님)
    links.new(rl.outputs['Image'], glare.inputs['Image'])
    links.new(glare.outputs['Image'], out.inputs[0])
    return glare
```

**후처리 순서와 절제** (미검증 주장 — [hyperrealism 07-post-compositing](https://raw.githubusercontent.com/Bartindigital/blender-hyperrealism-skill/main/references/07-post-compositing.md). 순서는 참고하되 수치는 레퍼런스로 확인)

1. 디노이즈(Albedo+Normal)
2. AO 패스(Distance 0.2 m)를 0.3~0.5로 multiply
3. 색 보정은 CDL(Offset/Power/Slope). Lift/Gamma/Gain은 쓰지 않음
4. Glare
5. 색수차(CA) dispersion 0.004~0.02 — 이보다 크면 과함
6. 아주 약한 lens distortion → 흐린 타원 비네트 → soften 0.05~0.2
7. 마지막에 실제 필름 그레인(스캔이나 노이즈 텍스처를 Overlay/Linear Light로). 5.x에서 그레인 전용 노드는 확인되지 않았습니다
- Mist는 start 약 5 m, depth 약 80 m.
- scene-referred(선형) 픽셀에 display-referred 블렌드 모드(Multiply, Screen, Overlay 등)를 쓰면 색이 망가집니다.
- 과한 CA·글로우·왜곡은 그 자체가 가짜의 신호입니다.

---

## 4. Unreal Engine (5.7 / 5.8)

> 이 장의 약어: **PPV** = Post Process Volume(후처리 볼륨), **MRQ** = Movie Render Queue, **HWRT** = Hardware Ray Tracing, **VSM** = Virtual Shadow Maps, **SMRT** = Shadow Map Ray Tracing(VSM의 부드러운 그림자 샘플링), **EV100** = ISO 100 기준 노출값, **NNE/NFOR** = Path Tracer 디노이저 종류.

### 4.1 버전 상태

| 기능 | UE 5.7 (2025-11) | UE 5.8 (2026-06-17, 보도 기준·Epic 원문 미확인) |
|---|---|---|
| MegaLights | Beta [UE 미러] | Production-Ready (보완 조사) |
| Substrate 머티리얼 | Production-Ready, 새 프로젝트 기본 활성 [UE 미러] | — |
| PCG Framework | Production-Ready | — |
| Nanite Foliage & Skinning | Experimental | — |
| Heterogeneous Volumes / SMAA | Beta / Experimental | — |
| Lumen Lite (Irradiance Field 기반 중간 품질 GI) | — | 신규. Lumen High Quality보다 약 2배 빠름, Switch 2에서 60fps(보완 조사) |
| 공식 MCP 플러그인 | — | Experimental(`ModelContextProtocol`, 기본 `http://127.0.0.1:8000/mcp`, 인증 없음, AllToolsets 필요). 자세한 설정은 [기타 MCP 가이드](03_other_mcp_dcc_cad_engines.md) |

출처: [UE 5.7 릴리스 노트 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/unreal-engine-5-7-release-notes.md), [UE 5.8 발표](https://www.unrealengine.com/news/unreal-engine-5-8-is-now-available), [Guru3D](https://www.guru3d.com/story/unreal-engine-58-debuts-lumen-lite-and-productionready-megalights/). 이 문서의 UE 세부 내용은 5.7 문서 미러 기준이라 5.8 변경분은 반영되지 않았을 수 있습니다.

### 4.2 Lumen (GI·반사)

[Lumen GI & Reflections](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine.md), [Lumen Technical Details](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/lumen-technical-details-in-unreal-engine.md) [UE 미러]

| 규칙 | 값·설정 | 이유 |
|---|---|---|
| 라이트 mobility | **Static만 미지원**. Stationary·Movable은 반영 | 커뮤니티 스킬(ibrews/ue5-mcp)의 "Static·Stationary는 Lumen GI 기여 0"은 Epic 문서와 모순(검증에서 반박). 에이전트가 만든 라이트를 Movable로 두는 관행 자체는 무해 |
| Nanite + Stationary | Movable 또는 VSM 권장 | VSM 문서 |
| 벽 두께 | **10 cm 이상** (Software RT, Distance Field 문맥) | 누광 방지 |
| 메시 구성 | 벽·바닥·천장을 분리된 모듈 메시로, 얇은 단면 메시 피하기 | 메시 카드·Distance Field 품질 |
| 작은 발광체 | **Emissive Light Source** 켜기 | 작은 오브젝트는 Lumen Scene에서 컬링됨 |
| 반사 최고 품질 | HWRT + **Hit Lighting for Reflections** | |
| 반사 바운스 | 기본 1 → PPV에서 최대 8, `r.Lumen.Reflections.MaxBounces`로 64까지(HWRT Hit Lighting 필요) | 거울·크롬이 서로 비치는 실내·제품 샷에서 반사 속 검은 영역 제거 |
| Lumen Scene View Distance | 기본 200 m, 최대 800 m | |
| 누광이 보일 때 | Max Trace Distance 조정, `r.Lumen.Visualize.CardPlacement 1`로 카드 점검 | |
| HWRT 비용 | 인스턴스 10만 개를 넘으면 씬 업데이트 비용이 큼 | |
| 스케일러빌리티 | Cinematic = MRQ용, Epic = 30fps(1080p에서 8 ms), High = 60fps(4 ms), Medium 이하 = Lumen 비활성 | |
| 품질 레버 | Final Gather Quality 게임 1.0~1.5 / 시네마틱 2.0~4.0, Lumen Scene Detail 1~2, 조명 전파가 느리면 Lighting Update Speed 상향 | 보완 조사([Lumen Performance Guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-performance-guide-for-unreal-engine), [실무 블로그](https://bitsoulhosting.com/marketplace/blog/ue5-lumen-gi-settings-asset-prep-performance-2026)). Scene Detail은 신뢰도 낮음 |

- 룩뎁은 Final Gather Quality 2~4로 기준 이미지를 만들고, 게임 빌드 값(1~1.5)과 비교합니다.
- 한계: 작고 밝은 발광 영역에서 노이즈가 생기고, 클리어코트는 상단 레이어만 낮은 roughness를 지원합니다.

### 4.3 MegaLights

[MegaLights 문서 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/megalights-in-unreal-engine.md) [UE 미러]

- 용도: 램프·네온·촛불 같은 실용광이 많은 AAA 실내·야경. 기존 섀도잉 라이트는 개수 제한 때문에 조명을 줄이거나 그림자를 끄게 되고, 이것이 싼 CG 느낌을 만듭니다.
- 켜기: Project Settings > Rendering > Direct Lighting > MegaLights + Support Hardware Ray Tracing. 라이트별 `Allow MegaLights`, 볼륨별로 PPV에서 제어.
- 최고 품질: `r.MegaLights.DownsampleMode 0`, `r.MegaLights.NumSamplesPerPixel 16`(5.7에서 downsample factor와 checkerboard CVar가 `DownsampleMode`로 합쳐짐). Directional은 기본 꺼짐 → `r.MegaLights.DirectionalLights 1`.
- 라이트 바운드를 좁게 잡아 광원이 지오메트리 안에 들어가지 않게 하고, 파티클 라이트는 작고 드물게 씁니다.
- 미지원: Forward 렌더러, 모바일, Switch, PS4/XB1, 구름 그림자. 조사 원자료에는 SSS 두께 추정, 물, 이종 볼륨도 미지원으로 적혀 있습니다.

### 4.4 Virtual Shadow Maps

[VSM 문서 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/virtual-shadow-maps-in-unreal-engine.md) [UE 미러]

| 항목 | 값 |
|---|---|
| 구조 | 16k × 16k 가상 해상도를 128 × 128 페이지 단위로 필요한 곳만 렌더. Directional은 clipmap으로 카메라 기준 64 cm~약 40 km |
| 전제 | Nanite 사용 전제, DX12 또는 Vulkan |
| 로컬 라이트 Source Radius | **기본 0 → 칼같이 딱딱한 그림자**. 실제 광원 크기로 올림 |
| Directional Source Angle | 실제 태양 크기로 |
| SMRT 품질 | `r.Shadow.Virtual.SMRT.RayCountLocal/Directional` (Epic 스케일러빌리티에서 기본 8 rays), `SamplesPerRay` 4~8 권장 |
| 로우폴리 아티팩트 | `r.Shadow.Virtual.NormalBias`(기본 0.5)를 올림 |

### 4.5 Substrate 머티리얼

[Substrate 개요 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/overview-of-substrate-materials-in-unreal-engine.md) [UE 미러]

- 고정 shading model 대신 slab(Interface: roughness·normal·F0/F90, Medium: MFP·albedo)을 쌓는 방식입니다. 수직 레이어링(코팅, 카페인트, 젖은 표면, 먼지 앉은 클리어코트), 수평 블렌딩, Thin-Film, Fuzz(직물), SSS를 지원합니다.
- **GBuffer 선택이 중요**: 새 프로젝트 기본은 **Blendable**(저비용)이라 다층 재질이 단일 closure로 단순화됩니다. AAA급 다층 재질이 목적이면 **Adaptive**(고품질, 쿡 시간 약 15% 증가)로 바꿉니다. Automotive·Arch 템플릿은 Adaptive가 기본입니다.
- 기존 프로젝트는 Project Settings > Rendering > Substrate materials에서 opt-in.
- 표기 충돌: 5.7 릴리스 노트는 Production-Ready, 같은 문서 제한사항 절에는 여전히 'Beta'와 'Beta support for Path Tracer'가 남아 있습니다. Path Tracer로 다층 Substrate를 렌더할 때는 결과를 확인하세요. slab 수에 비례해 비용이 늘어납니다.

### 4.6 노출·광량 단위·Bloom

| 항목 | 규칙 | 근거 |
|---|---|---|
| 광량 단위 | Directional = lux, Sky Light·Emissive = cd/m², Point/Spot/Rect = Candela·Lumen·Unitless 중 선택. 1 cd = 625 unitless. 노출은 EV100(ISO 100) | [Physical Lighting Units 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/using-physical-lighting-units-in-unreal-engine.md) |
| 태양 | 약 100,000~120,000 lux, EV100 약 14~15 | [UE 4.27 문서](https://docs.unrealengine.com/4.27/en-US/BuildingWorlds/LightingAndShadows/PhysicalLightUnits), 보완 조사 |
| 룩뎁 중 노출 | 자동노출 끄기: Metering Mode Manual(또는 Min EV100 = Max EV100) + **Apply Physical Camera Exposure**. 실내 EV100 약 5~7, 주광 14~15 | 자동노출이 켜져 있으면 조명·재질 변경 효과가 상쇄돼 스크린샷 비교가 무의미해짐(보완 조사) |
| 라이트를 놓자 화면이 하얘짐 | Auto Exposure Max EV100과 Histogram Max EV100을 올림 | [UE 문서](https://dev.epicgames.com/documentation/unreal-engine/using-physical-lighting-units-in-unreal-engine?lang=en-US), 보완 조사 |
| 역광·창가처럼 다이내믹 레인지가 큰 장면 | Local Exposure | [Auto Exposure 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/auto-exposure-in-unreal-engine.md) |
| Bloom 발생 조건 | PPV **Threshold**가 결정. -1이면 모든 색이 bloom에 기여. "emissive 1.0 초과면 bloom"은 노출·threshold에 따라 달라지는 경험칙이지 엔진 규칙이 아님 | [Bloom 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/bloom-in-unreal-engine.md), 검증에서 반박 |
| 시네마틱 bloom | Convolution bloom | [Post Process 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/post-process-effects-in-unreal-engine.md) |

물리 스케일과 임의 값(태양 3~10 같은)을 섞지 마세요. 섞으면 노출·bloom·자동노출이 예측 불가능해지고, 에이전트가 조명을 추가할 때마다 밸런스가 깨집니다.

### 4.7 Path Tracer + Movie Render Queue (파이널)

[Path Tracer 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/path-tracer-in-unreal-engine.md), [Cinematic Rendering Image Quality 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/cinematic-rendering-image-quality-settings-in-unreal-engine.md) [UE 미러]

- 켜는 순서: DX12 → Support Hardware Ray Tracing → Path Tracing → Support Compute Skin Cache. Windows와 RTX/DXR GPU가 필요합니다.
- PPV 설정: Max Bounces, Samples Per Pixel, Max Path Intensity(파이어플라이 클램프), Reference DOF, Reference Atmosphere, Denoiser(기본 NNE — OIDN과 같은 네트워크를 GPU에서 실행). 애니메이션은 시간 안정성이 있는 **NFOR** 디노이저.
- **알베도**: diffuse Base Color를 **0.8 미만**으로 유지하라는 권고가 있습니다. albedo가 1.0에 가까운 재질은 렌더 시간이 크게 늘어납니다. (Blender 쪽 scenario 감사 기준 sRGB 30~243과 함께 알베도 게이트로 쓰세요.)
- HDRIBackdrop은 조명을 이중으로 계산합니다.
- MRQ: TAA를 켠 상태에서 **Spatial Count × Temporal Count(곱)**이 8을 넘으면 Override Anti-Aliasing을 None으로 하거나 `r.TemporalAASamples`(기본 8)를 곱한 값에 맞춥니다(검증 정정: '합'이 아니라 '곱').
- 용도: 마케팅 스틸·룩 레퍼런스. 실시간(Lumen) 결과가 Path Tracer 레퍼런스와 얼마나 가까운지 비교하는 기준으로도 씁니다.
- Cine Camera: Focus Method Tracking, 조리개 날 4~16(스킬 문서 기준).

### 4.8 UE PPV 치트시트 (에이전트 기본값)

| 설정 | 룩뎁·시네마틱 | 게임 빌드 |
|---|---|---|
| Exposure | Manual + Apply Physical Camera Exposure, EV100 고정(실내 5~7 / 주광 14~15) | 필요하면 Auto(범위 제한) |
| Lumen Final Gather Quality | 2.0~4.0 | 1.0~1.5 |
| Lumen Reflections | Hit Lighting(HWRT), Max Reflection Bounces 필요한 만큼(최대 8) | 기본 |
| Bloom | Convolution, Threshold로 조절 | Standard |
| Local Exposure | 창가·역광 장면 | 동일 |
| Path Tracer | Reference DOF·Atmosphere 켬, 스틸 NNE / 애니메이션 NFOR | — |

### 4.9 MCP로 UE를 다룰 때

- Epic 공식 [Unreal Engine Skills for Claude Code](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin)(MIT, 약 308 stars): 기본적으로 `list_toolsets`, `describe_toolset`, `call_tool` 세 메타 도구만 노출되고, **AllToolsets 플러그인을 켜지 않으면 도구가 0개**입니다. README에 조명·포스트프로세스·렌더 전용 도구가 명시돼 있지 않아 렌더 품질 작업은 Python이나 콘솔 명령으로 우회해야 할 수 있습니다. [스킬 지침](https://raw.githubusercontent.com/EpicGames/unreal-engine-skills-for-claude-code-plugin/main/skills/unreal-mcp/SKILL.md): 일괄 변경 전 저장(MCP 편집은 항상 undo되지 않음), 의존 호출은 순차로, 도구가 실패해도 예외를 던지지 않는 경우가 많으니 결과를 매번 검증.
- 필요한 UE 버전은 Epic README·[setup.md](https://raw.githubusercontent.com/EpicGames/unreal-engine-skills-for-claude-code-plugin/main/skills/unreal-mcp/references/setup.md)에 적혀 있지 않고, '5.8+'는 커뮤니티 자료(VibeUE, ue-mcp) 근거입니다.
- 공식 MCP 서버는 인증이 없으므로 로컬 전용으로 두고(포트 8000 외부 차단), 배치·조명·머티리얼 변경마다 소스 컨트롤 체크포인트를 만드세요(보완 조사).
- 문서 조회: [ue5-docs-mcp](https://github.com/CharlieCardenasToledo/ue5-docs-mcp)는 UE 5.7 문서 3,444쪽을 `search_docs`·`get_doc`·`list_sections`로 검색하게 해 줘서 에이전트가 cvar·PPV 속성 이름을 추측하지 않게 합니다. 단 **도구 코드만 MIT이고 문서 본문은 Epic IP이며 개인·교육 목적 오프라인 접근으로 한정**됩니다. 비공식 미러라 변환 누락이 있고 5.8 변경분은 없습니다.
- [ibrews/ue5-mcp](https://github.com/ibrews/ue5-mcp)는 크래시 패턴·API 함정 참고용으로만 쓰세요. Lumen mobility와 'MovieRenderGraph는 5.8 전용'(5.7 릴리스 노트에 MRG 개선이 있음) 주장이 틀렸습니다.

---

## 5. 카메라

### 5.1 초점거리·높이·수직선

| 샷 | 초점거리(풀프레임 36 mm 센서) | 근거 |
|---|---|---|
| 실내 전체 | 24~35 mm (18 mm 이하 과장 광각 피하기) | [ArchRender](https://www.archrender.ai/blog/interior-rendering-the-complete-guide-2026)·[RenderInfinity](https://renderinfinity.com/blog/rendering-for-interior-design-focal-length/)(보완 조사), hyperrealism 스킬과 일치 |
| 워크스루 | 약 20 mm | (미검증 주장) |
| 풍경 establishing | 약 30 mm | (미검증 주장) |
| 사람 눈과 비슷한 화각 | 약 35 mm | (미검증 주장) |
| 와이드 | 18~28 mm | [arjun988 camera](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/camera-cinematography/SKILL.md) [스킬] |
| 스토리·제품 전체 형태 | 35~50 mm | arjun988 [스킬] |
| 디테일 컷 | 50~85 mm | 보완 조사 |
| 제품·가구 히어로(압축) | 80~100 mm | (미검증 주장) |
| 인물·히어로 | 85~135 mm | arjun988 [스킬] |

- **기본 50 mm 그대로 금지**: bpy로 만든 카메라의 기본값은 50 mm, 센서 36 mm, DOF 꺼짐, f/2.8, 조리개 날 0(완전한 원), 초점 거리 10 m입니다([실측] 5.0.1). 모든 샷이 50 mm인 것은 AI 결과물의 흔한 특징입니다.
- **높이**: 사람 눈높이 1.6~1.7 m([arjun988](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/camera-cinematography/SKILL.md) [스킬]). 가구 전체를 보여 주는 인테리어 컷은 1.2~1.6 m를 쓰기도 합니다(관례값, 신뢰도 낮음). 레퍼런스 사진의 카메라 높이를 따르세요.
- **수직선**: 건축·인테리어는 카메라 pitch를 수평(`rotation_euler.x = 90°`)으로 두고, 상하 프레이밍은 `shift_y`(예: 0.1~0.2, 관례값)로 합니다. 카메라를 기울이면 수직선이 모여 아마추어처럼 보입니다([arjun988 archviz](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/archviz/SKILL.md), 보완 조사).

### 5.2 조리개·DOF·모션블러

- **f-stop**(미검증 주장 — Blender Guru 인용, [hyperrealism 05-camera-optics](https://raw.githubusercontent.com/Bartindigital/blender-hyperrealism-skill/main/references/05-camera-optics.md)): 일반 f/5.6, 인물 f/3~5.6, 거리 f/11, 풍경 f/22 이상.
- **DOF는 없어도, 과해도 안 됩니다.** 없으면 물리적으로 불가능하게 선명하고, 과하면 미니어처(틸트시프트)처럼 보입니다. DOF가 미니어처처럼 보이면 f-stop보다 먼저 **장면 스케일**을 의심하세요.
- 조리개 날 6~8(5날이면 오각형 보케). 초점은 거리값 대신 Empty를 대상으로 잡습니다(물체를 옮겨도 초점 유지).
- 움직이는 것이 있으면 모션블러를 켜고, 셔터는 0.5프레임(180° 규칙).

### 5.3 구도

- 후보 앵글을 여러 개(hyperrealism 스킬은 6~7개) 렌더해 contact sheet로 비교한 뒤 하나를 고정하고, 그다음 조명과 디테일을 작업합니다.
- 삼분할(카메라 guide overlay), 전경·중경·배경 레이어, 헤드룸·리드룸, 프레임 가장자리에서 형태가 맞닿는 탄젠트 피하기, 수평선 수평([arjun988 camera](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/camera-cinematography/SKILL.md)).
- 문·아치·그림자로 프레임 안의 프레임을 만들어 깊이와 초점을 줍니다([80.lv Get Away](https://80.lv/articles/get-away-lighting-composition-in-environment-art), [Level Design Book](https://book.leveldesignbook.com/process/env-art), 보완 조사).

**코드: 물리 카메라** — [실측] 5.0.1·4.2.23에서 속성 설정 확인

```python
import bpy, math
scene = bpy.context.scene
cam = scene.camera
cam.data.lens = 35                              # 실내 24~35, 제품·가구 클로즈업 50~100
cam.data.sensor_width = 36                      # 풀프레임 기준(기본값)
focus = bpy.data.objects.get('CAM_Focus') or bpy.data.objects.new('CAM_Focus', None)
if focus.name not in scene.collection.objects:
    scene.collection.objects.link(focus)
focus.location = bpy.data.objects['Hero'].location     # 'Hero'를 실제 피사체 이름으로
cam.data.dof.use_dof = True                     # 기본은 꺼짐
cam.data.dof.focus_object = focus               # 거리값 대신 Empty에 초점
cam.data.dof.aperture_fstop = 5.6               # 기본 2.8
cam.data.dof.aperture_blades = 7                # 기본 0(완전한 원). 5날은 오각형 보케
cam.location.z = 1.6                            # 눈높이 1.6~1.7 m
cam.rotation_euler.x = math.radians(90)         # 수평 유지(건축): 수직선이 기울지 않음
cam.data.shift_y = 0.1                          # 상하 프레이밍은 shift로
scene.render.use_motion_blur = True             # 움직임이 있을 때만
scene.render.motion_blur_shutter = 0.5          # 180° 셔터
```

---

## 6. 아트디렉션

### 6.1 레퍼런스 보드와 프리프로덕션

- 착수 전에 스코프, 무드, 계절, 팔레트, **복제할 특징 목록**을 먼저 씁니다. 레퍼런스 없이 기억으로 작업하는 것이 가짜 느낌의 근본 원인입니다. 광원이 하나인 레퍼런스 사진이 따라 하기 쉽습니다.
- PureRef 보드를 만들고 Street View로 실제 장소를 조사합니다. 색 체계: 보색(긴장, 가장 많이 씀), 유사색(자연스러운 사실감), 단색(조화). 매 단계 레퍼런스와 비교하고, 어긋나면 앞 단계로 돌아갑니다(미검증 주장 — [hyperrealism 08-composition-workflow](https://raw.githubusercontent.com/Bartindigital/blender-hyperrealism-skill/main/references/08-composition-workflow.md)).
- 에이전트에게는 레퍼런스 이미지를 함께 주고, "레퍼런스와 다른 점 3가지"를 먼저 말하게 한 뒤 수정하게 하면 판정이 구체적이 됩니다.

### 6.2 시선: 히어로 하나, attention budget

- 한 뷰에 히어로 요소 **하나**. 디테일은 시선이 머무는 곳에만 쓰고, 디테일 클러스터 사이에 쉬는 공간과 넓은 그림자를 남깁니다. 모든 곳을 밝게 비추면 모델이 버티지 못할 정밀 검사를 부릅니다([arjun988 environment-artist](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/environment-artist/SKILL.md)).
- 값 구조(명암 덩어리)로 시선을 유도합니다. 흑백으로 봐도 읽히는지, 눈을 가늘게 떴을 때(squint test) 히어로가 먼저 보이는지 확인합니다. 로우키와 하이키 중 하나를 고릅니다. 측정 게이트는 `value_range` ≥ 0.30(scenario).
- 블록아웃 단계부터 그레이스케일 명도 렌더로 가독성을 확인하고, 중간 패스에서 다듬고, 최종 패스에서 무드와 포스트를 확정합니다(보완 조사).

### 6.3 레이어와 리딩 라인

- 전경·중경·배경을 모두 둡니다. 배경은 실루엣만 남겨도 됩니다.
- 리딩 라인(길, 난간, 테이블 모서리)이 히어로로 향하게 합니다.

### 6.4 스토리와 세트 드레싱

- **서사를 먼저 정하고** 소품을 클러스터 단위로 둡니다. 스토리 비트(식다 만 식사, 쓰던 작업대, 급히 떠난 흔적)마다 **소품 3~7개 + 마모·데칼 1~2개**([arjun988 set-dressing](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/set-dressing/SKILL.md) [스킬]).
- 순서: 레이아웃 고정 → 히어로 서사 소품 → 보조 클러스터 → 배경 필러 → 데칼 → 조명 확인 → QA.
- 반복 인스턴스에는 회전·스케일 지터를 줍니다. 축 정렬·등간격·모든 면을 채우는 '균일한 잡동사니 벽지'는 AI 배치의 전형입니다.
- 통제된 비대칭: 예를 들어 의자를 테이블과 평행하지 않게 5~15° 틀어 둡니다(관례값, 신뢰도 낮음). 구체적인 배치 규칙과 검사 코드는 [배치·레이아웃 가이드](08_scene_layout_placement.md)와 [placement_utils.py](../03_playbooks/scripts/README.md)에 있습니다.
- **AAA 환경 제작 순서**(80.lv 브레이크다운 요약, 보완 조사): 블록아웃 → 모듈러 키트 → 트림 시트 → 버텍스 페인트와 RGBA 마스크 변주 → 데칼 → 스토리 소품 → 라이팅·포스트. 한 번에 완성본을 만들면 반복과 균일함이 남습니다. 모듈러 반복을 깨는 핵심은 마감 패스(데칼·버텍스 페인트)입니다([80.lv 모듈러 씬](https://80.lv/articles/001agt-004adk-005cg-modular-scene-in-ue4-blockout-vertex-paint-decals)). AI 파이프라인도 이 단계를 분리해서 실행하세요.
- 텍셀 밀도는 장면 전체에서 통일합니다(배경 512 px/m, 플레이 공간 1024 px/m, 히어로·1인칭 2048 px/m, [polycount](https://polycount.com/discussion/234887/texel-density-standards-for-aaa-first-person-shooter-games), 보완 조사). 자세한 내용은 [텍스처링 가이드](05_texturing_materials.md).

### 6.5 스케일 단서

스케일이 틀리면 DOF, 광량 감쇠, SSS, 텍스처 밀도가 모두 틀어지고 재질·조명으로는 고칠 수 없습니다.

| 단서 | 값 | 비고 |
|---|---|---|
| 인물 더미 | 1.8 m | |
| 눈높이 | 1.6~1.7 m | |
| 문 높이 | 2.03~2.13 m (또는 2.1 × 0.9 m) | 80·84인치 미국 규격과 같음 → **[한국 사용자]** 한국 문 규격은 [실측 치수 기준표](../03_playbooks/05_reference_dimensions.md) |
| 천장 높이 | 2.4~3.5 m | 한국 주거 천장고도 05 문서 참고 |
| 창틀(창대) 높이 | 0.9 m | |
| 벽돌 | 0.065 × 0.215 m | |

출처: [arjun988 realistic-style](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/realistic-style/SKILL.md), [arjun988 environment-artist](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/environment-artist/SKILL.md) [스킬]. 트랜스폼(스케일)을 먼저 적용해야 베벨이 균일하게 들어갑니다. 치수 오류는 [scene_audit.py](../03_playbooks/scripts/README.md)로 자동 검사하세요.

### 6.6 색·값 금지 규칙

- **순흑(0)·순백(255)·채도 100% 픽셀 금지**(의도한 발광체와 의도한 검은 배경 제외). `review_render()`의 `pure_black_pct`, `clip_pct`, `sat100_pct`로 확인합니다.
- **알베도 범위**: 유전체 sRGB 30~240(scenario 감사 기준 30~243, 벗어나는 비율 2% 미만), 금속 180 이상([scenario texturing-shading](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-texturing-shading/SKILL.md) [스킬]). UE Path Tracer 문서는 diffuse Base Color 0.8 미만을 권합니다. 실세계 반사율 참고치(미검증 주장): 석탄 약 0.04, 아스팔트 0.05~0.12, 풀 0.15~0.25, 콘크리트 0.25~0.4, 눈 약 0.8.
- metallic은 0 또는 1, 유전체 specular 0.5(IOR 1.5). 중간 metallic값은 에너지적으로 불가능한 표면이라 플라스틱처럼 보입니다.
- 명암과 무드는 알베도가 아니라 조명과 뷰·컴포지터에서 만듭니다. 알베도로 무드를 내면 PBR 일관성이 깨지고 에셋을 재사용할 수 없습니다.

### 6.7 에셋 전략과 생성형 메시

- 배경 에셋은 라이브러리에서 쓰고, 히어로 에셋만 직접 만들거나 크게 커스터마이즈합니다. 흔한 것을 직접 만드는 것은 가치가 적고, 라이브러리만 쓰면 짜깁기처럼 보입니다. 에이전트의 모델링 한계를 우회하는 현실적인 전략이기도 합니다. 에셋 출처와 라이선스는 [에셋·라이선스 가이드](10_assets_pipeline_licensing.md)를 보세요.
- **생성형 3D 메시는 구워진 조명을 의심하세요.** RGB 텍스처에 음영·하이라이트가 구워져 있으면 새 조명 아래에서 광원 방향이 두 개인 것처럼 보입니다. 수입 게이트: HDRI를 0°/90°/180° 돌려 렌더해서 음영이 따라 움직이는지 확인하고, PBR 채널(albedo·roughness·metallic·normal)이 있는지, albedo가 범위 안인지 봅니다. 통과하지 못하면 de-light, PBR 재질 교체, 재텍스처링을 합니다([Tripo 블로그](https://www.tripo3d.ai/blog/why-ai-3d-models-look-bad), 벤더 자료·보완 조사). 생성 모델 선택은 [AI 3D 생성 가이드](04_ai_3d_generation.md)에 있습니다.

> **[한국 사용자]** Hunyuan3D 2.1은 이 문제 때문에 RGB 텍스처에서 PBR 파이프라인으로 옮겼다고 설명하지만, [라이선스](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE) 첫 줄이 "THIS LICENSE AGREEMENT DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA"이고 적용 지역 밖에서의 사용과 **출력물 사용**을 허가하지 않습니다. Hunyuan3D 계열 오픈웨이트(2.0/2.1/Omni/Part 등)를 한국에서 로컬로 쓰는 것은 라이선스 범위 밖입니다. MCP for Blender의 Hunyuan3D 연동도 마찬가지로 확인하세요.

---

## 7. 가짜처럼 보이는 원인 12가지와 처방

비전 모델에게 렌더 후 셀프 리뷰 항목으로 그대로 주세요. 여러 실무자가 합의한 CG의 티를 정리한 것입니다.

| # | 원인 | 렌더에서 보이는 증상 | 처방(수치) | 확인 방법 |
|---|---|---|---|---|
| 1 | Standard 뷰 변환·노출 관리 실패 | 하이라이트가 칼같이 하얀 덩어리, 창이 날아감, 채도 높은 빛이 이상한 색으로 뭉개짐 | AgX + Medium High Contrast(제품 색은 Khronos PBR Neutral). 밝기는 `exposure`로. 실내 벽 중간톤을 중간 회색에, 창 밖은 1~2 stop 밝게 | `clip_pct` ≤ 0.5%, False Color에서 피사체 회색 |
| 2 | 기본 50 mm, 눈높이가 아닌 카메라, 기울어진 수직선, DOF 없음 | 사진이 아니라 "3D 뷰포트" 같음, 건물이 넘어짐 | 실내 24~35 mm, 눈높이 1.6~1.7 m, pitch 90° + `shift_y`, DOF 켜고 f/5.6 안팎 | 카메라 속성 출력(`lens`, `location.z`, `rotation_euler.x`, `dof.use_dof`) |
| 3 | 광원 크기 0 | 칼같이 딱딱한 그림자 경계 | Point 반경·Area 크기 > 0(선명 0.1 m ~ 부드러움 2 m), Sun 0.5°~5°. UE는 Source Radius·Source Angle | 라이트 전수 검사: `shadow_soft_size == 0`이거나 Sun `angle` < 0.5°인 라이트 목록 |
| 4 | 카메라 축 정면광, 필을 쌓아 그림자를 없앰 | 평평하고 형태감이 없음, 모든 곳이 균일하게 밝음 | 키는 카메라 축에서 20° 이상(기본 40°, 위 35°). key:fill 3~4:1에서 시작. 필은 그럴듯한 반사면 근처에만 | `key_angle_deg()` ≥ 20, `value_range` ≥ 0.30 |
| 5 | 90° 칼날 같은 모서리 | 모서리에 하이라이트가 없어 형태가 안 읽힘 | 크기를 모르면 최대 치수의 0.5% 폭, 렌더 3 segments(게임 1~2), angle 30°, Harden Normals, Weighted Normal은 스택 맨 끝([scenario hard-surface](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-hard-surface/SKILL.md)). Auto Smooth는 4.1에서 제거 → Smooth by Angle | 클로즈업 렌더에서 모서리 하이라이트 확인 |
| 6 | 균일한 roughness, 순수 흑·백·원색, 중간 metallic | 플라스틱·밀랍 같음 | roughness 맵·노이즈(표준편차 > 0.01), metallic 0/1, albedo sRGB 30~240 | `pure_black_pct`, `sat100_pct`, 재질 감사 |
| 7 | 보이는 텍스처 타일링, 텍셀 밀도 불일치 | 반복 무늬, 이웃 물체끼리 선명도가 다름 | triplanar, 두 번째 텍스처 블렌딩, 손으로 칠한 브레이크업 마스크, UV 스케일을 실제 텍스처 크기에 맞춤, 텍셀 밀도 통일 | 넓은 면 클로즈업 렌더 |
| 8 | 축 정렬·등간격 배치 | 격자처럼 늘어선 가구·소품 | 클러스터 배치, 회전·스케일 지터, 통제된 비대칭 | [review_views.py](../03_playbooks/scripts/README.md) 위 정사영 뷰 |
| 9 | 잘못된 스케일 | 장난감·미니어처 같음(DOF가 과해 보임), 빛 감쇠가 어색 | 1 unit = 1 m, 트랜스폼 적용, 스케일 단서(6.5) | [scene_audit.py](../03_playbooks/scripts/README.md) 치수 범위 검사 |
| 10 | 과한 후처리, 렌더 노이즈를 그레인 대용 | 번짐·무지개 테두리, 애니메이션에서 지글거림 | Glare는 "분명히 → 의식되지 않을 때까지", CA dispersion ≤ 0.02, 완전히 디노이즈한 뒤 그레인은 마지막에 | `use_compositing` 끈 렌더와 A/B |
| 11 | 생성형 메시의 구워진 조명, HDRI와 배경·조명 불일치 | 그림자 방향이 두 개, 반사와 배경이 따로 놂 | PBR 채널로 교체·de-light, HDRI 해 위치와 태양 방향 일치 | HDRI 0°/90°/180° 회전 렌더 비교 |
| 12 | 먼지·마모·생활감 부재 | 쇼룸·CG 카탈로그 같음 | 스토리 비트당 소품 3~7개 + 마모 데칼 1~2개. 긁힘은 Normal/Bump, 지문·기름은 Roughness에만, 먼지는 위를 향한 면(Geometry Normal Z 마스크), 틈새 때는 AO·Pointiness 마스크 | 클로즈업 렌더, 체크리스트 |

더 자세한 목록(15개 항목, IOR 값 등)은 hyperrealism 스킬의 [10-mistakes-tools](https://raw.githubusercontent.com/Bartindigital/blender-hyperrealism-skill/main/references/10-mistakes-tools.md)에 있습니다(미검증 주장). 틀린 IOR 예: 물 1.33, 유리 1.45~1.52, 다이아몬드 약 2.42.

---

## 8. 규칙 간 충돌과 이 문서의 기본값

출처마다 숫자가 다른 곳은 "기본값으로 시작 → 레퍼런스와 비교해 조정"을 규칙으로 씁니다. 에이전트가 레퍼런스 없이 한쪽 숫자를 절대 기준처럼 쓰지 않게 하세요.

| 주제 | 출처 A | 출처 B | 이 문서의 기본값 |
|---|---|---|---|
| 필 비율 | 필 = 키의 1/2~1/4(arjun988) | 재질별 key:fill:rim(cc-blender-skill: 금속 4:1:2 … 제품 5:1:1.5). Blender Guru는 "고정 비율은 bogus"(hyperrealism 인용, 미검증) | key:fill 3~4:1로 시작, 레퍼런스 사진의 그림자 밀도에 맞춤. 재질별 표는 두 번째 기준 |
| 유리 roughness | 0(arjun988) | 최소 0.01(hyperrealism) | 0.01 이상에서 시작(완벽한 0은 드묾), 실물 레퍼런스로 확인 |
| 제품·가구 초점거리 | 35~50 mm(arjun988) | 80~100 mm(hyperrealism), 디테일 50~85 mm(보완 조사) | 전체 형태 설명 컷 35~50, 히어로·클로즈업 80~100 |
| 카메라 높이 | 눈높이 1.6~1.7 m(arjun988) | 인테리어 1.2~1.6 m(관례, 신뢰도 낮음) | 사람 시점 1.6, 레퍼런스 사진 높이를 따름 |
| 샘플 수 | 스틸 1000~4096 + adaptive | 창 하나 실내 약 250 + 디노이즈(신뢰도 낮음) | adaptive 0.01 유지, 테스트 약 100 → 노이즈가 보이면 올림 |
| 베벨 폭 | 최대 치수의 0.5%(scenario, 저자 추가값) | 0.01 m·3 seg(hyperrealism), 실물 본체 약 3 mm·디테일 약 1 mm, 가구 2~5 mm(관례) | 실제 크기를 알면 실물 기준, 모르면 0.5% |
| 태양 세기 | 물리 약 1000 W/m² + 노출 대폭 하향 | 아티스틱 3~10 + 노출 0(관례) | 한 장면에 하나만. UE는 물리 단위(lux) |
| 스토리 소품 수 | 비트당 3~7(arjun988) | 3~5(보완 조사) | 3~5로 시작, 큰 비트는 7까지 |
| UE bloom | "emissive 1.0 초과"(커뮤니티) | PPV Threshold가 결정(Epic 문서) | Threshold로 제어 |
| Clamp Indirect | 기본 10 | 1~3, 극단적으로 0.2(hyperrealism) | 10 유지, 파이어플라이가 보일 때만 3까지 |

---

## 9. 에이전트 규칙 블록 (CLAUDE.md / SKILL.md에 붙여 넣기)

전체 템플릿은 [CLAUDE.md 템플릿](../03_playbooks/templates/CLAUDE.md)과 [Blender 스킬 템플릿](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md)에 있습니다. 아래는 렌더·라이팅 부분만 모은 것입니다.

```text
## 렌더·라이팅 규칙 (Blender 5.x 기준, 4.x 차이는 버전 분기)
- 작업 순서: 레퍼런스·카메라 고정 → 색관리 → 스케일 → 광원(하나씩) → 재질 → 베벨·마모 → 카메라 광학 → 합성.
  한 번에 한 변수만 바꾼다. 코드를 쓰기 전에 bpy.app.version을 출력한다.
- 색관리: view_transform='AgX', look='AgX - Medium High Contrast' (제품 색 일치: 'Khronos PBR Neutral').
  Standard 금지. 전체 밝기는 view_settings.exposure로만 조정하고 램프 비율은 유지.
- 광원: 크기 0 금지. 색은 켈빈(use_temperature=True 후 color=(1,1,1)). 네온·SF만 RGB.
  키는 카메라 축에서 20° 이상(기본 40°, 위 35°, 피사체 반경 3배 거리, 크기=반경). key:fill 3~4:1에서 시작해 레퍼런스에 맞춤.
  "검정에서 시작": World 0 → HDRI → 키 → 실용광 → 고보. 필로 그림자를 지우지 않는다.
- Cycles: adaptive 0.01, OIDN(Albedo+Normal) 유지. 유리 많음 transmission>=16, 실용광 장면 max_bounces>=16.
  측정은 EXR(선형)로. 5.0+ 멀티레이어 EXR은 image_settings.media_type='MULTI_LAYER_IMAGE' 먼저.
- EEVEE: engine은 5.0+ 'BLENDER_EEVEE', 4.2~4.x 'BLENDER_EEVEE_NEXT'. use_bloom/use_ssr/use_gtao 사용 금지(없는 속성).
  파이널: use_raytracing=True, resolution_scale '1', fast_gi_step_count 16, shadow_step_count 12~16, shadow_ray_count 2.
- Bloom: 컴포지터 Glare. 5.0+는 scene.compositing_node_group + Group Output(Composite 노드 없음).
  inputs['Type']='Bloom' 명시(기본 Streaks). Strength·Size는 0~1. 보였다가 의식되지 않을 때까지 낮춘다.
- 카메라: 50mm 기본값 금지. 실내 24~35mm, 눈높이 1.6~1.7m, 건축은 pitch 90° + shift_y. DOF 켜고 Empty에 초점, 조리개 날 6~8.
- 금지: 순흑·순백·채도 100% 픽셀, 균일 roughness, metallic 중간값, 등간격·축정렬 배치, 50mm 기본 카메라.
- 노드는 이름이 아니라 bl_idname/type으로 찾는다(한국어 등 현지화 UI에서 이름이 번역됨).
- 위치를 바꾼 뒤 matrix_world를 읽기 전에 bpy.context.view_layer.update().
- 검증: 단계마다 review_render()로 beauty/falsecolor/linear.exr/stats.json을 저장하고 이미지를 직접 본다.
  게이트: clip_pct<=0.5(발광체·창 제외), value_range>=0.30, 피사체 False Color 회색, key_angle>=20.
  뷰포트 스크린샷으로 조명·재질을 판정하지 않는다. 렌더를 보지 않고 완료를 보고하지 않는다.
```

---

## 10. 추천 자료·도구 (렌더 품질 관점)

| 이름 | 무엇 | 라이선스·상태(2026-09) | 쓰는 법 | 주의 |
|---|---|---|---|---|
| [ahujasid MCP for Blender](https://github.com/ahujasid/blender-mcp) ([PyPI](https://pypi.org/project/mcp-for-blender/)) | 커뮤니티 표준 Blender MCP, Poly Haven·Sketchfab·Poly Pizza, Hyper3D Rodin·Hunyuan3D·Tripo 연동, 임의 Python 실행, `export_scene`, 노드 스키마·bpy API 조회 | MIT, 약 29.4k stars, `mcp-for-blender` 2.1.0(2026-09-25). 저장소 이름이 ahujasid/mcp-for-blender로 바뀜(기존 URL 리다이렉트) | HDRI는 1k~2k로, 렌더는 `execute_blender_code`로 파일 저장 | 렌더 tool 없음. Tripo 등 일부 생성은 유료 Premium. 익명 텔레메트리 기본 ON(`DISABLE_TELEMETRY=true`). `BLENDER_MCP_SAFE_MODE=1`은 샌드박스가 아님. 자세한 내용은 [Blender MCP 가이드](02_blender_mcp.md) |
| [scenario-labs/skills](https://github.com/scenario-labs/skills) | Blender lead 스킬 1개 + specialist 13개. lighting-rendering(`bx_light.py`, Blender 5.2.1 테스트 명시), expert(리뷰 루프·5.2 API 함정), texturing-shading, hard-surface | MIT([LICENSE](https://raw.githubusercontent.com/scenario-labs/skills/main/LICENSE)), 약 584 stars, 활발히 업데이트 | 측정 게이트로 자동 루프. Scenario MCP·API 없이 동작 | 게이트 수치 다수가 저자 추가값(`[added]`) |
| [RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill) | Claude Code 플러그인, 스킬 30개. 재질 클래스별 조명 비율, 거리 기반 에너지 공식, 실용광 레시피, 품질 autoloop | MIT, 70 stars, v1.3.0(2026-05-01), README상 Blender 5.1.1에서 검증 | 조명 레시피([lighting](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-lighting/SKILL.md)) | rendering 스킬의 `use_gtao`·`use_bloom`·`use_ssr`·`use_ssr_refraction`은 5.x에서 오류 |
| [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | 스킬 94개, 참조 파일 175개 이상(lighting, camera, set-dressing, archviz, qa-review 등). Claude Code·Cursor·Kiro·Codex | MIT, 약 229 stars, 커밋 15개 | 카메라·세트 드레싱·QA(SHIP/NO-SHIP) | rendering 스킬에 'Eevee Next', AO·Bloom 토글 같은 구식 개념 |
| [Bartindigital/blender-hyperrealism-skill](https://github.com/Bartindigital/blender-hyperrealism-skill) | '10 Laws', 11단계 워크플로, 렌더 전 체크리스트, 참조 챕터 11개 | MIT, 커밋 1, 스타 0 | 체크리스트 아이디어, 진단 항목 | 신뢰도 낮은 출처. 수치는 5.x 소스로 걸러서 사용 |
| [EaryChow/AgX](https://github.com/EaryChow/AgX) · [Khronos PBR Neutral](https://github.com/KhronosGroup/ToneMapping/tree/main/PBR_Neutral) | 뷰 변환 원저장소·사양 | 오픈소스·오픈 표준. Blender 5.x config에 포함 | 3.1 표 | Khronos는 3ds Max·Maya·Substance Painter에서도 OCIO로 사용 가능 |
| [Intel OIDN](https://github.com/RenderKit/oidn/releases) | Cycles 기본 디노이저 | v2.5.1(2026-08-18) | Albedo+Normal 패스 | |
| [Epic Unreal Engine Skills for Claude Code](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin) | UE 에디터 네이티브 MCP 연결, toolset 30개 이상 | MIT, 약 308 stars | `/plugin install unreal-engine-skills-for-claude-code@claude-plugins-official` | AllToolsets 필요. 조명·포스트 전용 도구 명시 없음 |
| [ue5-docs-mcp](https://github.com/CharlieCardenasToledo/ue5-docs-mcp) | UE 5.7 문서 3,444쪽 검색 MCP | 코드 MIT / 문서 Epic IP(개인·교육 목적 한정), 스타 1 | cvar·PPV 이름 확인 | 비공식 미러, 5.8 없음, 공식 출처로 인용 금지 |
| [ibrews/ue5-mcp](https://github.com/ibrews/ue5-mcp) | UE 함정 모음 스킬 | MIT, 39 stars | 크래시 패턴 참고 | 사실관계 근거로 쓰지 말 것(4.9) |

실제로 이 도구들을 쓴 사례(무엇을 만들었고 어디서 막혔는지)는 [사례 모음](../04_case_studies/01_case_studies.md)에 있습니다. 예를 들어 cc-blender-skill은 proof render 28장을 공개했고, 유리에서 강한 림이 볼륨 틴트를 씻어낸다는 교훈과 얇은 금속 플레어 미해결을 문서화했습니다.

---

## 흔한 실수와 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| `AttributeError: ... 'use_bloom'` (또는 `use_ssr`, `use_gtao`, `use_soft_shadows`) | 레거시 EEVEE 속성(4.2부터 없음) | 컴포지터 Glare(Bloom), EEVEE Raytracing 패널 속성 사용 |
| `enum "BLENDER_EEVEE_NEXT" not found` (5.x) 또는 반대로 `BLENDER_EEVEE` 오류(4.2~4.x) | 버전별 식별자 | `'BLENDER_EEVEE_NEXT' if (4,2,0) <= v < (5,0,0) else 'BLENDER_EEVEE'` |
| `'Scene' object has no attribute 'node_tree'` | 5.0 컴포지터 구조 변경 | `scene.compositing_node_group`에 `CompositorNodeTree`를 만들어 할당 |
| `Node type CompositorNodeComposite undefined` (5.0.1 실측) | Composite 노드 제거 | 그룹 인터페이스에 출력 소켓을 만들고 `NodeGroupOutput`으로 연결 |
| bloom을 넣었는데 줄무늬가 생김 | Glare 기본 Type이 Streaks | `glare.inputs['Type'].default_value = 'Bloom'` |
| 튜토리얼대로 Glare Size 9, mix -0.7을 넣으려는데 안 됨 | 4.3 이하 방식 | 5.x는 Strength·Size 0~1 소켓 |
| `enum "Punchy" not found` | Look 이름에 접두사 필요 | `'AgX - Punchy'` |
| `enum "OPEN_EXR_MULTILAYER" not found` (5.0.1 실측) | 5.0에서 `media_type` 도입 | `image_settings.media_type = 'MULTI_LAYER_IMAGE'` 먼저 |
| `'AreaLight' object has no attribute 'use_temperature'` (4.2.23 실측) | 4.x에는 라이트 켈빈 속성이 없음 | Blackbody 노드(Cycles) 또는 5.x 사용 |
| 켈빈을 켰는데 색이 이상함 | `use_temperature`가 켜지면 `color`가 곱해지는 틴트 | `color = (1, 1, 1)` |
| 라이트를 방금 옮긴 물체 기준으로 배치했는데 엉뚱한 곳(예: 바로 위)에 생김 | `matrix_world`가 아직 갱신되지 않음(이 문서를 쓰며 실제로 겪음) | `bpy.context.view_layer.update()` 후 읽기 |
| 발광 재질을 만들었는데 빛나지 않음 | Principled `Emission Strength` 기본값 0 | Strength 설정(작은 메시 전구 800~3000은 cc-blender-skill 값) |
| 렌더가 실패하거나 빈 이미지 | `scene.camera` 없음 | 렌더 전에 카메라 확인(`review_render()`가 먼저 검사) |
| 에이전트가 램프 값을 계속 오르내림 | 밝기를 램프로 조절 | `view_settings.exposure`로 조절, 램프 비율 고정 |
| 화면은 괜찮아 보이는데 인쇄·다른 뷰어에서 하얗게 날아감 | AgX가 클리핑을 숨김 | False Color·EXR 수치로 판정 |
| 뷰포트 스크린샷으로는 좋았는데 렌더가 다름 | 뷰포트는 최종 색관리·GI·DOF와 다름 | `review_render()`로 파일 렌더 |
| MCP 렌더 중 타임아웃, Blender 멈춤 | ahujasid 소켓 타임아웃 180초, `exec()`에는 제한 없음 | 검토 렌더는 50%·샘플 64 안팎, 최종은 헤드리스 |
| 헤드리스 렌더가 실패했는데 에이전트가 성공으로 보고 | `--python-exit-code 1` 누락 | 항상 붙임 |
| 한국어 UI에서 `nodes['Glare']`·`nodes['Principled BSDF']` KeyError | 새 노드 이름이 번역됨 | `bl_idname`·`type`으로 찾기([Blender MCP 가이드](02_blender_mcp.md) 12절) |
| UE: 라이트를 바꿔도 스크린샷 밝기가 같음 | 자동노출이 상쇄 | Manual 노출, EV100 고정 |
| UE: 크롬끼리 비치는 반사 속이 검음 | Lumen 반사 바운스 기본 1 | Hit Lighting + Max Reflection Bounces 상향 |
| UE: 작은 전구가 주변을 밝히지 않음 | 작은 발광체가 Lumen Scene에서 컬링 | Emissive Light Source |
| UE: Substrate로 코팅을 쌓았는데 단순해 보임 | 새 프로젝트 기본 Blendable GBuffer | Adaptive GBuffer |
| UE: 실내 벽 틈으로 빛이 샘 | 벽이 얇음(Software RT) | 벽 10 cm 이상, 모듈 메시, Max Trace Distance 조정 |

---

## 관련 문서

- [목적·범위](../00_purpose/purpose_and_scope.md) · [조사 방법·신뢰도 정책](../01_research/research_method.md) · [출처 카탈로그](../01_research/sources_catalog.md) · [검증 로그](../01_research/verification_log.md)
- [AI 모델 비교·MCP 클라이언트·비용](01_ai_models_and_clients.md): 비평 단계 모델 선택, Codex effort
- [Blender MCP 생태계](02_blender_mcp.md): 공식 Blender Lab 서버 vs ahujasid, API 함정 표, 한국어 UI 현지화(12절), 헤드리스 방식(6절)
- [기타 DCC·CAD·게임엔진 MCP](03_other_mcp_dcc_cad_engines.md): Unreal 5.8 공식 MCP 설정
- [AI 3D 생성](04_ai_3d_generation.md): 생성 모델 선택, 구워진 조명 후처리
- [텍스처링·재질](05_texturing_materials.md): PBR 규칙, roughness 변화, 텍셀 밀도, 베이크
- [오브젝트·가구·조형 모델링](07_modeling_objects_furniture_sculpture.md): 베벨, 부품 분해
- [배치·레이아웃](08_scene_layout_placement.md): 관계 제약, 충돌·부유 검사, 세트 드레싱
- [에이전트 워크플로·프롬프팅](09_agent_workflow_prompting.md): 시각 피드백 루프, 스킬 구성, 토큰 비용
- [에셋·파이프라인·라이선스](10_assets_pipeline_licensing.md): HDRI·재질 소스, Hunyuan3D 지역 제외
- [학술 연구](11_research_papers.md): 렌더→비평 폐루프 연구
- [빠른 시작](../03_playbooks/01_quickstart_setup.md) · [AAA 제작 플레이북](../03_playbooks/02_aaa_production_playbook.md) · [프롬프트 템플릿](../03_playbooks/03_prompt_templates.md) · [품질 체크리스트](../03_playbooks/04_quality_checklists.md) · [실측 치수 기준표](../03_playbooks/05_reference_dimensions.md)
- [보조 스크립트](../03_playbooks/scripts/README.md): `scene_audit.py`(치수·부유·관통), `placement_utils.py`(배치), `review_views.py`(4방향 검토 렌더) — Blender 4.2.23 LTS·5.0.1·5.2.2 LTS 테스트 통과
- [CLAUDE.md 템플릿](../03_playbooks/templates/CLAUDE.md) · [Blender 스킬 템플릿](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md)
- [사례 모음](../04_case_studies/01_case_studies.md) · [한국어 자료](../04_case_studies/02_korean_resources.md)

## 원자료

- [`01_research/raw/07_aaa-rendering-lighting.research.json`](../01_research/raw/07_aaa-rendering-lighting.research.json): AAA 라이팅·렌더·카메라·아트디렉션 조사(항목 22, 노하우 38, 사례 6, 출처 31)
- [`01_research/raw/07_aaa-rendering-lighting.verify.json`](../01_research/raw/07_aaa-rendering-lighting.verify.json): 독립 검증(판정 21, 항목 점검 13, 신뢰도 낮은 출처 5, 누락 항목 8). Glare 구버전 값·'판유리 208'·Lumen mobility·UE bloom 임계값·스킬 라이선스 반박, light linking 위치·Lumen 반사 바운스·Substrate GBuffer·Path Tracer 알베도 권고 보완
- [`01_research/raw/G5_aaa_practice.gap.json`](../01_research/raw/G5_aaa_practice.gap.json): AAA 실무 보완 조사(Blender 5.0~5.2·UE 5.7~5.8 변경점, 물리 조도·EV100, archviz 카메라, 80.lv 환경 제작 순서, 텍셀 밀도). 독립 검증 파일 없음
- 이 문서의 [실측] 값: pip `bpy` 5.0.1과 4.2.23 LTS를 헤드리스로 실행해 확인(2026-09-27). 코드 블록(검토 렌더, 광원 배치, EEVEE 설정, Bloom(5.0+ 전용), 카메라)을 실제로 실행했습니다
