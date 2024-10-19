from invariant_physics.dataset import get_dataset

import sys

if __name__ == "__main__":
    command = " ".join(sys.argv)
    print(f"Command: {command}")

    dataset = get_dataset()
    dataset.build()
    if dataset.args.extract_csv:
        dataset.extract_csv()
