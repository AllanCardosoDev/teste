import discord
from discord.ui import View, Button

class ConfirmationView(View):
    def __init__(self, tipo, valor, jogadores, mediator):
        super().__init__(timeout=None)
        self.tipo = tipo
        self.valor = valor
        self.jogadores = jogadores
        self.mediator = mediator
        self.confirmations = {jogador: False for jogador in jogadores}

        self.add_item(Button(label="Confirmar", style=discord.ButtonStyle.success, custom_id="confirmar"))
        self.add_item(Button(label="Sair", style=discord.ButtonStyle.danger, custom_id="sair"))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        custom_id = interaction.data['custom_id']
        if custom_id == "confirmar":
            await self.confirmar(interaction)
        elif custom_id == "sair":
            await self.sair(interaction)
        return True

    async def confirmar(self, interaction: discord.Interaction):
        jogador = interaction.user.mention
        if jogador in self.confirmations:
            self.confirmations[jogador] = True
            if all(self.confirmations.values()):
                await self.finalizar_aposta(interaction)
            else:
                await interaction.response.send_message("Aguardando confirmação do outro jogador...", ephemeral=True)
        else:
            await interaction.response.send_message("Você não está na lista de jogadores para esta aposta.", ephemeral=True)

    async def sair(self, interaction: discord.Interaction):
        jogador = interaction.user.mention
        if jogador in self.confirmations:
            await interaction.channel.delete()
            await interaction.response.send_message("Aposta cancelada.", ephemeral=True)
        else:
            await interaction.response.send_message("Você não está na lista de jogadores para esta aposta.", ephemeral=True)

    async def finalizar_aposta(self, interaction: discord.Interaction):
        await interaction.channel.send(f"Aposta confirmada! Mediador: {self.mediator.mention}")
        await interaction.channel.delete()
