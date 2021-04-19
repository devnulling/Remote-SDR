#!/usr/bin/python3
#Collect spectral data to be passed to a web client
#Recuperation des données  spectre de GNU_Radio et envoi vers le client web
import socket
import asyncio
import websockets
s_spectre = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = 'localhost'                           
port_spectre_Web = 8002
port_spectre_GR = 9002
s_spectre.bind((host, port_spectre_GR))                               
print("Passerelle Spectre vers client WEB")
# Reception 2048 bytes du spectre 
# on recupere les data de GNU-RADIO
async def spectre(websocket_s, path):
    while True:
        msg_spectre = s_spectre.recv(2048)
        await websocket_s.send(msg_spectre)

start_server_spectre = websockets.serve(spectre, "", port_spectre_Web)
asyncio.get_event_loop().run_until_complete(start_server_spectre)
asyncio.get_event_loop().run_forever()
