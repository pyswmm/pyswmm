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
        line_ending = cls.determine_line_ending(input_file)
        if not line_ending:
            raise Exception('Could not determine line ending')

        # Setup some pieces we will need

        # RE search for all block headers ie [HEADER]
        block_headers = re.finditer('(\[.*\])', input_file)
        # The start of the block we want to replace
        block_start = None
        # The end of the block we want to replace
        block_end = None
        # The header we want to search for in this method
        subcatchment_block_header = '[SUBCATCHMENTS]'

        if not block_headers:
            raise Exception('Block Headers not found file might be malformed')

        # Loop through the blocks and find the beginning and end of the subcatchments block
        for this_match in block_headers:
            this_line = this_match.group()
            # Look for the subcatchment block
            if subcatchment_block_header in this_line:
                block_start = this_match.end()
                continue
            # If we have already found the start then
            if block_start is not None:
                # The next block is the end! but we want to keep the last carriage return
                block_end = this_match.start() - 1
                break
        # If we didn't find the subcatchment block time to die
        if not block_start and not block_end:
            raise Exception('No SUBCATCHMENTS block found')

        # To make the parsing easier lets focus on just this section of the string
        subcatchment_block = input_file[block_start:block_end]
        # Parse the lines in this block
        subcatchment_block_lines = [
                {
                    # The raw line as read from the file
                    'line': this_line,
                    # Parse the subcatchment name
                    'subcatchment_name': this_line.split()[0] if this_line and ';;' not in this_line else None
                }
            for this_line in subcatchment_block.splitlines()
        ]

        # Make all the requested modifications
        for this_raw_line in subcatchment_block_lines:
            # If this line is a subcatchment and it is one we want to modify
            if this_raw_line['subcatchment_name'] and this_raw_line['subcatchment_name'] in modifications:
                # The do it!
                this_raw_line['line'] = cls.modify_percentage(modifications[this_raw_line['subcatchment_name']], this_raw_line['line'])
        # Rebuild the string using the correct line ending
        subcatchment_block = line_ending.join([this_raw_line['line'] for this_raw_line in subcatchment_block_lines])

        # Return the full input file string
        return input_file.replace(input_file[block_start:block_end], subcatchment_block)

    @classmethod
    def modify_percentage(self, percent, line):
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

    @classmethod
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
        :param output_file: String out RTP output file
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