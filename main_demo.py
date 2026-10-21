"""
Interactive demonstration of Problem 1 (LRU Cache) and Problem 2 (Event Scheduler).
"""

from lru_cache import LRUCache
from event_scheduler import can_attend_all, min_rooms_required, assign_rooms


def demo_problem_1():
    print("=" * 60)
    print("  PROBLEM 1: LRU CACHE DEMONSTRATION")
    print("=" * 60)

    cache = LRUCache(2)
    print("Initialized LRUCache with capacity = 2\n")

    steps = [
        ("put", 1, 1),
        ("put", 2, 2),
        ("get", 1),
        ("put", 3, 3),  # Should evict 2
        ("get", 2),    # Should return -1
        ("put", 4, 4),  # Should evict 1
        ("get", 1),    # Should return -1
        ("get", 3),    # Should return 3
        ("get", 4),    # Should return 4
    ]

    for step in steps:
        if step[0] == "put":
            cache.put(step[1], step[2])
            print(f">>> put({step[1]}, {step[2]})")
        else:
            res = cache.get(step[1])
            print(f">>> get({step[1]}) -> {res}")
        print(f"    Cache state (MRU -> LRU): {cache.to_list()}")
    print()


def demo_problem_2():
    print("=" * 60)
    print("  PROBLEM 2: EVENT SCHEDULER DEMONSTRATION")
    print("=" * 60)

    schedule_1 = [(9, 10), (10, 11), (11, 12)]
    print(f"Schedule 1: {schedule_1}")
    print(f"  Can attend all?         {can_attend_all(schedule_1)}")
    print(f"  Min rooms required:     {min_rooms_required(schedule_1)}")
    print(f"  Room assignments:       {assign_rooms(schedule_1)}")
    print()

    schedule_2 = [(0, 30), (5, 10), (15, 20)]
    print(f"Schedule 2: {schedule_2}")
    print(f"  Can attend all?         {can_attend_all(schedule_2)}")
    print(f"  Min rooms required:     {min_rooms_required(schedule_2)}")
    print("  Room assignments (with recycling):")
    for item in assign_rooms(schedule_2):
        print(f"    Meeting {item['event']} -> {item['room']}")
    print()

    schedule_3 = [(1, 10), (2, 7), (3, 19), (8, 12), (10, 20), (11, 30)]
    print(f"Schedule 3: {schedule_3}")
    print(f"  Can attend all?         {can_attend_all(schedule_3)}")
    print(f"  Min rooms required:     {min_rooms_required(schedule_3)}")
    print("=" * 60)


if __name__ == "__main__":
    demo_problem_1()
    demo_problem_2()
