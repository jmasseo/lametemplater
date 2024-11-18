import os
import shutil
import yaml
import argparse
from jinja2 import Environment, FileSystemLoader

# Step 1: Parse Command Line Arguments
parser = argparse.ArgumentParser(description="Generate code repository from templates.")
parser.add_argument("config", help="Path to the input configuration file.")
parser.add_argument("output", help="Path to the output directory.")
args = parser.parse_args()

config_path = args.config
output_dir = args.output

# Load Configuration
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

# Define input path for templates
TEMPLATE_DIR = config.get("template_directory", "templates")

# Step 2: Set up the Jinja2 environment
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Set up global context if available
global_context = config.get("global_context", {})

def copy_files(files, output_dir):
    for file in files:
        src = os.path.join(TEMPLATE_DIR, file)
        dst = os.path.join(output_dir, file)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

def render_template(template_name, context, output_file):
    template = env.get_template(template_name)
    # Merge global context with the specific context
    merged_context = {**global_context, **context}
    rendered_content = template.render(merged_context)
    output_path = os.path.join(output_dir, output_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(rendered_content)

def render_multiple(template_name, context_list, output_names):
    template = env.get_template(template_name)
    for context, output_name in zip(context_list, output_names):
        # Merge global context with the specific context
        merged_context = {**global_context, **context}
        rendered_content = template.render(merged_context)
        output_path = os.path.join(output_dir, output_name)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(rendered_content)

# Step 3: Process the Configuration
# Copy files that are meant to be directly copied
if "copy_files" in config:
    copy_files(config["copy_files"], output_dir)

# Render single templates
if "templates" in config:
    for template_info in config["templates"]:
        template_name = template_info["template"]
        output_name = template_info["output"]
        context = template_info.get("context", {})
        render_template(template_name, context, output_name)

# Render templates that produce multiple outputs
if "multiple_templates" in config:
    for multi_template in config["multiple_templates"]:
        template_name = multi_template["template"]
        contexts = multi_template["contexts"]
        output_names = multi_template["output_files"]
        render_multiple(template_name, contexts, output_names)

print(f"Repository creation completed. Output at: {output_dir}")
