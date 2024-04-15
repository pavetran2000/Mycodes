import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the necessary scopes
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Build the service
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()

        # Fetch data from Google Sheets
        spreadsheet_id = "13NTpqtQg3JKHJRR242uec7ZeFX9JffvGNXYf8LAbzbA"
        range_name = "Sheet1!A:D"  # Adjust range as needed
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])

        # Display available quantities for each food item
        print("Available Food Items:")
        for row in values[1:]:
            food_item, quantity, availability, price = row
            print(f"{food_item}:{quantity}")

        # Prompt the user to input desired quantities for each food item
        order = {}
        for row in values[1:]:
            food_item, quantity,_ ,_ = row
            quantity_required = int(input(f"How many {food_item}s do you want? (Available:{quantity})"))
            if quantity_required > int(quantity):
                print(f"Sorry, only {quantity} {food_item}s are available.")
                quantity_required = int(quantity)
            order[food_item] = quantity_required

        # Update quantities in the spreadsheet based on the user's order
        for food_item, quantity_ordered in order.items():
            for row in values[1:]:
                if row[0] == food_item:
                    current_quantity = int(row[1])
                    new_quantity = max(0, current_quantity - quantity_ordered)
                    sheet.values().update(spreadsheetId=spreadsheet_id,range=f"Sheet1!B{values.index(row) + 1}",valueInputOption="USER_ENTERED",body={"values": [[new_quantity]]}).execute()

        # Calculate total cost
        total_cost = sum([float(row[3]) * order.get(row[0], 0) for row in values[1:]])

        # Print the total cost
        print(f"Total Cost: ₹{total_cost}")

    except HttpError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

