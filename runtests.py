import unittest
import test.all_tests

testSuite = test.all_tests.create_test_suite()
textRunner = unittest.TextTestRunner().run(testSuite)
