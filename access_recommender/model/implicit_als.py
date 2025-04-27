import json

from fuzzywuzzy import process
from implicit.als import AlternatingLeastSquares
from sklearn.model_selection import train_test_split
from scipy.sparse import load_npz


def main():
    X = load_npz('data/processed/user_item_matrix.npz')
    print(X.shape)

    # train_X, test_X = train_test_split(X, test_size=0.2, random_state=42)

    model_als = AlternatingLeastSquares(factors=20)
    model_als.fit(X.T)

    with open("data/processed/item_mapper.json", "r") as f:
        item_mapper = json.load(f)

    with open("data/processed/item_inv_mapper.json", "r") as f:
        item_inv_mapper = json.load(f)

    item_query = "Mental health support plan"

    item_index = item_mapper[item_query]
    related = model_als.similar_items(item_index, N=len(item_mapper))
    print(related)
    print(f"Because you searched for {item_query}...")
    for r_index, r_score in zip(*related):
        recommended_title = item_inv_mapper[str(r_index)]
        if recommended_title != item_query:
            print(f"{recommended_title}: score {r_score}")


if __name__ == "__main__":
    main()
