import nltk
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from torch import embedding

# 1. Load a pretrained Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

df = pd.read_csv("data/raw/user_narratives.csv")
print(df.columns)
print(df['User Narrative'].head())

df = df.head(100)

# # 1. Tokenize the sentences
df['narrative_sentences'] = df['User Narrative'].apply(
    nltk.tokenize.sent_tokenize, language='english'
)
df_sentences = df[["Name", "narrative_sentences"]]

df_sentences = df_sentences.explode('narrative_sentences')


# # 2. Calculate embeddings by calling model.encode()
batch_size = 64

for i in range(0, len(df_sentences), batch_size):
    batch_sentences = df_sentences.iloc[i:i+batch_size].copy()
    batch_embeddings = model.encode(batch_sentences['narrative_sentences'].tolist())
    batch_sentences['embeddings'] = batch_embeddings.tolist()

    if i == 0:
        embeddings_df = batch_sentences
    else:
        embeddings_df = pd.concat([embeddings_df, batch_sentences])


# # 3. Calculate the embedding similarities

embeddings = np.stack(embeddings_df['embeddings'].tolist()[:10])

similarities = model.similarity(embeddings, embeddings)
print(similarities)
