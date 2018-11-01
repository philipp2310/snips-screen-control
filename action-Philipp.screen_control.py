#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    """ Write the body of the function that will be executed once the intent is recognized. 
    In your scope, you have the following objects : 
    - intentMessage : an object that represents the recognized intent
    - hermes : an object with methods to communicate with the MQTT bus following the hermes protocol. 
    - conf : a dictionary that holds the skills parameters you defined. 
      To access global parameters use conf['global']['parameterName']. For end-user parameters use conf['secret']['parameterName'] 
    
    Refer to the documentation for further details. 
    """ 
    import subprocess
    result_sentence = ""
    # Map parameters to variable and get default values if they are missing
    if "text_an" in conf['global']:
      text_an = conf['global']['text_an'] 
    else:
      text_an = "Bild an!"
    if "text_aus" in conf['global']:
      text_aus = conf['global']['text_aus'] 
    else:
      text_aus = "Bild aus!"
    if "acoustic_feedback" in conf['global']:
      feedback = conf['global']['akustisches_feedback']
    else:
      feedback = "1"
    
    
    if len(intentMessage.slots.state) > 0:
      if intentMessage.slots.state.first().value == 'an':
        subprocess.call('DISPLAY=:0 xset dpms force on', shell=True)
        if feedback == "1":
          result_sentence = text_an
        else:
          print(text_an)
        current_session_id = intentMessage.session_id
        hermes.publish_end_session(current_session_id, result_sentence)
    
      else: #turn off
        subprocess.call('DISPLAY=:0 xset dpms force off', shell=True)
        if feedback == "1":
          result_sentence = text_aus
        else:
          print(text_aus)
        current_session_id = intentMessage.session_id
        hermes.publish_end_session(current_session_id, result_sentence)
    else: # should never happen
        result_sentence = "I guess you found an impossible path.. turn back and send me your feedback!"
        current_session_id = intentMessage.session_id
        hermes.publish_end_session(current_session_id, result_sentence)
    


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("Philipp:toggleScreen", subscribe_intent_callback) \
         .start()
