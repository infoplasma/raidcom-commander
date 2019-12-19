from jinja2 import Environment, FileSystemLoader
from yaml import safe_dump, safe_load


with open('config/config.yaml') as yaml_data:
    cfg = safe_load(yaml_data)


def write_yaml(ldev_prefix='none',
               ldevs_gb='none',
               is_gad='none',
               gad_res_name='none',
               gad_dev_grp='0',
               pool_id='none',
               ser_pri='none',
               ser_sec='none',
               ldevs='none'):
    ldevs = [i.replace(":", "") for i in ldevs]
    ldev_dict = dict(zip(ldevs, ldevs_gb))

    data = {'ldevs': [{"ldev_id": i, "ldev_gb": j} for i, j in ldev_dict.items()],
            'ldevs_pfix': ldev_prefix,
            'gad':
                {'gad_grp': gad_dev_grp,
                 'gad_res_name': gad_res_name,
                 'is_gad': is_gad},
            'plural': '' if len(ldev_dict) == 1 else 's',
            'pool': {'pool_id': pool_id},
            'ser_pri': ser_pri,
            'ser_sec': ser_sec}


    with open("vars/params.yaml", "w", encoding='utf-8') as handle:
        safe_dump(data, handle)


def write_output(action_type):
    """
    """

    # Read the configuration file
    with open("vars/params.yaml", "r") as handle:
        devs = safe_load(handle)

    j2_env = Environment(loader=FileSystemLoader("."), trim_blocks=True, autoescape=True)

    if action_type == 'terminate':
        template = j2_env.get_template("templos/{}_terminator_templo.j2".format("gad" if devs['gad']['is_gad'] else "nogad"))
    else:
        template = j2_env.get_template("templos/{}_templo.j2".format("gad" if devs['gad']['is_gad'] else "nogad"))

    config = template.render(data=devs)
    with open(cfg['DEFAULT_OUTPUT_FILE'], "w") as output:
        output.write(config)
