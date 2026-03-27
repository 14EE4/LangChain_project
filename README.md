# Email Draft Agent (LangChain + Groq)

대화형으로 이메일 초안을 작성하고, 톤 추천/수정/모의 발송까지 지원하는 CLI 에이전트입니다.

## 주요 기능

- 수신자/목적을 바탕으로 이메일 톤 추천
- 이메일 초안 생성 (한국어/영어)
- 초안 수정 요청 반영
- 최근 초안 조회
- 모의 발송 처리

## 프로젝트 구조

- app.py: CLI 실행 진입점
- agent.py: LangChain 에이전트 생성
- Tools.py: 톤 추천, 초안 생성/수정/발송 도구
- Models.py: Pydantic 데이터 모델
- mock_db.py: 메모리 기반 저장소

## 요구 사항

- Python 3.10+
- 가상환경 (.venv 권장)
- GROQ_API_KEY

## 설치

1) 가상환경 활성화

Windows PowerShell:

```powershell
& .\.venv\Scripts\Activate.ps1
```

2) 패키지 설치

```powershell
python -m pip install langchain langchain-core langchain-groq python-dotenv pydantic
```

3) 환경 변수 설정 (.env)

프로젝트 루트에 .env 파일을 만들고 아래처럼 입력합니다.

```dotenv
GROQ_API_KEY=your_groq_api_key
```

## 실행

```powershell
python .\app.py
```

실행 후 프롬프트에서 여러 턴으로 대화를 이어갈 수 있습니다.
종료 명령: exit, quit, q

## 입력 예시

```text
you> 이메일 초안을 작성해줘. 수신자: 김대리(kim@example.com), 목적: 프로젝트 일정 변경 안내
you> 보내는 사람은 박매니저야
you> 좀 더 정중하게 바꿔줘
you> 발송해줘
you> exit
```

## 출력 예시

```text
이메일 에이전트 시작. 종료하려면 exit 입력
agent> 추천 톤은 neutral 입니다. 초안을 생성했습니다.

제목: [프로젝트 일정 변경 안내] 관련 문의 드립니다

김대리님께,

프로젝트 일정 변경 안내 관련하여 메일드립니다.

핵심 내용은 아래와 같습니다.
- 프로젝트 일정 변경
- 새로운 일정 및 마일스톤
- 회의 일정 조정
- 필요한 조치 및 확인 요청

추가로 필요한 사항이 있으면 말씀 부탁드립니다.

검토 부탁드립니다.
박매니저 드림

agent> 요청하신 대로 더 정중한 톤으로 수정했습니다.
agent> 모의 발송 완료: status=sent
종료합니다.
```

## 참고

- 이 프로젝트의 발송 기능은 실제 메일 전송이 아닌 모의 발송입니다.
- 저장소는 메모리 기반이므로 프로세스 종료 시 초기화됩니다.
