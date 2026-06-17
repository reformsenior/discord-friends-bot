# Implementation Plan: Discord Friends Bot

## Overview

Implementar um bot Discord simples para servidor de amigos usando Python e discord.py. O bot oferece comandos de diversão (piada, 8ball, dado, sorteio, moeda), mensagens de boas-vindas automáticas, e tratamento de erros amigável. A implementação segue uma arquitetura minimalista sem banco de dados.

## Tasks

- [ ] 1. Configurar estrutura do projeto e dependências
  - [x] 1.1 Criar estrutura de arquivos e configuração do ambiente
    - Criar `requirements.txt` com discord.py>=2.3.0, python-dotenv>=1.0.0 e hypothesis (dev)
    - Criar arquivo `.env.example` com DISCORD_TOKEN=seu_token_aqui
    - Criar `main.py` com ponto de entrada do bot
    - Configurar intents necessários (message_content, members)
    - _Requisitos: 8.1, 8.2, 8.4_

  - [x] 1.2 Implementar carregamento de configuração e validação do token
    - Usar python-dotenv para carregar variáveis do `.env`
    - Validar que DISCORD_TOKEN existe e não está vazio
    - Exibir mensagem de erro clara no console se token ausente
    - Encerrar com código de saída diferente de zero se token inválido
    - _Requisitos: 8.1, 8.2_

- [ ] 2. Implementar o Bot Core e eventos base
  - [x] 2.1 Criar classe do bot e evento on_ready
    - Instanciar `commands.Bot` com prefixo `!` e intents corretos
    - Implementar `on_ready` que registra no console o nome do bot
    - Garantir que reconexões (on_ready repetidos) não duplicam handlers
    - _Requisitos: 7.1, 7.3, 8.3, 8.4_

  - [ ] 2.2 Implementar evento de boas-vindas (on_member_join)
    - Enviar mensagem de boas-vindas no canal do sistema mencionando o novo membro
    - Ignorar silenciosamente se canal do sistema não existir ou bot não tiver permissão
    - _Requisitos: 6.1, 6.2, 6.3_

- [ ] 3. Implementar comandos de diversão
  - [x] 3.1 Criar listas de conteúdo (piadas e respostas 8ball)
    - Definir `PIADAS` com pelo menos 5 piadas em português (máx 200 caracteres cada)
    - Definir `RESPOSTAS_8BALL` com pelo menos 5 respostas (máx 200 caracteres cada)
    - Criar função utilitária `escolher_aleatorio(lista)` para seleção aleatória
    - _Requisitos: 1.2, 2.3_

  - [ ] 3.2 Implementar comando `!piada`
    - Selecionar piada aleatória da lista usando `escolher_aleatorio()`
    - Enviar resposta no mesmo canal do comando
    - Tratar caso de lista vazia com mensagem amigável
    - _Requisitos: 1.1, 1.3_

  - [ ] 3.3 Implementar comando `!8ball`
    - Aceitar argumento `pergunta` obrigatório
    - Responder com a pergunta do usuário e resposta aleatória formatada
    - Enviar erro amigável se pergunta não fornecida
    - _Requisitos: 2.1, 2.2_

  - [ ] 3.4 Implementar comando `!dado`
    - Aceitar argumento opcional `lados` com padrão 6
    - Validar: 2 <= lados <= 1000
    - Gerar número aleatório entre 1 e lados (inclusivo)
    - Retornar mensagem formatada com tipo do dado e resultado
    - Retornar erro amigável para valores inválidos (<2, >1000, não-numérico)
    - _Requisitos: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [ ] 3.5 Implementar comando `!sorteio`
    - Aceitar 2+ opções separadas por espaço
    - Escolher aleatoriamente uma opção e exibir resultado formatado
    - Retornar erro amigável se menos de 2 opções ou mais de 20
    - _Requisitos: 4.1, 4.2, 4.3_

  - [ ] 3.6 Implementar comando `!moeda`
    - Escolher aleatoriamente entre "Cara" e "Coroa" (50% cada)
    - Enviar resultado formatado com emoji
    - _Requisitos: 5.1, 5.2_

- [ ] 4. Checkpoint - Verificar funcionamento dos comandos
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implementar tratamento de erros global
  - [ ] 5.1 Implementar handler de erros de comandos
    - Capturar `MissingRequiredArgument` e enviar uso correto do comando
    - Capturar `BadArgument` e enviar mensagem sobre formato esperado
    - Capturar erros inesperados e enviar mensagem genérica amigável
    - Ignorar comandos desconhecidos (CommandNotFound) sem resposta
    - _Requisitos: 9.1, 9.2, 9.3, 9.4_

  - [ ] 5.2 Garantir que o bot ignora mensagens sem prefixo e de outros bots
    - Verificar que mensagens sem `!` não ativam comandos
    - Verificar que mensagens de bots (incluindo o próprio) são ignoradas
    - _Requisitos: 7.1, 7.2, 7.3_

- [ ] 6. Testes
  - [ ] 6.1 Escrever testes unitários para funções utilitárias
    - Testar `validar_dado()` com valores limites (1, 2, 1000, 1001)
    - Testar `escolher_aleatorio()` retorna item da lista
    - Testar formatação das respostas dos comandos
    - _Requisitos: 3.1, 3.3, 3.4, 1.1, 4.1_

  - [ ]* 6.2 Escrever teste de propriedade: aleatoriedade dentro dos limites
    - **Propriedade 1: Aleatoriedade dentro dos limites**
    - Usar hypothesis para gerar inteiros entre 2 e 1000
    - Verificar que resultado do dado está sempre entre 1 e N
    - **Valida: Requisito 3.1**

  - [ ]* 6.3 Escrever teste de propriedade: seleção de lista válida
    - **Propriedade 2: Seleção de lista válida**
    - Usar hypothesis para gerar listas não-vazias de strings
    - Verificar que `escolher_aleatorio()` sempre retorna item da lista
    - **Valida: Requisitos 1.1, 2.1, 5.1**

  - [ ]* 6.4 Escrever teste de propriedade: sorteio justo
    - **Propriedade 3: Sorteio justo**
    - Usar hypothesis para gerar listas de 2+ strings
    - Verificar que resultado do sorteio pertence às opções originais
    - **Valida: Requisito 4.1**

  - [ ]* 6.5 Escrever teste de propriedade: sem crash em entrada inválida
    - **Propriedade 5: Sem crash em entrada inválida**
    - Usar hypothesis para gerar inteiros fora dos limites (<2, >1000)
    - Verificar que `validar_dado()` retorna erro sem exceção
    - **Valida: Requisitos 3.3, 3.4, 3.5, 4.2, 9.1**

- [ ] 7. Checkpoint final - Garantir que tudo funciona
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marcadas com `*` são opcionais e podem ser puladas para um MVP mais rápido
- Cada task referencia requisitos específicos para rastreabilidade
- Checkpoints garantem validação incremental
- Testes de propriedade validam propriedades universais de corretude
- Testes unitários validam exemplos específicos e casos extremos
- O bot usa Python com discord.py>=2.3.0 e python-dotenv>=1.0.0
- Biblioteca hypothesis é usada para testes de propriedade

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2"] },
    { "id": 2, "tasks": ["2.1", "3.1"] },
    { "id": 3, "tasks": ["2.2", "3.2", "3.3", "3.4", "3.5", "3.6"] },
    { "id": 4, "tasks": ["5.1", "5.2"] },
    { "id": 5, "tasks": ["6.1", "6.2", "6.3", "6.4", "6.5"] }
  ]
}
```
