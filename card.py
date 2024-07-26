import requests
import json
import random
import itertools

# Defina a URL da API do Pipefy
url = "https://api.pipefy.com/graphql"

# Cabeçalho com o token de API
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJQaXBlZnkiLCJpYXQiOjE3MjE4ODc1NTMsImp0aSI6IjY3MWQ2YjE0LThlNGEtNGM1OC1hODJjLWNlM2I2ZGViMjk5ZSIsInN1YiI6MzA1MDE0NTQwLCJ1c2VyIjp7ImlkIjozMDUwMTQ1NDAsImVtYWlsIjoiZmVsaXBlLnBhcGFuaUB1ZnBlLmJyIn19.qQ7jeBinfMVCkW7E8Ut0Rgz1KG0pIPWkxaA53pJ8kpTIimUH2QoCoESJIKVt3zcZQjyVNF5b_GDK0jhurbBgWQ",
    "Content-Type": "application/json"
}

# Substitua pelo ID do pipe onde o card será criado
pipe_id = "304524179"

# Query para listar fases e campos de um pipe
query = """
{
  pipe(id: "%s") {
    phases {
      id
      name
      fields {
        id
        label
      }
    }
  }
}
""" % pipe_id

# Listas originais
nomes_atividades = [
    "Palestra sobre Neuroengenharia Avançada",
    "Workshop de Python para Iniciantes",
    "Mesa Redonda sobre Inteligência Artificial",
    "Sessão de Networking com Especialistas",
    "Demonstração de Tecnologia de Interface Cerebral",
    "Palestra sobre Ética na Neuroengenharia",
    "Workshop de Análise de Dados",
    "Mesa Redonda sobre Biotecnologia",
    "Sessão de Mentoria",
    "Demonstração de Realidade Virtual Terapêutica",
    "Palestra sobre Neuroplasticidade",
    "Workshop de Machine Learning",
    "Mesa Redonda sobre Startups em Saúde",
    "Sessão de Pitch de Projetos",
    "Demonstração de Tecnologia de Estimulação Cerebral"
]

descricao_atividades = [
    "Exploração das últimas tendências e inovações em neuroengenharia avançada.",
    "Curso introdutório prático ao uso do Python para projetos em neuroengenharia.",
    "Discussão sobre o impacto e futuro da inteligência artificial no setor de saúde.",
    "Oportunidade para se conectar e trocar ideias com especialistas da área.",
    "Demonstração ao vivo das mais recentes tecnologias de interface cérebro-computador.",
    "Debate sobre os desafios éticos na aplicação de tecnologias neuroengenheiras.",
    "Sessão prática sobre como analisar dados neurocientíficos usando Python.",
    "Discussão sobre as últimas inovações e desafios na biotecnologia.",
    "Encontro com mentores experientes para orientação e desenvolvimento de carreira.",
    "Exibição de aplicações de realidade virtual em tratamentos terapêuticos.",
    "Discussão sobre a capacidade do cérebro de se reorganizar e se adaptar.",
    "Introdução prática ao uso de machine learning em pesquisas neurocientíficas.",
    "Discussão sobre o impacto das startups e inovação no setor de saúde.",
    "Oportunidade para apresentar projetos inovadores e receber feedback.",
    "Demonstração das mais recentes tecnologias de estimulação cerebral para tratamentos médicos."
]

datas_atividades = [
    "2024-11-06",
    "2024-11-07",
    "2024-11-08",
    "2024-11-09"
]

# Gerar durações de 30 em 30 minutos, começando de 00:30 até 03:00
duracao_atividades = ["00:30","01:00","01:30","02:00","02:30","03:00","03:30","04:00","04:30",]
for hour in range(1, 4):
    for minute in [0, 30]:
        if hour == 3 and minute == 30:
            break
        duracao_atividades.append(f"{hour:02}:{minute:02}")

# Selecionar aleatoriamente algumas durações da lista gerada
duracao_atividades = random.sample(duracao_atividades, 5)

tipos_atividades = [
    "Palestra",
    "Workshop",
    "Mesa Redonda",
    "Outro"
]

# Combinando nome e descrição
atividades_combinadas = list(zip(nomes_atividades, descricao_atividades))

# Embaralhando as atividades combinadas
random.shuffle(atividades_combinadas)

# Separando as atividades embaralhadas em nomes e descrições
nomes_atividades_embaralhados, descricao_atividades_embaralhados = zip(*atividades_combinadas)

# Embaralhando datas, durações e tipos de atividades independentemente
random.shuffle(datas_atividades)
random.shuffle(duracao_atividades)
random.shuffle(tipos_atividades)

# Garantir que todas as listas tenham o mesmo tamanho
datas_atividades = itertools.cycle(datas_atividades)
duracao_atividades = itertools.cycle(duracao_atividades)
tipos_atividades = itertools.cycle(tipos_atividades)

# Loop para criar múltiplos cards
for i in range(len(nomes_atividades_embaralhados)):
    try:
        # Requisição POST para a API do Pipefy
        response = requests.post(url, headers=headers, json={"query": query})
        response.raise_for_status()  # Verifica se ocorreu algum erro HTTP

        # Exibir a resposta
        data = response.json()

        # Variável para armazenar o ID da fase "Recebimento de Propostas"
        recebimento_de_propostas_id = None
        # Lista para armazenar todos os IDs dos campos da fase "Recebimento de Propostas"
        field_ids = []

        # Extraindo IDs e Nomes das Fases e Campos
        phases = data.get('data', {}).get('pipe', {}).get('phases', [])

        for phase in phases:
            if phase['name'] == "Recebimento de Propostas":
                recebimento_de_propostas_id = phase['id']
                for field in phase['fields']:
                    field_ids.append(field['id'])

        if recebimento_de_propostas_id is None:
            raise ValueError("Não foi possível encontrar a fase 'Recebimento de Propostas'")

        # Criar fields_attributes dinamicamente com base nas listas embaralhadas
        fields_attributes = [
            {"field_id": field_ids[0], "field_value": nomes_atividades_embaralhados[i]},
            {"field_id": field_ids[1], "field_value": descricao_atividades_embaralhados[i]},
            {"field_id": field_ids[2], "field_value": next(tipos_atividades)},
            {"field_id": field_ids[3], "field_value": next(datas_atividades)},
            {"field_id": field_ids[4], "field_value": next(duracao_atividades)}
        ]

        # Debugging logs
        print(f"Phase ID: {recebimento_de_propostas_id}")
        print(f"Field IDs: {field_ids}")
        print(f"Fields Attributes: {fields_attributes}")

        # Criar a query de forma programática
        fields_attributes_str = ', '.join(
            [f'{{field_id: "{fa["field_id"]}", field_value: "{fa["field_value"]}"}}' for fa in fields_attributes]
        )

        values = [fa['field_value'] for fa in fields_attributes]

        mutation_query = f"""
        mutation {{
          createCard(input: {{
            pipe_id: "{pipe_id}",
            phase_id: "{recebimento_de_propostas_id}",
            fields_attributes: [{fields_attributes_str}],
            title: "{values[0]}" # Define o título do card como o nome da atividade
          }}) {{
            card {{
              id
              title
            }}
          }}
        }}
        """

        # Requisição POST para criar o card
        response = requests.post(url, headers=headers, json={"query": mutation_query})
        response.raise_for_status()  # Verifica se ocorreu algum erro HTTP

        # Exibir a resposta
        data = response.json()
        print("Resposta JSON:", data)

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
    except ValueError as e:
        print(f"Erro: {e}")
    except ValueError:
        print("Erro ao processar a resposta JSON")
print(field_ids)
