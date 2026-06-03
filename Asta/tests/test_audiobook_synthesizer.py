import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from asta.feature_architecture.creativity.audiobook_synthesizer import AudiobookSynthesizer

@pytest.mark.asyncio
async def test_audiobook_file_not_found():
    synth = AudiobookSynthesizer(output_dir="/tmp/audiobooks")
    result = await synth.ingest_and_synthesize("does_not_exist.txt", "Ghost Book")
    assert result["status"] == "failed"
    assert "not found" in result["error"].lower()
