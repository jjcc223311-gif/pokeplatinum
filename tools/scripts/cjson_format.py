"""Serialize JSON in cJSON's formatted style (tabs, "key":<TAB>value, inline scalar arrays),
which is how res/sound/pl_sound_data.json and the nitrogfx JSON files are written."""
import json


def _scalar(v):
    return json.dumps(v, ensure_ascii=False)


def dumps(value, depth=0):
    tab = '\t'
    if isinstance(value, dict):
        if not value:
            return '{\n' + tab * depth + '}'
        items = [tab * (depth + 1) + _scalar(k) + ':\t' + dumps(v, depth + 1) for k, v in value.items()]
        return '{\n' + ',\n'.join(items) + '\n' + tab * depth + '}'
    if isinstance(value, list):
        if not value:
            return '[]'
        if all(not isinstance(v, (dict, list)) for v in value):
            return '[' + ', '.join(_scalar(v) for v in value) + ']'
        return '[' + ', '.join(dumps(v, depth + 1) for v in value) + ']'
    return _scalar(value)
