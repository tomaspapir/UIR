from freeman import fill_pixels
import matplotlib.pyplot as plt


# counts the pixels in each row and writes it in the csv model file
def pixels_on_row(num, writer, filename):
    img = plt.imread(filename)
    if img.ndim > 2:
        img = img[:, :, 0]

    rows, cols = img.shape
    img_size = rows * cols
    img_1D_vector = img.reshape(img_size)
    img_1D_vector = fill_pixels(rows, cols, img_1D_vector)
    row_pixel_count = [0] * rows
    for k in range(rows):
        for l in range(cols):
            pixel = (cols * k) + l
            if img_1D_vector[pixel] != 0:
                row_pixel_count[k] += 1

    writer.writerow([str(num), str(row_pixel_count)])


# counts the pixels in each row
# returns pixel count in each row of the image
def pixels_on_row_sample(filename):
    img = plt.imread(filename)
    if img.ndim > 2:
        img = img[:, :, 0]

    rows, cols = img.shape
    img_size = rows * cols
    img_1D_vector = img.reshape(img_size)
    img_1D_vector = fill_pixels(rows, cols, img_1D_vector)
    row_pixel_count = [0] * rows
    for k in range(rows):
        for l in range(cols):
            pixel = (cols * k) + l
            if img_1D_vector[pixel] != 0:
                row_pixel_count[k] += 1

    return row_pixel_count
