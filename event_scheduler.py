"""
Problem 2: Event Scheduler Implementation

Functions:
- can_attend_all(events): Determines if a person can attend all meetings without overlap.
- min_rooms_required(events): Calculates the minimum number of rooms needed for all meetings.
- assign_rooms(events): Future-proofing extension that assigns specific room names ("Room A", "Room B", ...)
                       to events while recycling freed rooms efficiently.
"""

import heapq
from typing import List, Tuple, Dict, Any


def can_attend_all(events: List[Tuple[int, int]]) -> bool:
    """
    Returns True if a person can attend all events without overlaps, False otherwise.
    Adjacent events (where an end time equals a start time) are NOT overlaps.
    
    Time Complexity: O(n log n) due to sorting.
    Space Complexity: O(n) to store sorted events.
    """
    if not events or len(events) <= 1:
        return True

    # Sort events chronologically by start time
    sorted_events = sorted(events, key=lambda e: e[0])

    # Check for overlaps between consecutive events
    for i in range(len(sorted_events) - 1):
        current_end = sorted_events[i][1]
        next_start = sorted_events[i + 1][0]
        # Overlap occurs strictly if current meeting ends after next meeting starts
        if current_end > next_start:
            return False

    return True


def min_rooms_required(events: List[Tuple[int, int]]) -> int:
    """
    Returns the minimum number of meeting rooms required to schedule all events simultaneously.
    Adjacent events (where end time equals start time) can share the same room.

    Time Complexity: O(n log n) - sorting takes O(n log n), heap operations take O(n log k).
    Space Complexity: O(n) - stores events and at most n active meeting end times in heap.
    """
    if not events:
        return 0

    # Sort events by start time
    sorted_events = sorted(events, key=lambda e: e[0])

    # Min-heap storing the end times of ongoing meetings in active rooms
    room_end_times: List[int] = []

    for start, end in sorted_events:
        # If the earliest ending meeting has finished before or when this meeting starts,
        # that room is now free and can be reused.
        if room_end_times and room_end_times[0] <= start:
            heapq.heappop(room_end_times)

        # Allocate room (either the reused room or a new one) with current meeting's end time
        heapq.heappush(room_end_times, end)

    # The number of active rooms remaining in the heap is the minimum rooms required
    return len(room_end_times)


def assign_rooms(events: List[Tuple[int, int]]) -> List[Dict[str, Any]]:
    """
    Future-Proofing Extension:
    Assigns specific room names (e.g., 'Room A', 'Room B', ...) to each event,
    recycling freed rooms in alphabetical order.

    Returns a list of assignments preserving the original input order.
    """
    if not events:
        return []

    # Preserve original indices while sorting by start time
    indexed_events = sorted(
        [(start, end, idx) for idx, (start, end) in enumerate(events)],
        key=lambda x: x[0]
    )

    # Min-heap of active meetings: stores (end_time, room_id_int)
    active_rooms: List[Tuple[int, int]] = []

    # Min-heap of recycled room numbers: 0, 1, 2, ...
    freed_room_ids: List[int] = []
    next_room_id: int = 0

    assignments: List[Dict[str, Any]] = [{} for _ in range(len(events))]

    for start, end, original_idx in indexed_events:
        # Free up any rooms whose meetings have concluded before or at current start time
        while active_rooms and active_rooms[0][0] <= start:
            _, room_id = heapq.heappop(active_rooms)
            heapq.heappush(freed_room_ids, room_id)

        # Allocate an available recycled room or create a new room ID
        if freed_room_ids:
            room_id = heapq.heappop(freed_room_ids)
        else:
            room_id = next_room_id
            next_room_id += 1

        # Format room name (e.g. 0 -> 'Room A', 1 -> 'Room B')
        room_name = f"Room {chr(ord('A') + room_id)}"
        heapq.heappush(active_rooms, (end, room_id))

        assignments[original_idx] = {
            "event": (start, end),
            "room": room_name
        }

    return assignments
