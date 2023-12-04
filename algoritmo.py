import torch
from transformers import BertTokenizer, BertForSequenceClassification

class ModeloAnalisis:
    def __init__(self, model_path):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        self.model.eval()

        # Define el mapeo de índices a etiquetas textuales aquí
        self.indices_a_etiquetas = {
            0: "alerta maxima, esta persona tiene vacio existencial",
            1: "puede tener vacio existencial",
            2: "no tiene vacio existencial"
        }

    def analizar_texto(self, texto):
        # Tokenización y preparación del texto
        inputs = self.tokenizer.encode_plus(
            texto,
            add_special_tokens=True,
            max_length=512,
            return_token_type_ids=False,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
            truncation=True
    )
        # Hacer la predicción
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Obtener la clase con la probabilidad más alta
        prediction = torch.argmax(outputs.logits, dim=1).item()

        # Convertir el índice numérico en una etiqueta textual
        return self.indices_a_etiquetas[prediction]

modelo = ModeloAnalisis('C:/Users/Colibecas/Documents/app_tesis/primerDjango/modelo_entrenado.pth')
