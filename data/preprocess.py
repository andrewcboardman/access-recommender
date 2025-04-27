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
        movie_mapper: dict that maps movie id's to movie indices
        movie_inv_mapper: dict that maps movie indices to movie id's
    """
    N = df['Name'].nunique()
    M = df['Support Provided'].nunique()

    user_mapper = dict(zip(np.unique(df["Name"]), list(range(N))))
    movie_mapper = dict(zip(np.unique(df["Support Provided"]), list(range(M))))

    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["Name"])))
    movie_inv_mapper = dict(zip(list(range(M)), np.unique(df["Support Provided"])))

    user_index = [user_mapper[i] for i in df['Name']]
    movie_index = [movie_mapper[i] for i in df['Support Provided']]

    X = csr_matrix((df["rating"], (movie_index, user_index)), shape=(M, N))

    return X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper


def main():
    # Load your data
    df = pd.read_csv("Access_to_Work_Cost_Weighted_2000.csv")
    df["rating"] = np.random.randint(1, 5, size=len(df))  # Example ratings

    # Create sparse matrix X
    X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper = create_X(df)

    # Save the mappings for later use
    with open("data/user_mapper.json", "w") as f:
        json.dump(user_mapper, f)
    with open("data/movie_mapper.json", "w") as f:
        json.dump(movie_mapper, f)
    with open("data/user_inv_mapper.json", "w") as f:
        json.dump(user_inv_mapper, f)
    with open("data/movie_inv_mapper.json", "w") as f:
        json.dump(movie_inv_mapper, f)

    # Save the sparse matrix X
    save_npz('data/user_item_matrix.npz', X)


if __name__ == "__main__":
    main()
