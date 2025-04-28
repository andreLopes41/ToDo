import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repository.tarefa_repository import TarefaRepository
from model.Tarefa import Tarefa
from fastapi import FastAPI

repository = TarefaRepository()
app = FastAPI()


@app.post('/tarefas/cadastrar')
def cadastrar_tarefa(tarefa: Tarefa) -> dict:
    """Endpoint para cadastrar Tarefa

    Args:
        tarefa (Tarefa): Modelo de Tarefa

    Returns:
        dict: Informa o sucesso ou não na da requisição
    """
    try:
        repository.create(tarefa)
        return {'msg': 'Tarefa cadastrada com sucesso'}
    except Exception as e:
        return {'erro': str(e)}


@app.get('/tarefas/listar')
def listar_tarefas() -> list[Tarefa] | dict:
    """Endpont traz uma lista de tarefas cadastradas

    Returns:
        list[Tarefas] | dict: lista de Tarefas cadastradas ou Informa caso a requisição falhou
    """
    try:
        return repository.read()
    except Exception as e:
        return {'erro': str(e)}


@app.get('/tarefas/buscar_por_id/{id}')
def buscar_tarefa_por_id(id: str) -> Tarefa | dict:
    """Endpoint que busca uma tarefa pelo seu ID

    Args:
        id (str): id da tarefa

    Returns:
        Tarefa | dict: Retorna a tarefa encontrada ou Informa caso a requisição falhou
    """
    try:
        tarefas: list = repository.read()
        for tarefa in tarefas:
            if tarefa['id'] == id:
                return tarefa
        return {'msg': 'Tarefa não encontrada'}
    except Exception as e:
        return {'erro': str(e)}


@app.post('/tarefas/atualizar')
def atualizar_tarefa(tarefa: Tarefa) -> dict:
    """Endpoint que atualiza uma Tarefa

    Args:
        tarefa (Tarefa): Modelo de Tarefa

    Returns:
        dict: Informa o sucesso ou não na da requisição
    """
    try:
        if buscar_tarefa_por_id(tarefa.id):
            tarefa_atualizada: Tarefa = Tarefa(
                id=tarefa.id,
                nome=tarefa.nome,
                descricao=tarefa.descricao,
                data_criacao=tarefa.data_criacao,
                concluida=tarefa.concluida,
            )
            repository.update(tarefa_atualizada)
            return {'msg': 'Tarefa atualizada com sucesso'}
        return {'msg': 'Tarefa não encontrada'}
    except Exception as e:
        return {'erro': str(e)}


@app.delete('/tarefas/excluir')
def excluir_tarefa(tarefa: Tarefa) -> dict:
    """Endpoint que exclui uma Tarefa

    Args:
        tarefa (Tarefa): Modelo de Tarefa

    Returns:
        dict: Informa o sucesso ou não na da requisição
    """
    try:
        repository.delete(tarefa)
        return {'msg': 'Tarefa excluida com sucesso'}
    except Exception as e:
        return {'erro': str(e)}
