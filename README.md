# Random-Psychedelic-Art

This Python project generates artistic images using given expressions or creates random ones if no expression is provided.

#### Based on
This project is inspired by and based on [random-art](https://github.com/j2kun/random-art).

## Requirements

- Python 3.x
- Pillow (`pip install pillow`)

## Usage

1. Navigate to the project root directory.
2. Run the image generator using:

```bash
python -m genimg.genimg [options]
```

## Options:
* -s, --size: Size of the image (width and height). Default is 2048.
* -p, --pixels_per_unit: Pixels per unit. Default is 256.
* -c, --num_images: Number of images to generate. Default is 3.
* -f, --file: File containing expressions for image generation.

## Example:
To generate a single image from a provided expression file:

```bash
python -m genimg.genimg -c 1 -f path_to_file_with_expressions.txt
```

## Contributing
Feel free to fork this repository, add your own features, and create a pull request if you feel like your additions can benefit the main project!

## License
MIT License. Please see the license file for more information.