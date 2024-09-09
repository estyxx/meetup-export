import json
import re
from pathlib import Path

import pandas as pd
import requests

from meetup.env import Env
from meetup.jwt_ import generate_jwt
from meetup.meetup import graphql_query


# Helper function to remove extra spaces between words
def clean_whitespace(name):
    if isinstance(name, str):
        # Remove extra spaces between words and strip leading/trailing spaces
        return re.sub(r"\s+", " ", name).strip()
    return name


# Function to request an access token using the JWT
def request_access_token(jwt_token, client_key, client_secret):
    url = "https://secure.meetup.com/oauth2/access"

    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt_token,  # The JWT token we generated
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # Send POST request to get the access token
    response = requests.post(
        url, data=data, headers=headers, auth=(client_key, client_secret)
    )

    if response.status_code == 200:
        # Return the access token
        data = response.json()
        print(data)
        return data["access_token"]
    else:
        raise Exception(
            f"Failed to get access token: {response.status_code} - {response.text}"
        )


# Main function to execute the flow
def main():
    env = Env.get_env()

    print(env)

    # Your Meetup OAuth details
    client_key = env.MEETUP_COM_CLIENT_KEY  # Your OAuth client key
    client_secret = env.MEETUP_COM_SECRET  # Your OAuth client secret

    # Generate the JWT
    jwt_token = generate_jwt(env)

    # Request the access token
    access_token = request_access_token(jwt_token, client_key, client_secret)
    # Define your GraphQL query and variables
    query = Path("meetup/query.graphql").read_text()

    # Perform the GraphQL query with the access token
    result = graphql_query(
        query,
        access_token=access_token,
        variables={"eventId": "302810842", "proNetworkId": "610554310475497472"},
    )

    Path("output.json").write_text(json.dumps(result))
    csv_df = pd.read_csv("./Django London Meetup Sept - details.csv")

    tickets_data = []
    for edge in result["data"]["event"]["tickets"]["edges"]:
        user_data = edge["node"]["user"]
        tickets_data.append(
            {
                "name": clean_whitespace(user_data["name"]),
                "username": user_data["username"],
                "status": edge["node"]["status"],
                "answer": (
                    edge["node"]["answer"]["text"] if edge["node"]["answer"] else None
                ),
            }
        )
    tickets_df = pd.DataFrame(tickets_data)

    # Clean and normalize the 'full_name' column in the CSV data for merging
    csv_df["full_name"] = (
        (csv_df["First name"].str.strip() + " " + csv_df["Last name"].str.strip())
        .apply(clean_whitespace)
        .str.lower()
    )
    csv_df["First name"] = (
        csv_df["First name"].str.strip().apply(clean_whitespace).str.lower()
    )

    # Clean the 'name' column in the tickets_df
    tickets_df["name"] = tickets_df["name"].apply(clean_whitespace).str.lower()

    # Step 1: Merge csv_df (left) with tickets_df (right) on full names
    # This ensures we only keep rows from the CSV that match people who said "YES"
    merged_df = pd.merge(
        tickets_df,  # GraphQL (tickets_df) as the left source of truth
        csv_df,  # CSV data
        left_on="name",  # Match based on GraphQL names
        right_on="full_name",  # Match based on CSV names
        how="left",  # Left join ensures we only get people from tickets_df (who said "YES")
    )

    merged_df.to_csv("merged_attendees.csv", index=False)


if __name__ == "__main__":
    main()
