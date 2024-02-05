def percentage_calculator(data):
    sorted_data = sorted(data.items(), key=lambda x: x[1][0])
    total = sum(1 / (abs(value[0]) + 0.01) for _, value in sorted_data)
    percentages = {key: (1 / (abs(value[0]) + 0.01)) / total * 100 for key, value in sorted_data}

    return percentages