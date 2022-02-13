# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import pandas as pd

import numpy as np
import re, random
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

res_table = pd.read_csv("F:/_Daily/★_Chatbot_Renewal/LINA/★LINA-RASA/actions/RESPONSE_EXP_LINA.csv", encoding='utf-8')

entities_all = list(set(res_table['entity name'].to_list()))

class ActionRephraseResponse(Action):
    # 액션에 대한 이름을 설정
    def name(self) -> Text:
        return "action_rephrase_mentalcare"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message['entities'])

        self.intent = tracker.get_intent_of_latest_message()
        self.entity_dicts = tracker.latest_message['entities']

        self.data = res_table[res_table['intent'] == self.intent]
        self.intent_entities = set(self.data['entity name'].values)
        self.main_entity = 'NONE'

        for entity in self.entity_dicts:
            if entity['entity'] in self.intent_entities:
                self.main_entity = entity['entity']

        print(self.intent, '\t', self.main_entity)

        utter_row = self.data[self.data['entity name'] == self.main_entity]

        first_response = utter_row['response'].values[0].split(' / ')
        first_response = random.sample(first_response, 1)[0]
        dispatcher.utter_message(text=first_response)

        utter_link_text = utter_row["utter_link"].values[0].split(' / ')
        utter_link_text = random.sample(utter_link_text, 1)[0]
        dispatcher.utter_message(text=utter_link_text)

        dispatcher.utter_message(image=utter_row['utter_send_link'].values[0])

        utter_ask_more_text = utter_row["utter_ask_more"].values[0].split(' / ')
        utter_ask_more_text = random.sample(utter_ask_more_text, 1)[0]
        dispatcher.utter_message(text=utter_ask_more_text)

        return []

def Josa_Replace(pattern, sentence):
    if '](' in pattern:
        if len(pattern.split('](')) > 2:
            back_syl = pattern.split('](')[-2][-1]
        else:
            back_syl = pattern.split('](')[0][-1]
    else:
        back_syl = pattern[0]

    criteria = (ord(back_syl) - 44032) % 28
    if criteria == 0: #무종성
        repl_pattern = re.sub("<[이가]>", "가", pattern)
        repl_pattern = re.sub("<[은는]>", "는", repl_pattern)
        repl_pattern = re.sub("<[을를]>", "를", repl_pattern)
        repl_pattern = re.sub("<[와과]>", "와", repl_pattern)
        repl_pattern = re.sub("<(이랑|랑)>", "랑", repl_pattern)
        repl_pattern = re.sub("<(으로|로)>", "로", repl_pattern)
        repl_pattern = re.sub("<(이서|서)>", "서", repl_pattern)
    else:
        repl_pattern = re.sub("<[이가]>", "이", pattern)
        repl_pattern = re.sub("<[은는]>", "은", repl_pattern)
        repl_pattern = re.sub("<[을를]>", "을", repl_pattern)
        repl_pattern = re.sub("<[와과]>", "과", repl_pattern)
        repl_pattern = re.sub("<(이랑|랑)>", "이랑", repl_pattern)
        repl_pattern = re.sub("<(으로|로)>", "으로", repl_pattern)
        repl_pattern = re.sub("<(이서|서)>", "이서", repl_pattern)
    # print(pattern, '\t', back_syl , '\t', '%s' % repl_pattern)
    return sentence.replace(pattern, '%s' % repl_pattern)
