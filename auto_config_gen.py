from yaml import safe_load, safe_dump
from email_getter import get_email


def to_dev_list(list_gb=[0], first_ldev_id = "0x0000"):

    first_dev_id_dec = int(first_ldev_id, 16)

    dev_id_list = []
    for i in range(len(list_gb)):
        dev_id = first_dev_id_dec + i
        dev_id_list.append(f"{dev_id:0{4}x}".upper())

    return list(zip(dev_id_list, list_gb))


def read_config(yaml_file):
    with open(yaml_file, "r") as f:
        return safe_load(f)


def update_config(mode='create'):

    get_email()

    with open("config/defaults.yaml", "r") as handle:
        cfg = safe_load(handle)

    data = read_config("./vars/params.yaml")

    values = []

    if mode == 'create':
        for i in data['devices']:
            for j in range(int(i['qty'])):
                values.append(i['size_gb'])
        first_id = input('FIRST AVAILABLE LDEV ID? (0x0000): ')
        a, b = (zip(*to_dev_list(values, first_id)))
        cfg['LDEVS'] = ','.join(map(str, a))
        cfg['GB'] = ','.join(map(str, b))
    elif mode == 'terminate':
        print(data['devices'])
        cfg['LDEVS'] = ','.join([i['lun_id'] for i in data['devices']])
        cfg['GB'] = ','.join([i['size_gb'] for i in data['devices']])

    cfg['TIER_INDEX'] = data['tier_index']
    cfg['LDEV_PREFIX_INDEX'] = data['prefix_index']
    cfg['REPLICA_INDEX'] = data['replica_index']

    with open("config/defaults.yaml", "w", encoding='utf-8') as handle:
        safe_dump(cfg, handle)


if __name__ == '__main__':
    update_config()