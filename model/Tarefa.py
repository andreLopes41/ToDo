from pydantic import BaseModel
from typing import Optional


class Tarefa(BaseModel):
    id: str
    nome: str
    descricao: str
    data_criacao: Optional[str]
    concluida: bool
