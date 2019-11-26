import os
import re
import json
import glob

character_unsupported_keys = ['race',
                              'played by',
                              'royal house',
                              'predecessor',
                              'successor',
                              'heir',
                              'reign',
                              'coronation',
                              'personal arms',
                              'buried in',
                              'full name',
                              'books',
                              'book(s)']

character_rename_keys = {'born in': 'born',
                         'died in': 'died',
                         'titles': 'title',
                         'queen': 'spouse',
                         'consort': 'spouse'}


def clean_file(file_name: str, filter_dir, unsupported_keys=None, rename_keys=None):
    print(file_name)
    file = open(file_name, 'r')
    content = json.loads(file.read())
    file.close()

    if unsupported_keys is None:
        unsupported_keys = []
    if rename_keys is None:
        rename_keys = {}

    for entities in content.keys():
        # Removing Unsupported Columns
        for key in unsupported_keys:
            if key in content[entities].keys():
                content[entities].pop(key)
        for key in rename_keys.keys():
            if key in content[entities].keys():
                content[entities][rename_keys[key]] = content[entities].pop(key)

        # Removing [digit]
        for key in content[entities].keys():
            if type(content[entities][key]) == list:
                for i in range(len(content[entities][key])):
                    content[entities][key][i] = re.sub(r"\[\d*\]", "", content[entities][key][i])
            else:
                content[entities][key] = re.sub(r"\[\d*\]", "", content[entities][key])

        # Removing empty fields
        for key in content[entities].keys():
            if type(content[entities][key]) == list:
                index = []
                for i in range(len(content[entities][key])):
                    if content[entities][key][i] == "":
                        index.append(i)
                index.reverse()
                for i in index:
                    content[entities][key].pop(i)

        # Stripping spaces off fields contents
        for key in content[entities].keys():
            if type(content[entities][key]) == list:
                for i in range(len(content[entities][key])):
                    content[entities][key][i] = content[entities][key][i].strip()
            else:
                content[entities][key] = content[entities][key].strip()

    base_dir = os.getcwd()
    filter_dir = base_dir + filter_dir
    filtered_file = filter_dir + os.path.basename(file_name)
    if not os.path.exists(filter_dir):
        os.makedirs(filter_dir)
    file = open(filtered_file, 'w')
    file.write(json.dumps(content, indent=4))
    file.close()


if __name__ == '__main__':
    path = os.getcwd()
    for file_name in glob.glob(path + '/character/Character-*.json'):
        clean_file(file_name,
                   '/filter/character/',
                   character_unsupported_keys,
                   character_rename_keys)

    for file_name in glob.glob(path + '/region/Houses-of-*.json'):
        clean_file(file_name,
                   '/filter/region/')
