from crewai_tools import tool
import requests
from plantuml import PlantUML, PlantUMLHTTPError


@tool
def activity_diagram(plantuml_code: str, output_file: str = "activity_diagram.png"):
    """
    Generate an activity diagram image from PlantUML code and save it as a PNG file.

    Parameters:
    - plantuml_code (str): The PlantUML code that defines the activity diagram.
    - output_file (str): The name of the output file where the generated PNG image will be saved.
      Defaults to "activity_diagram.png".

    Returns:
    - None: This function does not return a value. The primary output is the component diagram image saved as a file.

    Example:
        plantuml_code = '''
        @startuml
        :User Authentication;
        :User sends login credentials;
        :System verifies credentials;
        :User granted access;
        @enduml
        '''
        activity_diagram(plantuml_code)
    """
    plantuml_server = PlantUML(url="http://www.plantuml.com/plantuml/img/")
    response = plantuml_server.processes(plantuml_code)
    with open(output_file, "wb") as f:
        f.write(response)


@tool
def component_diagram(plantuml_code: str, output_file: str = "component_diagram.png"):
    """
    Generate a component diagram image from PlantUML code and save it as a PNG file.

    Parameters:
    - plantuml_code (str): The PlantUML code that defines the component diagram.
    - output_file (str): The name of the output file where the generated PNG image will be saved.
      Defaults to "component_diagram.png".

    Returns:
    - None: This function does not return a value. The primary output is the component diagram image saved as a file.

    """
    plantuml_server = PlantUML(url="http://www.plantuml.com/plantuml/img/")
    response = plantuml_server.processes(plantuml_code)
    with open(output_file, "wb") as f:
        f.write(response)


@tool
def use_case_diagram(plantuml_code: str, output_file: str = "use_case_diagram.png"):
    """
    Generate a use case diagram image from PlantUML code and save it as a PNG file.

    Parameters:
    - plantuml_code (str): The PlantUML code that defines the use case diagram.
    - output_file (str): The name of the output file where the generated PNG image will be saved.
      Defaults to "use_case_diagram.png".

    Returns:
    - None: This function does not return a value. The primary output is the use_case_diagram image saved as a file.

    """
    plantuml_server = PlantUML(url="http://www.plantuml.com/plantuml/img/")
    response = plantuml_server.processes(plantuml_code)
    with open(output_file, "wb") as f:
        f.write(response)


@tool
def plantuml_to_flowchart(plantuml_code: str, output_file: str = "flowchart.png"):
    """
    Generate a flowchart image from PlantUML code and save it as a PNG file.

    This function utilizes the PlantUML server to process PlantUML code and generate a flowchart image in PNG format.
    The generated image is then saved to a specified file.

    Parameters:
    - plantuml_code (str): The PlantUML code that defines the flowchart. This code should follow the PlantUML syntax.
    - output_file (str): The name of the output file where the generated PNG image will be saved.
      Defaults to "flowchart.png".

    Returns:
    - None: This function does not return any value. It writes the generated image to the specified output file.
    """
    # Initialize PlantUML server
    plantuml_server = PlantUML(url="http://www.plantuml.com/plantuml/img/")

    # Generate PNG from PlantUML code
    response = plantuml_server.processes(plantuml_code)

    # Write the response content to a file
    with open(output_file, "wb") as f:
        f.write(response)
