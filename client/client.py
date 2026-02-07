import argparse
import socket

from common.protocol import decode_message, encode_message


class TriviaClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None
        self.reader = None
        self.writer = None

    def connect(self):
        self.sock = socket.create_connection((self.host, self.port))
        self.reader = self.sock.makefile("r")
        self.writer = self.sock.makefile("w")

    def close(self):
        if self.reader:
            self.reader.close()
        if self.writer:
            self.writer.close()
        if self.sock:
            self.sock.close()

    def send(self, message):
        self.writer.write(encode_message(message))
        self.writer.flush()
        response = self.reader.readline()
        return decode_message(response)


def prompt_choice(options, prompt_text="Choose an option:"):
    while True:
        for idx, option in enumerate(options, start=1):
            print(f"{idx}. {option}")
        value = input(f"{prompt_text} ").strip()
        if value.isdigit():
            choice = int(value) - 1
            if 0 <= choice < len(options):
                return choice
        print("Invalid selection.")


def main():
    parser = argparse.ArgumentParser(description="Trivia client")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    client = TriviaClient(args.host, args.port)
    client.connect()
    logged_in = False

    try:
        while True:
            if not logged_in:
                selection = prompt_choice(["Register", "Login", "Exit"], "Select")
                if selection == 2:
                    break
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                action = "register" if selection == 0 else "login"
                response = client.send(
                    {"type": action, "username": username, "password": password}
                )
                if response.get("status") == "ok":
                    print(response.get("message", "Success"))
                    if action == "login":
                        logged_in = True
                else:
                    print(f"Error: {response.get('message')}")
            else:
                selection = prompt_choice(
                    ["Play a round", "View stats", "Logout", "Exit"],
                    "Select",
                )
                if selection == 3:
                    break
                if selection == 2:
                    response = client.send({"type": "logout"})
                    logged_in = False if response.get("status") == "ok" else logged_in
                    print(response.get("message", "Logged out"))
                    continue
                if selection == 1:
                    response = client.send({"type": "get_stats"})
                    if response.get("status") == "ok":
                        stats = response.get("stats", {})
                        print(f"Points: {stats.get('points')}")
                        print(f"Games played: {stats.get('games_played')}")
                        print(f"Correct: {stats.get('correct_answers')}")
                        print(f"Incorrect: {stats.get('incorrect_answers')}")
                    else:
                        print(f"Error: {response.get('message')}")
                    continue

                categories_resp = client.send({"type": "get_categories"})
                if categories_resp.get("status") != "ok":
                    print(f"Error: {categories_resp.get('message')}")
                    continue
                categories = categories_resp.get("categories", [])
                if not categories:
                    print("No categories available.")
                    continue

                category = categories[prompt_choice(categories, "Choose category")]
                wager_input = input("Enter wager: ").strip()
                if not wager_input.isdigit():
                    print("Wager must be a positive integer.")
                    continue
                wager = int(wager_input)
                question_resp = client.send(
                    {"type": "request_question", "category": category, "wager": wager}
                )
                if question_resp.get("status") != "ok":
                    print(f"Error: {question_resp.get('message')}")
                    continue
                print(question_resp["question"])
                options = question_resp["options"]
                answer_index = prompt_choice(options, "Your answer")
                answer_resp = client.send(
                    {
                        "type": "submit_answer",
                        "question_id": question_resp["question_id"],
                        "answer_index": answer_index,
                    }
                )
                if answer_resp.get("status") == "ok":
                    print("Correct!" if answer_resp["correct"] else "Incorrect.")
                    print(
                        f"Points change: {answer_resp['delta']}, total: {answer_resp['points']}"
                    )
                else:
                    print(f"Error: {answer_resp.get('message')}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
