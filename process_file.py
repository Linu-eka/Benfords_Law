def ProcessFile(file):
    word_white_list = set()
    word_white_list.add("amount")
    word_white_list.add("amounts")
    word_white_list.add("amt")
    word_white_list.add("transaction")
    word_white_list.add("transactions")
    word_white_list.add("total")
    word_white_list.add("cost")

    amount_col = -1 # Initialize amount_col to -1 to indicate not found
    amounts = [] # Initialize amounts to an empty list
    # Read the csv file
    with open(file, 'r') as f:
        lines = f.readlines()
        header = lines[0].strip().split(',')

        # Check if the header contains any of the words in the white list
        for i in range(0,len(header)):
            if header[i].lower() in word_white_list:
                amount_col = i
                break 


        if amount_col == -1:
            print("No amount column found in the file.")
            return None
        else:
            # Extract every amount in the amount column
            amounts = [float(line.strip().split(',')[amount_col]) for line in lines[1:] if line.strip().split(',')[amount_col].replace('.', '', 1).isdigit()]
            return amounts



