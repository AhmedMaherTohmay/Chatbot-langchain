from typing import Optional
def search_transactions(type_of_transaction: Optional[str] = None) -> str:
    """
    Searches for and retrieves a transaction link based on the specified type.

    Parameters:
        type_of_transaction (Optional[str]): The type of transaction to search for.
                                                Accepted values are keys in the 'transaction_pages' dictionary.
                                                Defaults to None.

    Returns:
        str: A URL link enclosed in double quotes corresponding to the provided transaction type.
                Returns '"Transaction type not found."' if the type is not in the dictionary.
    """
    transaction_pages = {'video': "https://www.youtube.com/watch?v=b3XsvoFWp4c&t=2679s"}
    return f"here is the required page link:  {transaction_pages.get(type_of_transaction)}"

# print(search_transactions('video'))