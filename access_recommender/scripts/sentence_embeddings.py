import nltk
import pandas as pd
from sentence_transformers import SentenceTransformer

# 1. Load a pretrained Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

df = pd.read_csv("data/raw/user_narratives.csv")
print(df.columns)
print(df['User Narrative'].head())

# # 1. Tokenize the sentences
# for text in sentences:
#     print(nltk.tokenize.sent_tokenize(text, language='english'))


# # 2. Calculate embeddings by calling model.encode()
# embeddings = model.encode(sentences)
# print(embeddings.shape)
# # [3, 384]

# # 3. Calculate the embedding similarities
# similarities = model.similarity(embeddings, embeddings)
# print(similarities)
