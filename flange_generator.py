# Flange Design using Blender
#
bl_info = {
    "name": "Flange Generator",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Flange Tab",
    "description": "Create parametric flanges with custom bolt holes",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

import bpy
import math
from mathutils import Vector
import bmesh

# 플랜지 생성 함수
def create_flange(outer_diameter, inner_diameter, thickness, bolt_holes, bolt_diameter, pcd):
    # Blender에서는 기본적으로 미터 단위를 사용하므로 mm에서 미터로 변환
    scale_factor = 0.001  # 1mm = 0.001m

    # 치수를 미터로 변환
    outer_radius = (outer_diameter / 2) * scale_factor
    inner_radius = (inner_diameter / 2) * scale_factor
    thickness_m = thickness * scale_factor
    bolt_radius = (bolt_diameter / 2) * scale_factor
    pcd_radius = (pcd / 2) * scale_factor

    # 플랜지 기본 형태 생성 (실린더)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64,  # 원형 품질을 위해 충분한 정점 사용
        radius=outer_radius,
        depth=thickness_m,
        location=(0, 0, 0)
    )
    flange = bpy.context.active_object
    flange.name = "Flange"

    # 내부 구멍 생성 (불리언 연산 사용)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64,
        radius=inner_radius,
        depth=thickness_m * 2,  # 확실한 관통을 위해 두 배 두께 사용
        location=(0, 0, 0)
    )
    inner_hole = bpy.context.active_object
    inner_hole.name = "Inner_Hole"

    # 불리언 연산으로 내부 구멍 생성
    bool_mod = flange.modifiers.new(name="Inner_Hole", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = inner_hole
    bpy.context.view_layer.objects.active = flange
    bpy.ops.object.modifier_apply(modifier="Inner_Hole")

    # 내부 구멍 객체 제거
    bpy.data.objects.remove(inner_hole, do_unlink=True)

    # 볼트홀 생성
    for i in range(bolt_holes):
        # 각 볼트홀의 위치를 계산 (360도를 볼트홀 개수로 나눔)
        angle = math.radians(i * (360 / bolt_holes))
        
        # PCD 반경에 따른 x, y 위치 계산
        x = math.cos(angle) * pcd_radius
        y = math.sin(angle) * pcd_radius
        
        # 볼트홀 생성 (실린더)
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=32,
            radius=bolt_radius,
            depth=thickness_m * 2,  # 확실한 관통을 위해 두 배 두께 사용
            location=(x, y, 0)
        )
        bolt_hole = bpy.context.active_object
        bolt_hole.name = f"Bolt_Hole_{i+1}"
        
        # 불리언 연산으로 볼트홀 생성
        bool_mod = flange.modifiers.new(name=f"Bolt_Hole_{i+1}", type="BOOLEAN")
        bool_mod.operation = "DIFFERENCE"
        bool_mod.object = bolt_hole
        bpy.context.view_layer.objects.active = flange
        bpy.ops.object.modifier_apply(modifier=f"Bolt_Hole_{i+1}")
        
        # 볼트홀 객체 제거
        bpy.data.objects.remove(bolt_hole, do_unlink=True)

    # 재질 추가
    mat = bpy.data.materials.new(name="Flange_Material")
    mat.use_nodes = True
    principled_bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if principled_bsdf:
        # 금속 재질 설정
        principled_bsdf.inputs['Metallic'].default_value = 1.0
        principled_bsdf.inputs['Roughness'].default_value = 0.3
        principled_bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)

    # 재질 할당
    if len(flange.data.materials) == 0:
        flange.data.materials.append(mat)
    else:
        flange.data.materials[0] = mat

    return flange

# 사용자 인터페이스를 위한 패널 클래스 정의
class FlangeGeneratorPanel(bpy.types.Panel):
    """플랜지 생성기 패널"""
    bl_label = "플랜지 생성기"
    bl_idname = "OBJECT_PT_flange_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Flange'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # 사용자 입력 영역
        layout.label(text="플랜지 파라미터 (mm):")
        
        # 플랜지 파라미터
        layout.prop(scene, "flange_outer_diameter")
        layout.prop(scene, "flange_inner_diameter")
        layout.prop(scene, "flange_thickness")
        layout.prop(scene, "flange_bolt_holes")
        layout.prop(scene, "flange_bolt_diameter")
        layout.prop(scene, "flange_pcd")
        
        # 생성 버튼
        layout.operator("object.generate_flange")
        
        # 상태 표시
        if hasattr(scene, "flange_status"):
            layout.label(text=scene.flange_status)

# 플랜지 생성 오퍼레이터 클래스 정의
class OBJECT_OT_GenerateFlange(bpy.types.Operator):
    """플랜지 생성"""
    bl_idname = "object.generate_flange"
    bl_label = "플랜지 생성"
    
    def execute(self, context):
        scene = context.scene
        
        # 입력값 획득
        outer_diameter = scene.flange_outer_diameter
        inner_diameter = scene.flange_inner_diameter
        thickness = scene.flange_thickness
        bolt_holes = scene.flange_bolt_holes
        bolt_diameter = scene.flange_bolt_diameter
        pcd = scene.flange_pcd
        
        # 유효성 검사
        if inner_diameter >= outer_diameter:
            scene.flange_status = "오류: 내경이 외경보다 작아야 합니다"
            return {'CANCELLED'}
        
        if bolt_diameter * 2 > (outer_diameter - inner_diameter) / 2:
            scene.flange_status = "오류: 볼트홀이 너무 큽니다"
            return {'CANCELLED'}
            
        if pcd <= inner_diameter or pcd >= outer_diameter:
            scene.flange_status = "오류: PCD가 내경과 외경 사이에 있어야 합니다"
            return {'CANCELLED'}
        
        # 기존 플랜지 객체가 있으면 제거
        if "Flange" in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects["Flange"], do_unlink=True)
        
        # 플랜지 생성 함수 호출
        create_flange(outer_diameter, inner_diameter, thickness, bolt_holes, bolt_diameter, pcd)
        
        scene.flange_status = f"플랜지 생성 완료: 볼트홀 {bolt_holes}개"
        return {'FINISHED'}

# 애드온에 필요한 클래스들 목록
classes = (
    FlangeGeneratorPanel,
    OBJECT_OT_GenerateFlange,
)

# Blender에 프로퍼티 등록
def register_properties():
    # 플랜지 파라미터 프로퍼티 등록
    bpy.types.Scene.flange_outer_diameter = bpy.props.FloatProperty(
        name="외경", default=200.0, min=10.0, max=1000.0, description="플랜지 외경 (mm)")
    
    bpy.types.Scene.flange_inner_diameter = bpy.props.FloatProperty(
        name="내경", default=100.0, min=5.0, max=900.0, description="플랜지 내경 (mm)")
    
    bpy.types.Scene.flange_thickness = bpy.props.FloatProperty(
        name="두께", default=25.0, min=1.0, max=100.0, description="플랜지 두께 (mm)")
    
    bpy.types.Scene.flange_bolt_holes = bpy.props.IntProperty(
        name="볼트홀 개수", default=6, min=3, max=36, description="볼트홀 개수")
    
    bpy.types.Scene.flange_bolt_diameter = bpy.props.FloatProperty(
        name="볼트홀 직경", default=18.0, min=1.0, max=50.0, description="볼트홀 직경 (mm)")
    
    bpy.types.Scene.flange_pcd = bpy.props.FloatProperty(
        name="PCD", default=160.0, min=10.0, max=950.0, description="볼트홀 패턴 원 지름 (mm)")
    
    bpy.types.Scene.flange_status = bpy.props.StringProperty(
        name="상태", default="", description="플랜지 생성 상태")

# 등록 함수
def register():
    # 클래스 등록
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # 프로퍼티 등록
    register_properties()

# 등록 해제 함수
def unregister():
    # 클래스 등록 해제
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # 프로퍼티 등록 해제
    del bpy.types.Scene.flange_outer_diameter
    del bpy.types.Scene.flange_inner_diameter
    del bpy.types.Scene.flange_thickness
    del bpy.types.Scene.flange_bolt_holes
    del bpy.types.Scene.flange_bolt_diameter
    del bpy.types.Scene.flange_pcd
    del bpy.types.Scene.flange_status

# 스크립트가 직접 실행될 때만 등록 (애드온 테스트용)
if __name__ == "__main__":
    register()

