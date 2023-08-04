from rich.prompt import Prompt

class FlaskTemplateEngine:

    def __init__(self) -> None:
        
        pass

    def configure_flask_application(self) -> str:

        while True:

            http_port_choice = Prompt.ask("\n\nWhich http-port must flask run on")
            if http_port_choice.isnumeric() is True:
                break
            else:
                pass

        return http_port_choice

flask_template_engine = FlaskTemplateEngine()