#!/usr/bin/env python
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
import json
import os
import sys


class HotelInformation:  # filter hotel details based on number of stars
    def __init__(self):
        pass

    def parse_json_file(self, input_file, output_file, target_id):  # get key, value pair from json file
        # open json file
        try:
            f = open(input_file)
        except:
            sys.exit("Failed to open " + input_file)
        try:
            # returns JSON object as a dictionary
            json_tree = json.load(f)
            for element in json_tree:  # extract key, value
                for key, value in element.items():
                    for i in value:
                        if i.values()[1] == int(target_id):  # select if number if stars matches
                            name = "name: " + i.values()[0]  # name of hotel
                            stars = "stars: " + str(target_id)  # number of stars
                            destination = "destination: " + key.capitalize()  # capitalize first letter of destination
                            self.output_template(output_file, name, stars, destination)  # make output template
        except:
            sys.exit("Failed to parse " + input_file)

    @staticmethod
    def output_template(output_file, name, stars, destination):  # template of output file
        template = """

        { \n""" + "\t\t\t" + name + """
        """ + "\t" + stars + """
        """ + "\t" + destination + "\n\t\t},"
        try:
            file_object = open(output_file, 'a')
            file_object.write(template)  # append hotel details
        except:
            sys.exit("Failed to write hotel details in " + output_file)

    @staticmethod
    def maintain_structure(output_file):  # start and end of the output file
        try:
            with open(output_file, 'rb+') as file:
                file.seek(0, 2)  # end of file
                size = file.tell()  # the size
                file.truncate(size - 1)  # remove last character from file (,)
                content = file.read()
                file.seek(0)
                file.write("[" + content)  # add starting bracket
            file_object = open(output_file, 'a')
            file_object.write('\n]')  # add ending bracket
            file_object.close()
        except:
            sys.exit("Failed to write hotel details in " + output_file)


if __name__ == '__main__':
    hotel_object = HotelInformation()  # object

    input_file_name = "hotels_detail.json"
    output_file_name = "output.txt"

    # pass number od stars as an argument to script
    parser = ArgumentParser(description="""
        Filter hotel information based on the number of stars.

        (1) to filter hotel details based on number of stars: e.g., ./hotel_information.py --stars 3
        """, formatter_class=RawTextHelpFormatter)

    mandatory_arguments = parser.add_argument_group('Mandatory arguments')
    mandatory_arguments.add_argument('--stars', metavar='3', help='stars', type=str, required=True)
    args = parser.parse_args()

    try:
        if os.path.exists(output_file_name):
            os.remove(output_file_name)  # remove existing file
    except:
        sys.exit("Something wrong with " + output_file_name)

    try:
        hotel_object.parse_json_file(input_file_name, output_file_name, args.stars)
        hotel_object.maintain_structure(output_file_name)
        print args.stars + " star hotel details filtered successfully !"
    except:
        sys.exit("Failed to find " + args.stars + " star hotels from " + input_file_name + "file")