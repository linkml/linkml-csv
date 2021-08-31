# DEPRECATED

This has now been merged into the linkml core

 * E.g. https://github.com/linkml/linkml-runtime/blob/main/linkml_runtime/dumpers/csv_dumper.py
 * linkml-convert CLI in linkml repo

# linkml-csv

Extension to linkml-runtime for converting between instances of LinkML models and CSVs. This may involve selective normalization/denormalization, plus serialization of selected elements as JSON/YAML

This builds on [json-flattener](https://github.com/cmungall/json-flattener)

## Command Line Usage

Denormalizing conversion from YAML instance data to TSV

```
link-convert \
  -s examples/bookshop.schema.yaml \
  -C Shop \
  -S all_book_series \
  -o examples/shop1.instance.tsv \
  examples/shop1.instance.yaml
```

Converting back to YAML/JSON:

```
link-convert \
  -s examples/bookshop.schema.yaml \
  -C Shop \
  -S all_book_series \
  -o examples/shop1-troundtrip.instance.json \
  examples/shop1.instance.tsv
```
