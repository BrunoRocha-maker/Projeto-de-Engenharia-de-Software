# Dias da semana, horários permitidos e mapa numérico
dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
mapa_dias = {"1": "Segunda", "2": "Terça", "3": "Quarta", "4": "Quinta", "5": "Sexta"}
horarios = list(range(7, 19))

# Inicializa o cronograma
cronograma = {dia: {hora: "Livre" for hora in horarios} for dia in dias_semana}
cronograma["Quinta"][17] = "Treino Time"


def exibir_tabela():
    """Exibe a tabela de horários formatada no terminal."""
    print("\n" + "=" * 90)
    print(f"{'CRONOGRAMA DA QUADRA DE VÔLEI - IFRS RESTINGA':^90}")
    print("=" * 90)

    print(f"{'Hora':<7}", end="")
    for dia in dias_semana:
        print(f"{dia:<16}", end="")
    print("\n" + "-" * 90)

    for hora in horarios:
        print(f"{hora:02d}:00  ", end="")
        for dia in dias_semana:
            status = cronograma[dia][hora]
            
            # Se for um dicionário (agendamento de aluno), extrai o nome
            if isinstance(status, dict):
                texto = status["nome"]
            else:
                texto = status
                
            texto_formatado = texto[:14] if len(texto) > 14 else texto
            print(f"{texto_formatado:<16}", end="")
        print()
    print("-" * 90)


def escolher_dia():
    """Função auxiliar para validar a escolha do dia (texto ou número)."""
    print(f"Dias válidos: 1-Segunda, 2-Terça, 3-Quarta, 4-Quinta, 5-Sexta")
    entrada_dia = input("Escolha o dia da semana (Nome ou de 1 a 5): ").strip().capitalize()
    
    if entrada_dia in mapa_dias:
        return mapa_dias[entrada_dia]
    elif entrada_dia in dias_semana:
        return entrada_dia
    else:
        print("❌ Dia inválido!")
        return None


def fazer_agendamento():
    """Gerencia a lógica de novos agendamentos com os novos requisitos."""
    print("\n--- NOVO AGENDAMENTO ---")
    
    dia = escolher_dia()
    if not dia:
        return

    try:
        hora = int(input("Digite o horário (7 às 18): "))
    except ValueError:
        print("❌ Entrada inválida! Digite apenas o número.")
        return

    # Validações de horário
    if hora < 7 or hora > 18:
        print("❌ Horário fora do permitido (7h às 18h).")
        return
    if dia == "Quinta" and hora == 17:
        print("❌ Esse horário está indisponível: Treino do Time do Campus!")
        return
    if cronograma[dia][hora] != "Livre":
        print("❌ Conflito de horário! Este horário já está ocupado.")
        return

    # Coleta de dados do estudante
    print("\nPreencha os dados do responsável pela reserva:")
    nome = input("Nome completo: ").strip()
    email = input("E-mail: ").strip()
    matricula = input("Número de matrícula: ").strip()

    if not nome or not email or not matricula:
        print("❌ Todos os campos são obrigatórios!")
        return

    # Regra: O aluno só pode agendar um horário por dia
    for h in horarios:
        reserva_existente = cronograma[dia][h]
        if isinstance(reserva_existente, dict) and reserva_existente["matricula"] == matricula:
            print(f"❌ Limite atingido! A matrícula {matricula} já possui reserva na {dia} às {h}h.")
            return

    # Efetiva a reserva
    cronograma[dia][hora] = {
        "nome": nome,
        "email": email,
        "matricula": matricula
    }
    print(f"✅ Sucesso! Quadra agendada para '{nome}' na {dia} às {hora}h.")


def cancelar_agendamento():
    """Permite o cancelamento de uma reserva mediante confirmação da matrícula."""
    print("\n--- CANCELAR AGENDAMENTO ---")
    
    dia = escolher_dia()
    if not dia:
        return

    try:
        hora = int(input("Digite o horário da reserva (7 às 18): "))
    except ValueError:
        print("❌ Entrada inválida! Digite apenas o número.")
        return

    reserva = cronograma[dia][hora]

    # Verifica se há algo para cancelar
    if reserva == "Livre" or reserva == "Treino Time":
        print("❌ Não há reserva de estudante neste horário para ser cancelada.")
        return

    # Exige a matrícula para garantir que quem está cancelando é o dono da reserva
    matricula_confirmacao = input("Digite a matrícula usada na reserva para confirmar: ").strip()

    if reserva["matricula"] == matricula_confirmacao:
        cronograma[dia][hora] = "Livre"
        print("✅ Reserva cancelada com sucesso! O horário está livre novamente.")
    else:
        print("❌ Matrícula incorreta! Cancelamento não autorizado.")


def menu():
    """Loop principal do sistema."""
    while True:
        print("\n=== SISTEMA DE AGENDAMENTO IFRS-RESTINGA ===")
        print("1. Visualizar Tabela de Horários")
        print("2. Agendar Quadra")
        print("3. Cancelar Agendamento")
        print("4. Sair")

        opcao = input("Escolha uma opção (1-4): ").strip()

        if opcao == "1":
            exibir_tabela()
        elif opcao == "2":
            fazer_agendamento()
        elif opcao == "3":
            cancelar_agendamento()
        elif opcao == "4":
            print("\nEncerrando o sistema. Bom jogo!")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")


if __name__ == "__main__":
    menu()