# MCP-Blender 

### MCP Server for Blender 
- Blender MCP Server는 Model Context Protocol로 Blender와 Claude AI에 연결.
- Claude가 Blender와 직접 상호 작용하고 제어하여
- 신속하고 자연 기반으로 3D 모델링을 가능하게 하며,
- Parametric Design, Ralational Design이 가능하도록 합니다.
  (향후 Blender외 CATIA, SoildWorks용 MCP-Server 예정임)

### 1. Functions 
1) MCP를 사용한 CAD SW인 Blender와 연결
2) Belnder에서 Model 생성
3) Blender에서 tempoary code 수행

### 2. 필요 사항 
1) Blender (3.5이상)
2) Claude ai 
3) Python (3.10이상) 
4) UV Package 

### 3. 설치 
1) UV and UVX
``` text
pip install uv 
```
- https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2 참조

2) 설치 확인
```shell
uv --version
uvx --version 
```
3) 설치 경로 
