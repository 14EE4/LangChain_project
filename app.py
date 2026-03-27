from dotenv import load_dotenv
from langchain_groq import ChatGroq

from agent import create_email_agent

load_dotenv()

def run_demo() -> None:
    groq_llm_model = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.3,
    )
    agent = create_email_agent(llm=groq_llm_model, verbose=False)

    # 프로그램 소개
    print("=" * 70)
    print("✉️  AI 이메일 드래프트 어시스턴트")
    print("=" * 70)
    print()
    print("이 프로그램은 Groq의 LLM을 활용하여 전문적인 이메일 초안을 빠르게 작성합니다.")
    print()
    print("기능:")
    print("  • AI가 자동으로 완성도 높은 이메일 초안 생성")
    print("  • 톤(공식/중립/친근) 추천 및 적용")
    print("  • 초안 수정 및 버전 관리")
    print("  • 메모리에 임시 저장 (프로세스 종료 시 초기화)")
    print()
    print("시작하기 - 다음 정보를 제공하면 초안을 만들 수 있습니다:")
    print()
    print("  [필수]")
    print("    • 수신자 이름          - 예: '김민수'")
    print("    • 수신자 이메일        - 예: 'info@example.com'")
    print("    • 목적                 - 예: '회의 일정 조율'")
    print("    • 보내는 사람 이름      - 예: '홍길동'")
    print()
    print("  [선택]")
    print("    • 핵심 포인트         - 세미콜론 ';'로 구분. 예: '빠른 응답 필요;주말 회피'")
    print("    • 톤                  - 공식 / 중립 / 친근 (언급하지 않으면 자동 추천)")
    print()
    print("예시: '홍길동(info@example.com)에게 이메일 초안을 만들어줄래? 회의 일정을 조율하는 내용으로'")
    print()
    print("종료: 'exit', 'quit', 또는 'q' 입력")
    print("=" * 70)
    print()
    messages = []

    while True:
        try:
            user_input = input("you> ").strip()
        except EOFError:
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit", "q"}:
            print("종료합니다.")
            break

        messages.append({"role": "user", "content": user_input})
        response = agent.invoke({"messages": messages})
        assistant_message = response["messages"][-1].content
        print(f"agent> {assistant_message}")

        # tool call 히스토리를 포함해 다음 턴 문맥으로 사용한다.
        messages = response["messages"]


if __name__ == "__main__":
    run_demo()
