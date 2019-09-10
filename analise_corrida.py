"""
# Análise da corrida
Com base no arquivo de entrada que contém os dados da corrida vamos extrair os seguintes resultados:
* Posição Chegada, Código Piloto, Nome Piloto, Qtde Voltas Completadas e Tempo Total de Prova.
##### Bônus
* Descobrir a melhor volta de cada piloto
* Descobrir a melhor volta da corrida
* Calcular a velocidade média de cada piloto durante toda corrida
* Descobrir quanto tempo cada piloto chegou após o vencedor

Para isso usaremos o Python e a biblioteca de análise de dados Pandas.
"""

import pandas as pd

'''
### Formatando o arquivo de entrada

Antes de começarmos o log fornecido foi copiado e colado em um arquivo ('corrida') sem extensão para podermos 
manipula-lo.
O arquivo campos separados por espaços em branco e outros separados por tabulação (\t), dessa forma vamos tratar o 
arquivo, trocando todas as tabulações por espaços e salvando um novo arquivo ('corrida2').
'''

texto = []
# Abre o arquivo e carrega todas as linhas substituindo \t por um espaço em branco
with open('corrida', 'r', encoding='utf-8') as data_corrida:
    for line in data_corrida:
        texto.append(line.replace('\t', ' '))

# Salva o novo arquivo com o texto formatado
with open('corrida2', 'w', encoding='utf-8') as arquivo:
    arquivo.writelines(texto)

'''
### Carregando os dados no Pandas

Vamos carregar o novo arquivo no pandas utilizando o recurso *read_csv*, indicar o nome que cada coluna receberá, 
e por fim excluir o primeiro registro que representa o header do arquivo.
O processo foi feito dessa forma pois ao definir no pandas que o separador entre as colunas é o espaço, os nomes 
dos campos no header serão devidos em cada um de seus espaços, fazendo necessária a limpeza no dataframe.
'''

# Definindo o nome das colunas
names =[
    'hora', 'n_piloto', '-', 'piloto', 'n_volta', 'tempo_volta',
    'velocidade_media_volta', '1', '2', '3'
]

# Carregando as informações no pandas
df = pd.read_csv('corrida2', delim_whitespace=True, names=names)
# Deletando as colunas ['-', '1', '2', '3'] que não tem nem uma utilidade para nós
df = df.drop(columns=['-', '1', '2', '3'])
# Deletando a primeira linha do dataframe, nela estão as informações do header que descartamos.
df = df.drop([0], axis=0)

# Imprimindo o dataframe.
print(df)

'''
### Formatando o DataFrame

Nesse ponto o dataframe está carregado com as informações.
Alguns detalhes devem ser modificados para obter o resultado desejado:
* O nome do piloto F.MASSA está escrito errado em uma das linhas.
* Transformar o n_volta em um valor numérico, pois no momento todos os campos são objects
* Formatar o campo tempo_volta para time_delta, isso permite operações com tempo de forma mais fácil
* Formatar o campo velocidade_media_volta para numérico, assim podemos descobrir a velocidade média na corrida

Todos os campos foram carregados no pandas como Object, é preciso transformar os campos para realizar as operações 
aritméticas desejadas.
'''

# Corrigindo o erro no nome "F.MASS"
df['piloto'] = df['piloto'].replace('F.MASS', 'F.MASSA')
# Transformando o n_volta em numérico
df['n_volta'] = pd.to_numeric(df['n_volta'])
# Adicionando o '00:' ao tempo para ficar no padrão timedelta
df['tempo_volta'] = '00:' + df['tempo_volta']
# Transformando em time_delta
df['tempo_volta'] = pd.to_timedelta(df['tempo_volta'])
# Substituindo a virgula por ponto para ficar no padrão numérico
df['velocidade_media_volta'] = df['velocidade_media_volta'].str.replace(',', '.')
# Transformando em numérico
df['velocidade_media_volta'] = pd.to_numeric(df['velocidade_media_volta'])

print(df)

'''
## Obtendo os resultados espeados
* Posição Chegada, Código Piloto, Nome Piloto, Qtde Voltas Completadas e Tempo Total de Prova.
'''

# Agrupando o dataframe por n_piloto e piloto
agrupado = df.groupby(['n_piloto', 'piloto' ], sort=False)
# Com o dataframe agrupado, a função agg vai trazer o n_volta máximo de cada piloto
# e também a soma de tempo_volta de cada piloto
classificacao = agrupado.agg({'n_volta': 'max', 'tempo_volta': 'sum'})
# Ordenando o novo dataframe por tempo_volta, que agora corresponde a soma de todas as voltas.
classificacao = classificacao.sort_values(by='tempo_volta')
# print(classificacao)  # comentado para não poluir as saídas.

# Adicionando a coluna de classificação, em ordem porque o dataframe está ordenado do melhor
# para o pior tempo.
classificacao['posicao'] = [1, 2, 3, 4, 5 ,6]
# print(classificacao)  # comentado para não poluir as saídas.

# Renomeando as colunas e índices do dataframe para deixar os nome mais claros.
classificacao.rename(columns={'n_volta': 'Qtde Voltas Completadas', 'tempo_volta': 'Total de Prova',
                              'posicao': 'Posição Chegada'}, inplace='True')
classificacao.index.names = ['Código Piloto', 'Nome Piloto']

# resultado.
print(classificacao)

'''
## Bônus
* Descobrir a melhor volta de cada piloto
'''

# Utilizando o mesmo dataframe agrupado, pegando o menor tempo de cada piloto
melhor_volta = agrupado.agg({'tempo_volta': 'min'})

# resultado.
print(melhor_volta)

'''
## Bônus
* Descobrir a melhor volta da corrida
'''

# Resultado 1
# Filtrando somente o registro da melhor volta
print(df.where(df['tempo_volta'] == df['tempo_volta'].min()).dropna())

# Resultado 2
# Neste caso como o dataframe não é muito grande, é possível ordena-lo e ver as melhores voltas ordenas
# ordenando o dataframe por tempo, do menor para o maior.
print(df.sort_values(by='tempo_volta'))

'''
## Bônus
* Calcular a velocidade média de cada piloto durante toda corrida
'''

# Agrupando em um novo dataframe
agrupado = df.groupby(['n_piloto', 'piloto'], sort=False)
# Com o dataframe agrupado, mean traz a média da coluna velocidade_media_volta, ou seja,
# a velocidade média de cada piloto na corrida.
vel_media = agrupado.agg({'velocidade_media_volta': 'mean'})

# Resultado
print(vel_media)

'''
## Bônus
* Descobrir quanto tempo cada piloto chegou após o vencedor
'''

# Extraindo o tempo do vencedor. (O dataframe classificacao foi ordenado por melhor tempo de prova)
melhor_tempo = classificacao['Total de Prova'].iloc[0]
# Adicionando a coluna Tempo após vencedor com a diferença do tempo de cada piloto para o primeiro.
classificacao['Tempo após vencedor'] = classificacao['Total de Prova'] - melhor_tempo

# Resultado
print(classificacao)
