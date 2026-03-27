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

    print("이메일 에이전트 시작. 종료하려면 exit 입력")
    print("시작할 때 아래 정보를 알려주면 빠르게 초안을 만들 수 있습니다:")
    print("- 수신자 이름")
    print("- 수신자 이메일")
    print("- 목적")
    print("- 보내는 사람 이름")
    print("- 핵심 포인트(선택, 세미콜론 ';'로 구분)")
    print("- 톤(선택: formal/neutral/friendly)")
    print("- 언어(선택: ko/en)")
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
