# Nutrition assistent

The assistent answers questions about the calories, protein, carbohydrates, fats of any given food from database. You can also ask about their value in the given product weight.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install needed packages: SpeechRecognition, pyttsx3, paho-mqtt, pyaudio which are in the file requirements.txt

```bash
pip install -r requirements.txt
```

## User guide
1. To integrate MQTT into Nutrition Assistant, you need to setup an MQTT broker by setting it in the file spk.py.
2. In 3 terminals run files spk.py, mic.py and food.py
3. After entering question manually or (after enter) ask a question you should see it in spk.py and food.py.
4. Heard answer is printed in food.py and mic.py. Which means that the operation reached the MQTT server and came back to us because we are subscribing to the topic.

### Example:
![274016941_1472857043110338_4763022591450647126_n](https://user-images.githubusercontent.com/57807232/154250860-b0737ff0-1228-4be1-8380-81be5537ae8e.png)



## Logging
There is a standard Python logging module for logging. This module ensures that messages are formatted correctly according to our formatting standards. Logs are saved in the file speakerlog.py.

```python
import logging
```


## Nutrition Dataset
Dataset was taken from: ["Tabela wartości odżywczych"](https://cloud2x.edupage.org/cloud/TABELA_WARTOSCI_ODZYWCZYCH.pdf?z%3APDDb3bKBXlY%2FWjIPy4GrEnwqpQPbkRKS5bz%2B61bSkv9GuOPTeTEfb6uDNr0VpRuj)
