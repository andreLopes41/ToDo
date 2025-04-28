from model.Tarefa import Tarefa
from datetime import datetime
import requests
from requests import Response
import uuid


class TarefaController:
    def __init__(self) -> None:
        """Inicializa o controlador de Tarefas"""
        self.API_URL = 'http://127.0.0.1:8000/'

    def cadastrar_tarefa(self, nome: str, descricao: str):
        """Cadastra uma nova tarefa

        Args:
            nome (str): Nome da tarefa
            descricao (str): Descrição da tarefa

        Raises:
            ValueError: Se o nome ou descrição estiverem vazios
        """
        if not nome or not descricao:
            raise ValueError('Nome e descrição são obrigatórios')

        data: dict = {
            'id': str(uuid.uuid4()),
            'nome': nome,
            'descricao': descricao,
            'data_criacao': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'concluida': False,
        }

        self.valida_response(
            self.requisicao(
                api_url=self.API_URL,
                endpoint='tarefas/cadastrar',
                method='POST',
                json_data=data,
            )
        )

    def listar_tarefas(self) -> list[Tarefa]:
        """Retorna a lista com todas as tarefas cadastradas

        Returns:
            list[Tarefas]: Lista de tarefas

        Raises:
            ValueError: Se não existirem tarefas cadastradas
        """
        response = self.requisicao(
            api_url=self.API_URL, endpoint='tarefas/listar', method='GET'
        )
        self.valida_response(response)
        tarefas: list = response.json()
        if not tarefas:
            raise ValueError('Não há tarefas cadastradas.')
        return tarefas

    def buscar_tarefa_por_id(self, id: str) -> Tarefa:
        """Busca uma tarefa pelo seu id

        Args:
            id (str): Id da tarefa a ser buscada

        Returns:
            Tarefa: Modelo da tarefa

        Raises:
            ValueError: Se a tarefa não for encontrada
        """
        response = self.requisicao(
            api_url=self.API_URL,
            endpoint='tarefas/buscar_por_id',
            method='GET',
            json_data={'id': id},
        )
        self.valida_response(response)
        return response

    def atualizar_tarefa(
        self, id: str, novo_nome: str, nova_descricao: str, concluida: bool
    ) -> None:
        """Atualiza uma tarefa existente

        Args:
            id (str): id da tarefa a ser atualizada
            novo_nome (str): Novo nome da tarefa
            nova_descricao (str): Nova descrição da tarefa
            concluida (bool): Se a tarefa foi concluída

        Raises:
            ValueError: Se o id, nome, descrição ou concluida estiverem vazios
            ValueError: Se a tarefa não for encontrada
        """
        if not id or not novo_nome or not nova_descricao or not concluida:
            raise ValueError(
                'id, Novo nome, nova descrição e concluída são obrigatórios'
            )

        self.valida_response(
            self.requisicao(
                api_url=self.API_URL,
                endpoint='tarefas/buscar_por_id',
                method='GET',
                json_data={'id': id},
            )
        )

        data = {
            'id': id,
            'nome': novo_nome,
            'descricao': nova_descricao,
            'data_criacao': None,
            'concluida': concluida,
        }

        self.valida_response(
            self.requisicao(
                api_url=self.API_URL,
                endpoint='tarefas/atualizar',
                method='POST',
                json_data=data,
            )
        )

    def excluir_tarefa(self, id: str) -> None:
        """Exclui uma tarefa

        Args:
            id (str): Nome da tarefa a ser excluída

        Raises:
            ValueError: Se o id não foi passado
            ValueError: Se a tarefa não for encontrada
        """
        if not id:
            raise ValueError('id da tarefa é obrigatório')
        response = self.requisicao(
            api_url=self.API_URL,
            endpoint='tarefas/buscar_por_id',
            method='GET',
            json_data={'id': id},
        )
        self.valida_response(response)
        tarefa: Tarefa = response.json()

        data = {
            'id': tarefa['id'],
            'nome': tarefa['nome'],
            'descricao': tarefa['descricao'],
            'data_criacao': tarefa['data_criacao'],
            'concluida': tarefa['concluida'],
        }

        self.valida_response(
            self.requisicao(
                api_url=self.API_URL,
                endpoint='tarefas/excluir',
                method='DELETE',
                json_data=data,
            )
        )

    def listar_tarefas_concluidas(self, concluida: bool) -> list[Tarefa]:
        """Lista tarefas (Concluídas ou não) com base no valor passado por parâmetro

        Args:
            concluida (bool): True ou False para listar as tarefas correspondentes

        Returns:
            list[Tarefa]: tarefas filtradas com base no valor passado por parâmetro

        Raises:
            ValueError: Se não há tarefas cadastradas
            ValueError: Se não foi encontrado tarefas para concluir / desmarcar
        """
        response = self.requisicao(self.API_URL, 'tarefas/listar', 'GET')
        self.valida_response(response)
        tarefas: list = response.json()
        if not tarefas:
            raise ValueError('Não há tarefas cadastradas.')

        tarefas_filtradas: list = list(
            filter(lambda x: x['concluida'] == concluida, tarefas)
        )
        if not tarefas_filtradas:
            raise ValueError('Não há tarefas para concluir / desmarcar')
        return tarefas_filtradas

    def requisicao(
        self, api_url: str, endpoint: str, method: str, json_data: dict = {}
    ):
        """Faz a requisição para a API com base no endpoint e o meétodo da requisição

        Args:
            api_url (str): Url da api
            endpoint (str): endpoint da api
            method (str): método: GET, POST ou DELETE
            json_data (dict, optional): payload da requisição. Defaults to {}.

        Raises:
            ValueError: caso o método da requisição não for GET, POST ou DELETE

        Returns:
            Response: retorna a Response da requisição
        """
        match method.upper():
            case 'GET':
                return requests.get(f'{api_url}{endpoint}', params=json_data)
            case 'POST':
                return requests.post(f'{api_url}{endpoint}', json=json_data)
            case 'DELETE':
                return requests.delete(f'{api_url}{endpoint}', json=json_data)
            case _:
                raise ValueError('Método de requisição inválido')

    def valida_response(self, response: Response):
        """Retorna um raise caso o request não seja um http status code 200 (success)

        Args:
            response (Response): response feita pela requisição

        Raises:
            ValueError: a requisição não retornou status code 200
        """
        if response.status_code != 200:
            raise ValueError(f'Erro: {response.json()}')
