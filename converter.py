import re

import svgpathtools as svg


def svg_file_to_html(path_to_file) -> str:
    """
    Converts the SVG file located at the specified path to an HTML string.

    Args:
        path_to_file (str): The path to the SVG file.

    Returns:
        str: The HTML representation of the SVG file as a string.
    """
    return str(svg.Document(path_to_file))


class SvgCodeToHtmlConverter:

    def __init__(self, svg_code: str, hex_color: str, width: int = 20, height: int = 20, view_box: str = '0 0 20 20'):
        """
        Initializes the SvgCodeToHtmlConverter object with the provided SVG code and hex color.

        Args:
            svg_code (str): The SVG code to be converted to HTML.
            hex_color (str): The hex color code to be used for stroke and fill in the converted HTML code.
            width (int): The width of the SVG element in pixels. Default is 20.
            height (int): The height of the SVG element in pixels. Default is 20.
            view_box (str): The viewBox attribute defines the position and dimensions,
            in user space, of an SVG viewport. Default is '0 0 20 20'.
        """
        self.svg_code = svg_code
        self.hex_color = hex_color
        self.width = width
        self.height = height
        self.view_box = view_box

    @property
    def _svg_rows_list(self) -> list:
        """
        Splits the SVG code into a list of rows.

        Returns:
            list: A list of rows in the SVG code.
        """
        return self.svg_code.split('\n')

    @staticmethod
    def _get_clear_svg(svg_code: str) -> str:
        """
        Removes the 'svg:' and ':svg' tags from the SVG code.

        Args:
            svg_code (str): The SVG code to be cleared.

        Returns:
            str: The SVG code with 'svg:' and ':svg' tags removed.
        """
        new_svg_code = re.sub(r':svg', '', svg_code)
        return re.sub(r'svg:', '', new_svg_code)

    def _get_change_stroke(self, svg_code: str) -> str:
        """
        Replaces the stroke color in the SVG code with the hex color provided in the object initialization.

        Args:
            svg_code (str): The SVG code to be modified.

        Returns:
            str: The SVG code with the stroke color replaced with the hex color provided in the object initialization.
        """
        return re.sub(r'stroke="#\w+"', f'stroke="{self.hex_color}"', svg_code)

    def _get_change_fill(self, svg_code: str) -> str:
        """
        Replaces the fill color in the SVG code with the hex color provided in the object initialization.

        Args:
            svg_code (str): The SVG code to be modified.

        Returns:
            str: The SVG code with the fill color replaced with the hex color provided in the object initialization.
        """
        return re.sub(r'fill="#\w+"', f'fill="{self.hex_color}"', svg_code)

    def _get_change_svg_tag(self, svg_code: str) -> str:
        """
        Modifies the width, height, and viewBox attributes in the SVG code.

        Args:
            svg_code (str): The SVG code to be modified.

        Returns:
            str: The SVG code with modified width, height, and viewBox attributes.
        """
        new_svg_code = re.sub(r'width="\d+"', f'width="{self.width}"', svg_code)
        new_svg_code = re.sub(r'height="\d+"', f'height="{self.height}"', new_svg_code)
        new_svg_code = re.sub(r'viewBox="[-\d\.]+ [-\d\.]+ [\d\.]+ [\d\.]+"', f'viewBox="{self.view_box}"',
                              new_svg_code)
        return new_svg_code

    def get_svg_tag(self) -> str:
        """
        Converts the SVG code to HTML code by applying the modifications in the class methods.

        Returns:
            str: The converted HTML code.
        """
        result_list = []
        for svg_code in self._svg_rows_list:
            new_svg_code = self._get_clear_svg(svg_code=svg_code)
            new_svg_code = self._get_change_svg_tag(svg_code=new_svg_code)
            new_svg_code = self._get_change_stroke(svg_code=new_svg_code)
            new_svg_code = self._get_change_fill(svg_code=new_svg_code)
            result_list.append(new_svg_code)

        return '\n'.join(result_list)
