import yaml
import Levenshtein
import json
import csv
from keras.models import load_model
from classifier import load_tokenizer_and_encoder


class Dialog:

    def __init__(self, config):

        with open("config.yml", 'r') as file:
            yaml_config = yaml.load(file, Loader=yaml.BaseLoader)

        self.model = load_model(yaml_config["path"]["model"])
        self.tokenizer, self.encoder = load_tokenizer_and_encoder(yaml_config["path"]["label_dialogs"]["train"])
        self.ontology = json.loads(open(yaml_config["path"]["ontology"]).read())
        self.restaurant_list = self._load_restaurant_info(yaml_config["path"]["restaurant_info_file"])

        self.levenshtein_edit_distance = config["levenshtein_edit_distance"]
        self.lowercase = config["lowercase"]
        self.baseline = config["baseline"]
        self.output_all_caps = config["output_all_caps"]

    def _load_restaurant_info(self, csvfile):

        with open(csvfile, 'r') as file:
            restaurant_list = list(csv.reader(file))

        return restaurant_list[1:]




if __name__ == "__main__":

    config = {'levenshtein_edit_distance': 0,
              'lowercase': True,
              'baseline': False,
              'output_all_caps': False}

    dialogs = Dialog(config)
