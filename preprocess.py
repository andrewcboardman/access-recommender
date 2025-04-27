import json
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, save_npz


def create_X(df):
    """
    Generates a sparse matrix from ratings dataframe.

    Args:
        df: pandas dataframe

    Returns:
        X: sparse matrix
        user_mapper: dict that maps user id's to user indices
        user_inv_mapper: dict that maps user indices to user id's
        item_mapper: dict that maps item id's to item indices
        item_inv_mapper: dict that maps item indices to item id's
    """
    N = df["user_id"].nunique()
    M = df["item"].nunique()

    user_mapper = dict(zip(np.unique(df["user_id"]), list(range(N))))
    item_mapper = dict(zip(np.unique(df["item"]), list(range(M))))

    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["user_id"])))
    item_inv_mapper = dict(zip(list(range(M)), np.unique(df["item"])))

    user_index = [user_mapper[i] for i in df["user_id"]]
    item_index = [item_mapper[i] for i in df["item"]]

    X = csr_matrix((df["rating"], (item_index, user_index)), shape=(M, N))

    return X, user_mapper, item_mapper, user_inv_mapper, item_inv_mapper


def main():
    # Load your data
    df = pd.read_csv("./data/raw/Access_to_Work_Cost_Weighted_2000.csv")
    df.columns = ["user_id", "condition_group", "job_sector", "item", "cost", "notes"]

    df['item'] = df['item'].str.split(",")
    df = df.explode("item")

    df["rating"] = np.random.randint(1, 5, size=len(df))  # Example ratings

    df.to_csv("./data/processed/Access_to_Work_Cost_Weighted_2000_processed.csv", index=False)  # Example processed data file

    # Create sparse matrix X
    X, user_mapper, item_mapper, user_inv_mapper, item_inv_mapper = create_X(df)

    # Save the mappings for later use
    with open("./data/processed/user_mapper.json", "w") as f:
        json.dump(user_mapper, f)
    with open("./data/processed/item_mapper.json", "w") as f:
        json.dump(item_mapper, f)
    with open("./data/processed/user_inv_mapper.json", "w") as f:
        json.dump(user_inv_mapper, f)
    with open("./data/processed/item_inv_mapper.json", "w") as f:
        json.dump(item_inv_mapper, f)

    # Save the sparse matrix X
    save_npz("./data/processed/user_item_matrix.npz", X)


if __name__ == "__main__":
    main()
