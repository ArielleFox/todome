from typing import Dict, List, Set
import json
import os
from difflib import get_close_matches
from colorLib import *

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.show_data = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, show_data: dict):
        node = self.root
        word = word.lower()
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.show_data = show_data

    def search_prefix(self, prefix: str, max_suggestions: int = 5) -> List[tuple]:
        results = []
        node = self.root
        prefix = prefix.lower()

        # Traverse to the last node of prefix
        for char in prefix:
            if char not in node.children:
                return results
            node = node.children[char]

        # Use DFS to find all words with the prefix
        def dfs(node: TrieNode, current_word: str):
            if len(results) >= max_suggestions:
                return

            if node.is_end:
                results.append((current_word, node.show_data))

            for char, child in sorted(node.children.items()):
                dfs(child, current_word + char)

        dfs(node, prefix)
        return results

class ShowTracker:
    def __init__(self, filename: str = "shows_tracker.json"):
        self.filename = filename
        self.shows = self.load_shows()
        self.search_trie = Trie()
        self.rebuild_search_index()

    def rebuild_search_index(self):
        """Rebuild the search index with all shows"""
        self.search_trie = Trie()
        for service in self.shows:
            for show_name, details in self.shows[service].items():
                self.search_trie.insert(show_name, {
                    'service': service,
                    'name': show_name,
                    'details': details
                })

    def load_shows(self) -> Dict:
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}
        return {}

    def save_shows(self):
        with open(self.filename, 'w') as file:
            json.dump(self.shows, file, indent=4)
        self.rebuild_search_index()

    def add_show(self):
        """Add a new show to the tracker"""
        streaming_service = input("Enter streaming service: ").strip()
        show_name = input("Enter show name: ").strip()

        try:
            season = int(input("Enter season number: "))
            episode = int(input("Enter episode number: "))
        except ValueError:
            print("Season and episode must be numbers!")
            return

        # Create new service if it doesn't exist
        if streaming_service not in self.shows:
            self.shows[streaming_service] = {}

        # Add or update the show
        self.shows[streaming_service][show_name] = {
            "season": season,
            "episode": episode
        }

        self.save_shows()
        print(f"Added: {color_yellow_fg(show_name)} (S{season:02d}E{episode:02d}) on {streaming_service}")

    def search_shows(self, query: str, max_suggestions: int = 5) -> List[dict]:
        """
        Search for shows with autocompletion
        Returns a list of matching shows with their details
        """
        if not query:
            return []

        # Get exact and partial matches from Trie
        trie_results = self.search_trie.search_prefix(query, max_suggestions)

        # Convert results to list of shows
        results = []
        for _, show_data in trie_results:
            results.append(show_data)

        # If we have fewer results than requested, try fuzzy matching
        if len(results) < max_suggestions:
            all_shows = []
            for service in self.shows:
                for show_name in self.shows[service]:
                    if not any(r['name'].lower() == show_name.lower() for r in results):
                        all_shows.append(show_name)

            # Get fuzzy matches
            fuzzy_matches = get_close_matches(query, all_shows,
                                           n=max_suggestions-len(results),
                                           cutoff=0.6)

            # Add fuzzy matches to results
            for match in fuzzy_matches:
                for service in self.shows:
                    if match in self.shows[service]:
                        results.append({
                            'service': service,
                            'name': match,
                            'details': self.shows[service][match]
                        })

        return results

    def interactive_search(self):
        """Interactive search with real-time autocompletion"""
        print("\nSearch for shows (type at least 2 characters, press Enter to select)")
        print("Press Enter with empty query to cancel search")

        while True:
            query = input(f"\n{color_green_bg('Search:')} ").strip()
            if not query:
                return None

            if len(query) < 2:
                print("Please enter at least 2 characters")
                continue

            results = self.search_shows(query)

            if not results:
                print(f"{color_red_fg('No matches found.')}")
                continue

            print("\nMatching shows:")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result['name']} on {result['service']} "
                      f"(S{result['details']['season']:02d}E{result['details']['episode']:02d})")

            choice = input("\nSelect a number or continue typing to refine search: ").strip()

            if choice.isdigit() and 1 <= int(choice) <= len(results):
                return results[int(choice)-1]

    def edit_show_with_search(self):
        """Edit show using search functionality"""
        if not self.shows:
            print("No shows found!")
            return

        result = self.interactive_search()
        if not result:
            return

        try:
            season = int(input("Enter new season number: "))
            episode = int(input("Enter new episode number: "))
        except ValueError:
            print("Season and episode must be numbers!")
            return

        self.shows[result['service']][result['name']] = {
            "season": season,
            "episode": episode
        }

        self.save_shows()
        print(f"Updated: {result['name']} (S{season:02d}E{episode:02d}) on {result['service']}")

    def display_shows(self):
        """Display all shows in the tracker"""
        if not self.shows:
            print("No shows found!")
            return

        print("\nCurrent Shows:")
        for service in self.shows:
            print(f"\n{service}:")
            for show in self.shows[service]:
                details = self.shows[service][show]
                print(f"  - {show} (S{details['season']:02d}E{details['episode']:02d})")

def main():
    tracker = ShowTracker()

    while True:
        print(f"\n{color_yellow_fg('===')} TV Show Tracker {color_yellow_fg('===')}")
        print(f"1. Add new show")
        print(f"2. Edit existing show")
        print(f"3. Display all shows")
        print(f"4. Search shows")
        print(f"5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            tracker.add_show()
        elif choice == "2":
            tracker.edit_show_with_search()
        elif choice == "3":
            tracker.display_shows()
        elif choice == "4":
            result = tracker.interactive_search()
            if result:
                print(f"\nSelected show details:")
                print(f"Show: {result['name']}")
                print(f"Service: {result['service']}")
                print(f"Season: {result['details']['season']}")
                print(f"Episode: {result['details']['episode']}")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()

# Created/Modified files during execution:
# shows_tracker.json
