from langchain_community.llms import Ollama
import sys

def main():
    # Khởi tạo model kết nối với Ollama chạy local
    print("⏳ Đang kết nối với model Qwen2.5:7b qua Ollama...")
    try:
        llm = Ollama(model="qwen2.5:3b")
    except Exception as e:
        print(f"Lỗi kết nối: {e}")
        return

    print("\n" + "="*50)
    print("🤖 DEMO CONSOLE AI - QWEN 2.5 (7B)")
    print("Gõ 'thoat' hoặc 'quit' để kết thúc chương trình.")
    print("="*50 + "\n")

    # Vòng lặp hội thoại
    while True:
        user_input = input("🧑 Bạn: ")
        
        # Điều kiện thoát
        if user_input.lower() in ['thoat', 'quit', 'exit']:
            print("👋 Tạm biệt!")
            break
            
        if not user_input.strip():
            continue

        print("🤖 Qwen: ", end="", flush=True)
        
        # Sử dụng hàm stream() để in ra từng token ngay khi AI sinh ra
        # Giúp tiết kiệm thời gian chờ (latency) cho người dùng
        try:
            for chunk in llm.stream(user_input):
                print(chunk, end="", flush=True)
        except Exception as e:
            print(f"\n[Lỗi trong quá trình sinh văn bản: {e}]")
            
        print("\n" + "-"*50)

if __name__ == "__main__":
    main()