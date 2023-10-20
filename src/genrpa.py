import argparse
import os
import re

from multiprocessing import Process, Queue, cpu_count

from PIL import Image
from reverse import from_string
from funcs import build_expr


def simple_hash(input_string, desired_length=25):
    """Compute a simple hash for the given string."""
    if not input_string:
        return ""
    h = 0x00000666
    multiplier = 25
    for char in input_string:
        h = ((h * multiplier) + ord(char)) & 0xFFFFFFFFFFFFFFFF
    hex_value = hex(h)[2:]
    return (hex_value * (desired_length // len(hex_value) + 1))[:desired_length]


def calculate_intensity(exp, x, y):
    """Calculate pixel intensity."""
    z = exp.eval(x, y)
    return int(z * 127.5 + 127.5)


def pixel_function(x, y, r_exp, g_exp, b_exp):
    """Determine pixel color based on expressions."""
    return (
        calculate_intensity(r_exp, x, y),
        calculate_intensity(g_exp, x, y),
        calculate_intensity(b_exp, x, y),
    )


def worker_process(x_range, y_range, queue, r_exp, g_exp, b_exp, pixels_per_unit):
    """Worker process to compute pixel values."""
    queue.put(
        {
            (px, py): pixel_function(
                (px - pixels_per_unit) / pixels_per_unit,
                (py - pixels_per_unit) / pixels_per_unit,
                r_exp,
                g_exp,
                b_exp,
            )
            for px in x_range
            for py in y_range
        }
    )


class ImageGenerator:
    """Class to generate images based on given expressions."""

    def __init__(self, width, height, pixels_per_unit):
        self.width = width
        self.height = height
        self.pixels_per_unit = pixels_per_unit

    def _build_expressions(self, exps=None):
        """Build or retrieve expressions for RGB."""
        return (
            (exps["R"], exps["G"], exps["B"])
            if exps
            else (build_expr(), build_expr(), build_expr())
        )

    def _setup_processes(self, r_exp, g_exp, b_exp):
        """Setup worker processes and queues."""
        num_processes = cpu_count()
        queues = [Queue() for _ in range(num_processes)]
        x_chunk = self.width // num_processes

        processes = [
            Process(
                target=worker_process,
                args=(
                    list(
                        range(
                            i * x_chunk,
                            (i + 1) * x_chunk if i != num_processes - 1 else self.width,
                        )
                    ),
                    list(range(self.height)),
                    queues[i],
                    r_exp,
                    g_exp,
                    b_exp,
                    self.pixels_per_unit,
                ),
            )
            for i in range(num_processes)
        ]
        return processes, queues

    def _generate_image(self, dir_name, processes, queues):
        """Generate and save image."""
        filename = os.path.join(dir_name, "image.png")
        with Image.new("RGB", (self.width, self.height)) as img:
            pixels = img.load()

            for p in processes:
                p.start()

            # Gather results from worker processes
            for q in queues:
                for (x, y), color in q.get().items():
                    pixels[x, y] = color

            for p in processes:
                p.join()

            img.save(filename)

    def _save_details(self, dir_name, r_exp, g_exp, b_exp):
        """Save expression details to a file."""
        hash_name = simple_hash(f"({r_exp})_({g_exp})_({b_exp})")
        details_filename = os.path.join(dir_name, f"details_{hash_name}.txt")
        with open(details_filename, "w") as file:
            file.write(f"r_exp: {r_exp}\n")
            file.write(f"g_exp: {g_exp}\n")
            file.write(f"b_exp: {b_exp}\n")

    def generate(self, index, exps=None):
        """Main method to generate image."""
        r_exp, g_exp, b_exp = self._build_expressions(exps)
        processes, queues = self._setup_processes(r_exp, g_exp, b_exp)

        dir_name = f"generated_image_{index}"
        os.makedirs(dir_name, exist_ok=True)

        self._generate_image(dir_name, processes, queues)
        self._save_details(dir_name, r_exp, g_exp, b_exp)

    def get_expressions_from_file(self, filename):
        """Retrieve expressions from a file."""
        with open(filename, "r") as file:
            content = file.read()
            return {
                color.upper(): from_string(expr)
                for color, expr in re.findall(r"(r|g|b)_exp: (.+)", content)
            }


def main():
    parser = argparse.ArgumentParser(
        description="Generate artistic images using multiprocessing."
    )
    parser.add_argument(
        "-s",
        "--size",
        type=int,
        default=2048,
        help="Size of the image (width and height). Default is 2048.",
    )
    parser.add_argument(
        "-p",
        "--pixels_per_unit",
        type=int,
        default=256,
        help="Pixels per unit. Default is 256.",
    )
    parser.add_argument(
        "-c",
        "--num_images",
        type=int,
        default=3,
        help="Number of images to generate. Default is 3.",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default=None,
        help="File containing expressions for image generation.",
    )
    args = parser.parse_args()

    generator = ImageGenerator(args.size, args.size, args.pixels_per_unit)

    if not args.file:
        for i in range(args.num_images):
            print(f"Processing image {i + 1}/{args.num_images}...")
            generator.generate(i)
        print(f"Finished processing {args.num_images} images.")
    else:
        print("Processing image from provided expressions...")
        exps = generator.get_expressions_from_file(args.file)
        generator.generate(0, exps)
        print("Finished processing image.")


if __name__ == "__main__":
    main()
