from datasets import load_dataset
from torch.utils.data import DataLoader, Dataset


class CodeContestsDataset(Dataset):
    """This class loads the code contests dataset.

    On instantiation, this class automatically loads the code contests dataset
    found at https://huggingface.co/datasets/deepmind/code_contests.

    An item in this dataset is defined as a tuple (desciption, tests), where
    description is a string and tests is a dictionary that contains public,
    private, and generated tests.
    ```python
    self.tests = {
        "public_tests": data["public_tests"],
        "private_tests": data["private_tests"],
        "generated_tests": data["generated_tests"]
    }
    ```

    Args:
        select_columns (list): A list of columns to select from the dataset in
            addition to the default columns, which includes "name",
            "description", "public_tests", "private_tests", "generated_tests",
            "source", "difficulty", "solutions".
        codeforce (bool): If True, filters for only problems collected from
            code force (https://codeforces.com/).
    """
    def __init__(self, select_columns=None, codeforce=True):
        self.data = load_dataset("deepmind/code_contests", split="test")

        default_columns = [
            "name", "description", "public_tests", "private_tests",
            "generated_tests", "source", "difficulty", "solutions"
        ]
        if not select_columns:
            select_columns = []
        select_columns += default_columns

        self.data = self.data.remove_columns(
            [c for c in self.data.column_names if c not in select_columns])

        # Filter for CODEFORCES problems (CODEFORCES = 2).
        if codeforce:
            self.data = self.data.filter(lambda x: x["source"] == 2)


        self.len = len(self.data)

        self.data = self.data[:3]
        self.len = 3

        self.name = self.data["name"]
        self.descriptions = self.data["description"]
        self.tests = {
            "public_tests": self.data["public_tests"],
            "private_tests": self.data["private_tests"],
            "generated_tests": self.data["generated_tests"]
        }

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        tests = {
            "public_tests": self.data["public_tests"][idx],
            "private_tests": self.data["private_tests"][idx],
            "generated_tests": self.data["generated_tests"][idx]
        }
        return self.data["name"][idx], self.data["description"][idx], tests


if __name__ == "__main__":
    dataset = CodeContestsDataset()
    # dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

    # for name, desc, tests in dataloader:
    for name, desc, tests in dataset:
        print(name, tests["private_tests"])
        # break
