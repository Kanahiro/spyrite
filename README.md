# spyrite

Python library to create MapLibre/Mapbox compatible sprite file.

## Requirements

- Few dependencies (only Pillow)
- Input: Image files of icons
  - Parameters:
    - max_width: Maximum width of the sprite image, default is 1024
    - icon_height: Height of each icon, default is 64
- Output: MapLibre/Mapbox compatible sprite files (sprite.png and sprite.json)

## CLI Usage

```bash
python -m spyrite icons_dir
# This will generate sprite.png and sprite.json in the current directory

python -m spyrite icons_dir --output-dir output_dir --max-width 2048 --icon-height 128
# This will generate sprite.png and sprite.json in output_dir with specified parameters
```
