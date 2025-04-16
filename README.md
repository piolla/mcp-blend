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

### 3. 설치 Step #1: UV Package   
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

### 4. 설치 Step #2 : Blender Add-ons 
1) 'blender_addon.py' download
2) Blender 실행 
- Edit -> Preferences -> Add-ons -> Inrell Add-on -> blender_addon.py(download위치)
- -> 'Interface: Blender MCP' checkbox check(Activation)
- ![image](https://github.com/user-attachments/assets/6ea56892-d70b-4bfa-a5a4-fb243e898353)
- ![image](https://github.com/user-attachments/assets/7f758322-5864-47c4-809b-00c4695512aa)


### 5. 설치 Step #3 : Claude ai 
1) Claude ai open
2) 파일 -> 설정 -> 개발자 -> 설정 편집 -> 파일 탐색기에서 'claude_desktop_config.json' 파일 수정
3) claude_desktop_config.json (아래 참조하여 수정 )
```script
{
    "mcpServers":
    {
        "Blender":
        {
            "command": "D:\\Anaconda\\envs\\aria\\Scripts\\uvx.exe",
            "args": ["blender-mcp" ]
        }
    }
}
```

4) claude 종료하고 다시 실행하기
- claude 종료는 파일 메뉴에서 종료
- claude 실행하여 연결 확인
- ![image](https://github.com/user-attachments/assets/2fc7750d-9bc7-4c25-9d73-9bcd399b78b6)





