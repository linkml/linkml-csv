import io
import yaml
import json
from typing import Dict, List, Any

from linkml_runtime.dumpers.dumper_root import Dumper
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.utils.yamlutils import YAMLRoot
from linkml_runtime.linkml_model.meta import SlotDefinitionName, SchemaDefinition

from linkml_csv.utils.csvutils import GlobalConfig, get_configmap
from json_flattener import flatten_to_csv


class CSVDumper(Dumper):

    def dumps(self, element: YAMLRoot,
              index_slot: SlotDefinitionName = None,
              schema: SchemaDefinition = None,
              **kwargs) -> str:
        """ Return element formatted as CSV lines """
        element_j = json.loads(json_dumper.dumps(element))
        objs = element_j[index_slot]
        print(f'O={type(objs[0])}')
        configmap = get_configmap(schema, index_slot)
        config = GlobalConfig(key_configs=configmap)
        print(f'CM={configmap}')
        output = io.StringIO()
        flatten_to_csv(objs, output, config=config, **kwargs)
        return output.getvalue()
