import unittest
import argp


class ArgpTests(unittest.TestCase):
    def test_sub(self):
        argp.init()
        did_run = []

        def f1(args):
            did_run.append("f1")

        def f2(args):
            did_run.append("f2")

        s = argp.sub("sub1", f1)
        s2 = argp.sub("sub2", f2)
        argp.parse_list([])
        self.assertEqual(did_run, [])
        argp.parse_list(["sub1"])
        self.assertEqual(did_run, ["f1"])
        argp.parse_list(["sub1"])
        self.assertEqual(did_run, ["f1", "f1"])

        s2.arg("one", action="store_true")


if __name__ == '__main__':
    unittest.main()
