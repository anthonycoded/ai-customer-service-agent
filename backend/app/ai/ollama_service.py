import ollama


class OllamaService:
    def __init__(self, model: str = "llama3.2:1b"):
        self.model = model

    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> str:

        response = ollama.chat(
            model=self.model,
            messages=messages,
        )

        return response["message"]["content"]