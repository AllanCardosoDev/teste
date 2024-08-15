import discord
from discord.ui import View, Button, Select
import config
from mediators.mediator_config import MediatorConfigModal, UploadQRCodeModal

class MediatorConfigView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Select(placeholder="Selecione a ação que deseja executar.", options=[
            discord.SelectOption(label="Chave Pix", description="Sete sua chave pix."),
            discord.SelectOption(label="QR-code", description="Sete sua imagem qr-code.")
        ]))

    @discord.ui.select(placeholder="Selecione a ação que deseja executar.", min_values=1, max_values=1, options=[
        discord.SelectOption(label="Chave Pix", description="Sete sua chave pix."),
        discord.SelectOption(label="QR-code", description="Sete sua imagem qr-code.")
    ])
    async def select_action(self, interaction: discord.Interaction, select: discord.ui.Select):
        if select.values[0] == "Chave Pix":
            await interaction.response.send_modal(MediatorConfigModal())
        elif select.values[0] == "QR-code":
            await interaction.response.send_modal(UploadQRCodeModal())

class MediatorQueueView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Entrar na Fila", style=discord.ButtonStyle.success, custom_id="entrar_fila_mediador"))
        self.add_item(Button(label="Sair da Fila", style=discord.ButtonStyle.danger, custom_id="sair_fila_mediador"))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        custom_id = interaction.data['custom_id']
        if custom_id == "entrar_fila_mediador":
            await self.entrar_fila_mediador(interaction)
        elif custom_id == "sair_fila_mediador":
            await self.sair_fila_mediador(interaction)
        return True

    async def entrar_fila_mediador(self, interaction: discord.Interaction):
        mediator = interaction.user.mention
        if mediator not in config.FILAS['mediador']:
            config.FILAS['mediador'].append(mediator)
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.send_message("Você já está na fila!", ephemeral=True)

    async def sair_fila_mediador(self, interaction: discord.Interaction):
        mediator = interaction.user.mention
        if mediator in config.FILAS['mediador']:
            config.FILAS['mediador'].remove(mediator)
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    def create_embed(self):
        embed = discord.Embed(
            title="Fila de Controle",
            description="Mediadores disponíveis",
            color=0x00ff00
        )
        for idx, mediator in enumerate(config.FILAS['mediador']):
             embed.add_field(name=f"{idx + 1}. {mediator}", value="\u200b", inline=False)
        return embed
