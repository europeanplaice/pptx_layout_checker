# pptx_layout_checker

It checks whether the fonts used in the powerpoint file are different.

## usage

First, please create `config.json` in the same folder as `main.py`.
`filepath` and `font_to_be` must be defined.
```json
{
    "filepath": "font_sample/font_abadi.pptx ",
    "font_to_be": "Abadi"
}
```

Run python. `config.json` is loaded by python.
```python
python main.py

>>> Great, all grean.
```

## disclaimer
It is now being development.