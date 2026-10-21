"""
Problem 1: LRU Cache Implementation

Achieves strict O(1) time complexity for both get() and put() operations
using a Doubly Linked List and a Hash Map.
"""

from typing import Any, Optional


class Node:
    """Doubly linked list node holding key, value, and neighbor pointers."""

    def __init__(self, key: Any = None, value: Any = None):
        self.key: Any = key
        self.value: Any = value
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None

    def __repr__(self) -> str:
        return f"Node({self.key}: {self.value})"


class LRUCache:
    """
    Least Recently Used (LRU) Cache with fixed capacity.

    Operations:
    - get(key): Returns value if key exists, otherwise -1. Marks key as MRU.
    - put(key, value): Adds or updates key-value pair. Evicts LRU item if at capacity.
    Both operations run in O(1) time complexity.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer greater than 0.")
        self.capacity: int = capacity
        self.cache: dict[Any, Node] = {}

        # Sentinel boundary nodes: dummy head (MRU) and dummy tail (LRU)
        self.head: Node = Node()
        self.tail: Node = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        """Unlink an existing node from the doubly linked list in O(1)."""
        prev_node = node.prev
        next_node = node.next
        if prev_node:
            prev_node.next = next_node
        if next_node:
            next_node.prev = prev_node

    def _add_to_front(self, node: Node) -> None:
        """Insert a node right after dummy head (mark as MRU) in O(1)."""
        node.next = self.head.next
        node.prev = self.head
        if self.head.next:
            self.head.next.prev = node
        self.head.next = node

    def _move_to_front(self, node: Node) -> None:
        """Move an existing node to the MRU position in O(1)."""
        self._remove(node)
        self._add_to_front(node)

    def get(self, key: Any) -> Any:
        """
        Returns value associated with key, or -1 if not found.
        Marks accessed key as most recently used.
        Time Complexity: O(1)
        """
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._move_to_front(node)
        return node.value

    def put(self, key: Any, value: Any) -> None:
        """
        Adds or updates the key-value pair.
        Evicts the least recently used item if at capacity.
        Time Complexity: O(1)
        """
        if key in self.cache:
            # Key already exists: update value and promote to MRU
            node = self.cache[key]
            node.value = value
            self._move_to_front(node)
        else:
            # New key: check if eviction is necessary
            if len(self.cache) >= self.capacity:
                # Evict the LRU item (node right before dummy tail)
                lru_node = self.tail.prev
                if lru_node and lru_node != self.head:
                    self._remove(lru_node)
                    del self.cache[lru_node.key]

            # Insert new node at MRU position
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)

    def to_list(self) -> list[tuple[Any, Any]]:
        """Return cache contents from MRU (head) to LRU (tail)."""
        items = []
        curr = self.head.next
        while curr and curr != self.tail:
            items.append((curr.key, curr.value))
            curr = curr.next
        return items

    def __len__(self) -> int:
        return len(self.cache)

    def __repr__(self) -> str:
        items_str = ", ".join(f"{k}: {v}" for k, v in self.to_list())
        return f"LRUCache(capacity={self.capacity}, items=[{items_str}])"
