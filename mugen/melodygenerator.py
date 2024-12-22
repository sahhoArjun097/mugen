import json
import numpy as np
import tensorflow.keras as keras
import music21 as m21
from mugen.preprocess import SEQUENCE_LENGTH, MAPPING_PATH
import sys 



sys.stdout.reconfigure(encoding='utf-8')

class MelodyGenerator:
    """A class that wraps the LSTM model and offers utilities to generate melodies."""

    def __init__(self, model_number = 1):
        self.model_number = model_number
        
        model_path = f"model{model_number}.h5"
        try:
            self.model = keras.models.load_model(model_path)
        except ValueError as e:
            print(f"Error loading model: {e}")
            raise
        

        try:
            with open(MAPPING_PATH, "r") as fp:
                self._mappings = json.load(fp)
        except FileNotFoundError:
            print(f"Mapping file not found: {MAPPING_PATH}")
            raise


        self._start_symbols = ["/"] * SEQUENCE_LENGTH


    def generate_melody(self, seed, num_steps, max_sequence_length, temperature):
        """Generates a melody and returns a midi file.

        seed (str):                 Melody seed with the notation used to encode the dataset
        num_steps (int):            Number of steps to be generated
        max_sequence_len (int):     Max number of steps in seed to be considered for generation
        temperature (float):        Float in interval [0, 1]. Numbers closer to 0 make the model more deterministic.
                                    A number closer to 1 makes the generation more unpredictable.

        :return melody (list of str): List with symbols representing a melody
        """

        seed = seed.split()
        melody = seed
        seed = self._start_symbols + seed

        seed = [self._mappings[symbol] for symbol in seed]

        for _ in range(num_steps):

            seed = seed[-max_sequence_length:]

            encoded_seed = keras.utils.to_categorical(seed, num_classes = len(self._mappings))

            encoded_seed = encoded_seed[np.newaxis, ...]

            probabilities = self.model.predict(encoded_seed)[0]
            
            output_int = self._sample_with_temperature(probabilities, temperature)

            seed.append(output_int)

            output_symbol = [k for k, v in self._mappings.items() if v == output_int][0]

            if output_symbol == "/":
                break

            melody.append(output_symbol)

        return melody


    def _sample_with_temperature(self, probabilites, temperature):
        """Samples an index from a probability array reapplying softmax using temperature

        :param predictions (nd.array): Array containing probabilities for each of the possible outputs.
        :param temperature (float): Float in interval [0, 1]. Numbers closer to 0 make the model more deterministic.
            A number closer to 1 makes the generation more unpredictable.

        :return index (int): Selected output symbol
        """
        predictions = np.log(probabilites) / temperature
        probabilites = np.exp(predictions) / np.sum(np.exp(predictions))

        choices = range(len(probabilites)) # [0, 1, 2, 3]
        index = np.random.choice(choices, p=probabilites)
        
        print(index)
        return index


    def save_melody(self, melody, step_duration=0.25, format="midi"):
        """Converts a melody into a MIDI file

        :param melody (list of str):
        :param min_duration (float): Duration of each time step in quarter length
        :param file_name (str): Name of midi file
        :return:
        """

        file_name = f"model {self.model_number} mel 1.mid"
        stream = m21.stream.Stream()

        start_symbol = None
        step_counter = 1

        for i, symbol in enumerate(melody):

            if symbol != "_" or i + 1 == len(melody):

                if start_symbol is not None:

                    quarter_length_duration = step_duration * step_counter # 0.25 * 4 = 1

                    if start_symbol == "r":
                        m21_event = m21.note.Rest(quarterLength=quarter_length_duration)

                    else:
                        m21_event = m21.note.Note(int(start_symbol), quarterLength=quarter_length_duration)

                    stream.append(m21_event)

                    step_counter = 1

                start_symbol = symbol

            else:
                step_counter += 1

        stream.write(format, file_name)


if __name__ == "__main__":
    mg = MelodyGenerator(model_number = 4)
    seed1 = "67 _ 67 _ 67 _ _ 65 64 _ 64 _ 64 _ _ "
    seed2 = "67 _ _ _ _ _ 65 _ 64 _ 62 _ 60 _ _ _"
    seed3 = "55 _ _ 48 _ 61 _ 50 _ 52 _ r _ _ _"
    melody = mg.generate_melody(seed1, 60, SEQUENCE_LENGTH, 0.3)
    print(melody)
    mg.save_melody(melody)