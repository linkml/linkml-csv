from json_flattener import KeyConfig, GlobalConfig, Serializer
from json_flattener.flattener import CONFIGMAP
from linkml_runtime.linkml_model.meta import SlotDefinitionName, SchemaDefinition, ClassDefinition
from linkml_runtime.utils.yamlutils import YAMLRoot

def get_configmap(schema: SchemaDefinition, index_slot: SlotDefinitionName) -> CONFIGMAP:
    """

    :param schema: LinkML schema
    :param index_slot: key that indexes the top level object
    :return: mapping between top level keys and denormalization configurations
    """
    if index_slot is not None and schema is not None:
        slot = schema.slots[index_slot]
        if slot.range is not None and slot.range in schema.classes:
            tgt_cls = schema.classes[slot.range]
            cm = {}
            for sn in tgt_cls.slots:
                config = _get_key_config(schema, tgt_cls, sn)
                if config is not None:
                    cm[sn] = config
            return cm
        else:
            logging.warn(f'Slot range not to class: {slot.range}')
    else:
        logging.warn(f'Index slot or schema not specified')
    return {}

def _get_key_config(schema: SchemaDefinition, tgt_cls: ClassDefinition, sn: SlotDefinitionName, sep='_'):
    slot = schema.slots[sn]
    range = slot.range
    if range in schema.classes and slot.inlined:
        range_class = schema.classes[range]
        mappings = {}
        is_complex = False
        for inner_sn in range_class.slots:
            denormalized_sn = f'{sn}{sep}{inner_sn}'
            mappings[inner_sn] = denormalized_sn
            inner_slot = schema.slots[inner_sn]
            inner_slot_range = inner_slot.range
            if (inner_slot_range in schema.classes and inner_slot.inlined) or inner_slot.multivalued:
                is_complex = True
        if is_complex:
            serializers = [Serializer.json]
        else:
            serializers = []
        return KeyConfig(is_list=slot.multivalued, delete=True, flatten=True, mappings=mappings, serializers=serializers)
    else:
        return None


