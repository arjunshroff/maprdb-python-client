#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()
from builtins import *
from ojai.types.ODate import ODate
from ojai.types.OTime import OTime
from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from mapr.ojai.ojai_query.OJAIQueryCondition import OJAIQueryCondition
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory
from test.test_utils.constants import CONNECTION_STR, CONNECTION_OPTIONS

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class FindByIdTest(unittest.TestCase):

    def test_find_by_id(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)

        if connection.is_store_exists(store_path='/find-by-id-test-store1'):
            document_store = connection.get_store(store_path='/find-by-id-test-store1')
        else:
            document_store = connection.create_store(store_path='/find-by-id-test-store1')
        document = connection.new_document(dictionary={'_id': 'id008',
                                                       'test_int': 51,
                                                       'test_str': 'strstr',
                                                       'test_dict': {'test_int': 5},
                                                       'test_list': [5, 6],
                                                       'test_null': None,
                                                       'test_otime': OTime(timestamp=1518689532)})

        document_store.insert_or_replace(doc=document)

        self.assertTrue(connection.is_store_exists('/find-by-id-test-store1'))
        doc = document_store.find_by_id('id008')

        self.assertEqual(doc, document.as_dictionary())

    def test_insert_find_large_doc(self):
        document = OJAIDocument().set_id("121212") \
            .set('test_int', 123) \
            .set('first.test_int', 1235) \
            .set('first.test_long', 123456789) \
            .set('first.test_time', OTime(timestamp=1518689532)) \
            .set('first.test_date', ODate(days_since_epoch=3456)) \
            .set('first.test_bool', True) \
            .set('first.test_bool_false', False) \
            .set('first.test_invalid', ODate(days_since_epoch=3457)) \
            .set('first.test_str', 'strstr') \
            .set('first.test_dict', {'a': 1, 'b': 2}) \
            .set('first.test_dict2', {}) \
            .set('first.test_list', [1, 2, 'str', False, ODate(days_since_epoch=3457)]) \

        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)

        if connection.is_store_exists(store_path='/find-by-id-test-store1'):
            document_store = connection.get_store(store_path='/find-by-id-test-store1')
        else:
            document_store = connection.create_store(store_path='/find-by-id-test-store1')

        document_store.insert_or_replace(doc=document)

        self.assertTrue(connection.is_store_exists('/find-by-id-test-store1'))
        doc = document_store.find_by_id('121212', results_as_document=True)

        self.assertEqual(doc.as_json_str(), '{"_id": "121212", "test_int": {"$numberLong": 123}, "first": {'
                                            '"test_invalid": {"$dateDay": "1979-06-20"}, "test_time": {"$time": '
                                            '"12:12:12"}, "test_bool_false": false, "test_list": [{"$numberLong": 1}, '
                                            '{"$numberLong": 2}, "str", false, {"$dateDay": "1979-06-20"}], '
                                            '"test_long": {"$numberLong": 123456789}, "test_dict2": {}, "test_dict": '
                                            '{"a": {"$numberLong": 1}, "b": {"$numberLong": 2}}, "test_bool": true, '
                                            '"test_date": {"$dateDay": "1979-06-19"}, "test_str": "strstr", '
                                            '"test_int": {"$numberLong": 1235}}}')
        self.assertEqual(doc.as_dictionary(), document.as_dictionary())

    def test_find_by_id_as_dict(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)

        if connection.is_store_exists(store_path='/find-by-id-test-store1'):
            document_store = connection.get_store(store_path='/find-by-id-test-store1')
        else:
            document_store = connection.create_store(store_path='/find-by-id-test-store1')

        self.assertTrue(connection.is_store_exists('/find-by-id-test-store1'))
        doc = document_store.find_by_id('121212')

        document = OJAIDocument().set_id("121212") \
            .set('test_int', 123) \
            .set('first.test_int', 1235) \
            .set('first.test_long', 123456789) \
            .set('first.test_time', OTime(timestamp=1518689532)) \
            .set('first.test_date', ODate(days_since_epoch=3456)) \
            .set('first.test_bool', True) \
            .set('first.test_bool_false', False) \
            .set('first.test_invalid', ODate(days_since_epoch=3457)) \
            .set('first.test_str', 'strstr') \
            .set('first.test_dict', {'a': 1, 'b': 2}) \
            .set('first.test_dict2', {}) \
            .set('first.test_list', [1, 2, 'str', False, ODate(days_since_epoch=3457)])

        self.assertEqual(doc, document.as_dictionary())

    def test_find_by_id_empty_response(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)

        if connection.is_store_exists(store_path='/find-by-id-test-store1'):
            document_store = connection.get_store(store_path='/find-by-id-test-store1')
        else:
            document_store = connection.create_store(store_path='/find-by-id-test-store1')

        self.assertTrue(connection.is_store_exists('/find-by-id-test-store1'))
        doc_as_dict = document_store.find_by_id('id9999')

        self.assertEqual(doc_as_dict, {})

        doc_as_object = document_store.find_by_id('id9999', results_as_document=True)
        self.assertEqual(doc_as_object.as_dictionary(), {})

    def test_find_by_id_with_condition(self):
        connection = ConnectionFactory.get_connection(connection_str=CONNECTION_STR,
                                                      options=CONNECTION_OPTIONS)

        if connection.is_store_exists(store_path='/find-by-id-test-store1'):
            document_store = connection.get_store(store_path='/find-by-id-test-store1')
        else:
            document_store = connection.create_store(store_path='/find-by-id-test-store1')

        self.assertTrue(connection.is_store_exists('/find-by-id-test-store1'))

        condition = OJAIQueryCondition().exists_('false_field').close().build()
        doc = document_store.find_by_id('id008', condition=condition, results_as_document=True)
        self.assertEqual(doc.as_dictionary(), {})
        condition = OJAIQueryCondition().exists_('test_list').close().build()
        doc = document_store.find_by_id('id008', condition=condition, results_as_document=True,
                                        field_paths=['test_null', 'test_dict', '_id', 'test_str'])
        self.assertEqual(doc.as_dictionary(),
                         {'_id': 'id008', 'test_dict': {'test_int': 5},
                          'test_null': None, 'test_str': 'strstr'})


if __name__ == '__main__':

    test_classes_to_run = [FindByIdTest]
    loader = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
