import os
import re
import json
import glob

unsupported_keys = ['race', 'played by', 'royal house', 'predecessor', 'successor', 'heir', 'reign', 'coronation',
                    'personal arms', 'buried in', 'full name', 'books', 'book(s)']
rename_keys = {'born in': 'born', 'died in': 'died',  'titles': 'title',
               'queen': 'spouse', 'consort': 'spouse'}


def CharacterCleaner(file_name):
    file = open(file_name, 'r')
    content = json.loads(file.read())
    file.close()

    # Removing Unsupported Columns
    for characters in content.keys():
        for key in unsupported_keys:
            if key in content[characters].keys():
                content[characters].pop(key)
        for key in rename_keys.keys():
            if key in content[characters].keys():
                content[characters][rename_keys[key]] = content[characters].pop(key)

    # Removing [digit]
    for characters in content.keys():
        for key in content[characters].keys():
            if type(content[characters][key]) == list:
                for i in range(len(content[characters][key])):
                    content[characters][key][i] = re.sub(r"\[\d*\]", "", content[characters][key][i])
            else:
                content[characters][key] = re.sub(r"\[\d*\]", "", content[characters][key])

    # Removing empty fields
    for characters in content.keys():
        for key in content[characters].keys():
            if type(content[characters][key]) == list:
                index = []
                for i in range(len(content[characters][key])):
                    if content[characters][key][i] == "":
                        index.append(i)
                index.reverse()
                for i in index:
                    content[characters][key].pop(i)

    file = open('filter/character/'+file_name[68:], 'w')
    file.write(json.dumps(content, indent=4))
    file.close()


if __name__ == '__main__':
    path = os.getcwd()
    for file_name in glob.glob(path + '/character/Character-*.json'):
        CharacterCleaner(file_name)
