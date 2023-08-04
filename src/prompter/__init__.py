from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from ..flask_template_engine import flask_template_engine
from ..jinja_templater import flask_jinja_template_engine, system_utils_template_engine

import time, rich, json, os

class GeneralPrompt:

    def __init__(self) -> None:

        self.WEB_FRAMEWORKS: dict = {
            "1":"python-flask"
        }

        self.PROJECT_JSON_STRUCTURE_FILE = json.dumps({
            "project_name": "",
            "web_framework": "",
            "app_setting": ""
        }, indent=4)

        self.CONSOLE = Console()

    def show_loading(self, task_description: str, time_loading: int) -> None:
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description=task_description, total=None)
            time.sleep(time_loading)

    def ask_basic_setup(self) -> dict:

        project_name_choice = Prompt.ask("\n[Directory name] What's the name of your project :sunglasses:")

        while True:

            table = Table("Number", "Webframework")
            table.add_row(":keycap_1:", "Python (flask)")
            table.add_row(":exclamation:", "Future more frameworks stay tunned..")
            self.CONSOLE.print(table)
            web_framework_choice = Prompt.ask("\n\n[0-9] Which web-framework would you like to use :rocket:")
            if web_framework_choice.isnumeric() is True:
                try:
                    self.WEB_FRAMEWORKS[web_framework_choice]
                    break
                except KeyError:
                    pass
                    
        setup_data = {
            "project_name": project_name_choice,
            "web_framework": self.WEB_FRAMEWORKS[web_framework_choice]
        }

        return setup_data
    
    def ask_app_setup(self, type_web_framework: str) -> dict:

        # Python-flask installation
        if type_web_framework == self.WEB_FRAMEWORKS["1"]:

            self.show_loading(task_description="[*] Starting application setup... [*]", time_loading=1)
            return {
                "flask_host_port": flask_template_engine.configure_flask_application()
            }
          
        else:

            rich.print("[!] Not able to choose webframework [!]")
            return {
                "None": None
            }
        
    def create_folder(self, folder_name: str) -> None:
        """
        Create a new folder in the current working directory.
        """
        try:
            os.mkdir(folder_name)
            print(f"Folder '{folder_name}' created successfully.")
        except FileExistsError:
            print(f"Folder '{folder_name}' already exists.")
        except Exception as e:
            print(f"An error occurred while creating the folder: {e}")

    def create_project(self, project_meta_data: dict) -> dict:

        # Python-flask installation
        if project_meta_data["web_framework"] == self.WEB_FRAMEWORKS["1"]:

            ROOT_FOLDER: str = project_meta_data["project_name"]

            self.create_folder(ROOT_FOLDER)
            self.create_folder(f"{ROOT_FOLDER}/models")
            self.create_folder(f"{ROOT_FOLDER}/views")
            self.create_folder(f"{ROOT_FOLDER}/static")
            self.create_folder(f"{ROOT_FOLDER}/templates")
            self.create_folder(f"{ROOT_FOLDER}/lib")
            self.create_folder(f"{ROOT_FOLDER}/controllers")
            self.create_folder(f"{ROOT_FOLDER}/blueprints")

            # app.jinja2
            flask_jinja_template_engine.render_and_save_template(
                template_name="app.jinja2",
                context={
                    "flask_host_port": project_meta_data["app_setting"]["flask_host_port"]
                },
                output_file=f"{ROOT_FOLDER}/app",
                output_extension=".py"
            )
            # config.jinja2
            flask_jinja_template_engine.render_and_save_template(
                template_name="config.jinja2",
                context={
                    "" : "" # There no variable needed for this template
                },                
                output_file=f"{ROOT_FOLDER}/config",
                output_extension=".py"
            )
            # docker-compose.jinja2
            flask_jinja_template_engine.render_and_save_template(
                template_name="docker-compose.jinja2",
                context={
                    "flask_host_port": project_meta_data["app_setting"]["flask_host_port"],
                    "project_name": project_meta_data["project_name"]
                },
                output_file=f"{ROOT_FOLDER}/docker-compose",
                output_extension=".yml"
            )
            # extensions.jinja2
            flask_jinja_template_engine.render_and_save_template(
                template_name="extensions.jinja2",
                context={
                    "" : "" # There no variable needed for this template
                },      
                output_file=f"{ROOT_FOLDER}/extensions",
                output_extension=".py"
            )
            # readme.jinja2
            flask_jinja_template_engine.render_and_save_template(
                template_name="readme.jinja2",
                context={
                    "project_name": project_meta_data["project_name"]
                },
                output_file=f"{ROOT_FOLDER}/README",
                output_extension=".md"
            )
            # requirements.jinja2
            flask_jinja_template_engine.render_and_save_template(
                template_name="requirements.jinja2",
                context={
                    "" : "" # There no variable needed for this template
                },      
                output_file=f"{ROOT_FOLDER}/requirements",
                output_extension=".txt"
            )
            # docker_file_python.jinja2
            system_utils_template_engine.render_and_save_template(
                template_name="docker_file_python.jinja2",
                context={
                    "project_name": project_meta_data["project_name"],
                    "app_type": "flask",
                    "flask_host_port": project_meta_data["app_setting"]["flask_host_port"],
                    "python_docker_image": "coming"
                },
                output_file=f"{ROOT_FOLDER}/Dockerfile",
                output_extension=None
            )
            # docker_ignore.jinja2
            system_utils_template_engine.render_and_save_template(
                template_name="docker_ignore.jinja2",
                context={
                    "" : "" # There no variable needed for this template
                },      
                output_file=f"{ROOT_FOLDER}/.dockerignore",
                output_extension=None
            )

        else:

            pass

        # Project config
        with open(f"./{ROOT_FOLDER}/project_builder.config.json", "w") as json_file:
            json.dump(project_meta_data, json_file, indent=4)


general_prompt = GeneralPrompt()