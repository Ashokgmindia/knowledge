# import re
# from crewai_tools import tool


# @tool
# def read_content(file_path):
#     """
#     Read content to the specified file path.
#     """
#     with open(file_path, "r", encoding="utf-8") as file:
#         return file.read()


# @tool
# def write_content(file_path, content):
#     """
#     Write content to the specified file path.
#     """
#     with open(file_path, "w", encoding="utf-8") as file:
#         file.write(content)


# @tool
# def clean_html(content):
#     """
#     Clean HTML content by removing comments, extra whitespace, and extracting
#     the content within <html>...</html> tags.
#     """

#     # Remove HTML comments
#     content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)

#     # Extract content within <html>...</html> tags
#     match = re.search(r"(?s)<html.*?>.*?</html>", content)
#     if match:
#         content = match.group(0)
#     else:
#         content = ""  # If no <html>...</html> tags are found, result in empty content

#     # Remove extra whitespace and blank lines
#     content = re.sub(r"\n\s*\n", "\n", content)
#     content = content.strip()

#     return content


# @tool
# def clean_css(content):
#     """
#     Clean CSS content by removing everything before the first CSS rule starts
#     and everything after the last CSS rule ends. Also add responsive design rules.
#     """
#     # Find the content between the first '{' and the last '}'
#     match = re.search(r"\{.*?\}", content, flags=re.DOTALL)
#     if match:
#         # Extract the portion of content from the first '{' to the last '}'
#         start_index = content.find(".mobile-frame {")
#         end_index = content.rfind("}") + 1
#         # Extract the CSS rules
#         cleaned_content = content[start_index:end_index]
#     else:
#         # If no rules are found, return an empty string
#         cleaned_content = ""

#     # Remove CSS comments
#     cleaned_content = re.sub(r"/\*.*?\*/", "", cleaned_content, flags=re.DOTALL)

#     # Remove extra whitespace and blank lines
#     cleaned_content = re.sub(r"\n\s*\n", "\n", cleaned_content)
#     cleaned_content = cleaned_content.strip()

#     # Add responsive design CSS
#     responsive_css = """
# /* Responsive Design */
# @media only screen and (min-width: 768px) {
#   .mobile-frame {
#     width: 360px;
#     height: 640px;
#     border: none;
#     box-shadow: none;
#   }
# }
#     """
#     final_css = f"{cleaned_content}\n\n{responsive_css}"

#     return final_css


# @tool
# def main():
#     """
#     Main function to read, clean, and write HTML and CSS files.
#     """
#     # Paths for HTML and CSS files
#     html_input_file_path = "outs/designer_output.html"
#     html_output_file_path = "outs/designer_output.html"
#     css_input_file_path = "outs/designer_output.css"
#     css_output_file_path = "outs/designer_output.css"

#     # Clean HTML content
#     html_content = read_content(html_input_file_path)
#     cleaned_html_content = clean_html(html_content)
#     write_content(html_output_file_path, cleaned_html_content)
#     print(f"Cleaned HTML content has been written to '{html_output_file_path}'.")

#     # Clean CSS content
#     css_content = read_content(css_input_file_path)
#     cleaned_css_content = clean_css(css_content)
#     write_content(css_output_file_path, cleaned_css_content)
#     print(f"Cleaned CSS content has been written to '{css_output_file_path}'.")


# if __name__ == "__main__":
#     main()


from PIL import Image, ImageDraw, ImageFont


class ContactManagementWireframe:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw_wireframe(self):
        # Create a blank image with white background
        image = Image.new("RGB", (self.width, self.height), "white")
        draw = ImageDraw.Draw(image)

        # Draw header
        draw.rectangle(
            [0, 0, self.width, 60], outline="black", fill="lightgrey", width=2
        )
        draw.text((10, 20), "Contact Management System", fill="black")

        # Draw sidebar
        sidebar_width = 150
        draw.rectangle(
            [0, 60, sidebar_width, self.height],
            outline="black",
            fill="lightgrey",
            width=2,
        )
        draw.text((10, 80), "Contacts", fill="black")
        draw.text((10, 120), "Groups", fill="black")
        draw.text((10, 160), "Settings", fill="black")

        # Draw main content area
        content_x_start = sidebar_width + 10
        draw.rectangle(
            [content_x_start, 60, self.width, self.height], outline="black", width=2
        )

        # Draw search bar
        search_bar_height = 40
        draw.rectangle(
            [content_x_start + 10, 70, self.width - 10, 70 + search_bar_height],
            outline="black",
            width=1,
        )
        draw.text((content_x_start + 20, 80), "Search Contacts...", fill="grey")

        # Draw contact list
        list_y_start = 70 + search_bar_height + 10
        draw.rectangle(
            [
                content_x_start + 10,
                list_y_start,
                self.width // 2 - 10,
                self.height - 10,
            ],
            outline="black",
            width=1,
        )
        draw.text(
            (content_x_start + 20, list_y_start + 10), "Contact List", fill="black"
        )

        # Draw contact details section
        draw.rectangle(
            [self.width // 2 + 10, list_y_start, self.width - 10, self.height - 10],
            outline="black",
            width=1,
        )
        draw.text(
            (self.width // 2 + 20, list_y_start + 10), "Contact Details", fill="black"
        )

        # Draw Add Contact button
        button_width, button_height = 120, 40
        button_x_start = content_x_start + 10
        button_y_start = self.height - button_height - 20
        draw.rectangle(
            [
                button_x_start,
                button_y_start,
                button_x_start + button_width,
                button_y_start + button_height,
            ],
            outline="black",
            fill="lightblue",
            width=1,
        )
        draw.text(
            (button_x_start + 10, button_y_start + 10), "Add Contact", fill="black"
        )

        return image

    def save_image(self, filename="contact_management_wireframe.png"):
        image = self.draw_wireframe()
        image.save(filename)


# Example usage
wireframe_tool = ContactManagementWireframe(800, 600)
wireframe_tool.save_image("contact_management_wireframe.png")
