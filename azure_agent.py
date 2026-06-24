from langchain_core.language_models import LLM
from typing import Optional, List, Any
import os
from dotenv import load_dotenv
from models import Usuario

# Antes de rodar:
#    pip install azure-ai-projects>=2.1.0

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

# Endpoint do seu projeto
endpoint = os.getenv("ENDPOINT_AZURE")

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
""" 
    response = openai_client.responses.create(
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
def criar_conversa(user_info:Optional[Usuario]):
    if user_info == None :
        texto = "não á usuario cadastrado trate o usuario como visitante"
    else:
        texto =f"esses são os dados do usuario autenticado nome:{user_info.nome}, email:{user_info.email}, nascimento:{user_info.nascimento}"
        
    conversation = openai_client.conversations.create(
        items=[{"type": "message", "role": "system", "content": f"{texto} se limite a estes dados, quando for responder o usuario ou visitante "},
               {"type": "message", "role": "assistant", "content": "Olá! Sou Nicole, uma agente de inteligência artificial, que atuarei como a astronauta que posso te auxiliar a decolar nos recursos das Naves. O que posso te ajudar hoje?"}]
    
    )
    conversation_id = conversation.id

    print(texto)
    return conversation_id


class AzureFoundryLLM(LLM):
    conversation_id:str

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        pergunta = openai_client.conversations.items.create(
            conversation_id= self.conversation_id,
            items=[{"type": "message", "role":"user","content":prompt}]
        )


        response = openai_client.responses.create(
            conversation= self.conversation_id,
            extra_body={
                "agent_reference": {
                    "name": "Anfitriao",
                    "type": "agent_reference"
                }
            }
            
        )
        pergunta = openai_client.conversations.items.create(
            conversation_id= self.conversation_id,
            items=[{"type": "message", "role":"assistant","content":response.output_text}]
        )
        output = response.output_text
        print(openai_client.conversations.retrieve(
            conversation_id= self.conversation_id
        ))
        return output

    @property
    def _identifying_params(self) -> dict:
        return {"name": "AzureFoundryLLM"}

    @property
    def _llm_type(self) -> str:
        return "azure_foundry"
