import argparse
import subprocess
import os
import sys
from pathlib import Path
from dataset_manager import load_cleanvul_dataset

def run_setup_script():
    launch_script = Path('./build_scripts/launch.sh')
    if not launch_script.exists():
        print(f" Setup script not found at {launch_script}")
        print("Please ensure launch.sh exists in the build_scripts directory")
        return False
    
    try:
        print("🚀 Running setup script to build Docker image and extract datasets...")
        print("This may take a few minutes...")
        
        # Make sure the script is executable
        os.chmod(launch_script, 0o755)
        
        # Run the launch script
        result = subprocess.run(['bash', str(launch_script)], 
                              capture_output=True, 
                              text=True, 
                              cwd='.')
        
        if result.returncode == 0:
            print("Setup completed successfully!")
            print("Setup output:", result.stdout)
            return True
        else:
            print("Setup failed!")
            print("Error output:", result.stderr)
            return False
            
    except Exception as e:
        print(f"Error running setup script: {e}")
        return False

def run_cleanvul_scenario(validation_score):
    """Run CleanVul scenario with the specified validation score"""
    dataset_name = f"vulnscore_{int(validation_score)}"

    print("DATASET name:", dataset_name)

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

    run_setup_script()
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