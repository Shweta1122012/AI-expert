import base64
import os
import sys
import uuid

from openai import OpenAI


SYSTEM_BASE = """You are Tulip, a helpful, honest assistant.
You can chat in many languages, explain concepts clearly, and write code on request.
Be concise when possible, ask clarifying questions if the request is ambiguous,
and do not claim to be human.
"""


def get_system_prompt(preferred_language: str | None) -> str:
    if preferred_language:
        return (
            SYSTEM_BASE
            + f"\nPrefer replying in {preferred_language} unless the user asks for a different language."
        )
    return SYSTEM_BASE


def extract_text(response) -> str:
    if hasattr(response, "output_text") and response.output_text:
        return response.output_text.strip()
    parts = []
    for output in getattr(response, "output", []) or []:
        if output.type == "message":
            for content in output.content:
                if content.type == "output_text":
                    parts.append(content.text)
    return "\n".join(parts).strip()


def chat_loop() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        print("Missing OPENAI_API_KEY. Set it before running this script.")
        return

    client = OpenAI()
    history: list[dict] = []
    preferred_language: str | None = None

    print("Tulip ready. Type /help for commands.")

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            if user_input in ("/exit", "/quit"):
                break
            if user_input == "/reset":
                history.clear()
                print("Conversation reset.")
                continue
            if user_input == "/help":
                print(
                    "Commands: /help, /exit, /reset, /lang <name>, /image <prompt>"
                )
                continue
            if user_input.startswith("/lang "):
                preferred_language = user_input[len("/lang ") :].strip() or None
                print(
                    f"Preferred language set to: {preferred_language or 'auto'}"
                )
                continue
            if user_input.startswith("/image "):
                prompt = user_input[len("/image ") :].strip()
                if not prompt:
                    print("Provide a prompt after /image.")
                    continue
                try:
                    response = client.responses.create(
                        model="gpt-5",
                        input=prompt,
                        tools=[{"type": "image_generation"}],
                    )
                    image_data = [
                        output.result
                        for output in response.output
                        if output.type == "image_generation_call"
                    ]
                    if not image_data:
                        print("No image returned. Try a different prompt.")
                        continue
                    filename = f"image_{uuid.uuid4().hex[:8]}.png"
                    with open(filename, "wb") as f:
                        f.write(base64.b64decode(image_data[0]))
                    print(f"Saved: {filename}")
                except Exception as exc:
                    print(f"Image error: {exc}")
                continue

            print("Unknown command. Type /help.")
            continue

        system_prompt = get_system_prompt(preferred_language)
        try:
            response = client.responses.create(
                model="gpt-5",
                input=[{"role": "system", "content": system_prompt}] + history + [
                    {"role": "user", "content": user_input}
                ],
            )
        except Exception as exc:
            print(f"Request error: {exc}")
            continue

        assistant_text = extract_text(response) or "(No response text returned.)"
        print(assistant_text)
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": assistant_text})


if __name__ == "__main__":
    chat_loop()
