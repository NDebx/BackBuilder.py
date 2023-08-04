from .prompter import general_prompt
from rich import print_json, print
from pathlib import Path
import typer, json

HELPING_MESSAGE_APP = "Create and manage easy a flask application with this CLI-tool\n\nBased on the django-cli"

app = typer.Typer(help=HELPING_MESSAGE_APP)

@app.command()
def setup():

    APP_STRUCTURE: dict = {}

    general_prompt.show_loading(task_description="[*] Starting setup... [*]", time_loading=1)

    while True:

        APP_STRUCTURE = general_prompt.ask_basic_setup()
        APP_STRUCTURE['app_setting'] = general_prompt.ask_app_setup(type_web_framework=APP_STRUCTURE['web_framework'])
        general_prompt.create_project(APP_STRUCTURE)
        
        print("\n\n[*] Created project from: [*]\n\n")
        print_json(data=APP_STRUCTURE)
        break
        
@app.command()
def setup_json(config: Path = typer.Option(..., "--config", "-c", help="Path to the JSON config file")):
    general_prompt.show_loading("[*] Startin setup from existing json file... [*]", 1)

    try:
        with config.open("r") as json_file:
            data = json.load(json_file)
            APP_STRUCTURE = data

        while True:
            general_prompt.create_project(APP_STRUCTURE)

            print("\n\n[*] Created project from: [*]\n\n")
            print_json(data=APP_STRUCTURE)
            break
    except FileNotFoundError as e:
        typer.echo(f"[!] File not found: {e.filename}")

