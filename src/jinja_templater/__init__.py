from jinja2 import Environment, FileSystemLoader
import os 

class JinjaTemplateEngine:

    def __init__(self, template_dir):
        """
        Initialize the Jinja2Template class with the template directory.

        Args:
            template_dir (str): The directory where your Jinja2 templates are located.
        """
        current_file_dir = os.path.dirname(__file__)
        templates_dir = os.path.join(current_file_dir, "..", "templates", template_dir)
        self.env = Environment(loader=FileSystemLoader(templates_dir))

    def render_template(self, template_name, context):
        """
        Render the specified template with the provided context.

        Args:
            template_name (str): The name of the template file.
            context (dict): The dictionary containing the data to be used in the template.

        Returns:
            str: The rendered template as a string.
        """
        template = self.env.get_template(template_name)
        return template.render(context)


    def render_and_save_template(self, template_name, context, output_file, output_extension=".txt"):
        """
        Render the specified template with the provided context and save it to another file.
        """
        rendered_template = self.render_template(template_name, context)
    
        output_filename = f"{output_file}" if output_extension is None else f"{output_file}{output_extension}"
        output_path = os.path.join(os.getcwd(), output_filename)

        with open(output_path, "w") as output_file:
            output_file.write(rendered_template)

        return output_path

flask_jinja_template_engine = JinjaTemplateEngine("flask")
system_utils_template_engine = JinjaTemplateEngine("system-utils")