"""
Comprehensive test suite for Assessment Problems 1 & 2.
"""

import unittest
import threading
from lru_cache import LRUCache
from event_scheduler import can_attend_all, min_rooms_required, assign_rooms
from thread_safe_lru_cache import ThreadSafeLRUCache


class TestProblem1LRUCache(unittest.TestCase):

    def test_basic_get_put(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        self.assertEqual(cache.get(1), 1)
        cache.put(3, 3)  # Evicts 2
        self.assertEqual(cache.get(2), -1)
        cache.put(4, 4)  # Evicts 1
        self.assertEqual(cache.get(1), -1)
        self.assertEqual(cache.get(3), 3)
        self.assertEqual(cache.get(4), 4)

    def test_capacity_and_updates(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(1, 20)  # Update
        self.assertEqual(cache.get(1), 20)
        cache.put(2, 30)
        cache.put(3, 40)  # Evicts 1 (since 1 was LRU, 2 was MRU)
        self.assertEqual(cache.get(1), -1)
        self.assertEqual(cache.get(2), 30)
        self.assertEqual(cache.get(3), 40)

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            LRUCache(0)
        with self.assertRaises(ValueError):
            LRUCache(-1)


class TestProblem2EventScheduler(unittest.TestCase):

    def test_can_attend_all_true(self):
        # Non-overlapping adjacent events
        events = [(9, 10), (10, 11), (11, 12)]
        self.assertTrue(can_attend_all(events))

    def test_can_attend_all_false(self):
        # Overlapping events
        events = [(0, 30), (5, 10), (15, 20)]
        self.assertFalse(can_attend_all(events))

    def test_can_attend_all_empty_and_single(self):
        self.assertTrue(can_attend_all([]))
        self.assertTrue(can_attend_all([(9, 10)]))

    def test_min_rooms_adjacent_meetings(self):
        # Adjacent meetings share the same room
        events = [(9, 10), (10, 11), (11, 12)]
        self.assertEqual(min_rooms_required(events), 1)

    def test_min_rooms_concurrent_meetings(self):
        events = [(0, 30), (5, 10), (15, 20)]
        self.assertEqual(min_rooms_required(events), 2)

    def test_min_rooms_complex_schedule(self):
        events = [(1, 10), (2, 7), (3, 19), (8, 12), (10, 20), (11, 30)]
        self.assertEqual(min_rooms_required(events), 4)

    def test_min_rooms_empty(self):
        self.assertEqual(min_rooms_required([]), 0)


class TestFutureProofingRoomAssignment(unittest.TestCase):

    def test_assign_rooms(self):
        events = [(0, 30), (5, 10), (15, 20)]
        assignments = assign_rooms(events)
        self.assertEqual(len(assignments), 3)

        # Event (0, 30) gets Room A
        self.assertEqual(assignments[0]["room"], "Room A")
        # Event (5, 10) gets Room B
        self.assertEqual(assignments[1]["room"], "Room B")
        # Event (15, 20) starts after (5, 10) ended at 10, so Room B is recycled!
        self.assertEqual(assignments[2]["room"], "Room B")


class TestConcurrencyLRUCache(unittest.TestCase):

    def test_multithreaded_access(self):
        cache = ThreadSafeLRUCache(20)
        num_threads = 6
        ops_per_thread = 200
        errors = []

        def worker(t_id):
            try:
                for i in range(ops_per_thread):
                    key = (t_id * 10 + i) % 30
                    cache.put(key, i)
                    val = cache.get(key)
                    cache.peek(key)
            except Exception as e:
                errors.append(str(e))

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0)
        self.assertLessEqual(len(cache), 20)


if __name__ == "__main__":
    unittest.main()
