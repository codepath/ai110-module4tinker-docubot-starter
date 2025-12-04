# Entry point for interacting with DocuBot.

from docubot import DocuBot

def main():
    bot = DocuBot(folder_path="docs")

    print("Welcome to DocuBot. Ask me about your codebase or documentation!")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Query: ").strip()
        if query.lower() == "exit":
            break

        results = bot.retrieve(query)
        answer = bot.assemble_answer(query, results)
        print("\n" + answer + "\n")

if __name__ == "__main__":
    main()
