import matplotlib.pyplot as plt


# freeman algorithm
# outlines the numbers outline with the help of the 1 - 8 directions
# after the first direction, skips already taken pixels before the selected pixel for staying on the number outline
# returns freeman directions list
def freeman(num, writer, filename, isSample):
    img = plt.imread(filename)
    if img.ndim > 2:
        img = img[:, :, 0]

    rows, cols = img.shape
    img_size = rows * cols
    img_1D_vector = img.reshape(img_size)
    img_1D_vector = fill_pixels(rows, cols, img_1D_vector)
    first_point = get_first_point(cols, rows, img_1D_vector)

    directions = [1, 2, 3,
                  8, 4,
                  7, 6, 5]

    dir_indexes = [1, 2, 3, 4, 5, 6, 7, 8]

    change_x = [-1, 0, 1,
                -1, 1,
                -1, 0, 1]

    change_y = [-1, -1, -1,
                0, 0,
                1, 1, 1]

    dir_index = dict(zip(directions, dir_indexes))

    result = []
    current_point = first_point

    for direction in directions:
        index = dir_index[direction]
        index = index - 1
        new_point = (first_point[0] + change_x[index], first_point[1] + change_y[index])
        point_pos = (cols * new_point[1]) + new_point[0]

        if img_1D_vector[point_pos] != 0:
            result.append(direction)
            current_point = new_point
            break

    while True:
        b_direction = (direction + 5) % 8

        if b_direction == 0:
            b_direction = 1

        dirs_1 = range(b_direction, 9)
        dirs_2 = range(1, b_direction)
        dirs = []
        dirs.extend(dirs_1)
        dirs.extend(dirs_2)

        for direction in dirs:
            index = dir_index[direction]
            index = index - 1
            new_point = (current_point[0] + change_x[index], current_point[1] + change_y[index])
            point_pos = (cols * new_point[1]) + new_point[0]

            if new_point[1] >= rows:
                point_pos = ((cols - 1) * new_point[1]) + new_point[0]

            if img_1D_vector[point_pos] != 0:
                result.append(direction)
                current_point = new_point
                break

        if current_point == first_point:
            break

    if not isSample:
        writer.writerow([str(num), str(result)])

    return result


# returns the first non empty pixel
def get_first_point(cols, rows, img_vector):
    for k in range(rows):
        for l in range(cols):
            pixel = (cols * k) + l
            if img_vector[pixel] >= 0.2:
                if img_vector[pixel + 1] == 0:
                    img_vector[pixel + 1] = 1
                return l, k


# unifies the non empty pixel opacity
def fill_pixels(rows, cols, img_vector):
    for k in range(rows):
        for l in range(cols):
            pixel = (cols * k) + l
            if img_vector[pixel] >= 0.4:
                img_vector[pixel] = 0.3
            else:
                img_vector[pixel] = 0

    for h in range(len(img_vector) - 28, len(img_vector) - 1):
        img_vector[h] = 0

    return img_vector
