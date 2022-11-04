import wave
import json
from urllib.request import urlopen
import pygame

def geolocate():
    data = json.load(urlopen("http://ipinfo.io/json"))
    lat = data['loc'].split(',')[0]
    lon = data['loc'].split(',')[1]

    msg = "_-_-_ SOS _-_-_  at " + "LATTITUDE: " + str(lat) + ", LONGITUDE: " + str(lon)
    return msg

encoded_msg = geolocate()
#print(encoded_msg)

def send_sos(string):

    pygame.mixer.init()

    audio = wave.open("test.wav",mode="rb") #open the audio clip
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes()))) #acquire frames
    string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'@'
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit #encode message in the audio frame
    frame_modified = bytes(frame_bytes)
    # for i in range(0,10):
    #     print(frame_bytes[i])
    print("Audio Signal Encoded... RickRolling...")
    newAudio =  wave.open('distress.wav',mode='wb')
    newAudio.setparams(audio.getparams())
    newAudio.writeframes(frame_modified) # writing the modified frame into a new wav file


    audio.close()
    newAudio.close()
    

def read_sos():
    audio = wave.open("distress.wav", mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
    decoded = string.split("@@@")[0]
    print("Message Received: "+decoded)
    audio.close()	

send_sos(encoded_msg)

choice = input("Decode ? (1/0)")
if(choice):
    read_sos()
