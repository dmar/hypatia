import unittest
from repoze.catalog.query import ast_support


class ComparatorTestBase(unittest.TestCase):
    def _makeOne(self, index_name, value):
        return self._getTargetClass()(index_name, value)


class TestQuery(unittest.TestCase):
    def _makeOne(self):
        from repoze.catalog.query import Query as cls
        return cls()

    def test_intersection(self):
        from repoze.catalog.query import Intersection
        a = self._makeOne()
        b = self._makeOne()
        result = a & b
        self.failUnless(isinstance(result, Intersection))
        self.assertEqual(result.arguments[0], a)
        self.assertEqual(result.arguments[1], b)

    def test_intersection_type_error(self):
        a = self._makeOne()
        self.assertRaises(TypeError, a.__and__, 2)

    def test_or(self):
        from repoze.catalog.query import Union
        a = self._makeOne()
        b = self._makeOne()
        result = a | b
        self.failUnless(isinstance(result, Union))
        self.assertEqual(result.arguments[0], a)
        self.assertEqual(result.arguments[1], b)

    def test_union_type_error(self):
        a = self._makeOne()
        self.assertRaises(TypeError, a.__or__, 2)

    def test_difference(self):
        from repoze.catalog.query import Difference
        a = self._makeOne()
        b = self._makeOne()
        result = a - b
        self.failUnless(isinstance(result, Difference))
        self.assertEqual(result.left, a)
        self.assertEqual(result.right, b)

    def test_difference_type_error(self):
        a = self._makeOne()
        self.assertRaises(TypeError, a.__sub__, 2)

    def test_iter_children(self):
        a = self._makeOne()
        self.assertEqual(a.iter_children(), ())

    def test_print_tree(self):
        from repoze.catalog.query import Query

        class Derived(Query):
            def __init__(self, name):
                self.name = name
                self.children = []

            def __str__(self):
                return self.name

            def iter_children(self):
                return self.children

        from StringIO import StringIO
        a = Derived('A')
        b = Derived('B')
        c = Derived('C')
        a.children.append(b)
        a.children.append(c)

        buf = StringIO()
        a.print_tree(buf)
        self.assertEqual(buf.getvalue(), 'A\n  B\n  C\n')


class TestComparator(ComparatorTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import Comparator
        return Comparator

    def test_ctor(self):
        inst = self._makeOne('index', 'val')
        self.assertEqual(inst.index_name, 'index')
        self.assertEqual(inst.value, 'val')

    def test_eq(self):
        inst = self._makeOne('index', 'val')
        self.assertEqual(inst, self._makeOne('index', 'val'))


class TestContains(ComparatorTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import Contains
        return Contains

    def test_apply(self):
        catalog = DummyCatalog()
        inst = self._makeOne('index', 'val')
        result = inst.apply(catalog)
        self.assertEqual(result, 'val')
        self.assertEqual(catalog.index.contains, 'val')

    def test_to_str(self):
        inst = self._makeOne('index', 'val')
        self.assertEqual(str(inst), "'val' in index")

    def test_negate(self):
        from repoze.catalog.query import DoesNotContain
        inst = self._makeOne('index', 'val')
        self.assertEqual(inst.negate(), DoesNotContain('index', 'val'))


class TestDoesNotContain(ComparatorTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import DoesNotContain
        return DoesNotContain

    def test_apply(self):
        catalog = DummyCatalog()
        inst = self._makeOne('index', 'val')
        result = inst.apply(catalog)
        self.assertEqual(result, 'val')
        self.assertEqual(catalog.index.does_not_contain, 'val')

    def test_to_str(self):
        inst = self._makeOne('index', 'val')
        self.assertEqual(str(inst), "'val' not in index")

    def test_negate(self):
        from repoze.catalog.query import Contains
        inst = self._makeOne('index', 'val')
        self.assertEqual(inst.negate(), Contains('index', 'val'))


class TestEq(ComparatorTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import Eq
        return Eq

    def test_apply(self):
        catalog = DummyCatalog()
        inst = self._makeOne('index', 'val')
        result = inst.apply(catalog)
        self.assertEqual(result, 'val')
        self.assertEqual(catalog.index.eq, 'val')

    def test_to_str(self):
        inst = self._makeOne('index', 'val')
        self.assertEqual(str(inst), "index == 'val'")

    def test_negate(self):
        from repoze.catalog.query import NotEq
        inst = self._makeOne('index', 'val')
        self.assertEqual(inst.negate(), NotEq('index', 'val'))

class TestNotEq(ComparatorTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import NotEq
        return NotEq

    def test_apply(self):
        catalog = DummyCatalog()
        inst = self._makeOne('index', 'val')
        result = inst.apply(catalog)
        self.assertEqual(result, 'val')
        self.assertEqual(catalog.index.not_eq, 'val')

    def test_to_str(self):
        inst = self._makeOne('index', 'val')
        self.assertEqual(str(inst), "index != 'val'")

    def test_negate(self):
        from repoze.catalog.query import Eq
        inst = self._makeOne('index', 'val')
        self.assertEqual(inst.negate(), Eq('index', 'val'))


class TestGt(ComparatorTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import Gt
        return Gt

    def test_apply(self):
        catalog = DummyCatalog()
        inst = self._makeOne('index', 'val')
        result = inst.apply(catalog)
        self.assertEqual(result, 'val')
        self.assertEqual(catalog.index.gt, 'val')

    def test_to_str(self):
        inst = self._makeOne('index', 'val')
        self.assertEqual(str(inst), "index > 'val'")

    def test_negate(self):
        from repoze.catalog.query import Le
        inst = self._makeOne('index', 'val')
        self.assertEqual(inst.negate(), Le('index', 'val'))


class TestLt(ComparatorTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import Lt
        return Lt

    def test_apply(self):
        catalog = DummyCatalog()
        inst = self._makeOne('index', 'val')
        result = inst.apply(catalog)
        self.assertEqual(result, 'val')
        self.assertEqual(catalog.index.lt, 'val')

    def test_to_str(self):
        inst = self._makeOne('index', 'val')
        self.assertEqual(str(inst), "index < 'val'")

    def test_negate(self):
        from repoze.catalog.query import Ge
        inst = self._makeOne('index', 'val')
        self.assertEqual(inst.negate(), Ge('index', 'val'))


class TestGe(ComparatorTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import Ge
        return Ge

    def test_apply(self):
        catalog = DummyCatalog()
        inst = self._makeOne('index', 'val')
        result = inst.apply(catalog)
        self.assertEqual(result, 'val')
        self.assertEqual(catalog.index.ge, 'val')

    def test_to_str(self):
        inst = self._makeOne('index', 'val')
        self.assertEqual(str(inst), "index >= 'val'")

    def test_negate(self):
        from repoze.catalog.query import Lt
        inst = self._makeOne('index', 'val')
        self.assertEqual(inst.negate(), Lt('index', 'val'))


class TestLe(ComparatorTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import Le
        return Le

    def test_apply(self):
        catalog = DummyCatalog()
        inst = self._makeOne('index', 'val')
        result = inst.apply(catalog)
        self.assertEqual(result, 'val')
        self.assertEqual(catalog.index.le, 'val')

    def test_to_str(self):
        inst = self._makeOne('index', 'val')
        self.assertEqual(str(inst), "index <= 'val'")

    def test_negate(self):
        from repoze.catalog.query import Gt
        inst = self._makeOne('index', 'val')
        self.assertEqual(inst.negate(), Gt('index', 'val'))


class TestAll(ComparatorTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import All
        return All

    def test_apply(self):
        catalog = DummyCatalog()
        inst = self._makeOne('index', 'val')
        result = inst.apply(catalog)
        self.assertEqual(result, 'val')
        self.assertEqual(catalog.index.all, 'val')

    def test_to_str(self):
        inst = self._makeOne('index', [1, 2, 3])
        self.assertEqual(str(inst), "index all [1, 2, 3]")

    def test_negate(self):
        from repoze.catalog.query import NotAll
        inst = self._makeOne('index', 'val')
        self.assertEqual(inst.negate(), NotAll('index', 'val'))


class TestNotAll(ComparatorTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import NotAll
        return NotAll

    def test_apply(self):
        catalog = DummyCatalog()
        inst = self._makeOne('index', 'val')
        result = inst.apply(catalog)
        self.assertEqual(result, 'val')
        self.assertEqual(catalog.index.all, 'val')

    def test_to_str(self):
        inst = self._makeOne('index', [1, 2, 3])
        self.assertEqual(str(inst), "index not all [1, 2, 3]")

    def test_negate(self):
        from repoze.catalog.query import All
        inst = self._makeOne('index', 'val')
        self.assertEqual(inst.negate(), All('index', 'val'))


class TestAny(ComparatorTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import Any
        return Any

    def test_apply(self):
        catalog = DummyCatalog()
        inst = self._makeOne('index', 'val')
        result = inst.apply(catalog)
        self.assertEqual(result, 'val')
        self.assertEqual(catalog.index.any, 'val')

    def test_to_str(self):
        inst = self._makeOne('index', [1, 2, 3])
        self.assertEqual(str(inst), "index any [1, 2, 3]")

    def test_negate(self):
        from repoze.catalog.query import NotAny
        inst = self._makeOne('index', 'val')
        self.assertEqual(inst.negate(), NotAny('index', 'val'))


class TestNotAny(ComparatorTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import NotAny
        return NotAny

    def test_apply(self):
        catalog = DummyCatalog()
        inst = self._makeOne('index', 'val')
        result = inst.apply(catalog)
        self.assertEqual(result, 'val')
        self.assertEqual(catalog.index.not_any, 'val')

    def test_to_str(self):
        inst = self._makeOne('index', [1, 2, 3])
        self.assertEqual(str(inst), "index not any [1, 2, 3]")

    def test_negate(self):
        from repoze.catalog.query import Any
        inst = self._makeOne('index', 'val')
        self.assertEqual(inst.negate(), Any('index', 'val'))


class TestRange(ComparatorTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import Range
        return Range

    def _makeOne(self, index, begin, end,
                 begin_exclusive=False, end_exclusive=False):
        return self._getTargetClass()(
            index, begin, end, begin_exclusive, end_exclusive)

    def test_apply(self):
        catalog = DummyCatalog()
        inst = self._makeOne('index', 'begin', 'end')
        result = inst.apply(catalog)
        self.assertEqual(result, ('begin', 'end', False, False))
        self.assertEqual(
            catalog.index.range, ('begin', 'end', False, False))

    def test_apply_exclusive(self):
        catalog = DummyCatalog()
        inst = self._makeOne('index', 'begin', 'end', True, True)
        result = inst.apply(catalog)
        self.assertEqual(result, ('begin', 'end', True, True))
        self.assertEqual(
            catalog.index.range, ('begin', 'end', True, True))

    def test_to_str(self):
        inst = self._makeOne('index', 0, 5)
        self.assertEqual(str(inst), "0 <= index <= 5")

    def test_to_str_exclusive(self):
        inst = self._makeOne('index', 0, 5, True, True)
        self.assertEqual(str(inst), "0 < index < 5")

    def test_from_gtlt(self):
        from repoze.catalog.query import Ge
        from repoze.catalog.query import Le
        gt = Ge('index', 0)
        lt = Le('index', 5)
        inst = self._getTargetClass().fromGTLT(gt, lt)
        self.assertEqual(str(inst), "0 <= index <= 5")

    def test_from_gtlt_exclusive(self):
        from repoze.catalog.query import Gt
        from repoze.catalog.query import Lt
        gt = Gt('index', 0)
        lt = Lt('index', 5)
        inst = self._getTargetClass().fromGTLT(gt, lt)
        self.assertEqual(str(inst), "0 < index < 5")


class SetOpTestBase(unittest.TestCase):
    def _makeOne(self, left, right):
        return self._getTargetClass()(left, right)


class TestSetOp(SetOpTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import SetOp as cls
        return cls

    def test_iter_children(self):
        class Dummy(object):
            pass
        left, right = Dummy(), Dummy()
        o = self._makeOne(left, right)
        self.assertEqual(list(o.iter_children()), [left, right])


class TestNarySetOp(SetOpTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import NarySetOp as cls
        return cls

    def test_iter_children(self):
        class Dummy(object):
            pass
        left, right = Dummy(), Dummy()
        o = self._makeOne(left, right)
        self.assertEqual(list(o.iter_children()), [left, right])


class TestUnion(SetOpTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import Union as cls
        return cls

    def test_to_str(self):
        o = self._makeOne(None, None)
        self.assertEqual(str(o), 'Union')

    def test_apply(self):
        left = DummyQuery(set([1, 2]))
        right = DummyQuery(set([3, 4]))
        o = self._makeOne(left, right)
        o.family = DummyFamily()
        self.assertEqual(o.apply(None), set([1, 2, 3, 4]))
        self.failUnless(left.applied)
        self.failUnless(right.applied)
        self.assertEqual(o.family.union, (left.results, right.results))

    def test_apply_left_empty(self):
        left = DummyQuery(set())
        right = DummyQuery(set([3, 4]))
        o = self._makeOne(left, right)
        o.family = DummyFamily()
        self.assertEqual(o.apply(None), set([3, 4]))
        self.failUnless(left.applied)
        self.failUnless(right.applied)
        self.assertEqual(o.family.union, None)

    def test_apply_right_empty(self):
        left = DummyQuery(set([1, 2]))
        right = DummyQuery(set())
        o = self._makeOne(left, right)
        o.family = DummyFamily()
        self.assertEqual(o.apply(None), set([1, 2]))
        self.failUnless(left.applied)
        self.failUnless(right.applied)
        self.assertEqual(o.family.union, None)


class TestIntersection(SetOpTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import Intersection as cls
        return cls

    def test_to_str(self):
        o = self._makeOne(None, None)
        self.assertEqual(str(o), 'Intersection')

    def test_apply(self):
        left = DummyQuery(set([1, 2, 3]))
        right = DummyQuery(set([3, 4, 5]))
        o = self._makeOne(left, right)
        o.family = DummyFamily()
        self.assertEqual(o.apply(None), set([3]))
        self.failUnless(left.applied)
        self.failUnless(right.applied)
        self.assertEqual(o.family.intersection, (left.results, right.results))

    def test_apply_left_empty(self):
        left = DummyQuery(set([]))
        right = DummyQuery(set([3, 4, 5]))
        o = self._makeOne(left, right)
        o.family = DummyFamily()
        self.assertEqual(o.apply(None), set())
        self.failUnless(left.applied)
        self.failIf(right.applied)
        self.assertEqual(o.family.intersection, None)

    def test_apply_right_empty(self):
        left = DummyQuery(set([1, 2, 3]))
        right = DummyQuery(set())
        o = self._makeOne(left, right)
        o.family = DummyFamily()
        self.assertEqual(o.apply(None), set())
        self.failUnless(left.applied)
        self.failUnless(right.applied)
        self.assertEqual(o.family.intersection, None)


class TestDifference(SetOpTestBase):
    def _getTargetClass(self):
        from repoze.catalog.query import Difference as cls
        return cls

    def test_to_str(self):
        o = self._makeOne(None, None)
        self.assertEqual(str(o), 'Difference')

    def test_apply(self):
        left = DummyQuery(set([1, 2, 3]))
        right = DummyQuery(set([3, 4, 5]))
        o = self._makeOne(left, right)
        o.family = DummyFamily()
        self.assertEqual(o.apply(None), set([1, 2]))
        self.failUnless(left.applied)
        self.failUnless(right.applied)
        self.assertEqual(o.family.diff, (left.results, right.results))

    def test_apply_left_empty(self):
        left = DummyQuery(set([]))
        right = DummyQuery(set([3, 4, 5]))
        o = self._makeOne(left, right)
        o.family = DummyFamily()
        self.assertEqual(o.apply(None), set())
        self.failUnless(left.applied)
        self.failIf(right.applied)
        self.assertEqual(o.family.diff, None)

    def test_right_empty(self):
        left = DummyQuery(set([1, 2, 3]))
        right = DummyQuery(set())
        o = self._makeOne(left, right)
        o.family = DummyFamily()
        self.assertEqual(o.apply(None), set([1, 2, 3]))
        self.failUnless(left.applied)
        self.failUnless(right.applied)
        self.assertEqual(o.family.diff, None)


class Test_parse_query(unittest.TestCase):
    def tearDown(self):
        from repoze.catalog import query
        query.ast_support = True

    def _call_fut(self, expr, names=None):
        from repoze.catalog.query import parse_query as fut
        return fut(expr, names)

    def test_not_an_expression(self):
        self.assertRaises(ValueError, self._call_fut, 'a = 1')

    def test_multiple_expressions(self):
        self.assertRaises(ValueError, self._call_fut, 'a == 1\nb == 2\n')

    def test_unhandled_operator(self):
        self.assertRaises(ValueError, self._call_fut, 'a ^ b')

    def test_non_string_index_name(self):
        # == is not commutative in this context, sorry.
        self.assertRaises(ValueError, self._call_fut, '1 == a')

    def test_bad_value_name(self):
        self.assertRaises(NameError, self._call_fut, 'a == b')

    def test_bad_operand_for_set_operation(self):
        self.assertRaises(ValueError, self._call_fut, '(a == 1) | 2')
        self.assertRaises(ValueError, self._call_fut, '1 | (b == 2)')

    def test_bad_operand_for_bool_operation(self):
        self.assertRaises(ValueError, self._call_fut, '1 or 2')

    def test_bad_comparator_chaining(self):
        self.assertRaises(ValueError, self._call_fut, '1 < 2 > 3')
        self.assertRaises(ValueError, self._call_fut, 'x == y == z')

    def test_bad_func_call(self):
        self.assertRaises(ValueError, self._call_fut, 'a in foo(bar)')

    def test_wrong_number_or_args_for_any(self):
        self.assertRaises(ValueError, self._call_fut, 'a in any(1, 2)')

    def test_no_ast_support(self):
        from repoze.catalog import query
        query.ast_support = False
        self.assertRaises(NotImplementedError, self._call_fut, None)

    def test_num(self):
        self.assertEqual(self._call_fut('1'), 1)
        self.assertEqual(self._call_fut('1.1'), 1.1)

    def test_str(self):
        self.assertEqual(self._call_fut('"foo"'), 'foo')

    def test_unicode(self):
        self.assertEqual(self._call_fut('u"foo"'), u'foo')

    def test_list(self):
        self.assertEqual(self._call_fut('[1, 2, 3]'), [1, 2, 3])

    def test_tuple(self):
        a, b, c = 1, 2, 3
        self.assertEqual(self._call_fut('(a, b, c)', locals()), (1, 2, 3))

    def test_dotted_name(self):
        self.assertEqual(self._call_fut('a.foo').id, 'a.foo')

    def test_dotted_names(self):
        self.assertEqual(self._call_fut('a.foo.bar').id, 'a.foo.bar')

    def test_eq(self):
        from repoze.catalog.query import Eq
        eq = self._call_fut('a.foo == 1')
        self.failUnless(isinstance(eq, Eq))
        self.assertEqual(eq.index_name, 'a.foo')
        self.assertEqual(eq.value, 1)

    def test_not_eq(self):
        from repoze.catalog.query import NotEq
        not_eq = self._call_fut("a != 'one'")
        self.failUnless(isinstance(not_eq, NotEq))
        self.assertEqual(not_eq.index_name, 'a')
        self.assertEqual(not_eq.value, "one")

    def test_lt(self):
        from repoze.catalog.query import Lt
        lt = self._call_fut("a < foo", dict(foo=6))
        self.failUnless(isinstance(lt, Lt))
        self.assertEqual(lt.index_name, 'a')
        self.assertEqual(lt.value, 6)

    def test_le(self):
        from repoze.catalog.query import Le
        le = self._call_fut("a <= 4")
        self.failUnless(isinstance(le, Le))
        self.assertEqual(le.index_name, 'a')
        self.assertEqual(le.value, 4)

    def test_gt(self):
        from repoze.catalog.query import Gt
        gt = self._call_fut('b > 2')
        self.failUnless(isinstance(gt, Gt))
        self.assertEqual(gt.index_name, 'b')
        self.assertEqual(gt.value, 2)

    def test_ge(self):
        from repoze.catalog.query import Ge
        ge = self._call_fut("a >= 5")
        self.failUnless(isinstance(ge, Ge))
        self.assertEqual(ge.index_name, 'a')
        self.assertEqual(ge.value, 5)

    def test_contains(self):
        from repoze.catalog.query import Contains
        contains = self._call_fut("6 in a")
        self.failUnless(isinstance(contains, Contains))
        self.assertEqual(contains.index_name, 'a')
        self.assertEqual(contains.value, 6)

##    def test_does_not_contain(self):
##        from repoze.catalog.query import DoesNotContain
##        contains = self._call_fut("6 not in a")
##        self.failUnless(isinstance(contains, DoesNotContain))
##        self.assertEqual(contains.index_name, 'a')
##        self.assertEqual(contains.value, 6)

    def test_range_exclusive_exclusive(self):
        from repoze.catalog.query import Range
        comp = self._call_fut("0 < a < 5")
        self.failUnless(isinstance(comp, Range))
        self.assertEqual(comp.index_name, 'a')
        self.assertEqual(comp.start, 0)
        self.assertEqual(comp.end, 5)
        self.failUnless(comp.start_exclusive)
        self.failUnless(comp.end_exclusive)

    def test_range_exclusive_inclusive(self):
        from repoze.catalog.query import Range
        comp = self._call_fut("0 < a <= 5")
        self.failUnless(isinstance(comp, Range))
        self.assertEqual(comp.index_name, 'a')
        self.assertEqual(comp.start, 0)
        self.assertEqual(comp.end, 5)
        self.failUnless(comp.start_exclusive)
        self.failIf(comp.end_exclusive)

    def test_range_inclusive_exclusive(self):
        from repoze.catalog.query import Range
        comp = self._call_fut("0 <= a < 5")
        self.failUnless(isinstance(comp, Range))
        self.assertEqual(comp.index_name, 'a')
        self.assertEqual(comp.start, 0)
        self.assertEqual(comp.end, 5)
        self.failIf(comp.start_exclusive)
        self.failUnless(comp.end_exclusive)

    def test_range_inclusive_inclusive(self):
        from repoze.catalog.query import Range
        comp = self._call_fut("0 <= a <= 5")
        self.failUnless(isinstance(comp, Range))
        self.assertEqual(comp.index_name, 'a')
        self.assertEqual(comp.start, 0)
        self.assertEqual(comp.end, 5)
        self.failIf(comp.start_exclusive)
        self.failIf(comp.end_exclusive)

    def test_union(self):
        from repoze.catalog.query import Eq
        from repoze.catalog.query import Union
        op = self._call_fut("(a == 1) | (b == 2)")
        self.failUnless(isinstance(op, Union))
        query = op.arguments[0]
        self.failUnless(isinstance(query, Eq))
        self.assertEqual(query.index_name, 'a')
        self.assertEqual(query.value, 1)
        query = op.arguments[1]
        self.failUnless(isinstance(query, Eq))
        self.assertEqual(query.index_name, 'b')
        self.assertEqual(query.value, 2)

    def test_union_with_bool_syntax(self):
        from repoze.catalog.query import Eq
        from repoze.catalog.query import Union
        op = self._call_fut("a == 1 or b == 2")
        self.failUnless(isinstance(op, Union))
        query = op.arguments[0]
        self.failUnless(isinstance(query, Eq))
        self.assertEqual(query.index_name, 'a')
        self.assertEqual(query.value, 1)
        query = op.arguments[1]
        self.failUnless(isinstance(query, Eq))
        self.assertEqual(query.index_name, 'b')
        self.assertEqual(query.value, 2)

    def test_any(self):
        from repoze.catalog.query import Any
        op = self._call_fut("a == 1 or a == 2 or a == 3")
        self.failUnless(isinstance(op, Any), op)
        self.assertEqual(op.index_name, 'a')
        self.assertEqual(op.value, [1, 2, 3])

    def test_better_any(self):
        from repoze.catalog.query import Any
        op = self._call_fut("a in any([1, 2, 3])")
        self.failUnless(isinstance(op, Any), op)
        self.assertEqual(op.index_name, 'a')
        self.assertEqual(op.value, [1, 2, 3])

##    def test_not_any(self):
##        from repoze.catalog.query import NotAny
##        op = self._call_fut("not(a == 1 or a == 2 or a == 3)")
##        self.failUnless(isinstance(op, NotAny), op)
##        self.assertEqual(op.index_name, 'a')
##        self.assertEqual(op.value, [1, 2, 3])
##
##    def test_better_not_any(self):
##        from repoze.catalog.query import NotAny
##        op = self._call_fut("a not in any([1, 2, 3])")
##        self.failUnless(isinstance(op, NotAny), op)
##        self.assertEqual(op.index_name, 'a')
##        self.assertEqual(op.value, [1, 2, 3])

    def test_intersection(self):
        from repoze.catalog.query import Eq
        from repoze.catalog.query import Intersection
        op = self._call_fut("(a == 1) & (b == 2)")
        self.failUnless(isinstance(op, Intersection))
        query = op.arguments[0]
        self.failUnless(isinstance(query, Eq))
        self.assertEqual(query.index_name, 'a')
        self.assertEqual(query.value, 1)
        query = op.arguments[1]
        self.failUnless(isinstance(query, Eq))
        self.assertEqual(query.index_name, 'b')
        self.assertEqual(query.value, 2)

    def test_intersection_with_bool_syntax(self):
        from repoze.catalog.query import Eq
        from repoze.catalog.query import Intersection
        op = self._call_fut("a == 1 and b == 2")
        self.failUnless(isinstance(op, Intersection))
        query = op.arguments[0]
        self.failUnless(isinstance(query, Eq))
        self.assertEqual(query.index_name, 'a')
        self.assertEqual(query.value, 1)
        query = op.arguments[1]
        self.failUnless(isinstance(query, Eq))
        self.assertEqual(query.index_name, 'b')
        self.assertEqual(query.value, 2)

    def test_all(self):
        from repoze.catalog.query import All
        op = self._call_fut("a == 1 and a == 2 and a == 3")
        self.failUnless(isinstance(op, All), op)
        self.assertEqual(op.index_name, 'a')
        self.assertEqual(op.value, [1, 2, 3])

    def test_better_all(self):
        from repoze.catalog.query import All
        op = self._call_fut("a in all([1, 2, 3])")
        self.failUnless(isinstance(op, All), op)
        self.assertEqual(op.index_name, 'a')
        self.assertEqual(op.value, [1, 2, 3])

    def test_all_with_union(self):
        # Regression test for earlier bug where:
        #   a == 1 or a == 2 and a == 3
        # was transformed into:
        #   a any [1, 2, 3]
        from repoze.catalog.query import All
        from repoze.catalog.query import Eq
        from repoze.catalog.query import Union
        op = self._call_fut("a == 1 or a == 2 and a == 3")
        self.failUnless(isinstance(op, Union))
        self.failUnless(isinstance(op.arguments[0], Eq))
        self.failUnless(isinstance(op.arguments[1], All))
        self.assertEqual(op.arguments[1].index_name, 'a')
        self.assertEqual(op.arguments[1].value, [2, 3])

    def test_difference(self):
        from repoze.catalog.query import Eq
        from repoze.catalog.query import Difference
        op = self._call_fut("(a == 1) - (b == 2)")
        self.failUnless(isinstance(op, Difference))
        query = op.left
        self.failUnless(isinstance(query, Eq))
        self.assertEqual(query.index_name, 'a')
        self.assertEqual(query.value, 1)
        query = op.right
        self.failUnless(isinstance(query, Eq))
        self.assertEqual(query.index_name, 'b')
        self.assertEqual(query.value, 2)

    def test_convert_gtlt_to_range(self):
        from repoze.catalog.query import Range
        op = self._call_fut("a < 1 and a > 0")
        self.failUnless(isinstance(op, Range))
        self.assertEqual(op.start, 0)
        self.assertEqual(op.end, 1)
        self.assertEqual(op.start_exclusive, True)
        self.assertEqual(op.end_exclusive, True)

    def test_convert_gtlt_child_left_nephew_left(self):
        from repoze.catalog.query import Eq
        from repoze.catalog.query import Intersection
        from repoze.catalog.query import Range
        op = self._call_fut("a > 0 and (a < 5 and b == 7)")
        self.failUnless(isinstance(op, Intersection))
        self.failUnless(isinstance(op.arguments[0], Range))
        self.failUnless(isinstance(op.arguments[1], Eq))

    def test_strange_gtlt_child_left_nephew_right(self):
        from repoze.catalog.query import Eq
        from repoze.catalog.query import Intersection
        from repoze.catalog.query import Range
        op = self._call_fut("a > 0 and (b == 7 and a < 5)")
        self.failUnless(isinstance(op, Intersection))
        self.failUnless(isinstance(op.arguments[0], Range))
        self.failUnless(isinstance(op.arguments[1], Eq))

    def test_convert_gtlt_child_right_nephew_left(self):
        from repoze.catalog.query import Eq
        from repoze.catalog.query import Gt
        from repoze.catalog.query import Intersection
        from repoze.catalog.query import Range
        op = self._call_fut("a >= -1 and b == 2 and c > 3 and a <= 1")
        self.failUnless(isinstance(op, Intersection))
        self.failUnless(isinstance(op.arguments[0], Range))
        self.failUnless(isinstance(op.arguments[1], Eq))
        self.failUnless(isinstance(op.arguments[2], Gt))

    def test_convert_gtlt_both_descendants(self):
        from repoze.catalog.query import Eq
        from repoze.catalog.query import Gt
        from repoze.catalog.query import Intersection
        from repoze.catalog.query import Range
        op = self._call_fut("b == 2 and a > -1 and (a <= 1 and c > 3)")
        self.failUnless(isinstance(op, Intersection))
        self.failUnless(isinstance(op.arguments[0], Eq))
        self.failUnless(isinstance(op.arguments[1], Range))
        self.failUnless(isinstance(op.arguments[2], Gt))

    def test_convert_gtlt_both_descendants_multiple_times(self):
        from repoze.catalog.query import Intersection
        from repoze.catalog.query import Range
        op = self._call_fut(
            "(a > 0 and b > 0 and c > 0) and (a < 5 and b < 5 and c < 5)")
        self.failUnless(isinstance(op, Intersection))
        self.failUnless(isinstance(op.arguments[0], Range))
        self.failUnless(isinstance(op.arguments[1], Range))
        self.failUnless(isinstance(op.arguments[2], Range))

    def test_dont_convert_gtlt_to_range_with_or(self):
        from repoze.catalog.query import Gt
        from repoze.catalog.query import Lt
        from repoze.catalog.query import Union
        op = self._call_fut("a > 0 or a < 5")
        self.failUnless(isinstance(op, Union))
        self.failUnless(isinstance(op.arguments[0], Gt))
        self.failUnless(isinstance(op.arguments[1], Lt))

    def test_dont_convert_gtlt_to_range_with_or_spread_out(self):
        from repoze.catalog.query import Gt
        from repoze.catalog.query import Lt
        from repoze.catalog.query import Intersection
        from repoze.catalog.query import Union
        op = self._call_fut("a > 0 and b > 0 or a < 5 and b < 5")
        self.failUnless(isinstance(op, Union))
        self.failUnless(isinstance(op.arguments[0], Intersection))
        self.failUnless(isinstance(op.arguments[0].arguments[0], Gt))
        self.failUnless(isinstance(op.arguments[0].arguments[1], Gt))
        self.failUnless(isinstance(op.arguments[1], Intersection))
        self.failUnless(isinstance(op.arguments[1].arguments[0], Lt))
        self.failUnless(isinstance(op.arguments[1].arguments[1], Lt))


if not ast_support:  # pragma NO COVERAGE
    del Test_parse_query


class Dummy(object):
    __parent__ = None


class DummyCatalog(object):
    def __init__(self, index=None):
        if index is None:
            index = DummyIndex()
        self.index = index

    def __getitem__(self, name):
        return self.index


class DummyIndex(object):

    def applyContains(self, value):
        self.contains = value
        return value

    def applyDoesNotContain(self, value):
        self.does_not_contain = value
        return value

    def applyEq(self, value):
        self.eq = value
        return value

    def applyNotEq(self, value):
        self.not_eq = value
        return value

    def applyGt(self, value):
        self.gt = value
        return value

    def applyLt(self, value):
        self.lt = value
        return value

    def applyGe(self, value):
        self.ge = value
        return value

    def applyLe(self, value):
        self.le = value
        return value

    def applyAny(self, value):
        self.any = value
        return value

    def applyNotAny(self, value):
        self.not_any = value
        return value

    def applyAll(self, value):
        self.all = value
        return value

    def applyRange(self, start, end, start_exclusive, end_exclusive):
        self.range = (start, end, start_exclusive, end_exclusive)
        return self.range


class DummyFamily(object):
    union = None
    intersection = None
    diff = None

    @property
    def IF(self):
        return self

    def weightedUnion(self, left, right):
        self.union = (left, right)
        return None, left | right

    def weightedIntersection(self, left, right):
        self.intersection = (left, right)
        return None, left & right

    def difference(self, left, right):
        self.diff = (left, right)
        return left - right

    def Set(self):
        return set()


class DummyQuery(object):
    applied = False

    def __init__(self, results):
        self.results = results

    def apply(self, catalog):
        self.applied = True
        return self.results
