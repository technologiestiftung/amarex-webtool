import option_2


def process_input(input_array):
    # Create an input QVector<Point>
    input_vector = option_2.createPointVector()

    for point in input_array:
        c_point = option_2.createPoint(point[0], point[1])
        option_2.addPointToVector(input_vector, c_point)
        option_2.deletePoint(c_point)

    # Create an output QVector<Point>
    output_vector = option_2.createPointVector()

    # Call the processInput function
    option_2.processInput(input_vector, output_vector)

    # Clean up memory
    option_2.deletePointVector(input_vector)

    return output_vector
