import bentoml
import torch
from transformers import pipeline

model_name = "unsloth/Llama-3.2-3B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)


@bentoml.service(
    name="llama3_2_3b_instruct_service",
    resources={"cpu": "3"},
    traffic={"timeout": 240},
)
class Llama3_2_3BInstructMetaService:
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
