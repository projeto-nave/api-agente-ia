from openai import OpenAI

endpoint = "https://aih-anfitriao-prod-eastus-001.services.ai.azure.com/openai/v1"
deployment_name = "gpt-4o"
api_key = ""

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

with open("instrucoes.txt", "r", encoding="utf-8") as f:
    system_instructions = f.read()

completion = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "system",
            "content": system_instructions
        },
        {
            "role": "user",
            "content": "oi como você pode me ajudar?"
        }
    ],
)

assistente = completion.choices[0].message.content
print(assistente)