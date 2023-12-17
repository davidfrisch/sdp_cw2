import matplotlib.pyplot as plt
import numpy as np

def plot_lines_test_vs_target_dates(metric_lines_test, metric_lines_target, metric):
    
    test_file = [(x['commit'].committer_date, x[metric]) for x in metric_lines_test]
    target_file = [(x['commit'].committer_date, x[metric]) for x in metric_lines_target]

    test_file.sort(key=lambda x: x[0])
    target_file.sort(key=lambda x: x[0])

    test_file_dates = [x[0] for x in test_file]
    test_file_values = [x[1] for x in test_file]

    target_file_dates = [x[0] for x in target_file]
    target_file_values = [x[1] for x in target_file]

    plt.plot(test_file_dates, test_file_values, label='test')
    plt.plot(target_file_dates, target_file_values, label='target')

    # show data points
    plt.plot(test_file_dates, test_file_values, 'o', markersize=3)
    plt.plot(target_file_dates, target_file_values, 'o', markersize=3)

    plt.xlabel('Date')
    plt.ylabel(f'{metric}')

    plt.title(f'{metric} per date for test and target file')

    plt.legend()
    
    plt.gcf().autofmt_xdate()
    plt.show()



def plot_lines_test_vs_target_numeric(metric_lines_test, metric_lines_target, metric):
      
    test_file = [(x['commit'].committer_date, x[metric]) for x in metric_lines_test]
    target_file = [(x['commit'].committer_date, x[metric]) for x in metric_lines_target]

    test_file.sort(key=lambda x: x[0])
    target_file.sort(key=lambda x: x[0])

    test_file_dates = [x[0] for x in test_file]
    test_file_values = [x[1] for x in test_file]

    target_file_dates = [x[0] for x in target_file]
    target_file_values = [x[1] for x in target_file]

    all_dates = sorted(list(set(test_file_dates + target_file_dates)))
    x_axis = np.arange(len(all_dates))

    fig, ax = plt.subplots()

    ax.plot([all_dates.index(date) for date in test_file_dates], test_file_values, marker='x', label='Test')
    ax.plot([all_dates.index(date) for date in target_file_dates], target_file_values, marker='o', label='Target')

    ax.set_xticks(x_axis)

    ax.set_xlabel('Integer-based X-axis')
    ax.set_ylabel(metric)

    ax.legend()

    plt.show()


def plot_lines_test_vs_target_normalise_100(metric_lines_test, metric_lines_target, metric):
      
    test_file = [(x['commit'].committer_date, x[metric]) for x in metric_lines_test]
    target_file = [(x['commit'].committer_date, x[metric]) for x in metric_lines_target]

    test_file.sort(key=lambda x: x[0])
    target_file.sort(key=lambda x: x[0])

    test_file_dates = [x[0] for x in test_file]
    test_file_values = [x[1] for x in test_file]

    target_file_dates = [x[0] for x in target_file]
    target_file_values = [x[1] for x in target_file]

    all_dates = sorted(list(set(test_file_dates + target_file_dates)))
    min_value = min(all_dates)
    max_value = max(all_dates)

    # TODO David: check if this is correct the denominator
    denominator = max_value - min_value if max_value - min_value != 0 else 1
    normalized_x_axis = [((date - min_value) / denominator) * 100 for date in all_dates]
    fig, ax = plt.subplots()

    ax.plot([normalized_x_axis[all_dates.index(date)] for date in test_file_dates], test_file_values, marker='x', label='Test')
    ax.plot([normalized_x_axis[all_dates.index(date)] for date in target_file_dates], target_file_values, marker='o', label='Target')

    x_ticks = np.arange(0, 101, 10)
    ax.set_xticks(x_ticks)

    ax.set_xlabel('History time of target vs test files (%)')
    ax.set_ylabel(metric)

    ax.legend()

    plt.show()
