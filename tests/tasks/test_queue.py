import unittest
from src.task_manager.queue import UniqueQueue, EmptyQueueError


class TestQueue(unittest.TestCase):

    def setUp(self):
        self.queue = UniqueQueue()



    def test_no_exists_strategy(self):
        with self.assertRaises(TypeError):
            queue = UniqueQueue("FILA")

    def test_add_item_to_queue(self):
        item_1 = 3
        self.queue.add(item_1)
        item = self.queue.storage[0]
        self.assertEqual(item_1, item)

    def test_add_and_get_item_from_queue(self):
        item_1 = 3
        self.queue.add(item_1)
        item_remove_1 = self.queue.remove()
        self.assertEqual(item_1, item_remove_1)

    def test_get_item_from_empty_queue(self):
        with self.assertRaises(EmptyQueueError):
            self.queue.remove()

    def test_get_length_empty_queue(self):
        len = self.queue.get_length_of_queue()
        self.assertEqual(0, len)

    def test_get_length_of_queue(self):
        item_1 = 3
        item_2 = 5
        item_3 = 6
        self.queue.add(item_1)
        self.queue.add(item_2)
        self.queue.add(item_3)
        self.assertEqual(3, self.queue.get_length_of_queue())


    def test_get_last_item_queue(self):
        item_1 = 3
        item_2 = 4
        item_3 = 5
        self.queue.add(item_1)
        self.queue.add(item_2)
        self.queue.add(item_3)
        self.assertEqual(self.queue.get_last_item(), item_3)

    def test_get_last_item_empty_queue(self):
        with self.assertRaises(EmptyQueueError):
            self.queue.get_last_item()

    def test_unique_queue(self):
        item_1 = 3
        item_2 = 4
        item_3 = 5
        self.queue.add(item_1)
        self.queue.add(item_2)
        self.queue.add(item_3)
        self.queue.add(item_2)
        unique_storage = list(set(self.queue.storage))
        self.assertEqual(len(unique_storage), len(self.queue.storage))

    def test_get_item_from_unique_queue_lifo(self):
        item_1 = 3
        self.queue.add(item_1)
        self.assertEqual(self.queue.get_last_item(), item_1)
        item_2 = 4
        self.queue.add(item_2)
        self.assertEqual(self.queue.get_last_item(), item_2)
        item_3 = 5
        self.queue.add(item_3)
        self.assertEqual(self.queue.get_last_item(), item_3)
        self.queue.add(item_2)
        self.assertEqual(self.queue.get_last_item(), item_3)
        item = self.queue.remove()
        self.assertEqual(item, item_3)
        self.assertEqual(self.queue.get_last_item(), item_2)


if __name__ == '__main__':
    unittest.main()