import pandas as pd
df = pd.read_csv("book_sales.csv")
print(df)
print(df['Quantity_Sold'])

# print(df.head())
print(df.info())

#Replacement of missing values
print("Missing values replacement ")
# Step 2: Check missing values before replacing
print("Missing values before:\n", df.isnull().sum())

# Step 3: Replace missing values with 'unknown'
df = df.fillna("unknown")

# Step 4: Check missing values after replacing
print("\nMissing values after:\n", df.isnull().sum())

# Optional: see the updated DataFrame
print("\nUpdated DataFrame:\n", df.head())

#Date converted
df['Sale_Date'] = pd.to_datetime(df['Sale_Date'], errors='coerce')

# Check the first few rows
print(df.head())

#Drop duplicates
print("Duplicate dropping")
df = df.drop_duplicates()

# Optional: reset the index after removing duplicates
df = df.reset_index(drop=True)

# Check the DataFrame
print(df.head())
print("\nNumber of rows after removing duplicates:", len(df))

# Calculate total quantity sold

# Calculate total quantity sold
total_quantity = df['Quantity_Sold'].sum()

print("Total quantity of books sold:", total_quantity)
# Ensure Quantity_Sold and Price are numeric
df['Quantity_Sold'] = pd.to_numeric(df['Quantity_Sold'], errors='coerce').fillna(0)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)

# Calculate weighted average price
weighted_avg_price = (df['Quantity_Sold'] * df['Price']).sum() / df['Quantity_Sold'].sum()

print("Weighted average price of all books:", weighted_avg_price)

# Group by Genre and sum the Quantity_Sold
genre_totals = df.groupby('Genre')['Quantity_Sold'].sum()

# Display the result
print(genre_totals)

# Sort by Quantity_Sold descending and take top 3
top_books = df.sort_values(by='Quantity_Sold', ascending=False).head(3)

# Display the top 3 books
print(top_books[['Book_Title', 'Author', 'Quantity_Sold']])

# Find the row with the highest Customer_Rating
highest_rated_row = df.loc[df['Customer_Rating'].idxmax()]

# Display the Book_Title and rating
print("Highest rated book:", highest_rated_row['Book_Title'])
print("Customer Rating:", highest_rated_row['Customer_Rating'])