import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from asta.actuation_sensory.passive.audio_listener import AudioListener

def test_wake_word_init():
    listener = AudioListener(wake_word="jarvis")
    assert listener.wake_word == "jarvis"
