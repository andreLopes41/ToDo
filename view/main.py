import os
import sys
import questionary

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controller.tarefa_controller import TarefaController


def limpar_tela():
    """Limpa a tela do console"""

    os.system('cls' if os.name == 'nt' else 'clear')


def pressionar_enter():
    """Aguarda a tecla ENTER ser pressionada para liberar a interface"""

    print('\n')
    input('Pressione ENTER para continuar...')


def exibir_logo():
    """Exibe a logo do sistema"""

    print(
        '██████╗ ███████╗ █████╗               ████████╗ ██████╗ ██████╗  ██████╗'
    )
    print(
        '██╔══██╗██╔════╝██╔══██╗              ╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗'
    )
    print(
        '██████╔╝█████╗  ███████║    █████╗       ██║   ██║   ██║██║  ██║██║   ██║'
    )
    print(
        '██╔═══╝ ██╔══╝  ██╔══██║    ╚════╝       ██║   ██║   ██║██║  ██║██║   ██║'
    )
    print(
        '██║     ██║     ██║  ██║                 ██║   ╚██████╔╝██████╔╝╚██████╔╝'
    )
    print(
        '╚═╝     ╚═╝     ╚═╝  ╚═╝                 ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝ '
    )
    print(
        '\n                    Gerenciador de Tarefas                      \n'
    )


def menu_principal():
    """Exbibe o menu principal com as funcionalidades do sistema"""
    while True:
        limpar_tela()
        exibir_logo()

        print('╔════════════════════════════════════╗')
        print('║        MENU PRINCIPAL              ║')
        print('╠════════════════════════════════════╣')
        print('║ [1] 🎯 Gerenciar Tarefas           ║')
        print('║ [2] 📖 Guia do Sistema             ║')
        print('║ [0] 🚪 Sair                        ║')
        print('╚════════════════════════════════════╝')

        user_input: str = str(input('>> '))

        if user_input == '1':
            menu_gerenciar_tarefas()
        elif user_input == '2':
            menu_guia_sistema()
        elif user_input == '0':
            break
        else:
            print('\n')
            print('⚠️  Opção inválida!')
            pressionar_enter()


def menu_gerenciar_tarefas():
    """Fornece o menu de gestão de Tarefas"""

    while True:
        limpar_tela()

        print('╔════════════════════════════════════╗')
        print('║       🎯  GESTÃO DE TAREFAS        ║')
        print('╠════════════════════════════════════╣')
        print('║ [1] ➕ Incluir Tarefa              ║')
        print('║ [2] 📝 Alterar Tarefa              ║')
        print('║ [3] 🗑️  Excluir Tarefa              ║')
        print('║ [4] ✅  Concluir Tarefa            ║')
        print('║ [5] 🔄️  Desmarcar Tarefa           ║')
        print('║ [6] 👁️  Visualizar Tarefa           ║')
        print('║ [7] 📜 Listar Tarefas              ║')
        print('║ [0] 🔙 Voltar                      ║')
        print('╚════════════════════════════════════╝')

        user_input: str = str(input('>> '))

        if user_input == '1':
            incluir_tarefa()
        elif user_input == '2':
            alterar_tarefa()
        elif user_input == '3':
            excluir_tarefa()
        elif user_input == '4':
            concluir_tarefa()
        elif user_input == '5':
            desmarcar_tarefa()
        elif user_input == '6':
            visualizar_tarefa()
        elif user_input == '7':
            listar_tarefas()
        elif user_input == '0':
            break
        else:
            print('\n')
            print('⚠️  Opção inválida!')
            pressionar_enter()


def incluir_tarefa():
    """Faz a inclusão de uma nova Tarefa no sistema"""
    tarefa_controller = TarefaController()
    limpar_tela()

    print('╔════════════════════════════════════╗')
    print('║       ➕ INCLUIR TAREFA            ║')
    print('╚════════════════════════════════════╝\n')

    try:
        nome: str = input('Nome: ')
        descricao: str = input('Descrição: ')

        tarefa_controller.cadastrar_tarefa(nome, descricao)
        print('\n')
        print('✅ Tarefa cadastrada com sucesso.')
    except ValueError as e:
        print('\n')
        print(f'❌ {e}.')

    pressionar_enter()


def alterar_tarefa():
    """Altera uma Tarefa existente no sistema

    Raises:
        ValueError: Caso o usuário cancele a operação do Terminal Menu
    """

    tarefa_controller = TarefaController()
    limpar_tela()

    print('╔════════════════════════════════════╗')
    print('║       📝 ALTERAR TAREFA            ║')
    print('╚════════════════════════════════════╝\n')

    try:
        tarefas: list = tarefa_controller.listar_tarefas()

        menu_tarefas = []
        for tarefa in tarefas:
            item = f'{tarefa["nome"]}'
            menu_tarefas.append(item)

        tarefa_escolhida = create_terminal_menu(
            menu_tarefas, 'Selecione a tarefa'
        )

        if tarefa_escolhida is None:
            raise ValueError('Operação cancelada pelo usuário')

        index = menu_tarefas.index(tarefa_escolhida)
        tarefa = tarefas[index]

        nome: str = input('Novo nome: ')
        descricao: str = input('Nova Descricao: ')
        concluida = create_terminal_menu_opcoes_tarefa_concluida()

        tarefa_controller.atualizar_tarefa(
            tarefa['id'], nome, descricao, concluida
        )
        print('\n')
        print('✅ Tarefa alterada com sucesso.')
    except ValueError as e:
        print('\n')
        print(f'❌ {e}.')

    pressionar_enter()


def excluir_tarefa():
    """Exclui uma Tarefa existente no sistema

    Raises:
        ValueError: Caso o usuário cancele a operação do Terminal Menu
    """

    tarefa_controller = TarefaController()
    limpar_tela()

    print('╔════════════════════════════════════╗')
    print('║       🗑️  EXCLUIR TAREFA           ║')
    print('╚════════════════════════════════════╝\n')

    try:
        tarefas: list = tarefa_controller.listar_tarefas()

        menu_tarefas = []
        for tarefa in tarefas:
            item = f'{tarefa["nome"]}'
            menu_tarefas.append(item)

        tarefa_escolhida = create_terminal_menu(
            menu_tarefas, 'Selecione a tarefa'
        )

        if tarefa_escolhida is None:
            raise ValueError('Operação cancelada pelo usuário')

        index = menu_tarefas.index(tarefa_escolhida)
        tarefa = tarefas[index]

        tarefa_controller.excluir_tarefa(tarefa['id'])
        print('\n')
        print('✅ Tarefa excluída com sucesso.')
    except ValueError as e:
        print('\n')
        print(f'❌ {e}.')

    pressionar_enter()


def concluir_tarefa():
    """Conclui uma Tarefa existente no sistema

    Raises:
        ValueError: Caso o usuário cancele a operação do Terminal Menu
    """

    tarefa_controller = TarefaController()
    limpar_tela()

    print('╔════════════════════════════════════╗')
    print('║       ✅ CONCLUIR TAREFA           ║')
    print('╚════════════════════════════════════╝\n')

    try:
        tarefas: list = tarefa_controller.listar_tarefas_concluidas(False)

        menu_tarefas = []
        for tarefa in tarefas:
            item = f'{tarefa["nome"]}'
            menu_tarefas.append(item)

        tarefa_escolhida = create_terminal_menu(
            menu_tarefas, 'Selecione a tarefa que deseja Concluir'
        )

        if tarefa_escolhida is None:
            raise ValueError('Operação cancelada pelo usuário')

        index = menu_tarefas.index(tarefa_escolhida)
        tarefa = tarefas[index]

        tarefa_controller.atualizar_tarefa(
            tarefa['id'], tarefa['nome'], tarefa['descricao'], True
        )
        print('\n')
        print('✅ Tarefa Concluida com sucesso.')
    except ValueError as e:
        print('\n')
        print(f'❌ {e}.')

    pressionar_enter()


def desmarcar_tarefa():
    """Marca uma Tarefa como não concluida no sistema

    Raises:
        ValueError: Caso o usuário cancele a operação do Terminal Menu
    """

    tarefa_controller = TarefaController()
    limpar_tela()

    print('╔════════════════════════════════════╗')
    print('║       🔄️ DESMARCAR TAREFA          ║')
    print('╚════════════════════════════════════╝\n')

    try:
        tarefas: list = tarefa_controller.listar_tarefas_concluidas(True)

        menu_tarefas = []
        for tarefa in tarefas:
            item = f'{tarefa["nome"]}'
            menu_tarefas.append(item)

        tarefa_escolhida = create_terminal_menu(
            menu_tarefas, 'Selecione a tarefa que deseja Desmarcar'
        )

        if tarefa_escolhida is None:
            raise ValueError('Operação cancelada pelo usuário')

        index = menu_tarefas.index(tarefa_escolhida)
        tarefa = tarefas[index]

        tarefa_controller.atualizar_tarefa(
            tarefa['id'], tarefa['nome'], tarefa['descricao'], False
        )
        print('\n')
        print('✅ Tarefa Desmarcada com sucesso.')
    except ValueError as e:
        print('\n')
        print(f'❌ {e}.')

    pressionar_enter()


def visualizar_tarefa():
    """Exibe as informações de uma Tarefa existente no sistema

    Raises:
        ValueError: Caso o usuário cancele a operação do Terminal Menu
    """

    tarefa_controller = TarefaController()
    limpar_tela()

    print('╔════════════════════════════════════╗')
    print('║      👁️  VISUALIZAR TAREFA          ║')
    print('╚════════════════════════════════════╝\n')

    try:
        tarefas: list = tarefa_controller.listar_tarefas()

        menu_tarefas = []
        for tarefa in tarefas:
            item = f'{tarefa["nome"]}'
            menu_tarefas.append(item)

        tarefa_escolhida = create_terminal_menu(
            menu_tarefas, 'Selecione a tarefa'
        )

        if tarefa_escolhida is None:
            raise ValueError('Operação cancelada pelo usuário')

        index = menu_tarefas.index(tarefa_escolhida)
        tarefa = tarefas[index]

        print('╔════════════════════════════════════╗')
        print(f'  Nome: {tarefa["nome"]}')
        print(f'  Descrição: {tarefa["descricao"]}')
        print(f'  Data de Criação: {tarefa["data_criacao"]}')
        print(f'  Concluída? [ {('✔' if tarefa["concluida"] == True else '')} ]')
        print('╚════════════════════════════════════╝')

    except ValueError as e:
        print('\n')
        print(f'❌ {e}.')

    pressionar_enter()


def listar_tarefas():
    """Lista todas as Tarefas cadastradas no sistema"""

    tarefa_controller = TarefaController()
    limpar_tela()

    print('╔════════════════════════════════════╗')
    print('║       📜 LISTAR TAREFAS            ║')
    print('╚════════════════════════════════════╝\n')

    try:
        tarefas: list = tarefa_controller.listar_tarefas()

        for tarefa in tarefas:
            print('╔════════════════════════════════════╗')
            print(f'  Nome: {tarefa["nome"]}')
            print(f'  Descrição: {tarefa["descricao"]}')
            print(f'  Data de Criação: {tarefa["data_criacao"]}')
            print(f'  Concluída? [ {('✔' if tarefa["concluida"] == True else '')} ]')
            print('╚════════════════════════════════════╝')
    except ValueError as e:
        print('\n')
        print(f'❌ {e}')

    pressionar_enter()


def menu_guia_sistema():
    """Exibe o menu com um guia e dicas de utilização do sistema"""

    limpar_tela()

    print('╔════════════════════════════════════╗')
    print('║         📖 GUIA DO SISTEMA         ║')
    print('╚════════════════════════════════════╝\n')

    print('📌 VISÃO GERAL')
    print('O sistema TODO possui dois menus principais:')
    print(
        '• Gerenciar Tarefas: Gerenciamento e manutenção de tarefas do usuário.'
    )
    print(
        '• Guia do Sistema: Manual de referência para navegação e uso eficiente do sistema.\n'
    )

    print('🎯 GERENCIAR TAREFAS')
    print('Neste menu você pode:')
    print('• Cadastrar novas tarefas')
    print('• Alterar tarefas existentes')
    print('• Excluir tarefas')
    print('• Visualizar tarefas')
    print('• Concluir / Desmarcar uma tarefa específica\n')

    print('💡 DICAS DE NAVEGAÇÃO')
    print('• Use as teclas numéricas para selecionar as opções dos menus')
    print('• Em listas de seleção, use ↑↓ para navegar')
    print('• Pressione Enter para confirmar uma seleção')
    print('• Pressione ESC para cancelar uma operação')
    print('• Digite 0 para voltar ao menu anterior\n')

    print('╔══════════════════════════════════════════╗')
    print('║    Desenvolvido por: André Davi Lopes    ║')
    print('║                                          ║')
    print('║  © Copyright 2025 - All Rights Reserved  ║')
    print('╚══════════════════════════════════════════╝\n')

    pressionar_enter()


def create_terminal_menu_opcoes_tarefa_concluida() -> int:
    """Cria um menu interativo no terminal com as opções de Sim e Não.

    Returns:
        int: A opção selecionada pelo usuário.
    """
    tarefa_controller = TarefaController()
    tarefas: list = tarefa_controller.listar_tarefas()

    menu_opcoes = ['Sim', 'Não']
    opcao_escolhida = create_terminal_menu(menu_opcoes, 'Concluída?')

    if opcao_escolhida is None:
        raise ValueError('Operação cancelada pelo usuário')

    return True if menu_opcoes.index(opcao_escolhida) == 0 else False


def create_terminal_menu(itens: list, titulo: str) -> str:
    """Cria um menu interativo no terminal usando a biblioteca Questionary.

    Args:
        itens (list): Lista de opções para exibição no menu.
        titulo (str): Título do menu.

    Returns:
        str: A opção selecionada pelo usuário.
    """
    return questionary.select(
        message=f'{titulo} \n\n ↑↓: Navegar | Enter: Selecionar | CTRL + C: Cancelar \n',
        choices=itens,
        qmark='>>',
        pointer='>> ',
        style=questionary.Style(
            [
                ('pointer', 'fg:#1E90FF bold'),
                ('highlighted', 'fg:#000000 bg:#1E90FF bold'),
                ('selected', 'fg:#000000 bg:#1E90FF bold'),
                ('question', 'bold fg:#FFCC00'),
            ]
        ),
    ).ask()


try:
    menu_principal()
except Exception as e:
    print(f'❌ {e}')
