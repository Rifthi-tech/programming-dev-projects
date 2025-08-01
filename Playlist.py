import tkinter as tk
from tkinter import filedialog, messagebox
import os
import random
import pygame
from pygame import mixer

class SongNode:
    """Node class for the linked list representing each song in the playlist"""
    def __init__(self, song_path):
        self.song_path = song_path
        self.song_name = os.path.basename(song_path)
        self.next = None
        self.prev = None

class Playlist:
    """Linked List implementation of the playlist ADT"""
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.length = 0
    
    def add_song(self, song_path):
        new_node = SongNode(song_path)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1
    
    def remove_song(self, song_name):
        current = self.head
        while current:
            if current.song_name == song_name:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                
                if self.current == current:
                    self.current = current.next if current.next else self.head
                
                self.length -= 1
                return True
            current = current.next
        return False
    
    def shuffle(self):
        if self.length <= 1:
            return
        
        # Convert linked list to list
        nodes = []
        current = self.head
        while current:
            nodes.append(current)
            current = current.next
        
        # Shuffle the list
        random.shuffle(nodes)
        
        # Rebuild the linked list
        for i in range(len(nodes)):
            if i == 0:
                nodes[i].prev = None
                self.head = nodes[i]
            else:
                nodes[i].prev = nodes[i-1]
                nodes[i-1].next = nodes[i]
            
            if i == len(nodes) - 1:
                nodes[i].next = None
                self.tail = nodes[i]
            else:
                nodes[i].next = nodes[i+1]
        
        self.current = self.head
    
    def get_song_list(self):
        songs = []
        current = self.head
        while current:
            songs.append(current.song_name)
            current = current.next
        return songs
    
    def play_next(self):
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current.song_path
        return None
    
    def play_previous(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current.song_path
        return None

class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Playlist Management System")
        
        # Initialize pygame mixer
        mixer.init()
        
        # Create playlist
        self.playlist = Playlist()
        
        # GUI Elements
        self.create_widgets()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_widgets(self):
        # Playlist frame
        playlist_frame = tk.Frame(self.root)
        playlist_frame.pack(pady=10)
        
        self.playlist_listbox = tk.Listbox(playlist_frame, width=50, height=15)
        self.playlist_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        
        scrollbar = tk.Scrollbar(playlist_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.playlist_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.playlist_listbox.yview)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=10)
        
        add_button = tk.Button(buttons_frame, text="Add Song", command=self.add_song)
        add_button.grid(row=0, column=0, padx=5)
        
        remove_button = tk.Button(buttons_frame, text="Remove Song", command=self.remove_song)
        remove_button.grid(row=0, column=1, padx=5)
        
        shuffle_button = tk.Button(buttons_frame, text="Shuffle Playlist", command=self.shuffle_playlist)
        shuffle_button.grid(row=0, column=2, padx=5)
        
        # Playback controls frame
        playback_frame = tk.Frame(self.root)
        playback_frame.pack(pady=10)
        
        play_button = tk.Button(playback_frame, text="Play", command=self.play_song)
        play_button.grid(row=0, column=0, padx=5)
        
        pause_button = tk.Button(playback_frame, text="Pause", command=self.pause_song)
        pause_button.grid(row=0, column=1, padx=5)
        
        stop_button = tk.Button(playback_frame, text="Stop", command=self.stop_song)
        stop_button.grid(row=0, column=2, padx=5)
        
        next_button = tk.Button(playback_frame, text="Next", command=self.next_song)
        next_button.grid(row=0, column=3, padx=5)
        
        prev_button = tk.Button(playback_frame, text="Previous", command=self.previous_song)
        prev_button.grid(row=0, column=4, padx=5)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, pady=5)
    
    def add_song(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Songs",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")]
        )
        
        for file_path in file_paths:
            self.playlist.add_song(file_path)
        
        self.update_playlist_display()
        self.status_label.config(text=f"Added {len(file_paths)} song(s) to playlist")
    
    def remove_song(self):
        selected = self.playlist_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a song to remove")
            return
        
        song_name = self.playlist_listbox.get(selected[0])
        if self.playlist.remove_song(song_name):
            self.update_playlist_display()
            self.status_label.config(text=f"Removed {song_name} from playlist")
        else:
            messagebox.showerror("Error", f"Could not remove {song_name}")
    
    def shuffle_playlist(self):
        self.playlist.shuffle()
        self.update_playlist_display()
        self.status_label.config(text="Playlist shuffled")
    
    def play_song(self):
        selected = self.playlist_listbox.curselection()
        if selected:
            song_name = self.playlist_listbox.get(selected[0])
            current = self.playlist.head
            while current:
                if current.song_name == song_name:
                    self.playlist.current = current
                    break
                current = current.next
        
        if self.playlist.current:
            mixer.music.load(self.playlist.current.song_path)
            mixer.music.play()
            self.status_label.config(text=f"Now playing: {self.playlist.current.song_name}")
    
    def pause_song(self):
        if mixer.music.get_busy():
            mixer.music.pause()
            self.status_label.config(text="Playback paused")
        else:
            mixer.music.unpause()
            self.status_label.config(text="Playback resumed")
    
    def stop_song(self):
        mixer.music.stop()
        self.status_label.config(text="Playback stopped")
    
    def next_song(self):
        next_song_path = self.playlist.play_next()
        if next_song_path:
            mixer.music.load(next_song_path)
            mixer.music.play()
            self.update_playlist_display()
            self.status_label.config(text=f"Now playing: {self.playlist.current.song_name}")
        else:
            self.status_label.config(text="End of playlist reached")
    
    def previous_song(self):
        prev_song_path = self.playlist.play_previous()
        if prev_song_path:
            mixer.music.load(prev_song_path)
            mixer.music.play()
            self.update_playlist_display()
            self.status_label.config(text=f"Now playing: {self.playlist.current.song_name}")
        else:
            self.status_label.config(text="Beginning of playlist reached")
    
    def update_playlist_display(self):
        self.playlist_listbox.delete(0, tk.END)
        for song in self.playlist.get_song_list():
            self.playlist_listbox.insert(tk.END, song)
        
        # Highlight the current song
        if self.playlist.current:
            songs = self.playlist.get_song_list()
            try:
                index = songs.index(self.playlist.current.song_name)
                self.playlist_listbox.selection_clear(0, tk.END)
                self.playlist_listbox.selection_set(index)
                self.playlist_listbox.activate(index)
            except ValueError:
                pass
    
    def on_close(self):
        mixer.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()