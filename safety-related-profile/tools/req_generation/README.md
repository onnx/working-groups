# SONNX specification generator

This application uses [Jinja2}() to generate the markdown specification of an operator defined in a YAML file.

See the example given for the [**Div**](./div.yaml) operator.

Install the dependencies:
```
pip install -r requirements.txt
```

To generate a specification
- create the "op.yaml" file containing th definition of the operator
- then call
```
python render_operator.py --metadata op.yaml --template operator_spec.md.j2 --output op.generated.md
```

