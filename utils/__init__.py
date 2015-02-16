"""Collection of utilities to do some input file manipulation and output file scraping"""
import re
class InputManipulator(object):
    """ Class to modify the input file string passed in.
    """
    @classmethod
    def modify_impervious_cover(cls, input_file, modifications = None):
        """ Method to modify the impervious cover amount based on an input dictionary
        :param input_file: SWMM inp file as a string
        :param modifications: Dictionary of subcatchment_name and impervious percentage
        :return modified inp file as a string:
        """

        # Some sanity checks
        # Modifications have to specified as a dictionary lets raise an exception here
        if not isinstance(modifications, dict):
            raise TypeError('Modifications need to be specified as a dict of {subcatchment_name: percent}')
        line_ending = cls.determine_line_ending(InputManipulator(), input_file)
        if not line_ending:
            raise Exception('Could not determine line ending')

        # Setup some pieces we will need

        subcatchment_block_header = '[SUBCATCHMENTS]'

        subcatchment_block, block_start, block_end = cls.find_block(InputManipulator(), input_file, subcatchment_block_header)
        # Parse the lines in this block
        subcatchment_block_lines = [
                {
                    # The raw line as read from the file
                    'line': this_line,
                    # Parse the subcatchment name
                    'subcatchment_name': this_line.split()[0] if this_line and ';' not in this_line else None
                }
            for this_line in subcatchment_block.splitlines()
        ]

        # Make all the requested modifications
        for this_raw_line in subcatchment_block_lines:
            # If this line is a subcatchment and it is one we want to modify
            if this_raw_line['subcatchment_name'] and this_raw_line['subcatchment_name'] in modifications:
                # The do it!
                this_raw_line['line'] = cls.modify_impervious_percentage(InputManipulator(), modifications[this_raw_line['subcatchment_name']], this_raw_line['line'])
        # Rebuild the string using the correct line ending
        subcatchment_block = line_ending.join([this_raw_line['line'] for this_raw_line in subcatchment_block_lines])

        # Return the full input file string
        return input_file.replace(input_file[block_start:block_end], subcatchment_block)

    @classmethod
    def get_LID_controls(cls, input_file, return_json = True):

        LID_controls_block_header = '[LID_CONTROLS]'
        LID_block, block_start, block_end = cls.find_block(InputManipulator(), input_file, LID_controls_block_header)
        LID_block = LID_block.splitlines()
        LID_structures = set()
        for this_line in LID_block:
            if ';' not in this_line and this_line.split():
                LID_structures.add(this_line.split()[0])
        if return_json:
            import json
            output = json.dumps(list(LID_structures))
            return output
        else:
            return LID_structures

    @classmethod
    def get_LID_usage(cls, input_file, return_json = True):

        LID_usage_block_header = '[LID_USAGE]'
        LID_block, block_start, block_end = cls.find_block(InputManipulator(), input_file,
                                                           LID_usage_block_header)
        LID_block = LID_block.splitlines()
        LID_structures = []
        LID_HEADER = ['Subcatchment', 'LID Process', 'Number', 'Area', 'Width', 'InitSatur', 'FromImprv', 'ToPerv']
        for this_line in LID_block:
            if ';' not in this_line and this_line.split():
                LID_structures.append(dict(zip(LID_HEADER,this_line.split())))
        if return_json:
            import json
            output = json.dumps(list(LID_structures))
            return output
        else:
            return LID_structures

    @classmethod
    def set_LID_usage(cls, input_file, LID_usage):
        """ This method takes the LID_usage array specified and replaces the existing block with it.
        :param input_file: input file string
        :param LID_usage: list of dictionaries defining LID usages
        :return: full input file with the block replaced
        """

        line_ending = cls.determine_line_ending(InputManipulator(), input_file)
        if not line_ending:
            raise Exception('Could not determine line ending')

        LID_usage_block_header = '[LID_USAGE]'
        LID_block, block_start, block_end = cls.find_block(InputManipulator(), input_file,
                                                           LID_usage_block_header)
        LID_block = LID_block.splitlines()
        LID_HEADER = ['Subcatchment', 'LID Process', 'Number', 'Area', 'Width', 'InitSatur', 'FromImprv', 'ToPerv']
        avail_lid_controls = InputManipulator().get_LID_controls(input_file, return_json=False)
        output_lid_block = []

        # Grab the first two lines
        for this_line in LID_block:
            if ';' in this_line or not this_line.split():
                output_lid_block.append(this_line)
            else:
                break
        for this_LID_usage in LID_usage:
            if this_LID_usage['LID Process'] in avail_lid_controls:
                output_lid_block.append('\t'.join([this_LID_usage[this_key] for this_key in LID_HEADER]))
            else:
                error_message = 'The LID Process specified {0} is not defined in this inp. Defined list {1}'
                raise ValueError(error_message.format(this_LID_usage['LID Process'], avail_lid_controls))

        lid_usage_block = line_ending.join(output_lid_block)

        return input_file.replace(input_file[block_start:block_end], lid_usage_block)


    # TODO Consider making a set of NEW LID, Modify LID, Delete LID methods

    def find_block(self, input_file, block_header):
        """
        Generic method for finding blocks within a SWMM input file.
        :param input_file: str of the input file
        :param block_header: the block header to find
        :return: the_block(str), block_start(int), block_end(int)
        """
        # RE search for all block headers ie [HEADER]
        block_headers = re.finditer('(\[.*\])', input_file)
        # The start of the block we want to replace
        block_start = None
        # The end of the block we want to replace
        block_end = None
        if not block_headers:
            raise Exception('Block Headers not found file might be malformed')

        # Loop through the blocks and find the beginning and end of the block
        for this_match in block_headers:
            this_line = this_match.group()
            # Look for the subcatchment block
            if block_header in this_line:
                block_start = this_match.end()
                continue
            # If we have already found the start then
            if block_start is not None:
                # The next block is the end! but we want to keep the last carriage return
                block_end = this_match.start() - 1
                break
        # If we didn't find the subcatchment block time to die
        if not block_start and not block_end:
            raise Exception('No {} block found'.format(block_header))

        # To make the parsing easier lets focus on just this section of the string
        this_block = input_file[block_start:block_end]

        return this_block, block_start, block_end

    def modify_impervious_percentage(self, percent, line):
        """ Modify the subcatchments line with the new percentage
        :param percent: Percentage to replace with
        :param line: Raw line read from file
        :return modfied line:
        """
        # Split over white space
        temp_line = line.split()
        # Modify the 5th entry which is the percentage of impervious cover
        temp_line[4] = str(percent)
        # Formatting is hard so just tab separate for now....
        return '\t'.join(temp_line)

    def determine_line_ending(self, input_file):
        """ Potentially different line endings can be used depending on system
        :param input_file: input file string
        :return: line ending found
        """
        line_ending = None
        if re.search('\r\n$', input_file):
            line_ending = '\r\n'
        elif re.search('\n$', input_file):
            line_ending = '\n'
        elif re.search('\r$', input_file):
            line_ending = '\r'
        return line_ending

class RPTOutputReader(object):
    """ Class to read the rtp file output from SWMM and extract the runoff summary information and return that as a JSON
    """

    @classmethod
    def extract_subcatchment_summary_data(cls, output_file):
        """
        :param output_file: String of RTP output file
        :return: JSON string of parsed Subcatchment Summary area
        """
        # Break the file up by lines and turn it into an iterator
        lines = iter(output_file.splitlines())
        # Variable to track when the top of the block is found based on its name
        block_found = False

        # Where to store the data we plan to dump
        output_data = []

        # These are the fields that are found in this block
        HEADERS = [
            'Subcatchment',
            'Total Precip In',
            'Total Runon In',
            'Total Evap In',
            'Total Infill In',
            'Total Runoff In',
            'Total Runoff 10^6 gal',
            'Peak Runoff CPS',
            'Runoff Coeff'
        ]

        # Parse the file
        while True:
            # Grab the next line
            try:
                this_line = lines.next()
            except:
                break
            # If we found the block header sweet!
            if 'Subcatchment Runoff Summary' in this_line:
                block_found = True
                # Seek ahead 8 lines in the file to get to the actual data
                for i in range(8):
                    this_line = lines.next()
            # Lets handle the block of meaty data goodness
            if block_found:
                # This is a is the key that we have found the next block
                if '******************' in this_line:
                    break
                # Break the line up over whitespace
                this_line_list = this_line.split()
                # If the line is just a return move on
                if len(this_line_list) == 0:
                    continue
                # Lets parse the list we have the 0th element is the subcatchment name the rest are floats
                this_line_list = [this_line_list[0]] + map(float, this_line_list[1:])
                output_data.append(dict(zip(HEADERS, this_line_list)))
        # When we are finished json dumps the result
        import json
        return json.dumps(output_data)

# For convenience the class methods are defined into static functions

# Input file manipulation

# Modify the impervious cover for any subcatchment
modify_impervious_cover = InputManipulator().modify_impervious_cover

# Collect of tools for getting and setting LID features
get_LID_controls = InputManipulator().get_LID_controls
get_LID_usage = InputManipulator().get_LID_usage
set_LID_usage = InputManipulator().set_LID_usage

# Output file manipulation
extract_subcatchment_summary_data = RPTOutputReader().extract_subcatchment_summary_data

