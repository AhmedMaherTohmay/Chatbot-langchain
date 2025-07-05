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
    if not type_of_transaction:
        return '"Transaction type not found."'
    
    type_of_transaction = type_of_transaction.capitalize()
    transaction_pages = {
        'Electricity': "Services/elctricity/Billing",
        'Water': "Services/water/Billing",
        'Gas': "Services/gas/Billing",
        'Internet': "Services/internet/Billing",
        'Phone': "Services/phone/Billing",
        'Reference_Number': "Services/Reference_Number/Billing",
    }
    return f'"{transaction_pages.get(type_of_transaction, "Transaction type not found.")}"'

# print(search_transactions('Electricity'))