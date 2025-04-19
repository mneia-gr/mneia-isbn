#!/usr/bin/env python

import sys
import xml.etree.ElementTree  # nosec
from pathlib import Path
from typing import Any, Dict

import defusedxml.ElementTree
from black import FileMode, format_str

ranges: Dict[str, Dict[str, Any]] = {}

tree = defusedxml.ElementTree.parse("./src/data/ranges.xml")
root = tree.getroot()

ean_ucc_prefixes = root.find("EAN.UCCPrefixes")
if not isinstance(ean_ucc_prefixes, xml.etree.ElementTree.Element):
    sys.exit("Something went wrong: Could not parse EAN.UCCPrefixes.")

for ean_ucc_prefix in ean_ucc_prefixes:
    prefix = ean_ucc_prefix.find("Prefix")
    if not isinstance(prefix, xml.etree.ElementTree.Element):
        sys.exit("Something went wrong: Could not parse EAN.UCC Prefix.")
    if prefix.text is None:
        sys.exit("Something went wrong: EAN.UCC Prefix is None")
    ranges[prefix.text] = {}

registration_groups = root.find("RegistrationGroups")
if not isinstance(registration_groups, xml.etree.ElementTree.Element):
    sys.exit("Something went wrong: Could not parse RegistrationGroups.")

for registration_group in registration_groups:
    registration_group_prefix = registration_group.find("Prefix")
    if not isinstance(registration_group_prefix, xml.etree.ElementTree.Element):
        sys.exit("Something went wrong: Could not parse RegistrionGroup Prefix.")
    if registration_group_prefix.text is None:
        sys.exit("Something went wrong: RegistrationGroup Prefix is None.")
    prefix_id, group = registration_group_prefix.text.split("-")
    ranges[prefix_id][group] = {}

    agency = registration_group.find("Agency")
    if not isinstance(agency, xml.etree.ElementTree.Element):
        sys.exit("Something went wrong: Could not parse RegistrationGroup Agency.")
    ranges[prefix_id][group]["name"] = agency.text

    ranges[prefix_id][group]["ranges"] = []
    rules = registration_group.find("Rules")
    if not isinstance(rules, xml.etree.ElementTree.Element):
        sys.exit("Something went wrong: Could not parse RegistrationGroup Rules.")
    for rule in rules:
        if not isinstance(rule, xml.etree.ElementTree.Element):
            sys.exit("Something went wrong: Could not parse RegistrationGroup Rule.")
        rule_length = rule.find("Length")
        if not isinstance(rule_length, xml.etree.ElementTree.Element):
            sys.exit("Something went wrong: Could not parse RegistrationGroup Rule Length.")
        if rule_length.text is None:
            sys.exit("Something went wrong: RegistrationGroup Rule Length is None.")
        rule_length_int = int(rule_length.text)
        if rule_length_int == 0:
            continue
        rule_range = rule.find("Range")
        if not isinstance(rule_range, xml.etree.ElementTree.Element):
            sys.exit("Something went wrong: Could not parse RegistrationGroup Rule Range.")
        if rule_range.text is None:
            sys.exit("Something went wrong: RegistrationGroup Rule Range is None.")
        rule_min, rule_max = rule_range.text.split("-")
        ranges[prefix_id][group]["ranges"].append([rule_min[:rule_length_int], rule_max[:rule_length_int]])

output = Path("./src/isbn/constants/ranges.py")
output.write_text(
    format_str(
        f"from typing import Any, Dict\n\nRANGES: Dict[str, Dict[str, Any]] = {ranges}",
        mode=FileMode(),
    )
)
