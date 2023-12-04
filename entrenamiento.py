import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from sklearn.model_selection import train_test_split

# Ejemplo de datos
textos = [
    "No veo salida alguna a esta situación, me siento completamente atrapado y sin esperanza. A menudo me encuentro pensando que si no estuviera aquí, el dolor finalmente terminaría.",
    "Hoy es un buen dia para morir tranquilo",
    "Me siento como una carga para todos, y no sé cuánto tiempo más puedo soportar este dolor. Parece que la única solución es dejar de existir.",
    "He empezado a poner en orden mis asuntos, no veo un futuro y no quiero seguir siendo una molestia. Estoy considerando seriamente decir adiós.",
    "Día tras día, el pensamiento de acabar con mi vida se hace más fuerte; parece ser la única forma de escapar de este sufrimiento interminable.",
    "Cada mañana me despierto decepcionado de seguir aquí. He estado planeando una forma de terminar con todo esto, ya no puedo soportar esta agonía.",
    #----------------------------------------------------------------------------------
    "A veces cuando siento algún vacío siento demasiada tristeza, hay ocasiones en donde pienso que entro en una pequeña depresión, no puedo concentrarme en mis trabajos y simplemente me siento con mucha tristeza hasta cierto punto de llorar por mucho tiempo",
    "Al sentir esto uno como persona se siente que su vida no tiene algun motivo de poder seguir ya que se presentan problema tras problema que uno en su cabeza solo piensa en esas cosas y cada vez con mas carga haciendo que uno se sienta vacio.",
    "Que mi vida es miserable y triste, que he sufrido mucho y aún así temo miedo a morir Que mi vida es miserable y triste, que he sufrido mucho y aún así temo miedo a morir ",
    "más que nada pienso en por que eh llegado a ese punto y por que nunca eh podido mejorar muchos aspectos de mi vida",
    "Me da miedo que no pueda lograr lo que realmente me gustaría en el futuro, pensar en que podría suceder me puede dar demasiada incertidumbre, y a veces me siento sola",
    "No sé para qué estoy aquí, aveces las acciones que hago siento que no tienen propósito siento que voy navegando pero sin rumbo fijo",
    #---------------------------------------------------------------------------------
    "¡Hoy fue un gran día! Disfruté mucho en la reunión con mis amigos.",
    "Hoy fue un día productivo, logré terminar mi proyecto y me siento satisfecho con el trabajo realizado.",
    "Pasé una tarde maravillosa leyendo un libro que realmente capturó mi interés y me inspiró.",
    "Me encanta pasar tiempo con mi familia, cada momento juntos es valioso y lleno de risas.",
    "El ejercicio de esta mañana fue energizante; me siento revitalizado y listo para enfrentar el día.",
    "Acabo de empezar a aprender un nuevo hobby y estoy realmente emocionado por todos los progresos que estoy haciendo.",
    # -------------------------------------------------------------------------------------


]

etiquetas_textuales = [
    "alerta maxima, esta persona tiene vacio existencial", "alerta maxima, esta persona tiene vacio existencial", "alerta maxima, esta persona tiene vacio existencial", "alerta maxima, esta persona tiene vacio existencial", "alerta maxima, esta persona tiene vacio existencial", "alerta maxima, esta persona tiene vacio existencial",
    "Puede tener vacio existencial", "Puede tener vacio existencial", "Puede tener vacio existencial", "Puede tener vacio existencial", "Puede tener vacio existencial", "Puede tener vacio existencial",
    "no tiene vacio existencial", "no tiene vacio existencial", "no tiene vacio existencial", "no tiene vacio existencial", "no tiene vacio existencial", "no tiene vacio existencial",
]

# Mapeo de etiquetas textuales a índices numéricos
etiquetas_a_indices = {
    "alerta maxima, esta persona tiene vacio existencial": 0,
    "Puede tener vacio existencial": 1,
    "no tiene vacio existencial": 2
}

# Convertir etiquetas textuales a índices numéricos
indices_etiquetas = [etiquetas_a_indices[etiqueta] for etiqueta in etiquetas_textuales]

# Clase para el Dataset
class MyDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            return_token_type_ids=False,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
            truncation=True
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

# Tokenizador y modelo BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)

# Crear el dataset
dataset = MyDataset(textos, indices_etiquetas, tokenizer, max_length=512)

# Dividir en entrenamiento y prueba
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

# DataLoaders
train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=2)

# Optimizador
optimizer = AdamW(model.parameters(), lr=2e-5)

# Ciclo de entrenamiento
epochs = 50  # Puedes ajustar esto según sea necesario
for epoch in range(epochs):
    model.train()
    for batch in train_loader:
        optimizer.zero_grad()
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        labels = batch['labels']
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch + 1} completed")

# Mapeo inverso para interpretación de resultados
indices_a_etiquetas = {indice: etiqueta for etiqueta, indice in etiquetas_a_indices.items()}

# Validación y evaluación del modelo
model.eval()
total = 0
correct = 0
with torch.no_grad():
    for batch in test_loader:
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        labels = batch['labels']
        outputs = model(input_ids, attention_mask=attention_mask)
        predictions = torch.argmax(outputs.logits, dim=1)
        total += labels.size(0)
        correct += (predictions == labels).sum().item()
        # Opcional: Imprimir las predicciones en formato textual
        predictions_text = [indices_a_etiquetas[prediction.item()] for prediction in predictions]
        print("Predicciones:", predictions_text)

print(f"Accuracy: {100 * correct / total}%")

# Guardar el modelo entrenado
model_save_path = 'C:/Users/Colibecas/Documents/app_tesis/primerDjango/modelo_entrenado.pth'
torch.save(model.state_dict(), model_save_path)
print(f"Modelo guardado en {model_save_path}")

