# spyrite

Python library to create MapLibre/Mapbox compatible sprite file.

## Requirements

- Few dependencies (only Pillow)
- Input: PNG files of icons
  - Parameters:
    - max_width: Maximum width of the sprite image, default is 1024
    - icon_height: Height of each icon, default is 64
- Output: MapLibre/Mapbox compatible sprite files (sprite.png and sprite.json)
