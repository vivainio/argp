import argparse
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

    def test_with_own_parser(self):
        p = argparse.ArgumentParser()
        argp.init(p)
        called = [False]

        def f(args):
            called[0] = True

        argp.sub("sub1", f)
        parsed = p.parse_args(["sub1"])
        argp.dispatch_parsed(parsed)
        self.assertTrue(called[0])

    def test_nest_deep(self):
        called = [False, False]
        parser = argp.init()
        def f(args):
            called[0] = True
        def f2(args):
            called[1] = True

        s = argp.group("group", help="Group with other commands")
        s.sub("hello", f)
        s.sub("world", f2)
        argp.parse_list(["group", "hello"])
        argp.parse_list(["group", "world"])

        assert called == [True, True]
        help = parser.format_help()
        assert "Group with other commands" in help


if __name__ == "__main__":
    unittest.main()
