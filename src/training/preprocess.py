import pandas as pd


def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the input DataFrame by performing basic data cleaning.

    Args:
        df (pd.DataFrame): The input DataFrame to be preprocessed.

    Returns:
        pd.DataFrame: A new DataFrame containing the preprocessed data.
    """
    # Minimal example: drop NA rows
    return df.dropna().copy()