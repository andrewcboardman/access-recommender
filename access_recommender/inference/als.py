import json

from implicit.als import AlternatingLeastSquares


class ALSInferenceRunner():
    def __init__(self):
        
        model = AlternatingLeastSquares()
        self.model = model.load('models/als.model.npz')

        with open("data/processed/item_mapper.json", "r") as f:
            self.item_mapper = json.load(f)

        with open("data/processed/item_inv_mapper.json", "r") as f:
            self.item_inv_mapper = json.load(f)

    def get_similar_items(self, item_query):
        item_index = self.item_mapper[item_query]
        related = self.model.similar_items(item_index, N=len(self.item_mapper))
        print(related)
        if related is not None:
            output = f"Because you searched for {item_query}..."
            for r_index, r_score in zip(*related):
                recommended_title = self.item_inv_mapper[str(r_index)]
                if recommended_title != item_query:
                    output += f"\n{recommended_title}: score {r_score}"
            return output
        else:
            return "No similar items found."


if __name__ == "__main__":
    inference_runner = ALSInferenceRunner()

    item_query = "Mental health support plan"

    print(inference_runner.get_similar_items(item_query))
