import typer
from rich.console import Console
from rich.table import Table
from devkit.utils.gh import gh_json
from devkit.utils.ai import ask_gemini

# 1. On crée l'objet principal
app = typer.Typer()

# 2. ON DÉFINIT LA COMMANDE AVEC @app.command()
@app.command()
def issues():
    """Affiche les tickets du dépôt actuel."""
    console = Console()
    console.print("[bold blue]Recherche des tickets...[/bold blue]")
    
    data = gh_json('issue', 'list', '--json', 'number,title,author')

    if not data:
        console.print("[yellow]Aucun ticket trouvé.[/yellow]")
        return

    table = Table(title="Tickets")
    table.add_column("N°")
    table.add_column("Titre")
    table.add_column("Auteur")

    for item in data:
        table.add_row(str(item['number']), item['title'], item['author']['login'])

    console.print(table)


@app.command()
def prs():
    """Affiche les Pull Requests ouvertes."""
    console = Console()
    console.print("[bold magenta]Recherche des Pull Requests...[/bold magenta]")
    
    data = gh_json('pr', 'list', '--json', 'number,title,author')

    if not data:
        console.print("[yellow]Aucune PR trouvée.[/yellow]")
        return

    table = Table(title="Pull Requests")
    table.add_column("N°", style="cyan")
    table.add_column("Titre")
    table.add_column("Auteur", style="green")

    for item in data:
        table.add_row(str(item['number']), item['title'], item['author']['login'])

    console.print(table)

@app.command()
def suggest(query: str):
    """Demande une suggestion à l'IA pour une tâche donnée."""
    console = Console()
    with console.status("[bold green]L'IA réfléchit..."):
        result = ask_gemini(query)
    
    console.print("\n[bold]Suggestion de Gemini :[/bold]")
    console.print(result)

if __name__ == "__main__":
    app()
