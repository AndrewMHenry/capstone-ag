import itertools

PFAS_XS = [100, 200]

PFAS_DEFAULTS = dict(
        y=100,
        dx=100,
        dy=100,
        width=90,
        height=90,
        columns=6,
        rows=25
        )


def get_row_boxes(x, y, dx, width, height, columns):
    """Generate answer box coordinate tuples."""
    return [(xleft, y, xleft + width, y + height)
            for xleft in range(xleft, xleft + dx * columns, dx)
            ]

    boxes = [None for column in columns]
    ytop = y

    for column in columns:

        xleft = x + column * dx
        xright = xleft + width
        ybottom = ytop + height

        boxes[column] = (xleft, ytop, xright, ybottom)

    return boxes


def get_column_boxes(x, y, dx, dy, width, height, columns, rows):
    """Return list of lists of answer box tuples.

    a[0][0]         a[0][1]         ...     a[0][columns - 1]
    a[1][0]         a[1][1]         ...     a[1][columns - 1]
    ...             ...             ...     ...
    a[rows][0]      a[rows][1]      ...     a[rows - 1][columns - 1]

    """
    return [
            get_row_boxes(x, y + row * dy, dx, width, height, columns)
            for row in rows
            ]


PFAS_BOXES = list(itertools.chain(
    *[get_column_boxes(x=x, **PFAS_DEFAULTS) for x in PFAS_XS]
    ))


def process_PFAS(pfas_image):
    """Return dict of processed digit images from PFAS image."""
    answers = {
            str(i): [pfas_image.crop(box) for box in boxes]
            for i, boxes in enumerate(PFAS_BOXES, 1)
            }

    return {'answers': answers}

