import os
import re
import sys
from types import ModuleType

import click

from linkml.generators.yamlgen import YAMLGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.utils.compile_python import compile_python

from linkml_csv.dumpers.csv_dumper import CSVDumper
from linkml_runtime.dumpers.yaml_dumper import YAMLDumper
from linkml_runtime.dumpers.json_dumper import JSONDumper
from linkml_runtime.dumpers.dumper_root import Dumper
from linkml_csv.loaders.csv_loader import CSVLoader
from linkml_runtime.loaders.yaml_loader import YAMLLoader
from linkml_runtime.loaders.json_loader import JSONLoader
from linkml_runtime.loaders.loader_root import Loader

dumpers_loaders = {
    'tsv': (CSVDumper, CSVLoader),
    'csv': (CSVDumper, CSVLoader),
    'yaml': (YAMLDumper, YAMLLoader),
    'json': (JSONDumper, JSONLoader),
}

def make_python(schema) -> ModuleType:
    """
    Note: if you change the yaml schema and associated test instance objects,
    you may need to run this test twice
    """
    pstr = str(PythonGenerator(schema, mergeimports=True).serialize())
    m = compile_python(pstr)
    return m

def _get_format(input: str, input_format: str =None):
    if input_format is None:
        _, ext = os.path.splitext(input)
        if ext is not None:
            input_format = ext.replace('.', '')
        else:
            raise Exception(f'Must pass format option OR use known file suffix: {input}')
    return input_format.lower()

def _is_xsv(fmt: str) -> bool:
    return fmt == 'csv' or fmt == 'tsv'

def get_loader(fmt: str) -> Loader:
    return dumpers_loaders[fmt][1]()
def get_dumper(fmt: str) -> Loader:
    return dumpers_loaders[fmt][0]()


@click.command()
@click.option("--output", "-o")
@click.option("--input-format", "-f")
@click.option("--output-format", "-t")
@click.option("--schema", "-s")
@click.option("--index-slot", "-S", required=True)
@click.option("--target-class", "-C")
@click.argument("input")
def cli(input, output=None, input_format=None, output_format=None, index_slot=None, schema=None, target_class=None) -> None:
    """
    Converts to/from TSV to rich LinkML instance format (JSON/YAML/RDF)
    """
    print(f'IN={input}')
    python_module = make_python(schema)
    target_class = python_module.__dict__[target_class]
    schema = YAMLGenerator(schema).schema
    input_format = _get_format(input, input_format)
    output_format = _get_format(output, output_format)
    loader = get_loader(input_format)
    dumper = get_dumper(output_format)

    if _is_xsv(input_format):
        obj = loader.load(source=input, target_class=target_class, schema=schema, index_slot=index_slot)
    else:
        obj = loader.load(source=input,  target_class=target_class)
    print(f'Obj={obj}')
    if _is_xsv(output_format):
        obj = dumper.dump(obj, output, schema=schema, index_slot=index_slot)
    else:
        obj = dumper.dump(obj, output)


if __name__ == '__main__':
    cli(sys.argv[1:])
