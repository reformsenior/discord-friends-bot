"""Discord Friends Bot - Ponto de entrada principal."""

import os
import random
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

from content import PIADAS, RESPOSTAS_8BALL, escolher_aleatorio
from keep_alive import keep_alive


class FriendsBot(commands.Bot):
    """Bot simples para servidor de amigos.

    Garante que reconexões (on_ready repetidos) não duplicam handlers,
    pois comandos e eventos são registrados no __init__, não no on_ready.
    """

    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(command_prefix="!", intents=intents)
        self._ready_logged = False

    async def on_ready(self) -> None:
        """Registra no console que o bot está online.

        Seguro para reconexões: apenas loga a mensagem, sem registrar
        novos handlers ou listeners.
        """
        print(f"✅ Bot {self.user} está online e pronto para receber comandos!")

    async def on_member_join(self, member: discord.Member) -> None:
        """Envia mensagem de boas-vindas quando um novo membro entra no servidor.

        Ignora silenciosamente se o canal do sistema não existir ou se o bot
        não tiver permissão para enviar mensagens.
        """
        channel = member.guild.system_channel
        if channel is None:
            return

        try:
            await channel.send(
                f"Bem-vindo(a) ao servidor, {member.mention}! 🎉"
            )
        except discord.Forbidden:
            return

    async def on_message(self, message: discord.Message) -> None:
        """Processa mensagens ignorando bots."""
        if message.author.bot:
            return
        await self.process_commands(message)


def setup_commands(bot: commands.Bot) -> None:
    """Registra todos os comandos de diversão no bot.

    Estrutura extensível: novos comandos devem ser adicionados aqui.
    """

    @bot.command(name="piada")
    async def piada(ctx: commands.Context) -> None:
        """Conta uma piada aleatória."""
        if not PIADAS:
            await ctx.send("Nenhuma piada disponível no momento 😢")
            return
        await ctx.send(escolher_aleatorio(PIADAS))

    @bot.command(name="8ball")
    async def bola8(ctx: commands.Context, *, pergunta: str) -> None:
        """Bola 8 mágica responde sua pergunta."""
        resposta = escolher_aleatorio(RESPOSTAS_8BALL)
        await ctx.send(f"🎱 Pergunta: {pergunta}\nResposta: {resposta}")

    @bot.command(name="dado")
    async def dado(ctx: commands.Context, lados: int = 6) -> None:
        """Rola um dado com N lados (padrão: 6)."""
        if lados < 2:
            await ctx.send("Um dado precisa ter pelo menos 2 lados! 🎲")
            return
        if lados > 1000:
            await ctx.send("Calma, esse dado é grande demais! Máximo: 1000 🎲")
            return
        resultado = random.randint(1, lados)
        await ctx.send(f"🎲 Você rolou um d{lados} e tirou: {resultado}!")

    @bot.command(name="sorteio")
    async def sorteio(ctx: commands.Context, *opcoes: str) -> None:
        """Escolhe aleatoriamente entre as opções fornecidas."""
        if len(opcoes) < 2:
            await ctx.send(
                "Preciso de pelo menos 2 opções! Exemplo: `!sorteio pizza hamburguer sushi` 🎯"
            )
            return
        if len(opcoes) > 20:
            await ctx.send("Muitas opções! O máximo é 20. 🎯")
            return
        resultado = escolher_aleatorio(list(opcoes))
        await ctx.send(f"🎯 E o sorteado é... **{resultado}**!")


    @bot.command(name="moeda")
    async def moeda(ctx: commands.Context) -> None:
        """Joga cara ou coroa."""
        resultado = random.choice(["Cara", "Coroa"])
        await ctx.send(f"🪙 {resultado}!")

    @bot.command(name="entrar")
    async def entrar(ctx: commands.Context) -> None:
        """Entra no canal de voz do usuário."""
        if ctx.author.voice is None:
            await ctx.send("Você precisa estar em um canal de voz! 🔊")
            return
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"Entrei em **{channel.name}**! 🎧")

    @bot.command(name="sair")
    async def sair(ctx: commands.Context) -> None:
        """Sai do canal de voz."""
        if ctx.voice_client is None:
            await ctx.send("Não estou em nenhum canal de voz! 🔇")
            return
        await ctx.voice_client.disconnect()
        await ctx.send("Saí do canal de voz! 👋")


def main() -> None:
    """Inicializa e executa o bot."""
    load_dotenv()

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ Token não encontrado. Crie um arquivo .env com DISCORD_TOKEN=seu_token")
        sys.exit(1)

    bot = FriendsBot()
    setup_commands(bot)
    keep_alive()
    bot.run(token)


if __name__ == "__main__":
    main()
