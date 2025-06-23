import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run file with a validation score.")

    parser.add_argument(
        "--validation_score",
        type=float,
        required=False,  # Make True if you want to force the user to provide it
        help="Provide a numeric validation score (e.g., 0.85)."
    )

    args = parser.parse_args()

    if args.validation_score is not None:
        if args.validation_score in range(0, 4):
            print(f"Validation score provided: {args.validation_score}")
            # Your logic using the score

            #Retrieve.

            #Fill in scoring template.


    else:
        print("No validation score provided.")


if __name__ == "__main__":
    main()