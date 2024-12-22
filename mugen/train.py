import tensorflow.keras as keras
from mugen.preprocess import generate_training_sequences, SEQUENCE_LENGTH
import sys 

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_UNITS = 25
NUM_UNITS = [256]
LOSS = "sparse_categorical_crossentropy"
LEARNING_RATE = 0.001
EPOCHS = 90
BATCH_SIZE = 128

SAVE_MODEL_PATH = "model4.h5"


def build_model(output_units, num_units, loss, learning_rate):
    """Builds and compiles model

    output_units (int):         Num output units
    num_units (list of int):    Num of units in hidden layers
    loss (str):                 Type of loss function to use
    learning_rate (float):      Learning rate to apply

    return model (tf model): Where the magic happens :D
    """

    input = keras.layers.Input(shape=(None, output_units))
    x = keras.layers.LSTM(num_units[0])(input)
    x = keras.layers.Dropout(0.2)(x)

    output = keras.layers.Dense(output_units, activation="softmax")(x)

    model = keras.Model(input, output)

    # compile model
    model.compile(loss=loss,
                  optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
                  metrics=["accuracy"])

    model.summary()

    return model


def train(output_units=OUTPUT_UNITS, num_units=NUM_UNITS, loss=LOSS, learning_rate=LEARNING_RATE):
    """Train and save TF model.

    output_units (int):         Num output units
    num_units (list of int):    Num of units in hidden layers
    loss (str):                 Type of loss function to use
    learning_rate (float):      Learning rate to apply
    """

    # generate the training sequences
    inputs, targets = generate_training_sequences(SEQUENCE_LENGTH)

    # build the network
    model = build_model(output_units, num_units, loss, learning_rate)

    # train the model
    model.fit(inputs, targets, epochs=EPOCHS, batch_size=BATCH_SIZE)

    # save the model
    model.save(SAVE_MODEL_PATH)


if __name__ == "__main__":
    train()