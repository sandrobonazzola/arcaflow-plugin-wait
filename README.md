# arcaflow-plugin-wait

A plugin for introducing a pause during workflow execution.

## Testing

For testing this plugin:

```console
python -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install
python -m coverage run -a -m unittest discover -s tests -v
python -m coverage html
```
