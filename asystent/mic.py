#!/usr/bin/python3
# -*- coding: utf-8 -*-

end = None

import paho.mqtt.client as mqtt
import speech_recognition as sr

BROKER = "localhost"
# BROKER = 'mqtt.lab.ii.agh.edu.pl'

################################################################################

def send(topic,payload):
  global client

  client.publish(topic,payload,retain=False) #publish
end

################################################################################

def on_message(client, userdata, message):
  topic = message.topic
  payload = str(message.payload.decode("utf-8"))
end

################################################################################


def init():
  global client
  global r

  # print("creating new instance")
  client = mqtt.Client("mic-pc") #create new instance
#  client.on_message=on_message #attach function to callback
  print("connecting to broker")
  client.connect(BROKER) #connect to broker
  client.loop_start() #start the loop
#  client.subscribe([("xxxcmd/tts/pc",0),("ola/#",0)])

  r = sr.Recognizer()

end

################################################################################

def loop():
  global r

  while True:
    tekst = input(">>")
    if len(tekst)>0:
      send("sig/stt/pc",tekst)
    else:
      with sr.Microphone() as source:
        print("slucham ...")
        audio = r.listen(source)
        try:
          tekst = r.recognize_google(audio, language='pl_PL')
          send("sig/stt/pc",tekst)
          print(tekst)
          if tekst=='koniec':
            break
        except sr.UnknownValueError:
          print('nie rozumiem')
        except sr.RequestError as e:
          print('error:',e)
  end
end

################################################################################

init()
loop()

################################################################################
