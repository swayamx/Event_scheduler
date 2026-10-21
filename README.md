

## 🧩 Problem 2: Event Scheduler

### Logic and Approach (In Plain English)

#### 1. Can Attend All Meetings (`can_attend_all`)
- We sort the list of events chronologically by their start times.
- If a person wants to attend every meeting, each meeting must conclude before or at the exact moment the subsequent meeting begins.
- We iterate through adjacent pairs $(events[i], events[i+1])$: if $end_i > start_{i+1}$, there is a time conflict and we immediately return `False`. If no conflicts exist, we return `True`. Adjacent meetings where $end_i = start_{i+1}$ do not overlap.

#### 2. Minimum Meeting Rooms Required (`min_rooms_required`)
- To determine the minimum number of rooms needed simultaneously, we must know the **peak number of overlapping meetings** at any given moment.
- We first sort all meetings chronologically by their start times.
- We use a **Min-Heap (Priority Queue)** to track the end times of active meetings currently occupying rooms:
  1. For each meeting with interval $(start, end)$:
     - We inspect the root of the min-heap (which holds the meeting that finishes earliest across all occupied rooms).
     - If that earliest meeting finished at or before the current meeting starts ($heap[0] \le start$), that room is now empty! We pop it from the heap (`heappop`), effectively **reusing that room**.
     - If the earliest meeting has not yet finished ($heap[0] > start$), all currently occupied rooms are busy, so a new room must be allocated.
  2. We push the current meeting's end time onto the heap (`heappush`).
- At the end of the iteration, the number of elements in the heap represents the exact minimum number of rooms required.

---

## 📊 Final Discussion & Analysis

### 1. Time & Space Complexity Analysis

| Problem / Function | Time Complexity | Auxiliary Space Complexity | Explanation |
| :--- | :---: | :---: | :--- |
| **`LRUCache.get(key)`** | **$O(1)$** | $O(1)$ | Hash map key lookup is $O(1)$; unlinking and moving node to front of doubly linked list is $O(1)$ pointer adjustments. |
| **`LRUCache.put(key, val)`** | **$O(1)$** | $O(1)$ | Hash map search/insert is $O(1)$; node creation, eviction of tail node, and insertion at head are $O(1)$. |
| **`LRUCache` (Overall)** | — | **$O(C)$** | Where $C$ is the fixed cache capacity; bounded storage for $C$ nodes and map entries. |
| **`can_attend_all(events)`** | **$O(n \log n)$** | **$O(n)$** | Sorting $n$ intervals takes $O(n \log n)$. Linear pass checking adjacent elements takes $O(n)$. |
| **`min_rooms_required(events)`**| **$O(n \log n)$** | **$O(n)$** | Sorting takes $O(n \log n)$. Iterating over $n$ events with min-heap push/pop takes $O(n \log k)$, where $k \le n$ is room count. Overall $O(n \log n)$. |
| **`assign_rooms(events)`** | **$O(n \log n)$** | **$O(n)$** | Sorting $n$ events takes $O(n \log n)$; min-heap room recycling and assignment take $O(n \log k)$. |

---

### 2. Trade-offs: Why Hash Map + Doubly Linked List?

Alternative data structures fail to meet the strict $O(1)$ requirement:
1. **Array / List alone**:
   - Looking up an item takes $O(n)$.
   - Even if lookups were indexed by key, moving an element to the front of an array requires shifting all subsequent elements, taking $O(n)$ time.
2. **Hash Map alone**:
   - Lookups and insertions are $O(1)$, but a standard hash table does not track chronological access history. Finding the least recently used element would require scanning all elements ($O(n)$).
3. **Singly Linked List + Hash Map**:
   - Removing an arbitrary node requires updating its predecessor ($prev.next = node.next$). Without a backward pointer, locating the predecessor requires traversing from the head ($O(n)$).
4. **Doubly Linked List + Hash Map**:
   - **Trade-off**: Requires extra memory overhead per item (two pointer references: `prev` and `next`), but guarantees strict **$O(1)$ unlinking and insertion**. This space-for-time trade-off is universally preferred for low-latency caching systems.

---

### 3. Future Proofing: Assigning Specific Room Identifiers ("Room A", "Room B", ...)

To assign specific human-readable room labels rather than just returning a count:
1. **Maintain Two Heaps**:
   - `active_rooms`: A min-heap storing `(end_time, room_id)` for meetings in progress.
   - `freed_room_ids`: A min-heap of released room IDs (e.g. `[0, 1, 2, ...]`) ready to be recycled.
2. **Room Allocation & Recycling Logic**:
   - Before scheduling meeting at time $start$, inspect `active_rooms`. For any meeting with $end\_time \le start$, pop it and return its `room_id` to `freed_room_ids`.
   - When assigning a room:
     - If `freed_room_ids` is non-empty, pop the smallest available room ID (guaranteeing greedy reuse of earlier rooms, like "Room A" before "Room B").
     - If no rooms are free, create a new ID ($next\_room\_id = \text{total\_rooms} + 1$).
   - Convert numeric IDs to labels (e.g., $0 \rightarrow$ "Room A", $1 \rightarrow$ "Room B", $2 \rightarrow$ "Room C").
3. This is fully implemented and tested in [`assign_rooms()`](event_scheduler.py).

---

### 4. Concurrency: Making the LRU Cache Thread-Safe

In a multi-threaded application (e.g., web server handling concurrent requests), race conditions occur when multiple threads simultaneously read, write, or evict from the linked list and hash map.

To make the LRU Cache thread-safe:
1. **Reentrant Mutex Lock (`threading.RLock`)**:
   - Encapsulate all operations (`get`, `put`, `delete`, `clear`) inside a synchronized block:
     ```python
     with self._lock:
         # perform get or put
     ```
   - An `RLock` allows internal helper methods (like `_remove` and `_add_to_front`) to be called without deadlocking.
2. **Read-Write Lock (RWLock / Shared Lock)**:
   - For high-read workloads, a single global lock can cause thread contention.
   - *Optimization*: Note that in an LRU cache, even a `get()` is a write operation because it updates the node's position to MRU. To use RWLock effectively, one can decouple read access from recency promotion using asynchronous ring buffers (e.g., as done in Java's Caffeine cache).
3. **Fine-Grained / Segmented Locking (Striped LRU)**:
   - Partition the key space across $K$ independent sub-caches (e.g., `hash(key) % K`), each with its own lock, drastically reducing contention under high concurrency.
4. Fully implemented in [`thread_safe_lru_cache.py`](thread_safe_lru_cache.py).

---

## 🧪 How to Run

```powershell
# Run all tests
py -m unittest discover -s "C:\Users\offic\Desktop\assessment-solutions" -p "test_*.py"

# Run the interactive demo
py "C:\Users\offic\Desktop\assessment-solutions\main_demo.py"
```
