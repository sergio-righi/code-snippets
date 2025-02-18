import os
import re
import pdfplumber
import pandas as pd

def parse_month_day(date_str):
    # Define a mapping of month abbreviations to numbers
    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }
    
    # Extract the three-letter month and day using regex
    match = re.match(r"([A-Za-z]{3})(\d{1,2})", date_str)
    if not match:
        raise ValueError(f"Invalid date format: {date_str}")

    month_abbr, day = match.groups()
    
    # Convert extracted values
    month_num = month_map.get(month_abbr, None)
    if month_num is None:
        raise ValueError(f"Invalid month abbreviation: {month_abbr}")

    return month_num, int(day)

if __name__ == '__main__':

    # Define folder path
    FOLDER_PATH = "C:\\Users\\sergi\\Documents\\statements\\"

    # Regular expressions to extract relevant information
    account_summary_pattern = re.compile(r"#(\d{8}-\d{3})\s+([0-9,]+\.\d{2})\s+([0-9,]+\.\d{2})\s+([0-9,]+\.\d{2})\s+([0-9,]+\.\d{2})")
    transaction_pattern = re.compile(r"([A-Za-z]{3}\d{1,2})\s+(.+?)\s+([0-9,]+\.\d{2})(?:\s+([0-9,]+\.\d{2}))?")

    # Lists to store extracted data
    account_summaries = []
    transactions = []
    current_balance = 0

    # Process each PDF in the folder
    for filename in os.listdir(FOLDER_PATH):
        if filename.endswith("pdf"):
            file_path = os.path.join(FOLDER_PATH, filename)

            # Extract date from filename
            date_match = re.search(r"([A-Za-z]+) (\d{1,2}), (\d{4})", filename)
            if not date_match:
                print(f"Skipping {filename}: Date not found in filename")
                continue
            month, day, year = date_match.groups()
            
            # Read PDF
            with pdfplumber.open(file_path) as pdf:
                text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
                
            lines = text.split("\n")
            for line in lines:  
                            
                account_match = account_summary_pattern.match(line)
                # Extract account summary
                if account_match:
                    account_number, opening_balance, total_deducted, total_added, closing_balance = account_match.groups()
                    account_summaries.append({
                        "Month": month,
                        "Year": year,
                        "Account Number": account_number,
                        "Opening Balance": float(opening_balance.replace(",", "")),
                        "Total Deducted": float(total_deducted.replace(",", "")),
                        "Total Added": float(total_added.replace(",", "")),
                        "Closing Balance": float(closing_balance.replace(",", "")),
                    })
                    current_balance = float(opening_balance.replace(",", ""))
                
                # Extract transactions
                transaction_match = transaction_pattern.match(line)
                if transaction_match:
                    date, description, amount, balance = transaction_match.groups()
                    if (description == "Openingbalance" or description == "Closingtotals"):
                        continue;
                    amount = float(amount.replace(",", ""))
                    balance = float(balance.replace(",", "")) if balance else amount
                    
                    # Determine if transaction is added or deducted
                    if current_balance > balance:
                        amount = -amount
                        transaction_type = "Deducted"
                    elif current_balance < balance:
                        transaction_type = "Added"
                    else:
                        transaction_type = "Unknown"
                        
                    current_balance = balance
                    
                    transaction_month, transaction_day = parse_month_day(date)
                    
                    transaction = {
                        "Year": float(year) - 1 if month == "January" and transaction_month == 12 else float(year),
                        "Month": transaction_month,
                        "Day": transaction_day,
                        "Description": description,
                        "Amount": amount,
                        "Transaction Type": transaction_type,
                        "Balance After Transaction": balance
                    }
                    
                    transactions.append(transaction)
                    
                    


    # Convert lists to DataFrames
    df_summary = pd.DataFrame(account_summaries)
    df_transactions = pd.DataFrame(transactions)

    # Sort transactions by Year, Month, Day (ascending)
    df_transactions.sort_values(by=["Year", "Month", "Day"], ascending=True, inplace=True)


    # Save to CSV
    summary_csv_path = os.path.join(FOLDER_PATH, "account_summaries.csv")
    transactions_csv_path = os.path.join(FOLDER_PATH, "transactions.csv")

    df_summary.to_csv(summary_csv_path, index=False)
    df_transactions.to_csv(transactions_csv_path, index=False)

    print("\nTransactions:")
    print(df_transactions)

    print(f"\nCSV files saved at:\n{summary_csv_path}\n{transactions_csv_path}")
