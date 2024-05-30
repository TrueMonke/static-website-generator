from src.conv_funcs import extract_title, markdown_to_html_node
import os
import shutil


def extract_file_contents(file_path):

    try:
        with open(file_path, "r") as file:
            file_contents = file.read()

            return file_contents

    except FileNotFoundError:
        print("The file does not exist")
    except IOError:
        print("An error occurred while reading the file")


def generate_page(input_path: str, template_path: str, output_path: str) -> None:

    template_contents = extract_file_contents(template_path)
    markdown_contents = extract_file_contents(input_path)

    html_header = extract_title(markdown_contents)

    html_node = markdown_to_html_node(markdown_contents)

    html_contents = template_contents.replace("{{ Title }}", html_header).replace(
        "{{ Content }}", html_node.to_html()
    )

    try:
        with open(output_path, "w") as file:

            file.write(html_contents)

    except FileNotFoundError:
        print("The file does not exist")
    except IOError:
        print("An error occurred while reading the file")


def generate_html_files(input_dir, output_dir):

    try:

        template_path = "./template.html"

        entries = os.listdir(input_dir)

        for entry in entries:

            input_path = f"{input_dir}/{entry}"
            output_path = f"{output_dir}/{entry}"

            if os.path.isfile(input_path):
                print(f"Input Entry Path: {input_path}")

                if input_path[-3:] == ".md":

                    output_path = output_path.replace(".md", ".html")

                    generate_page(input_path, template_path, output_path)
                    print(f"Output Entry Path: {output_path}")

                else:
                    shutil.copy(input_path, output_path)
                    print(f"Output Entry Path: {output_path}")

            else:
                os.mkdir(output_path)
                generate_html_files(input_path, output_path)

    except FileNotFoundError:
        print("The directory does not exist")
    except PermissionError:
        print("You do not have permissions to access the directory")


if __name__ == "__main__":

    static_dir = "./content"
    public_dir = "./public"

    print("\n------------------------------\n")

    print(f"Clearing files in {public_dir}")
    shutil.rmtree(public_dir, ignore_errors=True)
    os.mkdir(public_dir)

    print("\n------------------------------\n")

    print(f"Copying Files from {static_dir} to {public_dir}")

    print("\n------------------------------\n")

    generate_html_files(static_dir, public_dir)

    print("\n------------------------------\n")
