def progress_bar(iteration, total, prefix='', length=100):
    percentage = iteration / float(total) * 100
    filled_length = length * iteration // total
    completed = '█' * filled_length
    uncompleted = '-' * (length - filled_length)
    print(f"\r{prefix} |{completed}{uncompleted}| {percentage:.1f} %", end='')
    if iteration == total:
        print()
