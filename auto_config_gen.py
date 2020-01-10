from yaml import safe_load, safe_dump
from email_getter import get_email


def to_dev_list(list_gb=[0], first_ldev_id = "0x0000"):

    first_dev_id_dec = int(first_ldev_id, 16)

    dev_id_list = []
    for i in range(len(list_gb)):
        dev_id = first_dev_id_dec + i
        dev_id_list.append(f"{dev_id:0{4}x}".upper())

    return list(zip(dev_id_list, list_gb))


def update_in_params_from_ssm_out_params():
    import os, shutil
    src_path = r"../../storage_service_manager/"
    dst_path = r"./vars/"
    file_name = r"out_params.yaml"
    if os.path.exists(os.path.join(src_path, file_name)) and os.path.exists(os.path.join(dst_path, file_name)):
        os.rename()
        shutil.move(os.path.join(src_path, file_name), os.path.join(dst_path, file_name))


def read_config(yaml_file):
    with open(yaml_file, "r") as f:
        return safe_load(f)


def update_config():

    get_email()

    with open("config/defaults.yaml", "r") as handle:
        cfg = safe_load(handle)

    data = read_config("./vars/params.yaml")

    values = []

    for i in data['devices']:
        for j in range(int(i['qty'])):
            values.append(i['size_gb'])


    first_id = input('FIRST ID: (0x0000)')
    a, b = (zip(*to_dev_list(values, first_id)))

    cfg['LDEVS'] = ','.join(map(str, a))
    cfg['LDEVS_GB'] = ','.join(map(str, b))

    with open("config/defaults.yaml", "w", encoding='utf-8') as handle:
        safe_dump(cfg, handle)


if __name__ == '__main__':
    update_config()