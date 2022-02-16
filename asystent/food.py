# -*- coding: utf-8 -*-

import time
import weakref
import paho.mqtt.client as mqtt
import csv
import re
import logging
BROKER = "localhost"
# BROKER = "mqtt.lab.ii.agh.edu.pl"
ID = "mag"


class FoodRepository:
  def __init__(self, file='./asystent/resources/data.csv'):
    with open(file, newline='', encoding='utf-8') as csvfile:
      lines = csv.reader(csvfile, delimiter=',', quotechar='|')
      self.data = {}
      for line in lines:
        line = [word.strip().lower() for word in line]
        if len(line) != 5:
          continue
        food, kcal, protein, fat, carbs = line
        self.data[food] = {
          'food': food,
          'kcal': kcal,
          'prot': protein,
          'fat': fat,
          'carbs': carbs
        }

  def find(self, food):
    try:
      return self.data[food.strip().lower()]
    except KeyError:
      return None

food_repo = FoodRepository()

################################################################################


def asystent(pytanie):
  list_of_words = list_pytanie = pytanie.split()
  words_re = re.compile("|".join(list_of_words))

  if words_re.search('kalori kalorii węglowodanu węglowodanów tłuszczy tłuszczu tłuszczów białka białek'):
  # if any([word in 'kalori kalorii węglowodany węglowodanów tłuszczy tłuszczu tłuszczów białka białek' for word in pytanie]):
    
    pytanie = pytanie.replace("posiada", "ma")
    pytanie = pytanie.replace("mają", "ma")
    pytanie = pytanie.replace("kalori", "kalorii")
    pytanie = pytanie.replace("węglowodanu", "węglowodanów")
    pytanie = pytanie.replace("tłuszczy", "tłuszczów")
    pytanie = pytanie.replace("tłuszczu", "tłuszczów")
    pytanie = pytanie.replace("białek", "białka")
    pytanie = pytanie.replace("dekagramach", "dkg")
    pytanie = pytanie.replace("kilo", "kg")
    pytanie = pytanie.replace("kilogramach", "kg")
    pytanie = pytanie.replace(" g", "gramach")


    list_pytanie = pytanie.split()
    weight = re.findall(r'\d+', pytanie)
    index = list_pytanie.index('ma') + 1

    if len(weight):
      try:
        food = list_pytanie[index: list_pytanie.index('w') ]
      except:
        food = list_pytanie[index: list_pytanie.index(weight) ]
      food = ' '.join(food)
      if re.search('gramach', pytanie):
        count = int(weight[0]) / 100
        weight_type = 'gramy'
      
      if re.search('kg', pytanie):
      
        count = (int(weight[0]) * 1000) / 100
        weight_type = 'kilogramy'

      if re.search('dkg', pytanie):
        count = (int(weight[0]) * 10) / 100
        weight_type = 'dekagramy'

      data = food_repo.find(food.strip())

      if data:
        if re.search('kalorii', pytanie ):
          return f"{data['food']} ma {float(data['kcal'])*count} kilo kalorii na {weight} {weight_type}"
        if re.search('węglowodanów', pytanie ):
          return f"{data['food']} ma {float(data['prot'])*count} gramów węglowodanów na {weight} {weight_type}"
        if re.search('tłuszczów', pytanie ):
          return f"{data['food']} ma {float(data['fat'])*count} gramów tłuszczu na {weight} {weight_type}"
        if re.search('białka', pytanie ):
          return f"{data['food']} ma {float(data['carbs'])*count} gramów białka na {weight} {weight_type}"
      else:
        return f"Nie ma takiego jedzenia w bazie"

    else:
      food = list_pytanie[index: ]
      food = ' '.join(food)
      
      data = food_repo.find(food.strip())

      if data:
        if re.search('kalorii', pytanie ):
          return f"{data['food']} ma {data['kcal']} kilo kalorii na 100 gram"
        if re.search('węglowodanów', pytanie ):
          return f"{data['food']} ma {data['prot']} gramów węglowodanów na 100 gram"
        if re.search('tłuszczów', pytanie ):
          return f"{data['food']} ma {data['fat']} gramów tłuszczu na 100 gram"
        if re.search('białka', pytanie ):
          return f"{data['food']} ma {data['carbs']} gramów białka na 100 gram"
      else:
        return f"Nie ma takiego jedzenia w bazie"
    return None


################################################################################

def s(topic,payload):
  global client
  print("snd",topic,payload)
  client.publish(topic,payload,retain=False) #publish


################################################################################

def on_message(client, userdata, message):
  topic = message.topic
  payload = str(message.payload.decode("utf-8"))

  print("rcv",topic,payload)

  odp = asystent(payload.lower())
  logging.basicConfig(level=logging.DEBUG, filename="speakerlogs.log", filemode="a")
  logging.debug("Question: {}".format(payload) + " Answer: {}".format(odp))
  if odp is not None:
    s("cmd/tts/"+ID,odp)



################################################################################

def init():
  global client
  # print("creating new instance")
  client = mqtt.Client(ID) #create new instance
  client.on_message=on_message #attach function to callback
  # print("connecting to broker")
  client.connect(BROKER) #connect to broker
  client.loop_start() #start the loop
  client.subscribe(("sig/stt/#",0))



################################################################################

def loop():
  while True:
    time.sleep(60)


################################################################################

init()
loop()

################################################################################
