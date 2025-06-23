#!/bin/bash

echo "Building Docker image..."
docker build -t cleanvul-test .

echo "Extracting datasets..."
docker create --name temp-cleanvul cleanvul-test
docker cp temp-cleanvul:/cleanvul_test/datasets ./
docker rm temp-cleanvul

echo "Updating dataset_manager.py for local use..."
sed -i 's|DATASETS_DIR = "/cleanvul_test/datasets"|DATASETS_DIR = "./datasets"|g' dataset_manager.py

echo "Done! Datasets are now available locally."
echo "You can run: python run_cleanvul_scenario.py --validation_score 0"

ls -la datasets/