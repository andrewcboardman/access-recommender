import json

import numpy as np
from scipy.sparse import load_npz
from sklearn.neighbors import NearestNeighbors


def find_similar_items(
    item_id, X, k, item_mapper, item_inv_mapper,
    metric="cosine", show_distance=False
):
    """
    Finds k-nearest neighbours for a given item id.

    Args:
        item_id: id of the item of interest
        X: user-item utility matrix
        k: number of similar items to retrieve
        metric: distance metric for kNN calculations

    Returns:
        list of k similar item ID's
    """
    neighbour_ids = []

    item_ind = item_mapper[item_id]
    item_vec = X[item_ind]
    kNN = NearestNeighbors(n_neighbors=k, metric=metric)
    kNN.fit(X)
    if isinstance(item_vec, (np.ndarray)):
        item_vec = item_vec.reshape(1, -1)
    neighbour = kNN.kneighbors(item_vec, return_distance=show_distance)
    for i in range(0, k):
        n = str(int(neighbour[0][i]))
        neighbour_ids.append(item_inv_mapper[n])
    neighbour_ids.pop(0)
    return neighbour_ids


def find_similar_users(
    user_id, X, k, user_mapper, user_inv_mapper,
    metric="cosine", show_distance=False
):
    """
    Finds k-nearest neighbours for a given item id.

    Args:
        item_id: id of the item of interest
        X: user-item utility matrix
        k: number of similar items to retrieve
        metric: distance metric for kNN calculations

    Returns:
        list of k similar item ID's
    """
    neighbour_ids = []

    user_ind = user_mapper[user_id]
    user_vec = X.T[user_ind]
    kNN = NearestNeighbors(n_neighbors=k, metric=metric)
    kNN.fit(X.T)
    if isinstance(user_vec, (np.ndarray)):
        user_vec = user_vec.reshape(1, -1)
    neighbour = kNN.kneighbors(user_vec, return_distance=show_distance)
    for i in range(0, k):
        n = str(int(neighbour[0][i]))
        neighbour_ids.append(user_inv_mapper[n])
    neighbour_ids.pop(0)
    return neighbour_ids


if __name__ == "__main__":
    # Load your data
    with open("data/processed/user_item_matrix.npz", "rb") as f:
        X = load_npz(f)

    with open("data/processed/item_mapper.json", "r") as f:
        item_mapper = json.load(f)

    with open("data/processed/item_inv_mapper.json", "r") as f:
        item_inv_mapper = json.load(f)

    with open("data/processed/user_mapper.json", "r") as f:
        user_mapper = json.load(f)

    with open("data/processed/user_inv_mapper.json", "r") as f:
        user_inv_mapper = json.load(f)

    item_name = "Mental health support plan"

    similar_item_ids = find_similar_items(
        item_name, X, 10, item_mapper, item_inv_mapper
    )  # Replace "item 1" with your item id

    print(f"Similar items for item '{item_name}' (id: 'item 1') are:")
    for i, item in enumerate(similar_item_ids):
        print(f"{i+1}. {item} (id: '{item_mapper[item]}')")

    user = list(user_mapper.keys())[0]  # Replace "user 1" with your user id

    similar_user_ids = find_similar_users(
        user, X, 5, user_mapper, user_inv_mapper
    )  # Replace "user 1" with your user id

    print(f"\nSimilar users for user {user} (id: 'user 1') are:")
    for i, user in enumerate(similar_user_ids):
        print(f"{i+1}. {user} (id: '{user_mapper[user]}')")
        print(item_inv_mapper[str(int(np.where(X.T[int(user_mapper[user])][0].toarray())[1]))])
