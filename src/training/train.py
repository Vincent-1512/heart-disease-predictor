import argparse
from src.training.preprocess import preprocess_df
from src.utils.io import save_model

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", default="data/raw/framingham.csv")
    parser.add_argument("--output-dir", default="model")
    args = parser.parse_args()

    # Placeholder for reading and processing the data
    # df = pd.read_csv(args.data_path)
    # processed_df = preprocess_df(df)

    # Placeholder for model training
    # model = train_model(processed_df)
    
    # Placeholder for saving the model
    # save_model(model, args.output_dir)

    print("Train script placeholder. Implement training pipeline here.")

if __name__ == "__main__":
    main()