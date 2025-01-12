import requests
import sys
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text
from rich.spinner import Spinner
from rich.live import Live
import time

BASE_URL = "http://127.0.0.1:5000"

console = Console()

def display_control_board():
	console.print("\n")
	table = Table(title="Control Keys")
	table.add_column("Key", style="bold cyan")
	table.add_column("Function", style="bold magenta")
	table.add_row("1", "Get details of an idea")
	table.add_row("2", "Enter a new query")
	table.add_row("3", "Explain the ranking of an idea")
	table.add_row("4", "Exit")
	console.print(table)

def display_ideas(ideas):
	console.print("\n")
	table = Table(title="Generated and Ranked Ideas")
	table.add_column("Rank", style="bold green")
	table.add_column("Idea", style="bold yellow")
	table.add_column("Score", style="bold blue")

	for i, idea_data in enumerate(ideas, 1):
		table.add_row(str(i), idea_data['idea'], str(idea_data['score']))

	console.print(table)

def main():
	while True:
		# Step 1: Input user query
		user_query = Prompt.ask("\n[bold cyan]Enter your query (e.g., 'What new app should I build?')[/bold cyan]")

		# Fetch ideas from the server
		response = requests.post(f"{BASE_URL}/generate_ideas", json={"query": user_query})
		if response.status_code != 200:
			console.print(f"[bold red]Error:[/bold red] {response.json().get('error', 'Unknown error')}")
			continue

		ideas = response.json().get("ideas", [])
		if not ideas:
			console.print("[bold yellow]No ideas generated. Try a different query.[/bold yellow]")
			continue

		display_ideas(ideas)

		while True:
			display_control_board()
			option = Prompt.ask("\n[bold cyan]Select an option[/bold cyan]")

			if option == "1":  # Get details of an idea
				selected = Prompt.ask("\n[bold cyan]Enter the idea number to get its details (e.g., '1')[/bold cyan]")
				try:
					idea_number = int(selected)
					if idea_number < 1 or idea_number > len(ideas):
						raise ValueError("Idea number is out of range.")

					response = requests.post(
						f"{BASE_URL}/get_suggestions",
						json={"selected_idea": ideas[idea_number - 1]['idea']}
					)
					if response.status_code != 200:
						console.print(f"[bold red]Error:[/bold red] {response.json().get('error', 'Unknown error')}")
						continue

					suggestion = response.json().get("suggestion", "No details available.")
					console.print(Text(f"\nDetails for Idea {idea_number}:\n\n{suggestion}", style="bold green"))
				except ValueError as e:
					console.print(f"[bold red]Error:[/bold red] {e}")
				except Exception as e:
					console.print(f"[bold red]Unexpected error:[/bold red] {e}")

			elif option == "2":  # Enter a new query
				break

			elif option == "3":  # Explain the ranking of an idea
				selected = Prompt.ask("\n[bold cyan]Enter the idea number to explain its ranking (e.g., '1')[/bold cyan]")
				try:
					idea_number = int(selected)
					if idea_number < 1 or idea_number > len(ideas):
						raise ValueError("Idea number is out of range.")

					response = requests.post(
						f"{BASE_URL}/explain_ranking",
						json={"idea": ideas[idea_number - 1]['idea']}
					)
					if response.status_code != 200:
						console.print(f"[bold red]Error:[/bold red] {response.json().get('error', 'Unknown error')}")
						continue

					explanation = response.json().get("explanation", "No explanation available.")
					console.print(Text(f"\nExplanation for Idea {idea_number}:\n\n{explanation}", style="bold green"))
				except ValueError as e:
					console.print(f"[bold red]Error:[/bold red] {e}")
				except Exception as e:
					console.print(f"[bold red]Unexpected error:[/bold red] {e}")

			elif option == "4":  # Exit
				console.print("[bold magenta]\nGoodbye![/bold magenta]")
				sys.exit(0)

			else:
				console.print("\n[bold red]Invalid option. Please select a valid option.[/bold red]")

if __name__ == "__main__":
	main()
