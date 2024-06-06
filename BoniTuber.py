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

# ===================================
# Detalhamento do Código (Português)
# ===================================
#
# Função get_video_urls
# Esta função é responsável por buscar todas as URLs de vídeos de um canal do YouTube.
# Utiliza a biblioteca 'scrapetube' para obter os vídeos do canal através do ID do canal.
# Itera sobre a lista de vídeos e extrai os IDs dos vídeos, criando as URLs correspondentes e armazenando-as em uma lista.
# A lista de URLs dos vídeos é retornada ao final da função.
#
# Função read_channels_from_file
# Esta função lê os canais e o intervalo de checagem de um arquivo especificado.
# Abre o arquivo e lê linha por linha, identificando o nome do canal, ID do canal, intervalo de checagem e os idiomas habilitados para output.
# Armazena essas informações em um dicionário de canais, no intervalo de checagem e no dicionário de idiomas.
# Retorna esses dados para serem utilizados em outras partes do código.
#
# Função write_channels_to_file
# Esta função escreve as URLs dos vídeos em arquivos específicos para cada canal.
# Itera sobre o dicionário de canais, cria ou abre arquivos nomeados de acordo com cada canal e escreve as URLs dos vídeos nesses arquivos.
#
# Função update_channels_from_youtube
# Esta função atualiza as URLs dos vídeos dos canais a partir do YouTube.
# Verifica se há novos vídeos para cada canal e, caso existam, atualiza a lista de URLs do canal.
# Imprime mensagens de atualização em diferentes idiomas, dependendo das configurações de idioma do usuário.
# Retorna 'True' se houver atualização e 'False' caso contrário.
#
# Função main
# Esta é a função principal que coordena a execução do script.
# Verifica se o arquivo 'lista_de_canais.txt' existe e, caso contrário, imprime mensagens de erro em diferentes idiomas.
# Em um loop infinito, lê os canais e o intervalo de checagem do arquivo, verifica e atualiza os vídeos dos canais e escreve as URLs atualizadas em arquivos.
# A cada ciclo, aguarda o intervalo de checagem especificado antes de repetir o processo.
#
# Estruturas condicionais
# Utilizadas para verificar a existência de arquivos e decidir quais mensagens imprimir com base nas configurações de idioma do usuário.
# Exemplo: if not os.path.exists(channels_file), if languages['english'] == 'enable'.
#
# Laços de repetição
# Utilizados para iterar sobre listas e dicionários.
# Exemplo: for video in videos, for line in lines, for channel, data in channels.items().
#
# Forks
# Utilizados para executar diferentes blocos de código com base nas configurações de idioma e na existência de novos vídeos.
# Exemplo: if update_channels_from_youtube(channels, languages), if not os.path.exists(channels_file).
#
# Variáveis
# Utilizadas para armazenar dados necessários para a execução do script, como listas de URLs, dicionários de canais, intervalo de checagem e configurações de idioma.
# Exemplo: channels, interval, languages, video_urls, filename, updated.
#
# Bibliotecas
# scrapetube: Utilizada para buscar vídeos de um canal do YouTube.
# os: Utilizada para interagir com o sistema operacional, verificando a existência de arquivos.
# time: Utilizada para pausar a execução do script por um determinado intervalo de tempo.
#
# Este é um guia detalhado sobre as funções, estruturas e variáveis do código. Sinta-se à vontade para expandir ou modificar o código conforme necessário.
#
# ==========================
# Code Details (English)
# ==========================
#
# Function get_video_urls
# This function is responsible for fetching all video URLs from a YouTube channel.
# It uses the 'scrapetube' library to get the channel's videos by its ID.
# It iterates over the list of videos and extracts the video IDs, creating the corresponding URLs and storing them in a list.
# The list of video URLs is returned at the end of the function.
#
# Function read_channels_from_file
# This function reads the channels and check interval from a specified file.
# It opens the file and reads it line by line, identifying the channel name, channel ID, check interval, and enabled output languages.
# It stores this information in a dictionary of channels, the check interval, and the language dictionary.
# It returns these data to be used in other parts of the code.
#
# Function write_channels_to_file
# This function writes the video URLs to specific files for each channel.
# It iterates over the dictionary of channels, creates or opens files named according to each channel, and writes the video URLs to these files.
#
# Function update_channels_from_youtube
# This function updates the video URLs of the channels from YouTube.
# It checks if there are new videos for each channel and, if there are, updates the channel's URL list.
# It prints update messages in different languages, depending on the user's language settings.
# It returns 'True' if there is an update and 'False' otherwise.
#
# Function main
# This is the main function that coordinates the script's execution.
# It checks if the 'lista_de_canais.txt' file exists and, if not, prints error messages in different languages.
# In an infinite loop, it reads the channels and check interval from the file, checks and updates the channels' videos, and writes the updated URLs to files.
# In each cycle, it waits for the specified check interval before repeating the process.
#
# Conditional structures
# Used to check for the existence of files and decide which messages to print based on the user's language settings.
# Example: if not os.path.exists(channels_file), if languages['english'] == 'enable'.
#
# Loops
# Used to iterate over lists and dictionaries.
# Example: for video in videos, for line in lines, for channel, data in channels.items().
#
# Forks
# Used to execute different blocks of code based on language settings and the existence of new videos.
# Example: if update_channels_from_youtube(channels, languages), if not os.path.exists(channels_file).
#
# Variables
# Used to store data needed for the script's execution, such as lists of URLs, dictionaries of channels, check interval, and language settings.
# Example: channels, interval, languages, video_urls, filename, updated.
#
# Libraries
# scrapetube: Used to fetch videos from a YouTube channel.
# os: Used to interact with the operating system, checking for file existence.
# time: Used to pause the script's execution for a specified interval.
#
# This is a detailed guide on the functions, structures, and variables of the code. Feel free to expand or modify the code as needed.
#
# ======================================
# Detalles del Código (Español)
# ======================================
#
# Función get_video_urls
# Esta función es responsable de obtener todas las URL de los videos de un canal de YouTube.
# Utiliza la biblioteca 'scrapetube' para obtener los videos del canal mediante su ID.
# Itera sobre la lista de videos y extrae los IDs de los videos, creando las URLs correspondientes y almacenándolas en una lista.
# La lista de URLs de los videos se devuelve al final de la función.
#
# Función read_channels_from_file
# Esta función lee los canales y el intervalo de verificación de un archivo especificado.
# Abre el archivo y lo lee línea por línea, identificando el nombre del canal, ID del canal, intervalo de verificación y los idiomas habilitados para salida.
# Almacena esta información en un diccionario de canales, el intervalo de verificación y el diccionario de idiomas.
# Devuelve estos datos para ser utilizados en otras partes del código.
#
# Función write_channels_to_file
# Esta función escribe las URLs de los videos en archivos específicos para cada canal.
# Itera sobre el diccionario de canales, crea o abre archivos nombrados de acuerdo con cada canal y escribe las URLs de los videos en estos archivos.
#
# Función update_channels_from_youtube
# Esta función actualiza las URLs de los videos de los canales desde YouTube.
# Verifica si hay nuevos videos para cada canal y, si los hay, actualiza la lista de URLs del canal.
# Imprime mensajes de actualización en diferentes idiomas, dependiendo de la configuración de idioma del usuario.
# Devuelve 'True' si hay una actualización y 'False' en caso contrario.
#
# Función main
# Esta es la función principal que coordina la ejecución del script.
# Verifica si el archivo 'lista_de_canais.txt' existe y, si no, imprime mensajes de error en diferentes idiomas.
# En un bucle infinito, lee los canales y el intervalo de verificación del archivo, verifica y actualiza los videos de los canales y escribe las URLs actualizadas en archivos.
# En cada ciclo, espera el intervalo de verificación especificado antes de repetir el proceso.
#
# Estructuras condicionales
# Utilizadas para verificar la existencia de archivos y decidir qué mensajes imprimir según la configuración de idioma del usuario.
# Ejemplo: if not os.path.exists(channels_file), if languages['english'] == 'enable'.
#
# Bucles
# Utilizados para iterar sobre listas y diccionarios.
# Ejemplo: for video in videos, for line in lines, for channel, data in channels.items().
#
# Bifurcaciones
# Utilizadas para ejecutar diferentes bloques de código según la configuración de idioma y la existencia de nuevos videos.
# Ejemplo: if update_channels_from_youtube(channels, languages), if not os.path.exists(channels_file).
#
# Variables
# Utilizadas para almacenar los datos necesarios para la ejecución del script, como listas de URLs, diccionarios de canales, intervalo de verificación y configuración de idioma.
# Ejemplo: channels, interval, languages, video_urls, filename, updated.
#
# Bibliotecas
# scrapetube: Utilizada para obtener videos de un canal de YouTube.
# os: Utilizada para interactuar con el sistema operativo, verificando la existencia de archivos.
# time: Utilizada para pausar la ejecución del script durante un intervalo de tiempo especificado.
#
# Esta es una guía detallada sobre las funciones, estructuras y variables del código. Siéntase libre de expandir o modificar el código según sea necesario.
