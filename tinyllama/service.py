import bentoml
import torch
from transformers import pipeline

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
pipe = pipeline(
    "text-generation",
    model=model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)


@bentoml.service(
    name="tinyllama_1b_chat_service",
    resources={"cpu": "2"},
    traffic={"timeout": 240},
)
class TinyLlamaService:
    def __init__(self) -> None:
        pass

    @bentoml.api
    def generate(self, input: str):
        if not input.strip():
            return {"error": "Prompt is empty."}
        messages = [
            {"role": "system", "content": "You are a chatbot assistant"},
            {"role": "user", "content": input},
        ]
        outputs = pipe(
            messages,
            max_new_tokens=256,
        )
        result = outputs[0]["generated_text"][-1]
        return {"output": result}
