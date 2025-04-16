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

### 3. 설치 Step #1   
1) UV and UVX
``` text
pip install uv 
```
- https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2 참조
"
2) 설치 확인
```shell
uv --version
uvx --version 
```

3) 설치 경로 확인
- 만약 가상환경에 설치 되었다면 가능한 Full path를 지정해주는 방법 권장
```shell
# 설치 경로 확인 
where uvx 
```

### 3. 설치 Step #2
1) 'blender_addon.py' download
2) Blender 실행 
- Edit -> Preferences -> Add-ons -> Inrell Add-on -> blender_addon.py(download위치)
- -> 'Interface: Blender MCP' checkbox check(Activation)
- ![image](https://github.com/user-attachments/assets/c17a1acd-7d01-4287-b67c-45ac2c792372)
- ![image](https://github.com/user-attachments/assets/98ffe461-e985-451b-801e-d4a0da577d2a)
- ![image](https://github.com/user-attachments/assets/9b664ae6-d524-43e0-ac4d-bf6cafb79d00)

- 



