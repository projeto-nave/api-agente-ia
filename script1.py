# Antes de rodar:
#    pip install azure-ai-projects>=2.1.0

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient



# Endpoint do seu projeto
endpoint = "https://aih-anfitriao-prod-eastus-001.services.ai.azure.com/api/projects/aip-anfitriao-prod-001"

# Cria o cliente do projeto
project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

# Nome e versão do agente
my_agent = "Anfitriao"
my_version = "5"

# Obter cliente OpenAI dentro do projeto
openai_client = project_client.get_openai_client()

# Enviar mensagem para o agente (histórico é mantido automaticamente)
response1 = openai_client.responses.create(
    input=[{"role": "user", "content": f"qual o seu nome?"}],
    extra_body={
        "agent_reference": {
            "name": my_agent,
            "version": my_version,
            "type": "agent_reference"
        }
    },
)
print("Resposta 1:", response1.output_text)

""" # Nova mensagem (continua a mesma conversa)
response2 = openai_client.responses.create(
    input=[{"role": "user", "content": f"{nova_mensagem}"}],
    extra_body={
        "agent_reference": {
            "name": my_agent,
            "version": my_version,
            "type": "agent_reference"
        }
    },
)
print("Resposta 2:", response2.output_text)
 """
