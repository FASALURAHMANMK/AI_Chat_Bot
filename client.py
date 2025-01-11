import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def display_control_board():
    print("\nOptions:")
    print("1. Get details of an idea")
    print("2. Enter a new query")
    print("3. Explain the ranking of an idea")
    print("4. Exit")

def main():
    while True:
        # Step 1: Input user query
        user_query = input("Enter your query (e.g., 'What new app should I build?'): ")

        # Fetch ideas from the server
        response = requests.post(f"{BASE_URL}/generate_ideas", json={"query": user_query})
        if response.status_code != 200:
            print("Error:", response.json().get("error", "Unknown error"))
            continue

        ideas = response.json().get("ideas", [])
        if not ideas:
            print("No ideas generated. Try a different query.")
            continue

        print("\nGenerated and Ranked Ideas:")
        for i, idea_data in enumerate(ideas, 1):
            print(f"{i}. {idea_data['idea']} (Score: {idea_data['score']})")

        while True:
            display_control_board()
            option = input("Select an option: ")

            if option == "1":  # Get details of an idea
                selected = input("Enter the idea number to get its details (e.g., '1'): ")
                try:
                    idea_number = int(selected)
                    if idea_number < 1 or idea_number > len(ideas):
                        raise ValueError("Idea number is out of range.")

                    response = requests.post(
                        f"{BASE_URL}/get_suggestions",
                        json={"selected_idea": ideas[idea_number - 1]['idea']}
                    )
                    if response.status_code != 200:
                        print("Error:", response.json().get("error", "Unknown error"))
                        continue

                    suggestion = response.json().get("suggestion", "No details available.")
                    print(f"\nDetails for Idea {idea_number}: \n{suggestion}")
                except ValueError as e:
                    print("Error:", e)
                except Exception as e:
                    print("Unexpected error:", e)

            elif option == "2":  # Enter a new query
                break

            elif option == "3":  # Explain the ranking of an idea
                selected = input("Enter the idea number to explain its ranking (e.g., '1'): ")
                try:
                    idea_number = int(selected)
                    if idea_number < 1 or idea_number > len(ideas):
                        raise ValueError("Idea number is out of range.")

                    response = requests.post(
                        f"{BASE_URL}/explain_ranking",
                        json={"idea": ideas[idea_number - 1]['idea']}
                    )
                    if response.status_code != 200:
                        print("Error:", response.json().get("error", "Unknown error"))
                        continue

                    explanation = response.json().get("explanation", "No explanation available.")
                    print(f"\nExplanation for Idea {idea_number}: {explanation}")
                except ValueError as e:
                    print("Error:", e)
                except Exception as e:
                    print("Unexpected error:", e)

            elif option == "4":  # Exit
                print("\nGoodbye!")
                sys.exit(0)

            else:
                print("Invalid option. Please select a valid option.")

if __name__ == "__main__":
    main()
