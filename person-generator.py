import csv
import sys
import requests
from tkinter import *
from adresses import generate_addresses
from option_lists import states, topics, full_states


def read_address_input(filename):
    with open(filename, "r") as infile:
        csv_reader = csv.DictReader(infile)
        # Read the input csv into an iterable of dicts and get
        # values for the first (and should be only) row
        row = csv_reader.__next__()
        state = row["input_state"]
        number = int(row["input_number_to_generate"])
    return state, number


def write_address_output(filename, addresses):
    with open(filename, "w", newline="") as outfile:
        fieldnames = ["input_state", "input_number_to_generate",
                      "output_content_type", "output_content_value"]
        csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        csv_writer.writeheader()
        for row in addresses:
            csv_writer.writerow(row)


def gen_addresses(state_var, number_to_gen, window):
    state = state_var.get().lower()
    number = int(number_to_gen.get())
    addresses = generate_addresses(state, number)
    text = Text(master=window)
    text.grid(row=5, column=1)
    text.insert(END, "INPUT_STATE,INPUT_NUMBER_TO_GENERATE," +
                "OUTPUT_CONTENT_TYPE,OUTPUT_CONTENT_VALUE")
    for address in addresses:
        text.insert(END, "\n" + address["input_state"] + "," +
                    str(address["input_number_to_generate"]) + "," +
                    address["output_content_type"] + "," +
                    address["output_content_value"])

    write_address_output("output.csv", addresses)


def get_content(state, topic):
    # Calls Malcolm Jeffers Content Generator microservice
    # running on local host to get a paragraph back about the
    # state and topic the user chose.
    url = "http://127.0.0.1:5001/get"
    params = {"pri": full_states[state], "sec": topic}
    request = requests.get(url, params=params)
    return request.json()["wiki"]


def gen_content(state_var, content_var, window):
    state = state_var.get().lower()
    topic = content_var.get().lower()
    content = get_content(state, topic)
    text = Text(master=window)
    text.grid(row=5, column=1)
    text.insert(END, content)


def config_window():
    # New function to split up run_gui()
    window = Tk()
    window.title("Person Generator")
    window.rowconfigure([0, 1, 2, 3, 4, 5], minsize=50, weight=1)
    window.columnconfigure([0, 1], minsize=50, weight=1)
    return window


def add_labels():
    # New function to split up run_gui()
    Label(text="Person Generator - Addresses").grid(row=0, column=0,
                                                    sticky="nw")
    Label(text="State:").grid(row=1, column=0, sticky="e")
    Label(text="Number to Generate:").grid(row=2, column=0, sticky="e")
    Label(text="Content Topic:").grid(row=3, column=0, sticky="e")


def add_selects(window, state_var, content_var):
    # New function to split up run_gui()
    # Adapted from https://stackoverflow.com/questions/45441885/
    #              how-can-i-create-a-dropdown-menu-from-a-list-in-tkinter
    state_options = OptionMenu(window, state_var, *states)
    state_options.grid(row=1, column=1, sticky="w")
    content_options = OptionMenu(window, content_var, *topics)
    content_options.grid(row=3, column=1, sticky="w")


def add_number_entry():
    # New function to split up run_gui()
    number_to_gen = Entry()
    number_to_gen.grid(row=2, column=1, sticky="w")
    return number_to_gen


def add_address_button(window, state_var, number_to_gen):
    # New function to split up run_gui()
    # Split this line after 79 chars
    generate_address = Button(master=window, text="Generate Addresses",
                              command=lambda: gen_addresses(state_var,
                                                            number_to_gen,
                                                            window))
    generate_address.grid(row=4, column=0, sticky="e")


def add_content_button(window, state_var, content_var):
    # New function to split up run_gui()
    # Split this line after 79 chars
    generate_content = Button(master=window, text="Generate Content",
                              command=lambda: gen_content(state_var,
                                                          content_var,
                                                          window))
    generate_content.grid(row=4, column=1, sticky="w")


def build_gui(window):
    # New functions to split up run_gui()
    add_labels()
    state_var = StringVar(window)
    content_var = StringVar(window)
    add_selects(window, state_var, content_var)
    number_to_gen = add_number_entry()
    add_address_button(window, state_var, number_to_gen)
    add_content_button(window, state_var, content_var)


def run_gui():
    # Took a lot of jobs of run_gui() into build_gui()
    window = config_window()
    build_gui(window)
    window.mainloop()


def main():
    if len(sys.argv) == 2:
        # If an input csv was given, run everything from the command line
        state, number = read_address_input(sys.argv[1])
        addresses = generate_addresses(state, number)
        write_address_output('output.csv', addresses)
        print("Addresses written to output.csv")
    else:
        run_gui()


if __name__ == '__main__':
    main()
