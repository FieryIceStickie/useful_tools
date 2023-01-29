import re
from typing import Optional

import pytest

stare_regex = r'^(I)?' \
              r'(C|AC|UD|)' \
              r'((?<=C)[UD]|(?<=AC)[UD]|(?<=UD)[LR]|(?=(?<!C))(?=(?<!AC|UD)))' \
              r'NMFubukiStare' \
              r'((?<=^INMFubukiStare)Back|(?<=^NMFubukiStare)Back)?$'


@pytest.mark.parametrize('name,output', [
    ('NMFubukiStare', (None, '', '', None)),
    ('NMFubukiStareBack', (None, '', '', 'Back')),
    ('CUNMFubukiStare', (None, 'C', 'U', None)),
    ('CDNMFubukiStare', (None, 'C', 'D', None)),
    ('UDLNMFubukiStare', (None, 'UD', 'L', None)),
    ('UDRNMFubukiStare', (None, 'UD', 'R', None)),
    ('ACUNMFubukiStare', (None, 'AC', 'U', None)),
    ('ACDNMFubukiStare', (None, 'AC', 'D', None)),
    ('INMFubukiStare', ('I', '', '', None)),
    ('INMFubukiStareBack', ('I', '', '', 'Back')),
    ('ICUNMFubukiStare', ('I', 'C', 'U', None)),
    ('ICDNMFubukiStare', ('I', 'C', 'D', None)),
    ('IUDLNMFubukiStare', ('I', 'UD', 'L', None)),
    ('IUDRNMFubukiStare', ('I', 'UD', 'R', None)),
    ('IACUNMFubukiStare', ('I', 'AC', 'U', None)),
    ('IACDNMFubukiStare', ('I', 'AC', 'D', None)),
])
def test_valid_name(name: str, output: tuple[Optional[str], str, str, Optional[str]]):
    assert re.match(stare_regex, name).groups() == output


@pytest.mark.parametrize('name', [
    'FubukiStare',
    'CNMFubukiStare',
    'ACNMFubukiStare',
    'UDNMFubukiStare',
    'LNMFubukiStare',
    'RNMFubukiStare',
    'UNMFubukiStare',
    'DNMFubukiStare',
    'CLNMFubukiStare',
    'CRNMFubukiStare',
    'UDUNMFubukiStare',
    'UDDNMFubukiStare',
    'ACLNMFubukiStare',
    'ACRNMFubukiStare',

    'FubukiStareBack',
    'CNMFubukiStareBack',
    'ACNMFubukiStareBack',
    'UDNMFubukiStareBack',
    'LNMFubukiStareBack',
    'RNMFubukiStareBack',
    'UNMFubukiStareBack',
    'DNMFubukiStareBack',
    'CLNMFubukiStareBack',
    'CRNMFubukiStareBack',
    'UDUNMFubukiStareBack',
    'UDDNMFubukiStareBack',
    'ACLNMFubukiStareBack',
    'ACRNMFubukiStareBack',

    'IFubukiStare',
    'ICNMFubukiStare',
    'IACNMFubukiStare',
    'IUDNMFubukiStare',
    'ILNMFubukiStare',
    'IRNMFubukiStare',
    'IUNMFubukiStare',
    'IDNMFubukiStare',
    'ICLNMFubukiStare',
    'ICRNMFubukiStare',
    'IUDUNMFubukiStare',
    'IUDDNMFubukiStare',
    'IACLNMFubukiStare',
    'IACRNMFubukiStare',

    'IFubukiStareBack',
    'ICNMFubukiStareBack',
    'IACNMFubukiStareBack',
    'IUDNMFubukiStareBack',
    'ILNMFubukiStareBack',
    'IRNMFubukiStareBack',
    'IUNMFubukiStareBack',
    'IDNMFubukiStareBack',
    'ICLNMFubukiStareBack',
    'ICRNMFubukiStareBack',
    'IUDUNMFubukiStareBack',
    'IUDDNMFubukiStareBack',
    'IACLNMFubukiStareBack',
    'IACRNMFubukiStareBack',
])
def test_invalid_name(name: str):
    assert re.match(stare_regex, name) is None


if __name__ == '__main__':
    pass
