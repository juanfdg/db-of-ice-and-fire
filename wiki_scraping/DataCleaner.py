import os
import re
import json
import glob

unsupported_keys = ['race', 'played by', 'royal house', 'predecessor', 'successor', 'heir', 'reign', 'coronation',
                    'personal arms', 'buried in', 'full name', 'books', 'book(s)']
rename_keys = {'born in': 'born', 'died in': 'died',  'titles': 'title',
               'queen': 'spouse', 'consort': 'spouse'}


def CharacterCleaner(file_name: str):
    file = open(file_name, 'r')
    content = json.loads(file.read())
    file.close()

    for characters in content.keys():
        # Removing Unsupported Columns
        for key in unsupported_keys:
            if key in content[characters].keys():
                content[characters].pop(key)
        for key in rename_keys.keys():
            if key in content[characters].keys():
                content[characters][rename_keys[key]] = content[characters].pop(key)

        # Removing [digit]
        for key in content[characters].keys():
            if type(content[characters][key]) == list:
                for i in range(len(content[characters][key])):
                    content[characters][key][i] = re.sub(r"\[\d*\]", "", content[characters][key][i])
            else:
                content[characters][key] = re.sub(r"\[\d*\]", "", content[characters][key])

        # Removing empty fields
        for key in content[characters].keys():
            if type(content[characters][key]) == list:
                index = []
                for i in range(len(content[characters][key])):
                    if content[characters][key][i] == "":
                        index.append(i)
                index.reverse()
                for i in index:
                    content[characters][key].pop(i)

        # Stripping spaces off fields contents
        for key in content[characters].keys():
            if type(content[characters][key]) == list:
                for i in range(len(content[characters][key])):
                    content[characters][key][i] = content[characters][key][i].strip()
            else:
                content[characters][key] = content[characters][key].strip()

    base_dir = os.getcwd()
    filter_dir = base_dir + '/filter/character/'
    filtered_file = filter_dir + os.path.basename(file_name)
    if not os.path.exists(filter_dir):
        os.makedirs(filter_dir)
    file = open(filtered_file, 'w')
    file.write(json.dumps(content, indent=4))
    file.close()


if __name__ == '__main__':
    path = os.getcwd()
    for file_name in glob.glob(path + '/character/Character-*.json'):
        CharacterCleaner(file_name)
