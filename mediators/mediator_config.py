import discord
from discord.ui import Modal, TextInput
import json
import os
import config

class MediatorConfig:
    def __init__(self):
        self.file_path = config.MEDIATORS_FILE
        self.mediators = self.load_mediators()

    def load_mediators(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        else:
            return {}

    def add_mediator(self, id, nome, chave_pix):
        self.mediators[str(id)] = {'nome': nome, 'chave_pix': chave_pix, 'qr_code_image': None}
        self.save_mediators()

    def update_qr_code(self, id, qr_code_image):
        if str(id) in self.mediators:
            self.mediators[str(id)]['qr_code_image'] = qr_code_image
            self.save_mediators()
        else:
            raise ValueError("Mediator not found")

    def save_mediators(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.mediators, f, indent=4)

    def get_mediators(self):
        return self.mediators

class MediatorConfigModal(Modal):
    def __init__(self):
        super().__init__(title="Configurar Chave PIX")
        self.add_item(TextInput(label="NOME", placeholder="Seu nome"))
        self.add_item(TextInput(label="CHAVE PIX", placeholder="Insira sua chave PIX aqui"))

    async def on_submit(self, interaction: discord.Interaction):
        nome = self.children[0].value
        chave_pix = self.children[1].value

        mediator_config = MediatorConfig()
        mediator_config.add_mediator(interaction.user.id, nome, chave_pix)

        await interaction.response.send_message("Cadastro realizado com sucesso!", ephemeral=True)

class UploadQRCodeModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(title="Enviar Imagem do QR Code", *args, **kwargs)
        self.add_item(TextInput(label="QR Code", placeholder="Digite o nome do arquivo conforme enviado no canal."))

    async def on_submit(self, interaction: discord.Interaction):
        qr_code_image = self.children[0].value
        file_path = os.path.join(config.IMAGES_PATH, qr_code_image)
        
        mediator_config = MediatorConfig()
        mediators = mediator_config.get_mediators()
        
        if str(interaction.user.id) in mediators:
            mediators[str(interaction.user.id)]['qr_code_image'] = file_path
            mediator_config.save_mediators()
            await interaction.response.send_message("QR Code enviado com sucesso!", ephemeral=True)
        else:
            await interaction.response.send_message("Você precisa se cadastrar primeiro.", ephemeral=True)
