
from __future__ import print_function

import os
import sys
import re

from model_test_helper import ModelTestHelper
from test_basic_run import tests

class TestBitReproducibility(ModelTestHelper):

    def __init__(self):
        super(TestBitReproducibility, self).__init__()

    def checksums_to_dict(self, filename):
        """
        Look at each line an make a dictionary entry.
        """

        regex = re.compile(r'\[chksum\]\s+(.*)\s+(-?[0-9]+)$')

        dict = {}
        with open(filename) as f:
            for line in f:
                m = regex.match(line)
                if m is not None:
                    dict[m.group(1).rstrip()] = int(m.group(2))

        return dict


    def expected_checksums(self, test_name):

        filename = os.path.join(self.my_path, 'checksums',
                                '{}.txt'.format(test_name))
        return self.checksums_to_dict(filename)


    def produced_checksums(self, test_name):
        """
        Extract checksums from model run output.
        """

        paths = self.make_paths(test_name)
        return self.checksums_to_dict(paths['stdout'])


    def check_run(self, key):

        # Compare expected to produced.
        expected = self.expected_checksums(key)
        produced = self.produced_checksums(key)

        for k in expected:
            assert(produced.has_key(k))
            if expected[k] != produced[k]:
                print('{}: expected {}, produced {}'.format(key, expected[k],
                                                            produced[k]))
            assert(expected[k] == produced[k])

    def test_checksums(self):
        for k in tests.keys():
            yield self.check_run, k


