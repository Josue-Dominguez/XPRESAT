import torch
from torch import nn
from django.conf import settings
from social.models import SocialPost
from django.db.models import Q
from .nlp_model import prepare_data
from .sentiment_analysis import analizar_sentimiento

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(768, 5)

    def forward(self, x):
        x = self.linear(x)
        return x

def get_dataset(user):
    posts = SocialPost.objects.filter(
        Q(author__profile__followers__in=[user.id]) |
        Q(author=user)
    ).order_by('-created_on')

    data = prepare_data(posts)

    labels = []
    for post in posts:
        # Suponiendo que tienes una forma de obtener una etiqueta para cada post
        label = get_label_for_post(post)
        labels.append(label)

    return data, torch.tensor(labels)

def train_and_save_model(user, model_path, learning_rate, epochs):
    data, labels = get_dataset(user)
    model = MyModel()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(epochs):
        output = model(data)
        loss = torch.nn.functional.cross_entropy(output, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    torch.save(model.state_dict(), model_path)


def get_label_for_post(post):
    sentimiento = analizar_sentimiento(post.body)
    if sentimiento == 'positivo':
        return 1
    elif sentimiento == 'negativo':
        return 0
    else:
        return 2  # para neutral o indefinido

# Ahora, puedes llamar a `train_and_save_model` desde una vista en Django.
