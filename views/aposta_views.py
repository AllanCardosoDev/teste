import discord
from discord.ui import Button, View
from data.aposta_data import fila_apostas, CONFIRMATION_CHANNEL_ID
from views.confirmation_views import ConfirmationView
from mediators.mediator_config import MediatorConfig

class ApostaFilaView(View):
    def __init__(self, tipo, valor):
        super().__init__(timeout=None)
        self.tipo = tipo
        self.valor = valor
        self.add_item(Button(label="Entrar na Fila", style=discord.ButtonStyle.success, custom_id="entrar_fila"))
        self.add_item(Button(label="Sair da Fila", style=discord.ButtonStyle.danger, custom_id="sair_fila"))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        custom_id = interaction.data['custom_id']
        if custom_id == "entrar_fila":
            await self.entrar_fila(interaction, self.tipo)
        elif custom_id == "sair_fila":
            await self.sair_da_fila(interaction, self.tipo)
        return True

    async def entrar_fila(self, interaction: discord.Interaction, tipo: str):
        jogador = interaction.user.mention
        if jogador not in fila_apostas[tipo]:
            fila_apostas[tipo].append(jogador)
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
            if len(fila_apostas[tipo]) == 2:
                await self.criar_confirmacao(interaction, tipo)
        else:
            await interaction.response.send_message("Você já está na fila!", ephemeral=True)

    async def sair_da_fila(self, interaction: discord.Interaction, tipo: str):
        jogador = interaction.user.mention
        if jogador in fila_apostas[tipo]:
            fila_apostas[tipo].remove(jogador)
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    async def criar_confirmacao(self, interaction: discord.Interaction, tipo: str):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, id=CONFIRMATION_CHANNEL_ID)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        jogadores = fila_apostas[tipo][:2]

        for jogador in jogadores:
            member = discord.utils.get(guild.members, mention=jogador)
            overwrites[member] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        mediator_config = MediatorConfig()
        mediator_id = next(iter(mediator_config.mediators), None)
        if mediator_id:
            mediator = guild.get_member(mediator_id)
            overwrites[mediator] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        channel = await category.create_text_channel(f"confirmação-{self.tipo}", overwrites=overwrites)

        for jogador in jogadores:
            member = discord.utils.get(guild.members, mention=jogador)
            await channel.set_permissions(member, read_messages=True, send_messages=True)

        await interaction.followup.send(f"Canal de confirmação criado: {channel.mention}", ephemeral=True)

        embed = discord.Embed(
            title="Confirmação de Aposta",
            description="Clique no botão de confirmação para prosseguir.",
            color=0x00ff00
        )
        embed.add_field(name="Estilo da partida", value=f"{self.tipo} — R${self.valor}")
        embed.set_footer(text="Horário • Hoje")
        view = ConfirmationView(self.tipo, self.valor, jogadores, mediator)
        await channel.send(embed=embed, view=view)

        fila_apostas[tipo].clear()
        embed = self.create_embed()
        await interaction.message.edit(embed=embed, view=self)

    def create_embed(self):
        embed = discord.Embed(
            title="🏆 | APOSTE JÁ",
            description=f"Formato: {self.tipo}\nValor: R${self.valor}",
            color=0xffd700
        )
        embed.add_field(name="Jogadores", value=f"{', '.join(fila_apostas[self.tipo]) or 'Sem jogadores'}")
        return embed

class GeloFilaView(View):
    def __init__(self, tipo, valor):
        super().__init__(timeout=None)
        self.tipo = tipo
        self.valor = valor
        self.add_item(Button(label="Gelo Normal", style=discord.ButtonStyle.primary, custom_id="gelo_normal"))
        self.add_item(Button(label="Gelo Infinito", style=discord.ButtonStyle.primary, custom_id="gelo_infinito"))
        self.add_item(Button(label="Sair da Fila", style=discord.ButtonStyle.danger, custom_id="sair_fila"))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        custom_id = interaction.data['custom_id']
        if custom_id == "gelo_normal":
            await self.entrar_fila(interaction, "Gelo Normal")
        elif custom_id == "gelo_infinito":
            await self.entrar_fila(interaction, "Gelo Infinito")
        elif custom_id == "sair_fila":
            await self.sair_da_fila(interaction, self.tipo)
        return True

    async def entrar_fila(self, interaction: discord.Interaction, tipo: str):
        jogador = interaction.user.mention
        if jogador not in fila_apostas[tipo]:
            fila_apostas[tipo].append(jogador)
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
            if len(fila_apostas[tipo]) == 2:
                await self.criar_confirmacao(interaction, tipo)
        else:
            await interaction.response.send_message("Você já está na fila!", ephemeral=True)

    async def sair_da_fila(self, interaction: discord.Interaction, tipo: str):
        jogador = interaction.user.mention
        if jogador in fila_apostas[tipo]:
            fila_apostas[tipo].remove(jogador)
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    async def criar_confirmacao(self, interaction: discord.Interaction, tipo: str):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, id=CONFIRMATION_CHANNEL_ID)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        jogadores = fila_apostas[tipo][:2]

        for jogador in jogadores:
            member = discord.utils.get(guild.members, mention=jogador)
            overwrites[member] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        mediator_config = MediatorConfig()
        mediator_id = next(iter(mediator_config.mediators), None)
        if mediator_id:
            mediator = guild.get_member(mediator_id)
            overwrites[mediator] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        channel = await category.create_text_channel(f"confirmação-{self.tipo}", overwrites=overwrites)

        for jogador in jogadores:
            member = discord.utils.get(guild.members, mention=jogador)
            await channel.set_permissions(member, read_messages=True, send_messages=True)

        await interaction.followup.send(f"Canal de confirmação criado: {channel.mention}", ephemeral=True)

        embed = discord.Embed(
            title="Confirmação de Aposta",
            description="Clique no botão de confirmação para prosseguir.",
            color=0x00ff00
        )
        embed.add_field(name="Estilo da partida", value=f"{self.tipo} — R${self.valor}")
        embed.set_footer(text="Horário • Hoje")
        view = ConfirmationView(self.tipo, self.valor, jogadores, self.mediator)
        await channel.send(embed=embed, view=view)

        fila_apostas[tipo].clear()
        embed = self.create_embed()
        await interaction.message.edit(embed=embed, view=self)

    def create_embed(self):
        embed = discord.Embed(
            title="🏆 | APOSTE JÁ",
            description=f"Formato: {self.tipo}\nValor: R${self.valor}",
            color=0xffd700
        )
        embed.add_field(name="Jogadores", value=f"{', '.join(fila_apostas[self.tipo]) or 'Sem jogadores'}")
        return embed
