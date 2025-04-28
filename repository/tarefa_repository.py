from model.Tarefa import Tarefa
import json
import os


class TarefaRepository:

    JSON_FILE = '../json/tarefa.json'

    @classmethod
    def create(cls, tarefa: Tarefa) -> None:
        """Cria uma nova tarefa

        Args:
            tarefa (Tarefa): Objeto Tarefa
        """

        tarefas: list = cls.read()

        tarefas.append(
            {
                'id': tarefa.id,
                'nome': tarefa.nome,
                'descricao': tarefa.descricao,
                'data_criacao': tarefa.data_criacao,
                'concluida': tarefa.concluida,
            }
        )

        cls.save(tarefas)

    @classmethod
    def read(cls) -> list:
        """Retorna as tarefas salvas no arquivo JSON

        Returns:
            list: Lista de Objetos Tarefas
        """
        os.makedirs('../json', exist_ok=True)

        try:
            with open(cls.JSON_FILE, 'r') as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            cls.save([])
            return []

    @classmethod
    def update(cls, tarefa: Tarefa) -> None:
        """Altera uma Tarefa com base no id

        Args:
            tarefa (Tarefa): Objeto Tarefa com os dados atualizados
        """

        tarefas: list = cls.read()

        for tar in tarefas:
            if tar['id'] == tarefa.id:
                tar['nome'] = tarefa.nome
                tar['descricao'] = tarefa.descricao
                tar['concluida'] = tarefa.concluida
                break

        cls.save(tarefas)

    @classmethod
    def delete(cls, tarefa: Tarefa) -> None:
        """Exclui uma Tarefa com base no id

        Args:
            tarefa (Tarefa): Objeto Tarefa
        """

        tarefas: list = cls.read()

        for tar in tarefas:
            if tar['id'] == tarefa.id:
                tarefas.remove(tar)
                break

        cls.save(tarefas)

    @classmethod
    def save(cls, tarefas: list) -> None:
        """Faz a persistência da Tarefa em arquivo JSON

        Args:
            tarefas (list): Lista de Objetos Tarefas
        """

        with open(cls.JSON_FILE, 'w') as arquivo:
            json.dump(tarefas, arquivo, indent=4)
