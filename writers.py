from jinja2 import Environment, FileSystemLoader
from yaml import safe_dump, safe_load


with open('config/defaults.yaml') as yaml_data:
    cfg = safe_load(yaml_data)


def write_yaml(data):

    with open("vars/out_params.yaml", "w", encoding='utf-8') as handle:
        safe_dump(data, handle)


def write_output(action_type):

    # Read the configuration file
    with open("vars/out_params.yaml", "r") as handle:
        devs = safe_load(handle)

    j2_env = Environment(loader=FileSystemLoader("."), trim_blocks=True, autoescape=True)

    if action_type == 'terminate':
        template = j2_env.get_template("templos/{}_terminator_templo.j2".format("gad" if devs['gad']['is_gad'] else "nogad"))
    elif action_type == 'create':
        template = j2_env.get_template("templos/{}_templo.j2".format("gad" if devs['gad']['is_gad'] else "nogad"))
    else:
        import sys
        sys.exit(1)

    config = template.render(data=devs)
    with open(cfg['DEFAULT_OUTPUT_FILE'], "w") as output:
        output.write(config)
