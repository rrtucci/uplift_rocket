import pandas as pd
import numpy as np


def create_binned_column(df,
                         col_name,
                         n,
                         xmin,
                         xmax):
    """
    Adds a new column 'binned_{col_name}' to the dataframe df by binning the
    '{col_name}' column into n equal-width bins between xmin and xmax.

    Parameters
    ----------
    df: pandas.DataFrame
    col_name: str
        column name
    n: int
        number of bins
    xmin: float
        minimum value for binning
    xmax: float
        maximum value for binning

    Returns
    -------
        pandas.DataFrame
            with a new column 'binned_x'
    """
    if col_name not in df.columns:
        raise ValueError(f"DataFrame must contain a column named {col_name}.")

    if xmax <= xmin:
        raise ValueError("xmax must be greater than xmin.")

    # Compute bin edges
    bins = np.linspace(xmin, xmax, n + 1)

    # Use np.digitize to assign bins (subtract 1 to get 0-based bin indices)
    binned = np.digitize(df[col_name], bins, right=False) - 1

    # Clip values to ensure that anything at xmax is included in the last bin
    binned = np.clip(binned, 0, n - 1)

    # Add new column to a copy of the DataFrame
    df_binned = df.copy()
    df_binned[f'binned_{col_name}'] = binned

    return df_binned


def get_value_positions(df: pd.DataFrame, col_name: str) -> dict:
    """
    Returns a dictionary mapping each distinct entry in the specified column
    to a list of positions (row indices) where that entry occurs.

    Parameters
    ----------
    df: pd.DataFrame
        The input DataFrame.
    col_name: str
        The name of the column to analyze.

    Returns
    -------
        dict
            A dictionary with unique column values as keys and lists of row
            indices as values.
    """
    if col_name not in df.columns:
        raise ValueError(
            f"Column '{col_name}' does not exist in the DataFrame.")

    value_positions = {}
    for idx, value in df[col_name].items():
        value_positions.setdefault(value, []).append(idx)

    return value_positions


def apply_function_to_column(df, col_name, fun):
    """
    Applies a function to a specified column in a DataFrame and returns a
    new DataFrame with the results in a new column.

    Parameters
    ----------
    df: pd.DataFrame
        The input DataFrame.
    col_name: str
        The name of the column to which the function should be applied.
    fun: function
        The function to apply to each element in the column.

    Returns
    -------
        pd.DataFrame
            A new DataFrame with an added column 'fun_<col_name>'.
    """
    new_df = df.copy()
    new_col_name = f"fun_{col_name}"
    new_df[new_col_name] = new_df[col_name].apply(fun)
    return new_df


if __name__ == "__main__":
    def main1():
        df = pd.DataFrame({'x': [0.5, 1.5, 2.5, 3.5]})
        result = create_binned_column(df, col_name='x', n=4, xmin=0, xmax=4)
        print(result)


    def main2():
        data = {'color': ['red', 'blue', 'red', 'green', 'blue', 'blue']}
        df = pd.DataFrame(data)
        print(get_value_positions(df, 'color'))
        # Output: {'red': [0, 2], 'blue': [1, 4, 5], 'green': [3]}


    def main3():
        # Sample DataFrame
        df = pd.DataFrame({'numbers': [1, 2, 3, 4]})

        # Function to apply
        def square(x):
            return x ** 2

        # Apply the function
        result_df = apply_function_to_column(df, 'numbers', square)

        print(result_df)


    main1()
    main2()
    main3()
