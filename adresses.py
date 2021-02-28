import csv
import random


def read_state_data(state):
    # Read the state data and return it as a list of dicts
    data_list = []
    with open("./archive/" + state.lower() + ".csv", "r",
              encoding="utf-8") as infile:
        csv_reader = csv.DictReader(infile)
        # Only get up to the first 1mil rows - more than that and it's too slow
        for i in range(1000000):
            try:
                data_list.append(csv_reader.__next__())
            except StopIteration:
                break
    return data_list


def format_address(row, state):
    # Given a row of state data, return a single string that
    # is the full address
    address_strings = [row["NUMBER"].strip(), " ",
                       row["STREET"].strip(), " ",
                       row["UNIT"].strip(), " ",
                       row["CITY"].strip(), ", ",
                       state.upper().strip(), " ",
                       row["POSTCODE"].strip()]
    return "".join(address_strings).replace("  ", " ")


def select_addresses(state_data, state, number_to_generate):
    # Takes a list of state data dicts and returns a selection of
    # random addresses up to the given number as dicts
    addresses = []
    hash_list = []
    while len(hash_list) != number_to_generate:
        random_index = random.randrange(0, len(state_data))
        # Make sure this address hasn't been selected before
        if state_data[random_index]['HASH'] not in hash_list:
            # Make sure this address has street data
            if (state_data[random_index]['STREET'] and
                    state_data[random_index]['STREET'] != 'N/A'):
                hash_list.append(state_data[random_index]['HASH'])
                addresses.append({"input_state": state,
                                  "input_number_to_generate":
                                      number_to_generate,
                                  "output_content_type": "street address",
                                  "output_content_value":
                                      format_address(state_data[random_index],
                                                     state)})
    return addresses


def generate_addresses(state, number_to_generate):
    data = read_state_data(state)
    addresses = select_addresses(data, state, number_to_generate)
    return addresses
