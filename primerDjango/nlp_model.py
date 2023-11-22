import torch
from transformers import BertTokenizer, BertModel, BertForSequenceClassification
from social.models import SocialPost  # Asegúrate de que esta importación coincida con la ubicación de tu modelo SocialPost

# Inicializa el tokenizador y el modelo BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')

def prepare_data(posts):
    """
    Prepara los datos para el entrenamiento o la inferencia.

    Args:
    - posts: Una lista de instancias de SocialPost.

    Returns:
    - Tensor de PyTorch que contiene los embeddings de los posts.
    """
    data = []
    for post in posts:
        # Asegúrate de que 'post.body' sea el atributo correcto que contiene el texto del post
        inputs = tokenizer(post.body, padding='max_length', truncation=True, max_length=128, return_tensors="pt")
        with torch.no_grad():
            outputs = bert_model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        data.append(embeddings)
    return torch.cat(data, dim=0)

# Inicializa el modelo BERT
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

# Obtiene los datos de entrenamiento
data = prepare_data(posts)

# Divide los datos de entrenamiento en un conjunto de entrenamiento y un conjunto de prueba
split = int(0.8 * len(data))
train_data = data[:split]
test_data = data[split:]

# Entrena el modelo
model.train(train_data)

# Evalúa el modelo
model.eval(test_data)