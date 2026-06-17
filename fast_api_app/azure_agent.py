from langchain_core.language_models import LLM
from typing import Optional, List, Any


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

#SDK
# Enviar mensagem para o agente (histórico é mantido automaticamente)
""" response = openai_client.responses.create(
    input=[{"role": "user", "content": f""}],
    extra_body={
        "agent_reference": {
            "name": my_agent,
            "version": my_version,
            "type": "agent_reference"
        }
    },
)
    print("Resposta :", response.output_text)
    return response.output_text
 """

# Seu cliente já inicializado
# langchain

class AzureFoundryLLM(LLM):
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = openai_client.responses.create(
            input=[{"role": "user", "content": prompt}],
            extra_body={
                "agent_reference": {
                    "name": "Anfitriao",
                    "version": "5",
                    "type": "agent_reference"
                }
            },
        )
        output = response.output_text
        return output

    @property
    def _identifying_params(self) -> dict:
        return {"name": "AzureFoundryLLM"}

    @property
    def _llm_type(self) -> str:
        return "azure_foundry"
