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
        'Education': "https://studentactivities.zu.edu.eg/Students/Registration/ed_login.aspx",
        'Electricity': "Services/elctricity/Billing"  # Note: Fixed typo from "elctricity" to "electricity"
    }
    return f'"{transaction_pages.get(type_of_transaction, "Transaction type not found.")}"'

# print(search_transactions('Electricity'))