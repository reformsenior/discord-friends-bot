# Requirements Document

## Introduction

Este documento descreve os requisitos para o Discord Friends Bot — um bot simples de Discord para um servidor de amigos, oferecendo comandos de diversão (piada, 8ball, dado, sorteio, moeda) e mensagens automáticas de boas-vindas. O bot prioriza simplicidade e diversão instantânea, sem necessidade de banco de dados ou configuração complexa.

## Glossary

- **Bot**: A aplicação Discord que responde a comandos e eventos no servidor
- **Comando**: Uma mensagem enviada pelo usuário com o prefixo `!` seguido do nome do comando
- **Prefixo**: O caractere `!` que precede todos os comandos do bot
- **Canal_do_Sistema**: O canal configurado no servidor Discord para mensagens do sistema (boas-vindas)
- **Lista_de_Piadas**: A coleção de piadas armazenadas como constantes no código
- **Lista_de_Respostas_8Ball**: A coleção de respostas da bola 8 mágica armazenadas como constantes no código

## Requirements

### Requisito 1: Comando de Piada

**User Story:** Como um usuário do servidor, eu quero pedir uma piada ao bot, para que eu possa me divertir com meus amigos.

#### Critérios de Aceitação

1. WHEN um usuário envia o comando `!piada`, THE Bot SHALL responder com uma piada selecionada aleatoriamente da Lista_de_Piadas no mesmo canal onde o comando foi recebido
2. THE Lista_de_Piadas SHALL conter pelo menos 5 piadas, cada uma com no máximo 200 caracteres
3. IF a Lista_de_Piadas está vazia no momento da execução do comando, THEN THE Bot SHALL responder com uma mensagem de erro amigável indicando que nenhuma piada está disponível

### Requisito 2: Comando Bola 8 Mágica

**User Story:** Como um usuário do servidor, eu quero fazer perguntas à bola 8 mágica, para que eu possa receber respostas divertidas e aleatórias.

#### Critérios de Aceitação

1. WHEN um usuário envia o comando `!8ball` seguido de uma pergunta, THE Bot SHALL responder com a pergunta do usuário e uma resposta aleatória da Lista_de_Respostas_8Ball no mesmo canal onde o comando foi recebido
2. IF um usuário envia o comando `!8ball` sem uma pergunta, THEN THE Bot SHALL responder com uma mensagem de erro amigável indicando o uso correto do comando
3. THE Lista_de_Respostas_8Ball SHALL conter pelo menos 5 respostas, cada uma com no máximo 200 caracteres

### Requisito 3: Comando de Dado

**User Story:** Como um usuário do servidor, eu quero rolar dados virtuais, para que eu possa usar em jogos e decisões com meus amigos.

#### Critérios de Aceitação

1. WHEN um usuário envia o comando `!dado` com um número N de lados (2 <= N <= 1000), THE Bot SHALL responder no mesmo canal com um número aleatório entre 1 e N (inclusivo), indicando o tipo de dado rolado e o resultado obtido
2. WHEN um usuário envia o comando `!dado` sem argumentos, THE Bot SHALL rolar um dado de 6 lados e responder no mesmo canal com o resultado entre 1 e 6 (inclusivo), no mesmo formato do critério 1
3. IF um usuário envia o comando `!dado` com um valor menor que 2, THEN THE Bot SHALL responder com uma mensagem de erro indicando que o dado precisa ter pelo menos 2 lados
4. IF um usuário envia o comando `!dado` com um valor maior que 1000, THEN THE Bot SHALL responder com uma mensagem de erro indicando que o valor máximo permitido é 1000 lados
5. IF um usuário envia o comando `!dado` com um argumento não-numérico, THEN THE Bot SHALL responder com uma mensagem de erro indicando o formato correto de uso do comando

### Requisito 4: Comando de Sorteio

**User Story:** Como um usuário do servidor, eu quero que o bot sorteie entre opções que eu fornecer, para que eu possa tomar decisões de forma divertida.

#### Critérios de Aceitação

1. WHEN um usuário envia o comando `!sorteio` seguido de 2 ou mais opções separadas por espaço, THE Bot SHALL responder com uma mensagem contendo exatamente uma das opções fornecidas, escolhida aleatoriamente, de modo que a opção exibida pertença ao conjunto original de argumentos recebidos
2. IF um usuário envia o comando `!sorteio` com menos de 2 opções (0 ou 1 argumento), THEN THE Bot SHALL responder com uma mensagem de erro indicando que são necessárias pelo menos 2 opções e mostrando um exemplo de uso correto do comando
3. IF um usuário envia o comando `!sorteio` com mais de 20 opções, THEN THE Bot SHALL responder com uma mensagem de erro indicando que o número máximo de opções permitidas é 20

### Requisito 5: Comando de Moeda

**User Story:** Como um usuário do servidor, eu quero jogar cara ou coroa, para que eu possa fazer decisões simples de forma divertida.

#### Critérios de Aceitação

1. WHEN um usuário envia o comando `!moeda`, THE Bot SHALL responder no mesmo canal com "Cara" ou "Coroa", cada resultado com probabilidade igual (50%)
2. WHEN o Bot responde ao comando `!moeda`, THE Bot SHALL incluir exatamente um dos dois resultados possíveis ("Cara" ou "Coroa") sem nenhum outro valor alternativo

### Requisito 6: Mensagem de Boas-Vindas

**User Story:** Como um administrador do servidor, eu quero que novos membros sejam recebidos automaticamente, para que eles se sintam acolhidos ao entrar no servidor.

#### Critérios de Aceitação

1. WHEN um novo membro entra no servidor, THE Bot SHALL enviar uma mensagem de boas-vindas no Canal_do_Sistema que mencione o nome ou menção do novo membro
2. IF o Bot não tem permissão para enviar mensagens no Canal_do_Sistema, THEN THE Bot SHALL ignorar o evento silenciosamente sem gerar erro
3. IF o Canal_do_Sistema não está configurado no servidor (valor nulo ou inexistente), THEN THE Bot SHALL ignorar o evento de entrada sem gerar erro

### Requisito 7: Prefixo de Comandos

**User Story:** Como um usuário do servidor, eu quero que o bot só responda a mensagens com o prefixo correto, para que conversas normais não ativem o bot acidentalmente.

#### Critérios de Aceitação

1. THE Bot SHALL processar apenas mensagens que começam com o prefixo configurado (`!`) na primeira posição da mensagem
2. IF uma mensagem não começa com o prefixo configurado, THEN THE Bot SHALL ignorar a mensagem sem enviar qualquer resposta ou executar qualquer comando
3. WHEN o Bot recebe uma mensagem de si mesmo ou de outro bot, THE Bot SHALL ignorar a mensagem independentemente do conteúdo

### Requisito 8: Inicialização e Configuração

**User Story:** Como um desenvolvedor, eu quero configurar o bot através de variáveis de ambiente, para que eu possa gerenciar credenciais de forma segura.

#### Critérios de Aceitação

1. WHEN o Bot inicia, THE Bot SHALL carregar o token de autenticação da variável de ambiente `DISCORD_TOKEN`
2. IF a variável `DISCORD_TOKEN` não está definida ou está vazia, THEN THE Bot SHALL exibir uma mensagem de erro no console indicando que a variável `DISCORD_TOKEN` é obrigatória e encerrar a execução com código de saída diferente de zero
3. WHEN o Bot reconecta ao Discord (evento on_ready repetido), THE Bot SHALL manter o mesmo conjunto de comandos e event listeners registrados sem duplicações, garantindo que nenhum handler seja registrado mais de uma vez
4. WHEN o Bot conecta ao Discord com sucesso (evento on_ready), THE Bot SHALL registrar no console o nome do bot e a indicação de que está pronto para receber comandos

### Requisito 9: Tratamento de Erros

**User Story:** Como um usuário do servidor, eu quero que o bot responda de forma amigável quando eu cometo um erro, para que eu saiba como usar os comandos corretamente.

#### Critérios de Aceitação

1. WHEN um comando recebe argumentos inválidos, THE Bot SHALL responder no mesmo canal com uma mensagem de erro que inclui o uso correto do comando e continuar aceitando e processando comandos subsequentes
2. WHEN ocorre um erro inesperado durante a execução de um comando, THE Bot SHALL enviar uma mensagem no mesmo canal indicando que ocorreu um problema e que o usuário pode tentar novamente, sem interromper o processamento de comandos subsequentes
3. WHEN o Bot perde a conexão com o Discord Gateway, THE Bot SHALL reconectar automaticamente utilizando o mecanismo de reconexão do discord.py
4. WHEN um usuário envia um comando com o prefixo `!` que não corresponde a nenhum comando registrado, THE Bot SHALL ignorar a mensagem sem enviar resposta
