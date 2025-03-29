from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import uvicorn
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Inicjalizacja aplikacji FastAPI
app = FastAPI()

# Wczytanie modelu
model = tf.keras.models.load_model("model.keras")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to allowed origins for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)
# Załadowanie tokenizera z pliku JSON
with open("tokenizer.json", "r") as f:
    tokenizer_json = json.load(f)

tokenizer = tokenizer_from_json(tokenizer_json)

MAX_SEQUENCE_LENGTH = 100

# Funkcja przetwarzająca tekst
def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))  # Usunięcie znaków
    words = word_tokenize(text)  # Tokenizacja
    words = [word for word in words if word not in stopwords.words('english')]  # Usunięcie stop-words
    return " ".join(words)


# Definicja modelu wejściowego (do walidacji danych wejściowych)
class TextData(BaseModel):
    text: str


# Ścieżka do przewidywania
@app.post('/predict')
async def predict(data: TextData):
    processed_text = preprocess_text(data.text)
    sequence = tokenizer.texts_to_sequences([processed_text])
    padded = pad_sequences(sequence, maxlen=MAX_SEQUENCE_LENGTH)
    prediction = model.predict(padded)[0][0]

    return {
        "prediction": "REAL" if int(prediction > 0.05) else "FAKE",
        "probability": float(prediction)  # Zwracamy prawdopodobieństwo jako wartość zmiennoprzecinkową
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)