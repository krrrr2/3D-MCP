"""
building_audit.py - "사람이 설계한 건물처럼 말이 되는가"를 점검하는 스크립트 (건축 상식 검사).

scene_audit.py 가 '떠 있음·관통·치수' 같은 물리 오류를 잡는다면, 이 스크립트는
백룸(Backrooms)처럼 기묘한 결과를 만드는 **건축적 비상식**을 잡는다.

  문     : 벽에 구멍이 없음, 바닥에서 뜸, 문을 열면 바로 벽, 허공·낭떠러지로 나감, 같은 방으로 되돌아옴, 가구가 막음, 크기 이상
  창문   : 벽에 구멍이 없음, 어정쩡한 창턱 높이, 천장을 파고듦, 실내 벽에 난 창(방↔방), 창 바로 앞이 벽, 가구가 가림,
           같은 벽 창들의 높이가 제각각, 유리 없는 창 구멍
  방     : 드나들 곳이 없는 밀폐된 방, 입구에서 갈 수 없는 방, 창 없는 생활 공간, 복도처럼 길쭉한 방, 천장 없음·이상,
           텅 빈 방, 똑같은 빈 방의 반복, 복도 비율 과다, 벽이 빠져 허공이 보이는 방 가장자리
  벽     : 천장까지 안 닿아 실제로 뚫려 보임, 벽 끝 사이로 실제로 뚫려 보이는 틈, 두께 이상
  계단   : 단 높이 불균일, 단 높이·너비 비상식(2R+T), 어디로도 안 이어짐
  가구   : 앉는 가구(앞뒤가 있는 것)가 코앞의 벽을 보고 있음
  종합   : 백룸 위험도(liminal_risk) — 창 없는 방·복도 과다·빈 방·반복·밀폐 방 등 이유와 함께

판정은 이름보다 **형상**을 우선합니다 (실제 AI 생성 장면에서 검증하며 바꾼 설계, 2026-09-27).
  - 방 연결: 문 오브젝트뿐 아니라 방 바닥 가장자리에서 벽 쪽으로 레이를 쏴서 문짝 없는 출입구(개구부)를 찾는다
  - 문·창 구멍: 벽 BVH 를 가로지르는 레이로 실제 구멍 폭을 잰다(열린 문, 벽을 나눠 만든 출입구도 처리)
  - 벽 방향: 루트 회전이 아니라 정점 분포(PCA)로 구한다(좌표에 직접 박힌 회전 벽도 처리). 곡선 벽은 직선 벽 전용 검사에서 뺀다
  - 틈·천장 틈: 틈 위치를 레이가 실제로 통과할 때만 보고한다(다른 조각이 메운 경우 제외)

근거
  - 문 앞 비움 구역 = 문 폭 × 문 폭 (NVlabs SAGE 배치 솔버), 문은 방과 방/외부를 잇고 창은 외벽에 둔다 (Holodeck, Infinigen Indoors)
  - 동선으로 모든 방에 갈 수 있어야 함 (SceneSmith Reachability 채점 항목)
  - 그 밖의 임계값은 특정 국가 법규가 아니라 넓게 잡은 "상식 범위"다. 02_guides/08_scene_layout_placement.md 참고.

역할 인식 (커스텀 프로퍼티 obj["role"], obj["room_type"] 가 있으면 그것이 우선)
  방 바닥   : Floor_<방종류>, FLOOR_LivingDining 등 (1 m² 미만 바닥 조각은 소품으로 간주)
  외부 지면 : Ground / Terrain  (없으면 "모델 바깥 = 모델링되지 않은 외부"로 본다)
  벽        : Wall_..., ..._wall, LINTEL_/HEADER_/SOFFIT_ (문 위 인방 등)
  천장·지붕 : Ceiling..., ..._roof, ..._plenum
  문·창     : Door_..., Window_... (door_handle, window_sill 처럼 뒤에 부속품 단어가 오면 부속품)
  마감재    : FRAME_/JAMB_/CASING_/SKIRT_/BASEBOARD_/COVE_/THRESHOLD_ 등 → 가구 검사에서 제외
  계단      : stair / stairs / staircase 가 들어간 부모 아래에 단(step)을 자식 메시로
  이름으로 못 정하면 컬렉션 이름(.../Walls, .../Floors, .../Ceilings, .../Openings, .../Trim)을 참고, 그래도 없으면 가구

사용
  import building_audit; rep = building_audit.audit_building(collection="House")
  blender -b house.blend --python building_audit.py -- --collection House --out building.json
scene_audit.py 와 같은 폴더에 두세요 (공통 함수를 가져다 씁니다). Blender 4.2 LTS / 5.0 에서 테스트.
"""

import json
import math
import os
import re
import statistics
import sys

import bpy
from mathutils import Vector, geometry
from mathutils.bvhtree import BVHTree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else ".")
import scene_audit as sa  # noqa: E402

# 방 종류 단어 → 분류
CIRCULATION = {"corridor", "hall", "hallway", "entry", "entrance", "foyer", "lobby", "stairwell", "passage", "vestibule"}
SERVICE = {"bathroom", "bath", "toilet", "wc", "restroom", "powder", "ensuite", "closet", "storage", "pantry", "utility",
           "laundry", "dressing", "walkin", "garage", "basement", "attic", "mudroom", "boiler", "shower"}
OUTDOOR = {"balcony", "terrace", "veranda", "porch", "deck", "patio"}
# 창이 없어도 자연스러운 실내 전용 공간 (창 없음 경고 제외, 빈 방 검사는 유지)
INTERIOR = {"bar", "game", "gaming", "media", "theater", "theatre", "cinema", "karaoke", "photo", "photography",
            "darkroom", "server", "vault", "cellar", "wine", "recording", "sauna", "gallery"}
HABITABLE = {"living", "bedroom", "kitchen", "dining", "office", "study", "family", "den", "library", "playroom",
             "guest", "master", "kids", "nursery", "room", "ldk", "gym", "lounge", "salon", "loft", "studio", "suite"}
ROOM_WORDS = CIRCULATION | SERVICE | OUTDOOR | INTERIOR | HABITABLE | {"bed", "level", "ground", "first", "second", "upper", "lower"}
SEATING = {"sofa", "chair", "armchair", "couch"}          # 앞뒤가 있는 좌석만 (스툴·벤치는 방향이 없음)
# 'wall_shelf', 'floor_lamp', 'door_handle', 'window_sill' 처럼 구조 단어 뒤에 붙으면 가구·부속품으로 보는 단어
ATTACHED = {"shelf", "shelves", "lamp", "light", "lights", "sconce", "art", "painting", "picture", "poster", "photo",
            "frame", "clock", "mirror", "cabinet", "cupboard", "tv", "hook", "rack", "decor", "plant", "planter", "fan",
            "vent", "socket", "outlet", "switch", "sign", "handle", "knob", "sill", "trim", "molding", "moulding",
            "baseboard", "curtain", "curtains", "blind", "blinds", "rug", "mat", "carpet", "cushion", "stopper", "hinge",
            "led", "plug", "cable", "wrap", "device", "mount", "plaque"}
TRIM_WORDS = {"frame", "jamb", "casing", "architrave", "skirt", "skirting", "baseboard", "cove", "cornice", "molding",
              "moulding", "trim", "threshold", "thresholds", "reveal", "lip", "stop", "finish", "finishes", "cladding",
              "lining", "wainscot", "wainscoting", "boiserie", "paneling", "panelling", "wallpaper"}
PLURALS = {"walls": "wall", "floors": "floor", "ceilings": "ceiling", "doors": "door", "windows": "window",
           "columns": "column", "roofs": "roof", "pillars": "pillar", "beams": "beam"}
# 이름에 이 단어가 있는 빈 그룹(Empty)은 '묶음'으로 보고 안의 자식들을 따로 검사한다 (GLB 가져오기 등)
CONTAINER_WORDS = {"house", "building", "home", "apartment", "flat", "scene", "root", "level", "storey", "story",
                   "architecture", "structure", "shell", "layout", "site", "world", "openings", "rooms", "interior",
                   "exterior", "furnishings", "furniture", "props", "decor", "group", "collection"}
# 한국어·중국어 이름 (AI 가 만든 장면에서 자주 보임). 위에서부터 먼저 맞는 것이 이긴다 (부속품·마감재를 먼저 거름)
CJK_ROLES = [
    ("trim", ("门套", "窗套", "门框", "窗框", "门槛", "踢脚", "线脚", "墙纸", "문틀", "창틀", "걸레받이", "몰딩", "벽지")),
    ("furniture", ("把手", "门吸", "门锁", "窗帘", "帘", "窗台", "灯", "画", "镜", "柜", "架", "开关", "插座", "装饰", "冰箱",
                   "손잡이", "커튼", "블라인드", "창턱", "벽등", "벽걸이", "조명", "액자", "거울", "선반", "수납")),
    ("railing", ("栏杆", "护栏", "扶手", "난간")),
    ("stair", ("楼梯", "台阶", "踏步", "계단")),
    ("window", ("窗", "창문", "창호")),
    ("door", ("门", "문짝", "출입문", "현관문", "방문", "미닫이문", "여닫이문", "문")),
    ("floor", ("地坪", "地板", "地面", "楼板", "바닥")),
    ("ceiling", ("天花", "吊顶", "顶棚", "천장", "천정")),
    ("roof", ("屋顶", "屋面", "지붕")),
    ("ground", ("草坪", "庭院地面", "잔디", "마당", "지면")),
    ("wall", ("墙", "벽")),
    ("column", ("柱", "기둥")),
]
CJK_ROOMS = [
    ("circulation", ("走廊", "过道", "玄关", "门厅", "복도", "현관", "홀")),
    ("service", ("卫生间", "卫", "浴室", "厕所", "储藏", "衣帽", "洗衣", "욕실", "화장실", "드레스룸", "창고", "다용도", "세탁")),
    ("outdoor", ("阳台", "露台", "庭院", "발코니", "베란다", "테라스")),
    ("habitable", ("客厅", "餐厅", "卧", "书房", "厨房", "起居", "거실", "침실", "안방", "주방", "서재", "방")),
]
WALL_EXTRA = {"lintel", "header", "soffit", "bulkhead", "parapet", "partition"}
RAILING = {"railing", "railings", "balustrade", "guardrail", "handrail", "banister", "baluster", "balusters", "fence"}
CEILING_EXTRA = {"plenum"}
COLUMN_WORDS = {"column", "pillar", "beam", "post", "pilaster"}
# 오픈 셀 격자·루버·배플 천장: 가는 막대 여러 개로 만들어도 '천장'이다 (예: 컬렉션 'Bar_Open_Ceiling_Grid')
GRID_WORDS = {"grid", "grids", "lattice", "baffle", "baffles", "louver", "louvers", "louvre", "slat", "slats", "eggcrate"}
COLLECTION_ROLES = {"walls": "wall", "wall": "wall", "floors": "floor", "floor": "floor", "ceilings": "ceiling",
                    "ceiling": "ceiling", "roof": "roof", "roofs": "roof", "doors": "door", "windows": "window",
                    "stairs": "stair", "trim": "trim", "openings": "trim", "columns": "column"}

# 상식 범위 (m). 특정 법규가 아니라 "이 범위를 벗어나면 사람이 설계한 건물로 보기 어렵다"는 넓은 기준
LIMITS = {
    "door_h": (1.90, 2.70), "door_w": (0.60, 2.00), "door_float": 0.05, "door_front_wall": 0.60,
    "door_drop": 0.40, "window_w": (0.30, 10.00), "window_h": (0.30, 3.20),
    "sill_awkward": (0.03, 0.25), "sill_high": 1.80, "window_front_wall": 0.50, "window_align": 0.05,
    "ceiling_h": (2.10, 4.50), "corridor_aspect": 4.0, "corridor_min_w": 0.80, "corridor_fraction": 0.35,
    "wall_t": (0.05, 0.60), "wall_top_gap": 0.02, "wall_end_gap": (0.01, 0.30),
    "riser": (0.12, 0.22), "tread": (0.22, 0.38), "blondel": (0.55, 0.70), "riser_spread": 0.01,
    "seat_front_wall": 0.50, "repeat_rooms": 3, "min_room_area": 1.0,
    "passage_min": 0.60, "window_opening_min": 0.30, "open_edge_min": 0.60, "sample_step": 0.20,
    "guard_drop": 1.00, "open_exterior_max": 2.50, "min_column_h": 1.00,
    "glazed_door_w_max": 6.00, "passage_narrow": 0.45, "window_blocked_frac": 0.25, "door_clearance_max_w": 1.30,
}


# ----------------------------------------------------------------------------- 기본 도구

def _toks(name):
    """scene_audit 토큰 + 글자·숫자 분리('bed1' → bed, 1) + 복수형 → 단수('walls' → wall)."""
    out = []
    for t in sa._name_tokens(name):
        for part in re.findall(r"[a-z]+|\d+", t):
            out.append(PLURALS.get(part, part))
    return out


CJK_DIRECTIONS = {"남", "북", "동", "서", "남쪽", "북쪽", "동쪽", "서쪽", "좌", "우", "앞", "뒤", "상", "하",
                  "东", "西", "南", "北", "左", "右", "上", "下", "前", "后"}
_CJK_RUN = re.compile(r"[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]+")


def _cjk_role(name):
    """한국어·중국어·일본어는 끝 단어가 핵심(창가_소파 = 소파, 窗边绿植 = 화분, 双门冰箱 = 냉장고).
    마지막 CJK 덩어리의 '끝'에 붙은 역할 단어로 판정한다."""
    runs = _CJK_RUN.findall(name)
    while len(runs) > 1 and runs[-1] in CJK_DIRECTIONS:
        runs.pop()                     # '외벽_남', '墙_北' 처럼 끝에 붙은 방향어는 건너뜀
    if not runs:
        return None
    seg = runs[-1]
    for role, words in CJK_ROLES:
        if any(seg.endswith(w) for w in words):
            return role
    return None


def _role(obj):
    r = obj.get("role") if hasattr(obj, "get") else None
    if r:
        return str(r).lower()
    cjk = _cjk_role(obj.name)
    if cjk:
        return cjk
    toks = _toks(obj.name)
    core = list(toks)
    while len(core) > 1 and sa._TRAILING_NOISE.match(core[-1]):
        core.pop()
    head = core[-1] if core else ""
    first = toks[0] if toks else ""
    plain = not any(t in ATTACHED for t in toks[1:])   # 뒤에 부속품 단어가 없음
    if first in TRIM_WORDS or "trim" in toks or (head in TRIM_WORDS and first in ("door", "window", "wall", "floor", "ceiling")):
        return "trim"
    if head == "floor" or (first == "floor" and plain):
        return "floor"
    if head in ("ground", "terrain", "lawn", "yard"):
        return "ground"
    if first in WALL_EXTRA or head in WALL_EXTRA:
        return "wall"
    if head in RAILING or first in RAILING:
        return "railing"
    if (first in CEILING_EXTRA or head in CEILING_EXTRA) and plain:
        return "ceiling"
    for role in ("wall", "ceiling", "roof", "door", "window"):
        # Wall_N / Wall_mid_x / north_wall / Door_bedroom / Window_living_2 모두 인식, wall_shelf·door_handle 은 가구
        if (head == role and not (toks and toks[-1] in ATTACHED)) or (first == role and plain):
            return role
    if any(t in ("stair", "stairs", "staircase", "stairway") for t in toks):
        return "stair"
    if head in COLUMN_WORDS or (first in COLUMN_WORDS and plain):
        return "column"
    # 이름으로 못 정하면 컬렉션 이름으로 (예: 'Game/Walls', 'Corridor/Floors')
    if head in GRID_WORDS and "ceiling" in toks:
        return "ceiling"
    for col in getattr(obj, "users_collection", ()):
        last = col.name.replace("\\", "/").split("/")[-1].strip().lower()
        if last in COLLECTION_ROLES:
            return COLLECTION_ROLES[last]
        ctoks = _toks(last)
        if ctoks and ctoks[-1] in GRID_WORDS and "ceiling" in ctoks:
            return "ceiling"
    return "furniture"


CURTAIN_WORDS = {"curtain", "curtains", "drape", "drapes", "drapery", "blind", "blinds", "sheer", "sheers", "shade", "shades"}


def _is_curtain(name):
    """커튼·블라인드는 창을 '가리는 가구'가 아니라 창 장식 (열고 닫는 것)."""
    return bool(set(_toks(name)) & CURTAIN_WORDS) or any(w in name for w in ("帘", "커튼", "블라인드", "カーテン"))


def _room_type(obj):
    rt = obj.get("room_type") if hasattr(obj, "get") else None
    if not rt and not obj.name.isascii():
        for name, words in CJK_ROOMS:
            if any(w in obj.name for w in words):
                return name
    toks = [str(rt).lower()] if rt else _toks(obj.name)
    for group, name in ((CIRCULATION, "circulation"), (SERVICE, "service"), (OUTDOOR, "outdoor"), (INTERIOR, "interior"),
                        (HABITABLE, "habitable")):
        if any(t in group for t in toks):
            return name
    if "bed" in toks:
        return "habitable"
    return "unknown"


def _subtree_extent(o):
    pts = []
    for m in sa._mesh_objects_under(o):
        pts.extend(m.matrix_world @ Vector(c) for c in m.bound_box)
    if not pts:
        return 0.0, 0.0
    bmin, bmax = sa._bbox_of_points(pts)
    return bmax.x - bmin.x, bmax.y - bmin.y


def _is_container(o):
    """자식이 있는 빈 그룹(Empty) 중 '집 전체·바닥들·열림부들' 같은 묶음이면 True → 자식을 각각 검사.
    문·창·계단처럼 역할이 있는 조립품, 의자처럼 작은 가구 조립품은 하나로 둔다."""
    if o.type == "MESH" or not o.children or (hasattr(o, "get") and o.get("role")):
        return False
    own = _role(o)
    if own in ("door", "window", "stair", "railing", "column", "trim"):
        return False
    if set(_toks(o.name)) & CONTAINER_WORDS or own in ("floor", "wall", "ceiling", "roof"):
        return True
    ex, ey = _subtree_extent(o)
    if ex > 6.0 and ey > 6.0:            # 가구 조립품은 가로·세로가 모두 6 m 를 넘지 않는다
        return True
    # 방 규모(가로·세로 2.5 m 이상) 그룹 안에 벽·바닥·문 같은 구조물이 있으면 묶음.
    # 작은 가구 속 'InnerWall'·'cabinet door' 같은 부품 이름에 속지 않도록 크기 조건을 둔다
    strong = ("floor", "wall", "ceiling", "roof", "door", "window", "stair", "ground")
    return ex >= 2.5 and ey >= 2.5 and any(_role(c) in strong or (c.type != "MESH" and c.children and _is_container(c))
                                           for c in o.children)


def _unit_roots():
    out = []

    def visit(o):
        if _is_container(o):
            for c in o.children:
                visit(c)
        else:
            out.append(o)
    for root in [o for o in bpy.context.scene.objects if o.parent is None]:
        visit(root)
    return out


def _islands(verts, polys):
    """같은 좌표의 정점을 붙인 뒤 서로 이어진 면끼리 묶는다 → [[폴리곤 인덱스...], ...]"""
    key = {}
    idx = [key.setdefault((round(v.x, 4), round(v.y, 4), round(v.z, 4)), len(key)) for v in verts]
    parent = list(range(len(key)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for poly in polys:
        r0 = find(idx[poly[0]])
        for i in poly[1:]:
            r = find(idx[i])
            if r != r0:
                parent[r] = r0
    groups = {}
    for pi, poly in enumerate(polys):
        groups.setdefault(find(idx[poly[0]]), []).append(pi)
    return list(groups.values())


def _cluster(verts, polys, groups, gap):
    """섬(islands)들을 bbox 간격 gap 이내끼리 묶는다 → [[폴리곤 인덱스...], ...]"""
    boxes = [sa._bbox_of_points([verts[i] for pi in g for i in polys[pi]]) for g in groups]
    parent = list(range(len(groups)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            (amin, amax), (bmin, bmax) = boxes[i], boxes[j]
            if all(amin[k] - gap <= bmax[k] and bmin[k] - gap <= amax[k] for k in range(3)):
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[rj] = ri
    out = {}
    for i, g in enumerate(groups):
        out.setdefault(find(i), []).extend(g)
    return list(out.values())


def _make_unit(root, name, role, meshes, per_mesh, verts, polys):
    bmin, bmax = sa._bbox_of_points(verts)
    return {"root": root, "name": name, "role": role, "meshes": meshes, "per_mesh": per_mesh,
            "verts": verts, "polys": polys, "bbox": (bmin, bmax), "bvh": BVHTree.FromPolygons(verts, polys)}


def _collect_units(collection):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    scoped = None
    if collection is not None:
        scoped = {o.name for o in bpy.data.collections[collection].all_objects}
    units = []
    for root in _unit_roots():
        meshes = sa._mesh_objects_under(root)
        if not meshes:
            continue
        if scoped is not None and root.name not in scoped and not any(m.name in scoped for m in meshes):
            continue
        verts, polys, per_mesh = [], [], []
        for m in meshes:
            v, p = sa._world_verts_and_polys(m, depsgraph)
            off = len(verts)
            verts.extend(v)
            polys.extend(tuple(i + off for i in poly) for poly in p)
            if v:
                per_mesh.append((m, sa._bbox_of_points(v)))
        if not verts or not polys:
            continue
        role = _role(root)
        groups = None
        if role in ("wall", "column"):
            # 벽 전체를 한 메시로 합친 경우(웹·게임용 AI 산출물에 흔함): 떨어진 조각마다 따로 검사
            groups = _islands(verts, polys)
        elif role in ("window", "door"):
            # 창·문 여러 개가 한 오브젝트로 합쳐진 경우(재질별 합치기 등): 가까운 조각끼리 묶어 창·문 하나씩으로
            bmin, bmax = sa._bbox_of_points(verts)
            ex, ey = bmax.x - bmin.x, bmax.y - bmin.y
            if min(ex, ey) > 1.5 or max(ex, ey) > 8.0:
                groups = _cluster(verts, polys, _islands(verts, polys), 0.15)
        if groups is not None and len(groups) > 1:
            parts = []
            for g in groups:
                used = sorted({i for pi in g for i in polys[pi]})
                remap = {old: k for k, old in enumerate(used)}
                parts.append(([verts[i] for i in used], [tuple(remap[i] for i in polys[pi]) for pi in g]))
            parts.sort(key=lambda vp: (round(min(v.x for v in vp[0]), 3), round(min(v.y for v in vp[0]), 3)))
            for k, (pv, pp) in enumerate(parts):
                units.append(_make_unit(root, f"{root.name}#{k}", role, meshes, per_mesh, pv, pp))
            continue
        units.append(_make_unit(root, root.name, role, meshes, per_mesh, verts, polys))
    for u in units:
        u["frame"] = _frame(u)
        # 한 변이 7 m 넘는 '가구'는 가구가 아니라 집 전체에 흩어진 마감재·장식을 합쳐 둔 묶음 (문 앞·창 앞 가림 검사에서 제외)
        bmin, bmax = u["bbox"]
        span = max(bmax.x - bmin.x, bmax.y - bmin.y)
        if u["role"] == "furniture" and (span > 7.0 or (span > 4.0 and len(_cluster(u["verts"], u["polys"],
                                                                                        _islands(u["verts"], u["polys"]), 0.3)) >= 3)):
            u["role"] = "trim"      # 여러 곳에 흩어진 조각을 재질별로 합친 묶음(문 손잡이 전부 등)도 가구 한 점이 아님
    return units


def _frame(u):
    """두 가지 축.
    ax/ay/ex/ey : 루트의 Z 회전(yaw) 기준 — 가구 '앞면(-Y)' 판정용
    long/normal/length/thick : 정점 분포(PCA) 기준 — 벽·문·바닥처럼 회전이 정점에 박힌 경우에도 맞는 방향
    """
    yaw = u["root"].matrix_world.to_euler("XYZ").z
    c, s = math.cos(yaw), math.sin(yaw)
    ax, ay = Vector((c, s, 0.0)), Vector((-s, c, 0.0))
    V = u["verts"]
    step = max(1, len(V) // 20000)
    pts = V[::step]
    zs = [v.z for v in V]
    xs = [v.dot(ax) for v in pts]
    ys = [v.dot(ay) for v in pts]
    ex, ey = max(xs) - min(xs), max(ys) - min(ys)
    # 2D PCA
    mx = sum(p.x for p in pts) / len(pts)
    my = sum(p.y for p in pts) / len(pts)
    sxx = sum((p.x - mx) ** 2 for p in pts)
    syy = sum((p.y - my) ** 2 for p in pts)
    sxy = sum((p.x - mx) * (p.y - my) for p in pts)
    ang = 0.5 * math.atan2(2 * sxy, sxx - syy)
    la = Vector((math.cos(ang), math.sin(ang), 0.0))
    na = Vector((-la.y, la.x, 0.0))
    ls = [p.dot(la) for p in pts]
    ns = [p.dot(na) for p in pts]
    length, thick = max(ls) - min(ls), max(ns) - min(ns)
    if thick > length:
        la, na, length, thick, ls, ns = na, -la, thick, length, [p.dot(na) for p in pts], [-p.dot(la) for p in pts]
    center = la * ((max(ls) + min(ls)) / 2) + na * ((max(ns) + min(ns)) / 2)
    center.z = (max(zs) + min(zs)) / 2
    return {"center": center, "ax": ax, "ay": ay, "ex": ex, "ey": ey, "zmin": min(zs), "zmax": max(zs),
            "long": la, "normal": na, "length": length, "thick": thick, "yaw": yaw}


def _cast(units, origin, direction, dist, with_normal=False):
    best = None
    for u in units:
        loc, nrm, _i, d = u["bvh"].ray_cast(origin, direction, dist)
        if loc is not None and (best is None or d < best[1]):
            best = (loc, d, u, nrm)
    if best is None:
        return None
    return best if with_normal else best[:3]


def _near(units, bmin, bmax, pad=0.0):
    """AABB(bmin~bmax, pad 만큼 확장)와 겹치는 유닛만 (레이 검사 대상을 줄이는 용도)."""
    out = []
    for u in units:
        umin, umax = u["bbox"]
        if all(umin[i] <= bmax[i] + pad and umax[i] >= bmin[i] - pad for i in range(3)):
            out.append(u)
    return out


def _aabb_overlap(a, b):
    (amin, amax), (bmin, bmax) = a, b
    return min(min(amax[i], bmax[i]) - max(amin[i], bmin[i]) for i in range(3))


def _zone_aabb(origin, along, depth, across, width, z0, z1):
    pts = []
    for dd in (0.0, depth):
        for ww in (-width / 2, width / 2):
            p = origin + along * dd + across * ww
            pts.append(Vector((p.x, p.y, z0)))
            pts.append(Vector((p.x, p.y, z1)))
    return sa._bbox_of_points(pts)


def _top_faces(u):
    top = u["bbox"][1].z
    V = u["verts"]
    faces = []
    for poly in u["polys"]:
        pts = [V[i] for i in poly]
        if len(pts) < 3 or any(abs(p.z - top) > 0.005 for p in pts):
            continue
        if geometry.normal(pts).z < 0.9:
            continue
        faces.append(poly)
    return faces


def _top_area(u):
    """윗면(법선이 위를 향하고 bbox 최상단 근처) 면적 = 방 바닥 면적."""
    V = u["verts"]
    area = 0.0
    for poly in _top_faces(u):
        pts = [V[i] for i in poly]
        for k in range(1, len(pts) - 1):
            area += geometry.area_tri(pts[0], pts[k], pts[k + 1])
    return area


def _top_boundary(u):
    """방 바닥 윗면의 경계 모서리들: (시작점, 방향, 바깥쪽 법선, 길이)."""
    V = u["verts"]
    edges = {}
    for poly in _top_faces(u):
        c = sum((V[i] for i in poly), Vector()) / len(poly)
        for a, b in zip(poly, poly[1:] + poly[:1]):
            edges.setdefault((min(a, b), max(a, b)), []).append(c)
    out = []
    for (a, b), cs in edges.items():
        if len(cs) != 1:
            continue
        pa, pb = V[a], V[b]
        d = Vector((pb.x - pa.x, pb.y - pa.y, 0.0))
        length = d.length
        if length < 0.05:
            continue
        d /= length
        n = Vector((-d.y, d.x, 0.0))
        mid = (pa + pb) / 2
        toc = cs[0] - mid
        if Vector((toc.x, toc.y, 0.0)).dot(n) > 0:
            n = -n
        out.append((pa, d, n, length))
    return out


def _runs(labels, step):
    """[(label, payload), ...] 연속 구간 → [(label, payload, 길이, 시작 인덱스)]"""
    runs, cur, cnt, pay, start = [], None, 0, None, 0
    for i, (lab, p) in enumerate(labels):
        if lab == cur:
            cnt += 1
        else:
            if cur is not None:
                runs.append((cur, pay, cnt * step, start))
            cur, cnt, pay, start = lab, 1, p, i
    if cur is not None:
        runs.append((cur, pay, cnt * step, start))
    return runs


# ----------------------------------------------------------------------------- 메인 점검

def audit_building(collection=None, limits=None):
    L = dict(LIMITS, **(limits or {}))
    units = _collect_units(collection)
    # 1 m² 미만의 '바닥' 조각(바닥에 깔린 소품 등)은 방이 아니다
    for u in units:
        if u["role"] == "floor" and _top_area(u) < L["min_room_area"]:
            u["role"] = "furniture"
        # 1 m 보다 낮은 '기둥'은 구조가 아니라 소품 부품(감지기 다리 등)
        if u["role"] == "column" and u["bbox"][1].z - u["bbox"][0].z < L["min_column_h"]:
            u["role"] = "furniture"
    by_role = {}
    for u in units:
        by_role.setdefault(u["role"], []).append(u)
    walls, floors, grounds = by_role.get("wall", []), by_role.get("floor", []), by_role.get("ground", [])
    ceilings = by_role.get("ceiling", []) + by_role.get("roof", [])
    doors, windows = by_role.get("door", []), by_role.get("window", [])
    trims = by_role.get("trim", [])
    furniture = by_role.get("furniture", [])
    solids = walls + by_role.get("column", [])
    ground_like = floors + grounds
    has_ground = bool(grounds)
    issues = []
    openings_out = []

    def add(sev, code, obj, detail):
        issues.append({"severity": sev, "code": code, "object": obj, "detail": detail})

    def classify(p):
        """점 p 아래를 보고 방/외부/허공 판정. 외부 지면이 하나도 없으면 허공은 '모델링되지 않은 외부'."""
        hit = _cast(ground_like, Vector((p.x, p.y, p.z)), Vector((0, 0, -1)), 100.0)
        if hit is None:
            return {"kind": "void" if has_ground else "exterior", "top": None, "unit": None, "unmodeled": not has_ground}
        loc, _d, u = hit
        kind = "room" if u["role"] == "floor" else "exterior"
        return {"kind": kind, "top": loc.z, "unit": u, "unmodeled": False}

    # --- 벽 직선성 (곡선·L자 벽은 직선 벽 전용 검사에서 제외)
    for w in walls:
        f = w["frame"]
        w["straight"] = False
        for fr in (0.25, 0.5, 0.75):
            for hz in (0.3, 0.5):
                c = f["center"] + f["long"] * ((fr - 0.5) * f["length"])
                z = w["bbox"][0].z + hz * (w["bbox"][1].z - w["bbox"][0].z)
                o = Vector((c.x, c.y, z)) - f["normal"] * (f["thick"] / 2 + 0.05)
                h1 = w["bvh"].ray_cast(o, f["normal"], f["thick"] + 0.1)
                if h1[0] is None:
                    continue
                h2 = w["bvh"].ray_cast(h1[0] + f["normal"] * 1e-4, f["normal"], f["thick"] + 0.1)
                if h2[0] is not None and abs((h2[0] - h1[0]).length - f["thick"]) <= 0.03:
                    w["straight"] = True
                    break
            if w["straight"]:
                break

    room_info = {u["name"]: {"doors": [], "passages": set(), "windows": [], "glassless": [], "glazed_doors": [], "furniture": [], "unit": u}
                 for u in floors}
    graph = {u["name"]: set() for u in floors}
    graph["EXTERIOR"] = set()

    # --- 문·창 공통: 끼워진 벽 찾기 + 실제 구멍 찾기
    def candidate_walls(o, pad=0.2):
        """문·창 bbox(pad 만큼 확장)와 겹치는 벽들, 겹치는 부피가 큰 순서."""
        omin, omax = o["bbox"]
        out = []
        for w in walls:
            ov = [min(omax[i] + pad, w["bbox"][1][i]) - max(omin[i] - pad, w["bbox"][0][i]) for i in range(3)]
            if min(ov) > 0:
                out.append((ov[0] * ov[1] * ov[2], w))
        return [w for _v, w in sorted(out, key=lambda x: -x[0])]

    def inside_solid(near, p):
        """p 가 벽 같은 닫힌 솔리드 속이면 True (위로 쏜 레이가 윗면을 '안에서' 만남)."""
        hit = _cast(near, p, Vector((0, 0, 1)), 20.0, True)
        return hit is not None and hit[3].z > 0

    def crossing_open(near, c, n, t, z):
        """벽 두께 방향으로 c 를 가로지르는 선분이 비어 있는가 (구멍)."""
        q = Vector((c.x, c.y, z))
        if _cast(near, q - n * (t / 2 + 0.15), n, t + 0.3) is not None:
            return False
        return not inside_solid(near, q)

    def find_openings(c0, n, along, t, z, search, near):
        """c0 주변 ±search 를 벽 방향으로 훑어 뚫린 구간들을 [(중심 오프셋, 폭, 끝에 닿음)] 으로 돌려준다."""
        step = 0.04
        k = int(search / step)
        flags = [(i * step, crossing_open(near, c0 + along * (i * step), n, t, z)) for i in range(-k, k + 1)]
        runs, cur = [], []
        for s_, open_ in flags + [(None, False)]:
            if open_:
                cur.append(s_)
            elif cur:
                runs.append(((cur[0] + cur[-1]) / 2, len(cur) * step, cur[0] == -k * step or cur[-1] == k * step))
                cur = []
        return runs

    def hole_vertical(near, c, n, t, z_mid, zlo, zhi):
        """구멍의 실제 아래·위 높이 (창턱·인방 사이). 커튼·창틀 장식이 붙은 창도 유리 구멍 높이로 판단."""
        if not crossing_open(near, c, n, t, z_mid):
            return None
        lo = hi = z_mid
        while lo - 0.02 > zlo and crossing_open(near, c, n, t, lo - 0.02):
            lo -= 0.02
        while hi + 0.02 < zhi and crossing_open(near, c, n, t, hi + 0.02):
            hi += 0.02
        return lo, hi

    def opening_report(o, kind):
        f = o["frame"]
        cands = candidate_walls(o)
        if not cands:
            add("error", f"{kind}_not_in_wall", o["name"], f"{kind}가 어떤 벽에도 끼워져 있지 않습니다(허공에 선 {kind}).")
            return None
        zmin, zmax = o["bbox"][0].z, o["bbox"][1].z
        leaf = max(f["length"], 0.3)
        search = max(2 * leaf, leaf + 0.6, 1.2)      # 미닫이 문짝이 구멍 옆에 열린 채 겹쳐 있어도 구멍이 범위에 들어오게
        z_probe = zmin + (1.0 if kind == "door" else (zmax - zmin) / 2)
        omin, omax = o["bbox"]
        oc0 = Vector((f["center"].x, f["center"].y, 0.0))
        near_all = _near(solids, Vector((oc0.x - search - 1.0, oc0.y - search - 1.0, zmin - 0.5)),
                         Vector((oc0.x + search + 1.0, oc0.y + search + 1.0, zmax + 0.5)))

        def local_t(p, n):
            """p 근처 벽의 실제 두께와 벽 중심까지의 오프셋(n 방향). 구멍 위(인방)·아래(창턱 벽)에서 잰다.
            p 가 벽 속이면 양쪽 벽면까지, 벽 밖이면 가장 가까운 벽면으로 들어가서 반대 면까지."""
            for z in (zmax + 0.08, zmin - 0.10, zmax + 0.25):
                q = Vector((p.x, p.y, z))
                a = _cast(near_all, q, n, 0.5, True)
                b = _cast(near_all, q, -n, 0.5, True)
                if a and b and a[3].dot(n) > 0 and b[3].dot(-n) > 0 and 0.04 < a[1] + b[1] < 0.8:
                    return a[1] + b[1], (a[1] - b[1]) / 2          # 두께, 벽 중심까지 오프셋
                found = []
                for dv in (n, -n):
                    h1 = _cast(near_all, q, dv, 0.4, True)
                    if h1 is None or h1[3].dot(dv) >= 0:
                        continue                                    # 벽면에 '들어가는' 방향이 아님
                    h2 = _cast(near_all, h1[0] + dv * 1e-4, dv, 0.8, True)
                    if h2 is not None and h2[3].dot(dv) > 0 and 0.04 < h2[1] < 0.8:
                        found.append((h1[1], h2[1], dv))
                if found:
                    d1, th, dv = min(found, key=lambda x: x[0])
                    return th, (d1 + th / 2) * (1.0 if dv.dot(n) > 0 else -1.0)
            return None, 0.0

        # 구멍 가설: (벽 법선, 벽 방향, 두께, 벽 중심선 위의 기준점, 벽 오브젝트 방향인가)
        hyps = []
        for w in cands:
            if not w.get("straight"):
                continue            # 곡선·합쳐진 벽의 PCA 축은 이 자리의 벽 방향이 아니다
            wf = w["frame"]
            n, along = wf["normal"], wf["long"]
            c = oc0 - n * (oc0 - Vector((wf["center"].x, wf["center"].y, 0.0))).dot(n)   # 벽 두께 중심선으로 투영
            hyps.append((n, along, wf["thick"], c, True))
        # 문·창 자신의 방향 (벽이 한 메시로 합쳐졌거나 곡선이어도 통함): 닫힌 문·창은 자기 긴 축이 벽 방향
        axes = [(f["normal"], f["long"])]
        # 주변 벽면의 법선 (문짝이 비스듬히 열려 있어도 벽 방향은 벽면이 알려 준다)
        for z in (z_probe, zmax + 0.1):
            for w in cands:
                loc, nrm, _i, dist = w["bvh"].find_nearest(Vector((oc0.x, oc0.y, z)))
                if loc is not None and dist < leaf and math.hypot(nrm.x, nrm.y) > 0.7:
                    a = Vector((nrm.x, nrm.y, 0.0)).normalized()
                    b = Vector((-a.y, a.x, 0.0))
                    for n_, al in ((a, b), (b, a)):
                        if all(abs(n_.dot(x[0])) < 0.996 for x in axes):
                            axes.append((n_, al))
        for n, along in axes:
            t0, off0 = local_t(oc0, n)
            hyps.append((n, along, t0 or 0.3, oc0 + n * off0, False))
        fallback = hyps[0]
        if kind == "door":
            # 열린 문짝: 경첩(문짝 한쪽 끝)에서 문짝과 직각 방향으로 벽이 이어진다
            for sgn in (1, -1):
                n = f["long"] * sgn
                h = oc0 + n * (f["length"] / 2)
                th, offh = local_t(h + n * 0.1, n)
                hyps.append((n, f["normal"], th or 0.3, h + n * (0.1 + offh if th else 0.15), False))
        # 가설마다 실제 구멍을 찾고 "문짝 폭과 맞고 문짝 바로 옆에 있는 구멍"을 고른다
        # (90° 열린 문짝은 옆벽에 붙어 있어서 bbox 만으로는 옆벽을 고르기 쉽다)
        best = None
        for n, along, t, c, wall_axis in hyps:
            near = _near(solids, Vector((c.x - search - 0.5, c.y - search - 0.5, zmin - 0.5)),
                         Vector((c.x + search + 0.5, c.y + search + 0.5, zmax + 0.5)))
            for off, width, hit_edge in find_openings(c, n, along, t, z_probe, search, near):
                if hit_edge and not wall_axis:
                    continue        # 추정한 방향에서 끝없이 뚫린 구간 = 구멍이 아니라 방 안 빈 공간
                oc = c + along * off
                dx = max(omin.x - oc.x, 0.0, oc.x - omax.x)
                dy = max(omin.y - oc.y, 0.0, oc.y - omax.y)
                wd = leaf if hit_edge else width
                if math.hypot(dx, dy) > wd / 2 + 0.15:
                    continue        # 구멍은 문·창과 붙어 있어야 한다 (벽 끝 너머 바깥 공간 등 배제)
                score = math.hypot(dx, dy) + abs(wd - leaf) + (1.0 if hit_edge else 0.0)
                if best is None or score < best[0]:
                    best = (score, n, along, t, oc, wd, near)

        def nearest_wall(p):
            q = Vector((p.x, p.y, z_probe))
            return min(cands, key=lambda w: (w["bvh"].find_nearest(q)[3] or 1e9))
        hole = None
        if best is None:
            n, along, t, c, _wa = fallback
            w = nearest_wall(c)
            width = leaf
            add("error", "opening_not_cut", o["name"],
                f"{w['name']}에 {kind} 구멍이 없습니다(벽을 가로지르는 레이가 모두 막힘). Boolean으로 뚫거나 벽을 나눠 만드세요.")
        else:
            _score, n, along, t, c, width, near = best
            tr, offr = local_t(c, n)                 # 찾은 구멍 자리에서 벽 두께·중심선을 다시 맞춤
            if tr is not None and abs(offr) < 0.3:
                t, c = tr, c + n * offr
            w = nearest_wall(c)
            # 구멍 아래 끝은 양옆 바닥보다 내려가지 않는다 (바닥까지 내려온 유리문·창)
            tops = [classify(Vector((c.x, c.y, z_probe)) + n * sg * (t / 2 + 0.3))["top"] for sg in (1, -1)]
            tops = [x for x in tops if x is not None and x <= z_probe]
            zlo = max(zmin - 0.6, min(tops)) if tops else zmin - 0.6
            hole = hole_vertical(near, c, n, t, z_probe, zlo, zmax + 0.6)
        open_leaf = abs(f["long"].dot(along)) < 0.5       # 문짝이 벽과 60° 이상 벌어짐 = 열린 문
        probe_z = zmin + 1.0 if kind == "door" else (zmin + zmax) / 2
        if hole is not None:
            probe_z = (hole[0] + hole[1]) / 2 if kind == "window" else min(hole[0] + 1.0, (hole[0] + hole[1]) / 2)
        sides = []
        for sgn in (1, -1):
            d = n * sgn
            start = Vector((c.x, c.y, probe_z)) + d * (t / 2 + 0.01)
            ahead = _cast(_near(solids + furniture, start - Vector((3, 3, 1)), start + Vector((3, 3, 1))), start, d, 3.0)
            side = classify(start + d * 0.5)
            if side["kind"] != "room":
                # 창 앞에 걸터앉는 턱(베이창·飘窗)·화단 같은 게 있으면 한 걸음 더 들어가 본다
                p5 = start + d * 0.5
                under = _cast([x for x in units if x["role"] not in ("floor", "ground")], p5, Vector((0, 0, -1)), 5.0)
                if under is not None and under[2]["role"] in ("furniture", "trim"):
                    for dist in (1.0, 1.5):
                        s2 = classify(start + d * dist)
                        if s2["kind"] == "room":
                            side = s2
                            break
            side["dir"] = d
            side["start"] = start
            side["ahead"] = (ahead[1], ahead[2]) if ahead else None
            sides.append(side)
        return {"wall": w, "n": n, "along": along, "t": t, "c": c, "width": width, "zmin": zmin, "zmax": zmax,
                "sides": sides, "open_leaf": open_leaf, "hole": hole, "cut": best is not None}

    def intrudes(fu, origin, d, along, depth, width, z0, z1):
        """가구 fu 가 (origin 에서 d 방향 depth, along 방향 ±width/2, 높이 z0~z1) 상자 안으로 들어오는가."""
        zb = _zone_aabb(origin, d, depth, along, width, z0, z1)
        if _aabb_overlap(zb, fu["bbox"]) <= 0.0:
            return False
        V = fu["verts"]
        for v in V[::max(1, len(V) // 5000)]:
            r = v - origin
            if 0.0 <= r.dot(d) <= depth and abs(r.dot(along)) <= width / 2 and z0 <= v.z <= z1:
                return True
        corners = []
        for dd in (0.0, depth):
            for ww in (-width / 2, width / 2):
                for zz in (z0, z1):
                    q = origin + d * dd + along * ww
                    corners.append(Vector((q.x, q.y, zz)))
        box_faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
        return bool(BVHTree.FromPolygons(corners, box_faces).overlap(fu["bvh"]))

    def glazed(u):
        words = ("glass", "glazing", "glazed", "玻璃", "유리")
        for m in u["meshes"]:
            names = [m.name.lower()] + [s.material.name.lower() for s in m.material_slots if s.material]
            if any(wd in nm for nm in names for wd in words):
                return True
        return False

    # --- 문
    door_holes = []
    for o in doors:
        r = opening_report(o, "door")
        if r is None:
            continue
        if r["cut"]:
            door_holes.append((r["c"], r["along"], r["n"], r["t"], r["width"]))
        h = r["zmax"] - r["zmin"]
        if not r["open_leaf"] and not (L["door_h"][0] <= h <= L["door_h"][1]):
            add("warning", "door_size", o["name"], f"문 높이 {h:.2f} m (상식 범위 {L['door_h'][0]}~{L['door_h'][1]} m)")
        is_glazed = glazed(o)
        if not (L["door_w"][0] <= r["width"] <= (L["glazed_door_w_max"] if is_glazed else L["door_w"][1])):
            add("warning", "door_size", o["name"], f"문(구멍) 폭 {r['width']:.2f} m (상식 범위 {L['door_w'][0]}~{L['door_w'][1]} m)")
        tops = [s["top"] for s in r["sides"] if s["kind"] == "room" and s["top"] is not None]
        ref = max(tops) if tops else max((s["top"] for s in r["sides"] if s["top"] is not None), default=None)
        if ref is not None:
            gap = r["zmin"] - ref
            if gap > L["door_float"]:
                add("error", "door_floating", o["name"], f"문 아랫단이 바닥보다 {gap:.2f} m 떠 있습니다.")
            elif gap < -L["door_float"]:
                add("error", "door_sunk", o["name"], f"문 아랫단이 바닥보다 {-gap:.2f} m 아래에 박혀 있습니다.")
        names = []
        for s in r["sides"]:
            if s["ahead"] is not None and s["ahead"][1]["role"] in ("wall", "column") and s["ahead"][0] < L["door_front_wall"]:
                add("error", "door_faces_wall", o["name"],
                    f"문을 지나면 {s['ahead'][0]:.2f} m 앞이 벽({s['ahead'][1]['name']})입니다. 지나갈 수 없는 문.")
            if s["kind"] == "void":
                add("error", "door_to_void", o["name"], "문 한쪽 아래에 바닥도 지면도 없습니다(허공으로 나가는 문).")
            elif ref is not None and s["top"] is not None and ref - s["top"] > L["door_drop"]:
                add("error", "door_to_drop", o["name"],
                    f"문 한쪽이 {ref - s['top']:.2f} m 낭떠러지입니다(발코니·계단 없이 밖으로 나가는 문).")
            names.append(s["unit"]["name"] if s["kind"] == "room" else ("EXTERIOR" if s["kind"] == "exterior" else None))
            # 문 앞: ① 통로(폭 0.6 m × 깊이 0.6 m)를 막으면 오류, ② 여유 공간(문 폭 × 문 폭, 최대 1 m —
            # SAGE 배치 솔버의 문 앞 비움 구역)에 걸리면 경고. 실제 형상으로 판정(회전된 가구의 bbox 과대평가 방지)
            origin = Vector((r["c"].x, r["c"].y, 0)) + s["dir"] * (r["t"] / 2)
            fz = s["top"] if s["top"] is not None else r["zmin"]
            near_f = [fu for fu in furniture if fu["bbox"][1].z - fu["bbox"][0].z >= 0.03]   # 러그 등 바닥 깔개 제외
            # 문 폭 안 어디든 폭 0.6 m 통로가 하나라도 비어 있으면 지나갈 수 있다 (넓은 미닫이·양개문 포함)
            pw = min(r["width"], L["passage_min"])
            span = max(0.0, (r["width"] - pw) / 2)
            offsets = [0.0] + [k * 0.1 * sg for k in range(1, int(span / 0.1) + 1) for sg in (1, -1)]
            blockers_by_strip = []
            for off in offsets:
                org = origin + r["along"] * off
                hit = [fu["name"] for fu in near_f if intrudes(fu, org, s["dir"], r["along"], L["passage_min"], pw,
                                                               fz + 0.05, fz + 1.8)]
                blockers_by_strip.append(hit)
                if not hit:
                    break
            if blockers_by_strip and all(blockers_by_strip):
                who = sorted({nm for strip in blockers_by_strip for nm in strip})
                # 0.45 m 폭이라도 비어 있으면 '좁은 통로'(경고), 그마저 없으면 '막힘'(오류)
                pn = min(r["width"], L["passage_narrow"])
                sp = max(0.0, (r["width"] - pn) / 2)
                offs = [0.0] + [k * 0.05 * sg for k in range(1, int(sp / 0.05) + 1) for sg in (1, -1)]
                narrow_ok = any(not any(intrudes(fu, origin + r["along"] * off, s["dir"], r["along"], L["passage_min"], pn,
                                                 fz + 0.05, fz + 1.8) for fu in near_f) for off in offs)
                if narrow_ok:
                    add("warning", "door_narrow", o["name"],
                        f"{', '.join(who)} 때문에 문을 지나는 통로가 {L['passage_narrow']}~{L['passage_min']} m 로 좁습니다.")
                else:
                    add("error", "door_blocked", o["name"], f"문을 지나자마자(0.6 m 안) {', '.join(who)}가 통로를 막고 있습니다.")
            elif r["width"] <= L["door_clearance_max_w"]:
                # 여닫이 문 앞 여유 공간(문 폭 × 문 폭, 최대 1 m — SAGE 배치 솔버의 문 앞 비움 구역)
                # 벽에 붙은 얇은 물건(그림·스위치·후크)은 문짝이 스치지 않으므로 제외
                standing = [fu for fu in near_f if not (min(fu["frame"]["length"], fu["frame"]["thick"]) < 0.10
                                                        and fu["bbox"][0].z > fz + 0.25)]
                hit = [fu["name"] for fu in standing if intrudes(fu, origin, s["dir"], r["along"], min(max(r["width"], 0.8), 1.0),
                                                                 r["width"], fz + 0.05, fz + 2.0)]
                if hit:
                    add("warning", "door_clearance", o["name"],
                        f"문 앞 여유 공간(문 폭 × 문 폭)에 {', '.join(hit)}가 걸립니다(여닫이라면 문이 부딪히거나 동선이 좁음).")
        a, b = names
        openings_out.append({"name": o["name"], "kind": "door", "wall": r["wall"]["name"], "width_m": round(r["width"], 2),
                             "at": [round(r["c"].x, 2), round(r["c"].y, 2)], "sides": names, "open_leaf": r["open_leaf"]})
        if a is not None and a == b and a != "EXTERIOR":
            add("warning", "door_same_room", o["name"], f"문 양쪽이 같은 방({a})입니다. 의미 없는 문.")
        if not r["cut"]:
            continue                   # 구멍 없는 문(벽에 붙인 그림 같은 문)은 방을 잇지 않는다
        for nm in (a, b):
            if nm in room_info:
                room_info[nm]["doors"].append(o["name"])
        # 밖(외부·발코니)으로 난 유리문은 창처럼 빛이 들어온다
        if glazed(o):
            for nm, other in ((a, b), (b, a)):
                if nm in room_info and (other == "EXTERIOR" or (other in room_info and
                                                                _room_type(room_info[other]["unit"]["root"]) == "outdoor")):
                    room_info[nm]["glazed_doors"].append(o["name"])
        if a and b and a != b:
            graph.setdefault(a, set()).add(b)
            graph.setdefault(b, set()).add(a)

    # --- 창문
    window_rows = []
    for o in windows:
        r = opening_report(o, "window")
        if r is None:
            continue
        wz0, wz1 = r["hole"] if r["hole"] else (r["zmin"], r["zmax"])    # 커튼·창틀 장식이 아니라 실제 유리 구멍 높이
        h = wz1 - wz0
        if not (L["window_w"][0] <= r["width"] <= L["window_w"][1]) or not (L["window_h"][0] <= h <= L["window_h"][1]):
            add("warning", "window_size", o["name"], f"창 크기 {r['width']:.2f} × {h:.2f} m 가 상식 범위를 벗어납니다.")
        rooms = [s for s in r["sides"] if s["kind"] == "room"]
        outs = [s for s in r["sides"] if s["kind"] != "room"]
        floor_top = max((s["top"] for s in rooms), default=None)
        if floor_top is None:
            floor_top = max((s["top"] for s in r["sides"] if s["top"] is not None), default=0.0)
        sill = wz0 - floor_top
        if sill < -0.02:
            add("error", "window_below_floor", o["name"], f"창 아랫단이 바닥보다 {-sill:.2f} m 아래입니다.")
        elif L["sill_awkward"][0] < sill < L["sill_awkward"][1]:
            add("warning", "window_awkward_sill", o["name"],
                f"창턱 높이 {sill:.2f} m: 바닥까지 내린 창(0)도 일반 창(0.3 m 이상)도 아닌 어정쩡한 높이입니다.")
        elif sill > L["sill_high"]:
            add("warning", "window_too_high", o["name"], f"창턱 높이 {sill:.2f} m: 사람 눈높이보다 높아 밖이 안 보입니다(의도한 고창이 아니면 이상).")
        for s in rooms:
            ch = _cast(ceilings + floors, Vector((s["start"].x, s["start"].y, s["top"] + 0.05)), Vector((0, 0, 1)), 20.0)
            if ch is not None and wz1 > ch[0].z + 0.01:
                add("error", "window_cuts_ceiling", o["name"], f"창 윗단이 천장보다 {wz1 - ch[0].z:.2f} m 높습니다.")
        if (len(rooms) == 2 and rooms[0]["unit"] is not rooms[1]["unit"]
                and "outdoor" not in (_room_type(rooms[0]["unit"]["root"]), _room_type(rooms[1]["unit"]["root"]))):
            add("warning", "interior_window", o["name"],
                f"실내 벽에 난 창입니다({rooms[0]['unit']['name']} ↔ {rooms[1]['unit']['name']}). 외벽이 아니면 이상해 보입니다.")
        for s in outs:
            if s["ahead"] is not None and s["ahead"][1]["role"] in ("wall", "column") and s["ahead"][0] < L["window_front_wall"]:
                add("warning", "window_faces_wall", o["name"], f"창 바깥 {s['ahead'][0]:.2f} m 앞이 벽입니다(열어도 벽만 보이는 창).")
        for s in rooms:
            # 창 면적을 격자로 나눠 방 쪽 0.6 m 안에서 창을 향해 레이 → 가구에 막히는 비율 (수전·화분 가장자리 같은 건 무시)
            origin = Vector((r["c"].x, r["c"].y, 0)) + s["dir"] * (r["t"] / 2)
            cand = [fu for fu in furniture if not _is_curtain(fu["name"])
                    and intrudes(fu, origin, s["dir"], r["along"], 0.6, r["width"], wz0 + 0.05, wz1)]
            if cand:
                hits, total = {}, 0
                for i in range(7):
                    for j in range(5):
                        q = origin + r["along"] * ((i + 0.5) / 7 - 0.5) * r["width"] * 0.95
                        q = Vector((q.x, q.y, wz0 + (j + 0.5) / 5 * (wz1 - wz0)))
                        total += 1
                        hit = _cast(cand, q + s["dir"] * 0.6, -s["dir"], 0.6)
                        if hit is not None:
                            hits[hit[2]["name"]] = hits.get(hit[2]["name"], 0) + 1
                frac = sum(hits.values()) / total
                if frac >= L["window_blocked_frac"]:
                    who = ", ".join(f"{k} {v / total:.0%}" for k, v in sorted(hits.items(), key=lambda kv: -kv[1]))
                    add("warning", "window_blocked", o["name"], f"창 면적의 {frac:.0%}를 가구가 가립니다({who}).")
            if s["unit"]["name"] in room_info:
                room_info[s["unit"]["name"]]["windows"].append(o["name"])
        nn = r["n"] if (r["n"].x > 1e-6 or (abs(r["n"].x) <= 1e-6 and r["n"].y > 0)) else -r["n"]
        line = (round(math.degrees(math.atan2(nn.y, nn.x))), round(r["c"].dot(nn) / 0.3))   # 같은 벽면 = 같은 방향·같은 선
        window_rows.append((o["name"], line, round(floor_top, 1), wz0, wz1, r["wall"]["name"]))
        openings_out.append({"name": o["name"], "kind": "window", "wall": r["wall"]["name"], "width_m": round(r["width"], 2),
                             "at": [round(r["c"].x, 2), round(r["c"].y, 2)], "sill_m": round(sill, 2),
                             "sides": [s["unit"]["name"] if s["kind"] == "room" else s["kind"].upper() for s in r["sides"]]})

    # 같은 벽·같은 층 창들의 높이 정렬
    groups = {}
    for name, line, lvl, zmin, zmax, wall in window_rows:
        groups.setdefault((line, lvl), []).append((name, zmin, zmax, wall))
    for (_line, _lvl), rows in groups.items():
        if len(rows) < 2:
            continue
        head_med = statistics.median(z for _, _, z, _w in rows)
        for name, _zmin, zmax, wall in rows:
            if abs(zmax - head_med) > L["window_align"]:
                add("warning", "window_misaligned", name,
                    f"{wall}의 다른 창들과 윗선 높이가 {abs(zmax - head_med):.2f} m 다릅니다(창 높이가 제각각인 벽).")

    # --- 계단이 잇는 곳: 맨 아래 단이 놓인 방/외부 (층과 층, 테라스와 마당을 잇는 동선)
    stairs = by_role.get("stair", [])
    railings = by_role.get("railing", [])
    for st in stairs:
        low = min(st["per_mesh"], key=lambda mb: mb[1][1].z)[1]
        b = classify(Vector(((low[0].x + low[1].x) / 2, (low[0].y + low[1].y) / 2, low[0].z + 0.01)))
        st["base"] = b["unit"]["name"] if b["kind"] == "room" else "EXTERIOR"

    def stair_at(q, top):
        for st in stairs:
            smin, smax = st["bbox"]
            if smin.x - 0.1 <= q.x <= smax.x + 0.1 and smin.y - 0.1 <= q.y <= smax.y + 0.1 and smax.z >= top - 0.35:
                return st
        return None

    # --- 방 가장자리 스캔: 문짝 없는 출입구, 유리 없는 창 구멍, 벽이 빠진 가장자리 (형상 기반)
    blockers = solids + doors + windows + trims
    step = L["sample_step"]
    for u in floors:
        info = room_info[u["name"]]
        outdoor = _room_type(u["root"]) == "outdoor"
        top = u["bbox"][1].z
        open_edges = []
        for pa, d, n, length in _top_boundary(u):
            labels = []
            k = max(1, int((length - 0.2) / step) + 1)
            for i in range(k):
                s_ = 0.1 + i * step if length > 0.2 else length / 2
                p = pa + d * s_
                inner = Vector((p.x, p.y, top)) - n * 0.12
                near = _near(blockers, inner - Vector((1.5, 1.5, 0.1)), inner + Vector((1.5, 1.5, 2.5)))
                res = {}
                for h in (0.3, 1.2, 1.8):
                    hit = _cast(near, Vector((inner.x, inner.y, top + h)), n, 1.2)
                    if hit is None:
                        # 윗부분만 안쪽으로 물러난 계단식 벽(베이창 턱 등): 조금 더 안쪽에서 다시 쏜다
                        deep = inner - n * 0.5
                        hit = _cast(near, Vector((deep.x, deep.y, top + h)), n, 1.7)
                    res[h] = hit[2]["role"] if hit else None
                roles = set(res.values())
                in_hole = any(abs(Vector((p.x - c.x, p.y - c.y, 0)).dot(al)) <= wd / 2 + 0.05 and
                              abs(Vector((p.x - c.x, p.y - c.y, 0)).dot(nn)) <= t_ / 2 + 0.35 for c, al, nn, t_, wd in door_holes)
                if "door" in roles or in_hole:            # 문짝이 열려 있어 레이가 빠져도 문 구멍 자리면 문
                    labels.append(("door", None))
                elif "window" in roles:
                    labels.append(("window", None))
                elif res[0.3] is None and res[1.2] is None:
                    q = Vector((p.x, p.y, top + 1.0)) + n * 0.6
                    b = classify(q)
                    drop = top - b["top"] if b["top"] is not None else None
                    st = stair_at(q, top)
                    guarded = railings and any(
                        _cast(_near(railings, inner - Vector((1.5, 1.5, 0.1)), inner + Vector((1.5, 1.5, 1.5))),
                              Vector((inner.x, inner.y, top + h)), n, 1.0) for h in (0.5, 0.9))
                    if b["kind"] == "room" and b["unit"] is not u and abs(b["top"] - top) <= 0.35:
                        labels.append(("passage", b["unit"]["name"]))
                    elif b["kind"] == "room" and b["unit"] is u:
                        labels.append(("inside", None))
                    elif st is not None:
                        labels.append(("stair", st["name"]))
                    elif guarded:
                        labels.append(("guarded", None))
                    elif b["kind"] == "void" or (b["kind"] == "exterior" and b.get("unmodeled")):
                        labels.append(("open_void", None))
                    elif drop is not None and drop > (L["guard_drop"] if outdoor else L["door_drop"]):
                        labels.append(("open_drop", None))
                    elif b["kind"] == "room" and drop is not None and drop > 0:
                        labels.append(("step_down", b["unit"]["name"]))   # 낮은 단차로 이어진 옆 방(발코니 등)
                    else:
                        labels.append(("open_exterior", None))
                elif res[0.3] is not None and (res[1.2] is None or res[1.8] is None):
                    labels.append(("window_opening", None))
                else:
                    labels.append(("wall", None))
            for lab, pay, run, i0 in _runs(labels, step):
                mid = pa + d * (0.1 + (i0 + run / step / 2 - 0.5) * step if length > 0.2 else length / 2)
                where = f"({mid.x:.1f}, {mid.y:.1f})"
                if lab in ("passage", "step_down") and run >= L["passage_min"]:
                    info["passages"].add(pay)
                    graph.setdefault(u["name"], set()).add(pay)
                    graph.setdefault(pay, set()).add(u["name"])
                elif lab == "stair" and run >= L["passage_min"]:
                    base = next(s["base"] for s in stairs if s["name"] == pay)
                    info["passages"].add(pay)
                    if base != u["name"]:
                        graph.setdefault(u["name"], set()).add(base)
                        graph.setdefault(base, set()).add(u["name"])
                elif lab == "window_opening" and run >= L["window_opening_min"]:
                    info["glassless"].append(f"{run:.1f} m @ {where}")
                elif lab == "open_void" and outdoor and not has_ground and run >= L["open_edge_min"]:
                    graph.setdefault(u["name"], set()).add("EXTERIOR")   # 외부가 없는 모델의 발코니: 높이를 알 수 없음
                    graph["EXTERIOR"].add(u["name"])
                elif lab in ("open_void", "open_drop") and run >= L["open_edge_min"]:
                    open_edges.append(f"{run:.1f} m({'허공' if lab == 'open_void' else '낭떠러지'}) @ {where}")
                elif lab == "open_exterior" and run >= L["open_edge_min"]:
                    graph.setdefault(u["name"], set()).add("EXTERIOR")
                    graph["EXTERIOR"].add(u["name"])
                    if not outdoor and run > L["open_exterior_max"]:
                        open_edges.append(f"{run:.1f} m(외벽 없이 밖으로 통째로 뚫림) @ {where}")
        if open_edges:
            add("warning", "room_edge_open", u["name"],
                f"벽·난간 없이 뚫린 가장자리: {', '.join(open_edges)}. 벽이 빠졌거나, 출입구로 보기엔 너무 넓거나, 외부가 모델링되지 않았습니다.")

    # --- 가구 → 방 소속
    for fu in furniture:
        bmin, bmax = fu["bbox"]
        p = Vector(((bmin.x + bmax.x) / 2, (bmin.y + bmax.y) / 2, bmin.z + 0.05))
        hit = _cast(floors, p, Vector((0, 0, -1)), 0.5)
        if hit is not None:
            room_info[hit[2]["name"]]["furniture"].append(fu["name"])

    # --- 방
    reach = set()
    stack = ["EXTERIOR"]
    while stack:
        cur = stack.pop()
        if cur in reach:
            continue
        reach.add(cur)
        stack.extend(graph.get(cur, ()))
    has_entrance = bool(graph["EXTERIOR"])
    rooms_out, total_area, circ_area = [], 0.0, 0.0
    for name, info in room_info.items():
        u = info["unit"]
        f = u["frame"]
        rtype = _room_type(u["root"])
        area = _top_area(u) or f["length"] * f["thick"]
        w_, d_ = f["length"], f["thick"]
        aspect = w_ / max(d_, 1e-6)
        top = u["bbox"][1].z
        # 천장고: 방 가운데 5×5 지점에서 위로 쏜 레이 중 가장 낮은 천장 (격자 천장은 막대 사이로 레이가 빠지므로 여러 점)
        over = ceilings + [x for x in floors if x is not u]
        hs = []
        for i in (-2, -1, 0, 1, 2):
            for j in (-2, -1, 0, 1, 2):
                q = f["center"] + f["long"] * (i * min(0.3, w_ * 0.12)) + f["normal"] * (j * min(0.3, d_ * 0.12))
                ch = _cast(over, Vector((q.x, q.y, top + 0.05)), Vector((0, 0, 1)), 20.0)
                if ch is not None:
                    hs.append(ch[0].z - top)
                # 격자 천장: 막대 사이로 레이가 빠져도 머리 위 가까운 천장 면(막대 밑면)을 천장으로 본다
                qh = Vector((q.x, q.y, top + 1.8))
                for cu in _near(ceilings, qh - Vector((1.0, 1.0, 0.0)), qh + Vector((1.0, 1.0, 1.0))):
                    loc, _n, _i, _d = cu["bvh"].find_nearest(qh, 1.0)
                    if loc is not None and loc.z > top + 1.5:
                        hs.append(loc.z - top)
        ceil_h = min(hs) if hs else None
        total_area += area
        if rtype == "circulation":
            circ_area += area
        openings = len(set(info["doors"])) + len(info["passages"])
        n_windows = len(set(info["windows"])) + len(info["glassless"]) + len(set(info["glazed_doors"]))
        row = {"name": name, "type": rtype, "area_m2": round(area, 2), "size_m": [round(w_, 2), round(d_, 2)],
               "ceiling_h_m": round(ceil_h, 2) if ceil_h is not None else None,
               "doors": len(set(info["doors"])), "passages": sorted(info["passages"]),
               "windows": len(set(info["windows"])), "glassless_window_openings": info["glassless"],
               "glazed_doors_to_outside": sorted(set(info["glazed_doors"])),
               "furniture": len(info["furniture"])}
        rooms_out.append(row)
        if rtype == "outdoor":
            continue
        if openings == 0:
            add("error", "sealed_room", name, "문도 출입구도 없는 밀폐된 방입니다.")
        elif has_entrance and name not in reach:
            add("error", "unreachable_room", name, "입구에서 문·출입구를 따라 갈 수 없는 방입니다.")
        if info["glassless"]:
            add("warning", "window_opening_without_glass", name,
                f"유리(창 오브젝트) 없는 창 구멍 {len(info['glassless'])}곳: {', '.join(info['glassless'])} (폭 @ 위치). 유리를 넣거나 의도한 개구부인지 확인하세요.")
        if rtype in ("habitable", "unknown") and n_windows == 0:
            add("warning", "windowless_room", name, f"창이 없는 {'거실·침실 등 생활 공간' if rtype == 'habitable' else '방'}입니다.")
        if rtype == "circulation":
            if d_ < L["corridor_min_w"]:
                add("warning", "corridor_too_narrow", name, f"복도 폭 {d_:.2f} m")
        elif aspect > L["corridor_aspect"]:
            add("warning", "corridor_like_room", name, f"가로세로비 {aspect:.1f}:1 — 방이 아니라 복도처럼 길쭉합니다.")
        if ceil_h is None:
            add("warning", "no_ceiling", name, "방 위에 천장·지붕이 없습니다.")
        elif not (L["ceiling_h"][0] <= ceil_h <= L["ceiling_h"][1]):
            add("warning", "ceiling_height", name, f"천장 높이 {ceil_h:.2f} m (상식 범위 {L['ceiling_h'][0]}~{L['ceiling_h'][1]} m)")
        if rtype in ("habitable", "unknown", "interior") and not info["furniture"]:
            add("warning", "empty_room", name, "가구가 하나도 없는 빈 방입니다.")
        row["windows_total"] = n_windows
    if floors and (doors or any(r["passages"] for r in rooms_out)) and not has_entrance:
        add("error", "no_entrance", "(building)", "외부로 통하는 문·출입구가 하나도 없습니다.")

    # 똑같은 빈 방의 반복
    sig = {}
    for row in rooms_out:
        if row["furniture"] == 0 and row["type"] != "outdoor":
            key = (round(row["size_m"][0], 1), round(row["size_m"][1], 1), row["ceiling_h_m"], row.get("windows_total", 0))
            sig.setdefault(key, []).append(row["name"])
    repeated = [v for v in sig.values() if len(v) >= L["repeat_rooms"]]
    for names in repeated:
        add("warning", "repetitive_empty_rooms", ", ".join(names), f"크기가 같은 빈 방 {len(names)}개가 반복됩니다.")

    # --- 벽
    everything = [u for u in units if u["role"] != "floor"]

    def see_through(mid, n, t, exclude=(), reach=0.1):
        """mid 에서 벽 법선 방향으로 벽 두께(+양쪽 reach)를 가로지를 때 아무것도 없으면 True (정말 뚫려 보임)."""
        o = mid - n * (t / 2 + reach)
        span = t + 2 * reach
        e = o + n * span
        lo = Vector((min(o.x, e.x), min(o.y, e.y), min(o.z, e.z))) - Vector((0.5, 0.5, 0.5))
        hi = Vector((max(o.x, e.x), max(o.y, e.y), max(o.z, e.z))) + Vector((0.5, 0.5, 0.5))
        cand = [u for u in _near(everything, lo, hi) if u["name"] not in exclude]
        return _cast(cand, o, n, span) is None and _cast(cand, o + n * span, -n, span) is None

    for w in walls:
        f = w["frame"]
        straight = w.get("straight", False)
        if straight and not (L["wall_t"][0] <= f["thick"] <= L["wall_t"][1]):
            add("warning", "wall_thickness", w["name"], f"벽 두께 {f['thick']:.2f} m")
        wtop = w["bbox"][1].z
        over = ceilings + floors

        def up(q):
            return _cast(over, Vector((q.x, q.y, wtop - 0.01)), Vector((0, 0, 1)), 1.01, True)

        hit = up(f["center"])
        # 아래를 향한 면(천장 밑면)에 먼저 닿으면 그 사이가 빈 것. 위를 향한 면이면 이미 슬래브 안에서 시작(= 붙어 있음)
        if hit is not None and hit[3].z < 0 and hit[0].z - wtop > L["wall_top_gap"]:
            gap = hit[0].z - wtop
            # 벽 양옆 어느 쪽이든 벽 윗단 높이에 천장(격자 천장·내림 천장 포함)이 붙어 있으면 틈은 그 위 설비 공간이라 안 보인다.
            # 격자 막대 사이로 레이가 빠질 수 있으므로 '벽 옆 0.4 m 안의 가장 가까운 천장 면 높이'로 판단
            covered = False
            for side in (-1, 1):
                for fr in (-0.3, 0.0, 0.3):
                    q = f["center"] + f["long"] * (fr * f["length"]) + f["normal"] * side * (f["thick"] / 2 + 0.2)
                    q = Vector((q.x, q.y, wtop + 0.01))
                    for cu in _near(ceilings, q - Vector((0.4, 0.4, 0.4)), q + Vector((0.4, 0.4, 0.4))):
                        loc, _n, _i, _d = cu["bvh"].find_nearest(q, 0.4)
                        if loc is not None and loc.z <= wtop + L["wall_top_gap"] + 0.03:
                            covered = True
                            break
                    if covered:
                        break
                if covered:
                    break
            mid = Vector((f["center"].x, f["center"].y, wtop + gap / 2))
            # 양쪽 0.6 m 까지 트여 있어야 '건너편이 보이는' 틈 (윗부분만 안쪽으로 물러난 계단식 벽은 제외)
            if not covered and see_through(mid, f["normal"], f["thick"], reach=0.6):
                add("error", "wall_short_of_ceiling", w["name"], f"벽 위와 천장 사이가 {gap:.2f} m 비어 있어 건너편이 보입니다.")
        if not straight:
            continue  # 곡선·꺾인 벽은 끝점 개념이 모호하므로 틈 검사 생략
        others = [x for x in walls + by_role.get("column", []) if x is not w]
        openings = doors + windows
        for sgn in (1, -1):
            end = Vector((f["center"].x, f["center"].y, f["center"].z)) + f["long"] * sgn * (f["length"] / 2)
            # 벽 끝면 위의 여러 점(두께 양쪽 × 높이 3단)에서 이웃 벽까지의 최소 거리. L자·T자로 맞물리면 0
            pts = [end]
            for side in (-1, 1):
                for hz in (w["bbox"][0].z + 0.1, f["center"].z, w["bbox"][1].z - 0.1):
                    q = end + f["normal"] * side * (f["thick"] / 2)
                    pts.append(Vector((q.x, q.y, hz)))
            best = None
            for x in others:
                if min(end[i] - x["bbox"][1][i] if end[i] > x["bbox"][1][i] else x["bbox"][0][i] - end[i]
                       if end[i] < x["bbox"][0][i] else 0.0 for i in range(3)) > L["wall_end_gap"][1] + 0.1:
                    continue
                dmin, near = None, None
                for q in pts:
                    if all(x["bbox"][0][i] - 0.002 <= q[i] <= x["bbox"][1][i] + 0.002 for i in range(3)):
                        dmin, near = 0.0, q
                        break
                    loc, _n, _i, dist = x["bvh"].find_nearest(q)
                    if loc is not None and (dmin is None or dist < dmin):
                        dmin, near = dist, loc
                if dmin is not None and (best is None or dmin < best[0]):
                    best = (dmin, near, x)
            if best is None:
                continue
            dist, loc, x = best
            if L["wall_end_gap"][0] < dist < L["wall_end_gap"][1]:
                mid = (end + loc) / 2
                if any(all(o["bbox"][0][i] - 0.02 <= mid[i] <= o["bbox"][1][i] + 0.02 for i in range(3)) for o in openings):
                    continue
                # 틈을 벽 법선 방향으로 실제로 관통할 수 있을 때만 (다른 조각이 메웠으면 정상)
                probes = [Vector((mid.x, mid.y, w["bbox"][0].z + hz * (w["bbox"][1].z - w["bbox"][0].z))) for hz in (0.25, 0.6)]
                if any(see_through(pm, f["normal"], f["thick"]) or see_through(pm, f["long"], dist + 0.02) for pm in probes):
                    add("error", "wall_gap", w["name"], f"{x['name']}와 벽 끝 사이 {dist:.2f} m 틈으로 건너편이 보입니다.")

    # --- 계단
    for st in by_role.get("stair", []):
        cand = [mb for mb in st["per_mesh"] if {"step", "tread", "steps"} & set(sa._name_tokens(mb[0].name))]
        steps = sorted(cand or st["per_mesh"], key=lambda mb: mb[1][1].z)
        if len(steps) < 3:
            add("warning", "stair_unanalyzable", st["name"], "단이 개별 메시가 아니라서 단 높이를 검사할 수 없습니다(단을 자식 메시로 나누세요).")
            continue
        tops = [bb[1].z for _, bb in steps]
        centers = [((bb[0] + bb[1]) / 2) for _, bb in steps]
        risers = [b - a for a, b in zip(tops, tops[1:])]
        treads = [math.hypot(b.x - a.x, b.y - a.y) for a, b in zip(centers, centers[1:])]
        base = _cast(ground_like, Vector((centers[0].x, centers[0].y, steps[0][1][0].z + 0.01)), Vector((0, 0, -1)), 5.0)
        if base is not None:
            risers.insert(0, tops[0] - base[0].z)
        if max(risers) - min(risers) > L["riser_spread"]:
            add("error", "stair_uneven_risers", st["name"],
                f"단 높이가 제각각입니다({min(risers):.3f}~{max(risers):.3f} m). 사람이 걸려 넘어지는 계단.")
        r_med = statistics.median(risers)
        t_med = statistics.median(treads) if treads else 0.0
        if not (L["riser"][0] <= r_med <= L["riser"][1]):
            add("warning", "stair_riser", st["name"], f"단 높이 {r_med:.3f} m (상식 범위 {L['riser'][0]}~{L['riser'][1]} m)")
        if treads and not (L["tread"][0] <= t_med <= L["tread"][1]):
            add("warning", "stair_tread", st["name"], f"단 너비 {t_med:.3f} m (상식 범위 {L['tread'][0]}~{L['tread'][1]} m)")
        if treads and not (L["blondel"][0] <= 2 * r_med + t_med <= L["blondel"][1]):
            add("warning", "stair_blondel", st["name"], f"2×단높이+단너비 = {2 * r_med + t_med:.3f} m (보폭 공식 0.55~0.70 m 밖)")
        last_top, last_c = tops[-1], centers[-1]
        landing = False
        for g in ground_like + [x for x in furniture if "landing" in sa._name_tokens(x["name"])]:
            gt = g["bbox"][1].z
            if last_top - 0.02 <= gt <= last_top + r_med + 0.03:
                gmin, gmax = g["bbox"]
                dx = max(gmin.x - last_c.x, 0, last_c.x - gmax.x)
                dy = max(gmin.y - last_c.y, 0, last_c.y - gmax.y)
                if math.hypot(dx, dy) < 1.0:
                    landing = True
                    break
        if not landing:
            add("error", "stair_to_nowhere", st["name"], "계단 맨 위가 어떤 바닥에도 이어지지 않습니다.")

    # --- 앉는 가구(앞뒤가 있는 것)가 코앞의 벽을 보고 있음. 앞면 = 등받이 반대쪽(판별 안 되면 로컬 -Y 규약)
    for fu in furniture:
        toks = sa._name_tokens(fu["name"])
        if not any(t in SEATING for t in toks) or any(t in sa.ACCESSORY_TOKENS for t in toks):
            continue
        f = fu["frame"]
        front, basis = -f["ay"], "-Y 규약"
        # 등받이(높은 부분)가 한쪽으로 쏠려 있으면 그 반대쪽이 앞면 (회전이 정점에 박힌 모델도 처리)
        bmin, bmax = fu["bbox"]
        zc = bmin.z + 0.65 * (bmax.z - bmin.z)
        hi = [v for v in fu["verts"][::max(1, len(fu["verts"]) // 20000)] if v.z > zc]
        if hi:
            off = Vector((sum(v.x for v in hi) / len(hi) - (bmin.x + bmax.x) / 2,
                          sum(v.y for v in hi) / len(hi) - (bmin.y + bmax.y) / 2, 0.0))
            if off.length > 0.12 * max(bmax.x - bmin.x, bmax.y - bmin.y):
                front, basis = -off.normalized(), "등받이 반대쪽"
        start = Vector((f["center"].x, f["center"].y, fu["bbox"][0].z + 0.5))
        cand = [x for x in _near(solids + furniture, start - Vector((5, 5, 1)), start + Vector((5, 5, 1))) if x is not fu]
        hit = _cast(cand, start, front, 5.0)
        if hit is not None and hit[2]["role"] in ("wall", "column"):
            sample = fu["verts"][::max(1, len(fu["verts"]) // 20000)]
            gap = hit[1] - (max(v.dot(front) for v in sample) - start.dot(front))
            if gap < L["seat_front_wall"]:
                add("warning", "seat_faces_wall", fu["name"],
                    f"앞면({basis}) {max(gap, 0):.2f} m 앞이 벽({hit[2]['name']})입니다(벽을 보고 앉는 배치).")

    # --- 종합: 백룸 위험도
    reasons = []
    hab = [r for r in rooms_out if r["type"] in ("habitable", "unknown")]
    if hab and sum(1 for r in hab if r.get("windows_total", 0) == 0) / len(hab) >= 0.5:
        reasons.append("생활 공간의 절반 이상에 창이 없음")
    if total_area > 0 and circ_area / total_area > L["corridor_fraction"]:
        reasons.append(f"복도 면적 비율 {circ_area / total_area:.0%}")
    if sum(1 for i in issues if i["code"] == "corridor_like_room") >= 2:
        reasons.append("복도처럼 길쭉한 방이 여러 개")
    lived = [r for r in rooms_out if r["type"] in ("habitable", "unknown", "interior")]
    if lived and sum(1 for r in lived if r["furniture"] == 0) / len(lived) >= 0.5:
        reasons.append("생활 공간의 절반 이상이 빈 방")
    if repeated:
        reasons.append("똑같은 빈 방의 반복")
    if any(i["code"] in ("sealed_room", "unreachable_room", "no_entrance") for i in issues):
        reasons.append("갈 수 없거나 밀폐된 방")
    if any(i["code"] in ("door_faces_wall", "door_to_void", "door_to_drop") for i in issues):
        reasons.append("어디로도 안 가는 문")
    risk = "high" if len(reasons) >= 3 else ("medium" if reasons else "low")

    notes = []
    if not has_ground:
        notes.append("외부 지면(Ground/Terrain)이 없어 모델 바깥은 '모델링되지 않은 외부'로 보았습니다.")
    bent = [w["name"] for w in walls if not w.get("straight")]
    if bent:
        notes.append(f"직선이 아닌 벽 {len(bent)}개(곡선·꺾임·구멍 많음)는 두께·끝 틈 검사를 생략했습니다: {', '.join(bent[:8])}")
    report = {
        "rooms": rooms_out,
        "openings": openings_out,
        "issues": issues,
        "summary": {
            "rooms": len(rooms_out), "doors": len(doors), "windows": len(windows), "walls": len(walls),
            "trim": len(trims), "errors": sum(1 for i in issues if i["severity"] == "error"),
            "warnings": sum(1 for i in issues if i["severity"] == "warning"),
            "liminal_risk": risk, "liminal_reasons": reasons, "collection": collection, "notes": notes,
        },
    }
    return report


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    collection, out = None, None
    for k, v in zip(argv[::2], argv[1::2]):
        if k == "--collection":
            collection = v
        elif k == "--out":
            out = v
    text = json.dumps(audit_building(collection=collection), ensure_ascii=False, indent=2)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
    print(text)


if __name__ != "building_audit":
    main()
