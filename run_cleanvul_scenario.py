import pandas as pd
import argparse
from dataset_manager import load_cleanvul_dataset

def run_cleanvul_scenario(validation_score):
    """Run CleanVul scenario with the specified validation score"""
    dataset_name = f"vulnscore_{int(validation_score)}"

    # Load the corresponding dataset
    dataset = load_cleanvul_dataset(dataset_name)
    
    if dataset is None:
        print(f"Failed to load dataset for validation score {validation_score}")
        return None
    
    return dataset


def main():
    parser = argparse.ArgumentParser(description="Run file with a validation score.")

    parser.add_argument(
        "--validation_score",
        type=int, 
        required=False,  # Make True if you want to force the user to provide it
        choices=[0, 1, 2, 3, 4],
        help="Provide a numeric validation score (e.g., 0.85)."
    )

    args = parser.parse_args()

    if args.validation_score is not None:
        if args.validation_score in range(0, 4):
            dataset = run_cleanvul_scenario(args.validation_score)

            if dataset is not None:
                print(f"\n Successfully loaded and processed CleanVul dataset {args.validation_score}")
                print(f"Dataset contains {len(dataset)} rows and {len(dataset.columns)} columns")
            else:
                print(f"\n Failed to process CleanVul dataset {args.validation_score}")

            print(f"Validation score provided: {args.validation_score}")
            # Your logic using the score

            #Retrieve.

            #Fill in scoring template.


    else:
        print("No validation score provided.")


if __name__ == "__main__":
    main()