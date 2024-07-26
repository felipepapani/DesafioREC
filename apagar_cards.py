import requests

# Define the URL of the Pipefy API
url = "https://api.pipefy.com/graphql"

# Headers with the API token
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJQaXBlZnkiLCJpYXQiOjE3MjE4ODc1NTMsImp0aSI6IjY3MWQ2YjE0LThlNGEtNGM1OC1hODJjLWNlM2I2ZGViMjk5ZSIsInN1YiI6MzA1MDE0NTQwLCJ1c2VyIjp7ImlkIjozMDUwMTQ1NDAsImVtYWlsIjoiZmVsaXBlLnBhcGFuaUB1ZnBlLmJyIn19.qQ7jeBinfMVCkW7E8Ut0Rgz1KG0pIPWkxaA53pJ8kpTIimUH2QoCoESJIKVt3zcZQjyVNF5b_GDK0jhurbBgWQ",
    "Content-Type": "application/json"
}

# Substitute with the ID of the pipe where cards will be deleted
pipe_id = "304524179"


# Query to list cards in a pipe (Corrected)
list_cards_query = """
{
  pipe(id: "%s") {
    phases {
      cards {
        edges {
          node {
            id
          }
        }
      }
    }
  }
}
""" % pipe_id


# Function to list cards
def list_cards():
    response = requests.post(url, headers=headers, json={"query": list_cards_query})
    response.raise_for_status()
    data = response.json()

    # Check for expected data structure and return card IDs
    if 'data' in data and 'pipe' in data['data'] and 'phases' in data['data']['pipe']:
        card_ids = []
        for phase in data['data']['pipe']['phases']:
            for edge in phase['cards']['edges']:
                card_ids.append(edge['node']['id'])
        return card_ids
    else:
        print("Error: Data structure not as expected.")
        print(data)
        return []


# Function to delete a card (No changes)
def delete_card(card_id):
    delete_card_mutation = """
    mutation {
      deleteCard(input: {id: "%s"}) {
        success
      }
    }
    """ % card_id
    response = requests.post(url, headers=headers, json={"query": delete_card_mutation})
    response.raise_for_status()
    data = response.json()
    return data['data']['deleteCard']['success']


# Confirm deletion before proceeding (No changes)
confirm = input("This script will delete ALL cards from the pipe. Are you sure? (y/n): ")

if confirm.lower() == 'y':
    # List all cards
    card_ids = list_cards()

    # Delete each card
    for card_id in card_ids:
        success = delete_card(card_id)
        print(f"Card {card_id} deleted: {success}")
else:
    print("Deletion cancelled.")
