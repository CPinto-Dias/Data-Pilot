import json
import os
from decimal import Decimal
import pandas as pd
from dotenv import load_dotenv
from openrouter import OpenRouter
from openrouter.components import ChatFunctionToolFunctionTypedDict, ChatMessagesTypedDict
from openai import OpenAI
from typing import Callable, cast

from src.metrics import (
    average_ticket_value,
    monthly_revenue,
    total_orders,
    total_revenue,
    top5_clients,
    top5_products,
    completed_orders,
    products_sold,
    unique_clients,
    cancellation_rate,
)

DEFAULT_MODEL = "openai/gpt-4o-mini"
MAX_TOOLS_ROUNDS = 3

TOOLS: list[ChatFunctionToolFunctionTypedDict] = [
    {
        "type": "function",
        "function":{
            "name": "sales_summary",
            "description": "Retorna os principais indicadores consolidados de vendas.",
            "parameters": {"type": "object", "properties":{}},
        },
    },
    {
       "type": "function",
        "function":{
            "name": "monthly_revenue",
            "description": "Retorna a receita de pedidos concluídos agrupada por mês.",
            "parameters": {"type": "object", "properties":{}},
        }, 
    },
    {
       "type": "function",
        "function":{
            "name": "cancellation_rate",
            "description": "Retorna a taxa de cancelamento dos pedidos, em percentual.",
            "parameters": {"type": "object", "properties":{}},
        }, 
    },    

]
def execute_tool(name: str, df: pd.DataFrame) -> dict[str, object]:
    tools: dict[str, Callable[[], dict[str, object]]]= {
        "sales_summary": lambda: {
            "completed_orders": int(len(completed_orders(df))),
            "total_revenue": float(total_revenue(df)),
            "products_sold": int(products_sold(df)),
            "unique_clients": int(unique_clients(df)),
            "average_ticket_value": float(average_ticket_value(df)),
            "top5_clients": top5_clients(df).to_dict(orient="records"),
            "top5_products": top5_products(df).to_dict(orient="records"),
        },
        "monthly_revenue": lambda: {
            "monthly_revenue": monthly_revenue(df).to_dict(orient="records")
        },
        "cancellation_rate": lambda: {
            "cancellation_rate": float(cancellation_rate(df)),
        },
    }
    tool = tools.get(name)
    return tool() if tool else {"error": f"Ferramenta desconhecida:{name}"}


def run_agent(question: str, df: pd.DataFrame) -> str:
        _ = load_dotenv()  # Load environment variables from .env file
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return "Defina OPENROUTER_API_KEY para conversar com dados."
    
        messages: list[ChatMessagesTypedDict] = [
        {
            "role": "system",
            "content": (
                "Você é um agente de análise de vendas. Responda em português do Brasil, "
                "sem inventar dados. Use as ferramentas quando precisar de dados; elas são "
                "a única fonte permitida."
            ),
        },

        {"role": "user", "content": question}
    ]
        with OpenRouter(api_key=api_key) as client:

            for _ in range(MAX_TOOLS_ROUNDS):
                response = client.chat.send(
                model=os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL),
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
            )
            message = response.choices[0].message
            tool_calls = message.tool_calls or []
            if not tool_calls:
                return (
                    message.content
                    if isinstance(message.content, str)
                    else "O modelo não retornou uma resposta válida."
                )
            messages.append(
                cast(
                    ChatMessagesTypedDict,
                    cast(object, message.model_dump(exclude_none=True)),
                )
            )
            for tool_call in tool_calls:
                try:
                    json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    result = {"error": "Argumentos inválidos para a ferramenta."}
                else:
                    result = execute_tool(tool_call.function.name, df)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(
                            result, ensure_ascii=False, default=_json_default
                        ),
                    }
                )
        return "Não foi possível concluir a análise no número permitido de consultas."

# --------------------------------------------------------------
# Trecho do programa onde o contexo e o prompt são construídos
# --------------------------------------------------------------

def build_data_context(df: pd.DataFrame) -> dict[str, object]:
    return {
        "total_revenue": float(total_revenue(df)),
        "total_orders": int(total_orders(df)),
        "products_sold": int(products_sold(df)),
        "unique_clients": int(unique_clients(df)),
        "average_ticket_value": float(average_ticket_value(df)),
        "cancellation_rate": float(cancellation_rate(df)),
        "top5_clients": top5_clients(df).to_dict(orient="records"),
        "top5_products": top5_products(df).to_dict(orient="records"),
        "monthly_revenue": monthly_revenue(df).to_dict(orient="records"),      
        "completed_orders": int(len(completed_orders(df))),
    }

def build_prompt(question: str, data_context: dict[str, object]) -> str:
    data = json.dumps(data_context, ensure_ascii=False, default=_json_default)
    return f"""You are a sales data assistant. Answer in Brazilian Portuguese, clearly and without inventig data.
    Use only the calculated data below. if it is not enough to answer, say that you do not know based on the provided data.

    Question: {question}
    Calculated data: {data}"""

def ask_openrouter(question: str, df: pd.DataFrame) -> str:
    _ = load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "Defina OPENROUTER_API_KEY para conversar com dados."
    try:
        with OpenRouter(api_key=api_key) as client:
            response = client.chat.send(
                model=os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL),
                messages=[
                    {"role": "user",
                     "content": build_prompt(question, build_data_context(df))
                     }
                ],
            )
        content = response.choices[0].message.content
           
        if isinstance(content, str):
            return content
        return "O modelo não retornou uma resposta válida. Tente novamente."
    
    except Exception as exc:
        print(f"Erro inesperado: {exc}")
        return "Não foi possível conectar ao OpenRouter. Tente novamente."
    
def _json_default(value: object) -> str:
    if isinstance(value, Decimal):
        return str(value)
    raise TypeError(f"Unsupported value {type(value).__name__} ")