#!/opt/homebrew/bin/python3

import json
import argparse

def load_json(args):

    with open(args.gene_panel) as gene_json:
        gene_panel = json.load(gene_json)

    return gene_panel

def insert_new_ids(args, tx_dict):

    with open(args.map) as map_file:
        map = map_file.readlines()

    parsed_map = dict()
    for line in map:
        parsed_map[line.split('\t')[0]] = line.split('\t')[1]

    for i in range(len(tx_dict["payload"]["targets"])):
        try:
            id = tx_dict["payload"]["targets"][i]['type']['data']['id']
            new_name = parsed_map[id]
            tx_dict["payload"]["targets"][i]['type']['data']['name'] = new_name
        except KeyError:
            pass

    return tx_dict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gene_panel", help="10X experiments gene_panel.json")
    parser.add_argument("--map", help="Gene to new-name mapping file, in form of gene_id\tnew_gene_id")
    args = parser.parse_args()

    in_json = load_json(args)
    new_json = insert_new_ids(args, in_json)

    with open("/mnt/modified-panel.json", 'w') as write_file:
        json.dump(new_json, write_file, indent=4)
    write_file.close()



    

if __name__ == "__main__":
    main()
