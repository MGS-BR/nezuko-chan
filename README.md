# Nezuko-chan Discord Bot

Bot de Discord desenvolvido em **Python** usando **Disnake**, com comandos slash, sistema de economia, níveis, perfis, tags, memes, interações sociais, comandos de anime e ferramentas administrativas para servidores.

## Funcionalidades

- Comandos slash (`/`) com suporte a inglês e português.
- Sistema de economia com moedas, daily e leaderboard.
- Sistema de XP/níveis global e por servidor.
- Perfis personalizados com descrição e background.
- Comandos sociais com GIFs/imagens de anime.
- Busca de animes, personagens, notícias e waifus.
- Geração de imagens/montagens de meme.
- Sistema de tags por servidor.
- Moderação com ban, unban, lock, unlock, lockdown e clear.
- Armazenamento de dados em MongoDB.

## Tecnologias utilizadas

- Python
- Disnake
- MongoDB / PyMongo
- Easy PIL
- Animec
- PRAW
- Emoji
- Pytz

## Estrutura do projeto

```txt
nezuko-chan-main/
├── main.py
├── config.json
└── cogs/
    ├── commands/
    │   ├── admin/
    │   ├── normal/
    │   └── tags/
    ├── custom/
    ├── errors/
    ├── images/
    └── utilities/
```

## Configuração

Crie um arquivo chamado `config.json` na raiz do projeto:

```json
{
  "token": "TOKEN_DO_SEU_BOT",
  "mongo": "URL_DE_CONEXAO_DO_MONGODB"
}
```

> Nunca envie o `config.json` com token real para o GitHub. Adicione ele ao `.gitignore`.

Exemplo de `.gitignore`:

```gitignore
config.json
__pycache__/
*.pyc
.env
```

## Instalação

Clone o repositório:

```bash
git clone https://github.com/MGS-BR/nezuko-chan.git
cd nezuko-chan
```

Instale as dependências:

```bash
pip install disnake pymongo easy-pil animec praw emoji pytz
```

Execute o bot:

```bash
python main.py
```

## Comandos

### Administração

| Comando | Descrição |
|---|---|
| `/lock [channel]` | Bloqueia um canal para impedir mensagens de membros comuns. |
| `/unlock [channel]` | Desbloqueia um canal. |
| `/lockdown start` | Inicia lockdown no servidor, bloqueando os canais. |
| `/lockdown end` | Finaliza o lockdown. |
| `/clear amount [user] [message]` | Apaga mensagens do canal, com filtro opcional por usuário ou conteúdo. |
| `/ban user [time] [reason]` | Bane um usuário. Aceita tempo como `s`, `m`, `h` ou `d`. |
| `/unban user [reason]` | Remove o banimento de um usuário. |

### Anime

| Comando | Descrição |
|---|---|
| `/anime search anime` | Pesquisa informações sobre um anime. |
| `/anime character search` | Pesquisa informações sobre um personagem. |
| `/anime news [amount]` | Mostra notícias de anime. |
| `/anime waifu` | Mostra uma waifu aleatória. |

### Informações gerais

| Comando | Descrição |
|---|---|
| `/server info [server]` | Mostra informações do servidor. |
| `/server icon [server]` | Mostra o ícone do servidor. |
| `/server banner [server]` | Mostra o banner do servidor. |
| `/user info [user]` | Mostra informações de um usuário. |
| `/user avatar [user]` | Mostra o avatar de um usuário. |
| `/user banner [user]` | Mostra o banner de um usuário. |
| `/emoji info emoji` | Mostra informações de um emoji. |

### Economia

| Comando | Descrição |
|---|---|
| `/daily` | Recebe moedas diárias. |
| `/balance [user]` | Mostra o saldo de moedas. |
| `/coins leaderboard` | Mostra o ranking de moedas. |

### Níveis e XP

| Comando | Descrição |
|---|---|
| `/xp stats [user]` | Mostra estatísticas de XP do usuário. |
| `/xp leaderboard global` | Mostra o ranking global de XP. |
| `/xp leaderboard local` | Mostra o ranking de XP do servidor. |

### Perfil

| Comando | Descrição |
|---|---|
| `/profile [user]` | Mostra o perfil de um usuário. |
| `/profilechange description text` | Altera a descrição do perfil. |
| `/profilechange background` | Altera o plano de fundo do perfil. |

### Social

| Comando | Descrição |
|---|---|
| `/hug user` | Abraça um usuário. |
| `/kiss user` | Beija um usuário. |
| `/slap user` | Dá um tapa em um usuário. |
| `/attack user` | Ataca um usuário. |
| `/dance user` | Dança com um usuário. |
| `/pat user` | Faz carinho em um usuário. |

### Memes e imagens

| Comando | Descrição |
|---|---|
| `/meme` | Envia um meme aleatório do Reddit. |
| `/memes bolsonaro [user] [image]` | Cria montagem usando template Bolsonaro. |
| `/memes perfeito [user] [image]` | Cria montagem usando template perfeito. |
| `/memes morrepraga [user] [image]` | Cria montagem usando template morre praga. |
| `/memes rip [user] [image]` | Cria montagem RIP. |
| `/memes wanted [user] [image]` | Cria montagem de procurado. |

### Tags

| Comando | Descrição |
|---|---|
| `/tag view name [category]` | Visualiza uma tag. |
| `/tag create name content [category]` | Cria uma tag. |
| `/tag delete name [category]` | Exclui uma tag. |
| `/tag edit name content [category]` | Edita uma tag. |
| `/tag list` | Lista as tags do servidor. |

### Idioma

| Comando | Descrição |
|---|---|
| `/language change` | Altera o idioma do servidor. Requer administrador. |
| `/language info` | Mostra o idioma atual do servidor. |

## Permissões necessárias

Para funcionar corretamente, o bot precisa das permissões de:

- Ler mensagens e canais
- Enviar mensagens
- Usar comandos slash
- Anexar arquivos
- Gerenciar mensagens
- Gerenciar canais
- Banir membros
- Ver membros do servidor

Alguns comandos administrativos exigem permissões específicas tanto do bot quanto do usuário.

## Banco de dados

O bot usa MongoDB para salvar dados de:

- Servidores
- Usuários
- XP
- Economia
- Tags
- Configurações de idioma
- Banimentos temporários

As principais collections usadas são:

```txt
discord.guilds
discord.users
discord.guilds_xp
discord.guilds_tags
discord.ban_time
```

## Observações importantes

- O bot usa comandos slash, então pode demorar alguns minutos para os comandos aparecerem no Discord.
- No `main.py`, existe um `test_guilds=[863538221366509578]`. Para usar em outro servidor, remova esse parâmetro ou troque pelo ID do seu servidor.
- O prefixo antigo configurado é `n!`, mas o próprio bot informa que o uso principal é por `/`.
- O projeto possui tratamento de erros para cooldowns, permissões e erros gerais.

## Licença

Adicione aqui a licença do projeto, caso queira publicar no GitHub.
