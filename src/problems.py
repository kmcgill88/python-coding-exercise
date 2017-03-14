#!/usr/bin/python
from base import Base
import json


def problem_1(base_class, results, weather_files):
    """Run problem one.

    :param base_class: Base class that runs all problems and
    :param results: A dictionary to organize data for output
    :param weather_files: A list of sorted (ascending) weather station files
    """
    print("Running Problem 1")

    # Create file for output
    output_file = open('{0}/{1}'.format(base_class.answers_dir, "MissingPrcpData.out"), 'w')

    # Loop through all files
    for weather_file in weather_files:
        results[weather_file] = 0
        # Open and split data by line numbers for use
        weather_data_lines = open("{0}/{1}".format(base_class.weather_dir, weather_file), 'r').read().split('\n')

        for line_item in weather_data_lines:
            line_item = line_item.split('\t')
            # Find number of days in which the maximum temperature and minimum temperature data are present but the
            # precipitation data is missing.
            if len(line_item) == 4:
                if line_item[1] != "-9999" and line_item[2] != "-9999" and line_item[3] == "-9999":
                    # Found expected result, increment
                    results[weather_file] += 1

        # Write output per file
        output_file.write("{0}\t{1}\n".format(weather_file, results[weather_file]))


def problem_2(base_class, results, weather_files):
    """Run problem two.

    :param base_class: Base class that runs all problems and
    :param results: A dictionary to organize data for output
    :param weather_files: A list of sorted (ascending) weather station files
    """
    print("Running Problem 2.")

    output_file = open('{0}/{1}'.format(base_class.answers_dir, "YearlyAverages.out"), 'w')
    # Loop through all files
    for weather_file in weather_files:
        # Open and split data by line numbers for use
        weather_data_lines = open("{0}/{1}".format(base_class.weather_dir, weather_file), 'r').read().split('\n')

        for line_item in weather_data_lines:
            line_item = line_item.split('\t')

            # Make sure we have a valid line
            if len(line_item) == 4:
                year = line_item[0][:4]
                if year not in results:
                    # Init if needed
                    results[year] = {}
                    results[year]['high'] = 0
                    results[year]['high_entries'] = 0
                    results[year]['low'] = 0
                    results[year]['low_entries'] = 0
                    results[year]['precipitation'] = 0

                if line_item[1] != "-9999":
                    high = (results[year]['high'] * results[year]['high_entries'])
                    high += float(line_item[1])
                    results[year]['high_entries'] += 1
                    results[year]['high'] = high / results[year]['high_entries']

                if line_item[2] != "-9999":
                    low = (results[year]['low'] * results[year]['low_entries'])
                    low += float(line_item[2])
                    results[year]['low_entries'] += 1
                    results[year]['low'] = low / results[year]['low_entries']

                if line_item[3] != "-9999":
                    results[year]['precipitation'] += float(line_item[3])

        output = ""
        keys = results.keys()
        keys.sort()
        for year in keys:
            output += "\t{0}\t{1}\t{2}\t{3}".format(year,
                                                    format(float(results[year]['high']), '.2f'),
                                                    format(float(results[year]['low']), '.2f'),
                                                    format(float(results[year]['precipitation']), '.2f'))

        output_file.write('{0}{1}\n'.format(weather_file, output))
        results = {}  # Reset for fresh averages the next go around


def problem_3(base_class, results, weather_files):
    """Run problem three.

    I didn't understand the instructions here so I improvised. I loop through all averages from problem 2 and collect
    the highest average high per year across weather stations. I repeat for low, precipitation only had a total so I
    skipped it. Then I go through each station and get a count how many times the high and lows occur.

    :param base_class: Base class that runs all problems and
    :param results: A dictionary to organize data for output
    :param weather_files: A list of sorted (ascending) weather station files
    """
    print("Running Problem 3.")

    averages = open('{0}/{1}'.format(base_class.answers_dir, "YearlyAverages.out"), 'r').read().split('\n')

    print("Determining highest averages across all weather stations.")
    for average in averages:
        line_item = average.split('\t')
        year_index = 1
        for data in line_item:
            # stop searching on this line if there is no next year
            if year_index >= len(line_item) - 1:
                break

            year = line_item[year_index]
            if year not in results:
                results[year] = {}
                results[year]['high'] = 0
                results[year]['low'] = 999999999.99
                results[year]['precipitation'] = 0

            if float(line_item[year_index + 1]) > results[year]['high']:
                results[year]['high'] = float(line_item[year_index + 1])

            if float(line_item[year_index + 2]) < results[year]['low']:
                results[year]['low'] = float(line_item[year_index + 2])

            if float(line_item[year_index + 3]) > results[year]['precipitation']:
                results[year]['precipitation'] = float(line_item[year_index + 3])

            # Increment to the next year in the line
            year_index += 4

    # Save data for problem 4
    open('{0}/{1}'.format(base_class.answers_dir, "avgs.dat"), 'w').write(json.dumps(results))

    # Determine how many times per weather station per year weather data
    for weather_file in weather_files:
        # Open and split data by line numbers for use
        weather_data_lines = open("{0}/{1}".format(base_class.weather_dir, weather_file), 'r').read().split('\n')

        for line_item in weather_data_lines:
            line_item = line_item.split('\t')
            if len(line_item) == 4:
                year = line_item[0][:4]

                if line_item[1] != "-9999" and float(line_item[1]) >= results[year]['high']:
                    if 'high_count' not in results[year]:
                        results[year]['high_count'] = 0

                    results[year]['high_count'] += 1

                if line_item[2] != "-9999" and float(line_item[2]) <= results[year]['low']:
                    if 'low_count' not in results[year]:
                        results[year]['low_count'] = 0

                    results[year]['low_count'] += 1

    output_file = open('{0}/{1}'.format(base_class.answers_dir, "YearHistogram.out"), 'w')
    years = results.keys()
    years.sort()
    for yr in years:
        output_file.write('{0}\t{1}\t{2}\n'.format(yr, results[yr]['high_count'], results[yr]['low_count']))


def problem_4(base_class, results, weather_files):
    """Run problem four to find the Pearson Correlation.

    Here I am using the high and low saved to avg.dat in problem 3 to find the Pearson correlation. I am not a
    Pearson correlation expert however it looked like to calculate you must have even data sets. ie. 10 temp entries
    then we must have 10 yield entries.

    Instead, I took the high, low and precipitation across all weather stations and compared that to the yield data per
    average, per year.

    :param base_class: Base class that runs all problems and
    :param results: A dictionary to organize data for output
    :param weather_files: A list of sorted (ascending) weather station files
    """
    print("Running problem 4.")

    # Collect grain yield data
    grain_yield = {}
    yield_list = open('{0}/{1}'.format(base_class.yield_dir, "US_corn_grain_yield.txt"), 'r').read().split('\n')
    for entry in yield_list:
        entry = entry.split('\t')
        if len(entry) == 2:
            grain_yield[entry[0]] = float(entry[1])

    averages = json.loads(open('{0}/{1}'.format(base_class.answers_dir, "avgs.dat"), 'r').read())
    output_file = open('{0}/{1}'.format(base_class.answers_dir, "Correlations.out"), 'w')

    keys = averages.keys()
    keys.sort()

    results['highs'] = []
    results['lows'] = []
    results['precipitation'] = []
    results['yields'] = []
    for year in keys:
        results['yields'].append(grain_yield[year])
        results['precipitation'].append(averages[year]['precipitation'])
        results['highs'].append(averages[year]['high'])
        results['lows'].append(averages[year]['low'])

    string_out = "High Correlation: {0}\n".format(format(base_class.pearson_def(results['highs'],
                                                                                results['yields']), '.2f'))
    string_out += "Low Correlation: {0}\n".format(format(base_class.pearson_def(results['lows'],
                                                                                results['yields']), '.2f'))
    string_out += "Precipitation Correlation: {0}\n".format(format(base_class.pearson_def(results['precipitation'],
                                                                                          results['yields']), '.2f'))
    output_file.write(string_out)

# Run all problems at once
base = Base()
base.run_problem(problem=problem_1)
base.run_problem(problem=problem_2)
base.run_problem(problem=problem_3)
base.run_problem(problem=problem_4)
