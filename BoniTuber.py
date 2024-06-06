# Código desenvolvido por Rodrigo Bonicenha Ferreira
# Para contatos profissionais, treinamentos, projetos e consultoria entre em contato através dos canais abaixo:
# Linkedin: https://www.linkedin.com/in/rodrigo-bonicenha/
# Whatsapp: +5541991392100
#
# Este código é livre para edição e uso, desde que as informações sobre o autor não sejam removidas.
#
# Data de Criação: 05/06/2024
# Versão: v1.0.0
# Última modificação em: 05/06/2024
#
# Código developed by Rodrigo Bonicenha Ferreira
# For professional contacts, training, projects, and consulting, please reach out through the channels below:
# Linkedin: https://www.linkedin.com/in/rodrigo-bonicenha/
# Whatsapp: +5541991392100
#
# This code is free for editing and use, as long as the author's information is not removed.
#
# Creation Date: 2024-06-05
# Version: v1.0.0
# Last modified on: 2024-06-05
#
# Code desarrollado por Rodrigo Bonicenha Ferreira
# Para contactos profesionales, capacitaciones, proyectos y consultoría, comuníquese a través de los siguientes canales:
# Linkedin: https://www.linkedin.com/in/rodrigo-bonicenha/
# Whatsapp: +5541991392100
#
# Este código es libre para edición y uso, siempre y cuando no se elimine la información sobre el autor.
#
# Fecha de Creación: 05/06/2024
# Versión: v1.0.0
# Última modificación en: 05/06/2024
#
# Este código es libre para edición y uso, siempre y cuando no se elimine la información sobre el autor.

import scrapetube
import os
import time


def get_video_urls(channel_id):
    """
    Função para buscar todas as URLs de vídeos de um canal do YouTube.
    Función para obtener todas las URL de los videos de un canal de YouTube.
    Function to fetch all video URLs from a YouTube channel.

    Parâmetros / Parameters / Parámetros:
    - channel_id: ID do canal do YouTube / YouTube channel ID / ID del canal de YouTube

    Retorna / Returns / Devuelve:
    - Lista de URLs dos vídeos do canal / List of video URLs from the channel / Lista de URL de los videos del canal
    """
    # Buscar todos os vídeos do canal / Fetch all videos from the channel / Obtener todos los videos del canal
    videos = scrapetube.get_channel(channel_id)

    # Criar uma lista de URLs dos vídeos / Create a list of video URLs / Crear una lista de URL de los videos
    video_urls = []
    for video in videos:
        video_id = video['videoId']
        video_url = f'www.youtube.com/watch?v={video_id}'
        video_urls.append(video_url)

    return video_urls


def read_channels_from_file(filename):
    """
    Função para ler os canais e o intervalo de checagem de um arquivo.
    Function to read channels and the check interval from a file.
    Función para leer los canales y el intervalo de verificación de un archivo.

    Parâmetros / Parameters / Parámetros:
    - filename: Nome do arquivo contendo a lista de canais e intervalo / Name of the file containing the list of channels and interval / Nombre del archivo que contiene la lista de canales y el intervalo

    Retorna / Returns / Devuelve:
    - Dicionário de canais com seus IDs e URLs / Dictionary of channels with their IDs and URLs / Diccionario de canales con sus ID y URL
    - Intervalo de checagem em segundos / Check interval in seconds / Intervalo de verificación en segundos
    - Dicionário com o status dos idiomas para o output / Dictionary with language status for output / Diccionario con el estado de los idiomas para la salida
    """
    channels = {}
    interval = 300  # Padrão de 300 segundos / Default to 300 seconds / Predeterminado a 300 segundos
    languages = {'portugues': 'disable', 'spanish': 'disable', 'english': 'disable'}

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            current_channel = None
            for line in lines:
                line = line.strip()
                if line.startswith("Nome_do_Canal_"):
                    current_channel = line.split(" = ")[1]
                    channels[current_channel] = {"id": None, "urls": []}
                elif line.startswith("ID_do_Canal_"):
                    current_channel_id = line.split(" = ")[1]
                    channels[current_channel]["id"] = current_channel_id
                elif line.startswith("Intervalo_de_Checagem"):
                    interval = int(line.split(" = ")[1])
                elif line.startswith("portugues") or line.startswith("spanish") or line.startswith("english"):
                    lang, status = line.split(" = ")
                    languages[lang] = status

    return channels, interval, languages


def write_channels_to_file(channels):
    """
    Função para escrever as URLs dos vídeos em arquivos de canais.
    Function to write video URLs to channel files.
    Función para escribir las URL de los videos en archivos de canales.

    Parâmetros / Parameters / Parámetros:
    - channels: Dicionário de canais com seus URLs / Dictionary of channels with their URLs / Diccionario de canales con sus URL
    """
    for channel, data in channels.items():
        channel_formatted = channel.replace(" ", "_")
        filename = f"{channel_formatted}.txt"
        with open(filename, 'w') as file:
            for url in data['urls']:
                file.write(f"{url}\n")


def update_channels_from_youtube(channels, languages):
    """
    Função para atualizar as URLs dos vídeos dos canais a partir do YouTube.
    Function to update video URLs of channels from YouTube.
    Función para actualizar las URL de los videos de los canales desde YouTube.

    Parâmetros / Parameters / Parámetros:
    - channels: Dicionário de canais com seus IDs e URLs / Dictionary of channels with their IDs and URLs / Diccionario de canales con sus ID y URL
    - languages: Dicionário com o status dos idiomas para o output / Dictionary with language status for output / Diccionario con el estado de los idiomas para la salida

    Retorna / Returns / Devuelve:
    - Verdadeiro se houver atualização, Falso caso contrário / True if there is an update, False otherwise / Verdadero si hay una actualización, Falso en caso contrario
    """
    updated = False
    for channel, data in channels.items():
        print(f"Verificando actualizaciones de videos del Canal {channel}")
        if languages['english'] == 'enable':
            print(f"Checking for video updates from Channel {channel}")

        current_urls = get_video_urls(data['id'])
        new_videos = [url for url in current_urls if url not in data['urls']]

        if new_videos:
            if languages['portugues'] == 'enable':
                print(
                    f"Foram encontrados {len(new_videos)} vídeos novos para o Canal {channel}. Atualizando nossa base de dados...")
            if languages['spanish'] == 'enable':
                print(
                    f"Se encontraron {len(new_videos)} videos nuevos para el Canal {channel}. Actualizando nuestra base de datos...")
            if languages['english'] == 'enable':
                print(f"Found {len(new_videos)} new videos for Channel {channel}. Updating our database...")

            data['urls'].extend(new_videos)
            updated = True

    return updated


def main():
    """
    Função principal que coordena a execução do script.
    Main function that coordinates the execution of the script.
    Función principal que coordina la ejecución del script.
    """
    channels_file = 'lista_de_canais.txt'

    # Verificar se o arquivo lista_de_canais.txt existe
    # Check if the file lista_de_canais.txt exists
    # Verificar si el archivo lista_de_canais.txt existe
    if not os.path.exists(channels_file):
        print(
            f"O arquivo {channels_file} não existe. Por favor, crie este arquivo com a lista de canais e intervalo de checagem.")
        if languages['english'] == 'enable':
            print(
                f"The file {channels_file} does not exist. Please create this file with the list of channels and check interval.")
        if languages['spanish'] == 'enable':
            print(
                f"El archivo {channels_file} no existe. Por favor, cree este archivo con la lista de canales e intervalo de verificación.")
        return

    while True:
        # Ler canais e intervalo de checagem do arquivo
        # Read channels and check interval from the file
        # Leer los canales y el intervalo de verificación del archivo
        channels, check_interval, languages = read_channels_from_file(channels_file)

        # Verificar se os arquivos de canais existem e ler URLs existentes
        # Check if the channel files exist and read existing URLs
        # Verificar si los archivos de los canales existen y leer las URL existentes
        if channels:
            for channel in channels:
                channel_formatted = channel.replace(" ", "_")
                filename = f"{channel_formatted}.txt"
                if os.path.exists(filename):
                    with open(filename, 'r') as file:
                        lines = file.readlines()
                        channels[channel]["urls"] = [line.strip() for line in lines]

            # Atualizar vídeos dos canais apenas se houver novos vídeos
            # Update the channel videos only if there are new videos
            # Actualizar los videos de los canales solo si hay nuevos videos
            if update_channels_from_youtube(channels, languages):
                write_channels_to_file(channels)

        # Informar o próximo ciclo de checagem
        # Inform the next check cycle
        # Informar el próximo ciclo de verificación
        if languages['portugues'] == 'enable':
            print(f"Aguardando {check_interval} segundos para a próxima checagem...")
        if languages['spanish'] == 'enable':
            print(f"Esperando {check_interval} segundos para la próxima verificación...")
        if languages['english'] == 'enable':
            print(f"Waiting {check_interval} seconds for the next check...")

        time.sleep(check_interval)


if __name__ == "__main__":
    main()
