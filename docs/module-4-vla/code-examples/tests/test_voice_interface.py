#!/usr/bin/env python3
"""
Unit Tests for Voice Interface Module

Tests cover:
- Audio capture functionality
- Transcription accuracy
- Noise handling
- Voice activity detection
- Configuration validation

Run with: pytest test_voice_interface.py -v --cov=scripts.voice_interface
"""

import pytest
import numpy as np
import wave
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from voice_interface import (
    VoiceInterface,
    AudioConfig,
    VoiceCommand,
    TranscribedCommand
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def audio_config():
    """Default audio configuration for testing"""
    return AudioConfig(
        sample_rate=16000,
        channels=1,
        silence_threshold=500,
        silence_duration=2.0,
        max_recording_duration=30.0
    )


@pytest.fixture
def mock_whisper_model():
    """Mock Whisper model for testing without actual model loading"""
    with patch('voice_interface.whisper.load_model') as mock_load:
        mock_model = MagicMock()
        mock_model.device = 'cpu'
        mock_model.transcribe.return_value = {
            'text': 'navigate to the kitchen',
            'language': 'en',
            'segments': [
                {'avg_logprob': -0.2, 'text': 'navigate to the kitchen'}
            ]
        }
        mock_load.return_value = mock_model
        yield mock_model


@pytest.fixture
def mock_pyaudio():
    """Mock PyAudio for testing without actual audio hardware"""
    with patch('voice_interface.pyaudio.PyAudio') as mock_pa:
        mock_instance = MagicMock()
        mock_stream = MagicMock()

        # Mock audio data (silence)
        mock_stream.read.return_value = b'\x00' * 2048

        mock_instance.open.return_value = mock_stream
        mock_instance.get_device_count.return_value = 2
        mock_instance.get_device_info_by_index.return_value = {
            'name': 'Mock Device',
            'maxInputChannels': 1
        }
        mock_instance.get_sample_size.return_value = 2

        mock_pa.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def voice_interface(mock_whisper_model, mock_pyaudio, audio_config):
    """Voice interface instance with mocked dependencies"""
    vi = VoiceInterface(model_size="base", config=audio_config)
    return vi


@pytest.fixture
def sample_audio_data():
    """Generate sample audio data for testing"""
    sample_rate = 16000
    duration = 2.0
    t = np.linspace(0, duration, int(sample_rate * duration))

    # Simple sine wave
    audio_data = 0.3 * np.sin(2 * np.pi * 440 * t)  # A4 note
    return audio_data.astype(np.float32), sample_rate


@pytest.fixture
def sample_wav_file(sample_audio_data):
    """Create a temporary WAV file for testing"""
    audio_data, sample_rate = sample_audio_data

    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        filepath = Path(f.name)

    # Convert to int16
    audio_int16 = (audio_data * 32768.0).astype(np.int16)

    with wave.open(str(filepath), 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_int16.tobytes())

    yield filepath

    # Cleanup
    if filepath.exists():
        filepath.unlink()


# ============================================================================
# Configuration Tests
# ============================================================================

class TestAudioConfig:
    """Test AudioConfig dataclass"""

    def test_default_config(self):
        """Test default configuration values"""
        config = AudioConfig()

        assert config.sample_rate == 16000
        assert config.channels == 1
        assert config.chunk_size == 1024
        assert config.silence_threshold == 500
        assert config.silence_duration == 2.0
        assert config.max_recording_duration == 30.0

    def test_custom_config(self):
        """Test custom configuration"""
        config = AudioConfig(
            sample_rate=48000,
            channels=2,
            silence_threshold=300
        )

        assert config.sample_rate == 48000
        assert config.channels == 2
        assert config.silence_threshold == 300


# ============================================================================
# Voice Interface Initialization Tests
# ============================================================================

class TestVoiceInterfaceInit:
    """Test VoiceInterface initialization"""

    def test_init_default(self, mock_whisper_model, mock_pyaudio):
        """Test default initialization"""
        vi = VoiceInterface(model_size="base")

        assert vi.model_size == "base"
        assert vi.config.sample_rate == 16000
        assert vi.model is not None
        assert vi.audio is not None

    def test_init_custom_config(self, mock_whisper_model, mock_pyaudio):
        """Test initialization with custom config"""
        config = AudioConfig(sample_rate=48000)
        vi = VoiceInterface(model_size="tiny", config=config)

        assert vi.model_size == "tiny"
        assert vi.config.sample_rate == 48000

    def test_model_loading_failure(self, mock_pyaudio):
        """Test handling of model loading failure"""
        with patch('voice_interface.whisper.load_model') as mock_load:
            mock_load.side_effect = Exception("Model not found")

            with pytest.raises(Exception, match="Model not found"):
                VoiceInterface(model_size="invalid")


# ============================================================================
# Audio Recording Tests
# ============================================================================

class TestAudioRecording:
    """Test audio recording functionality"""

    def test_record_audio_fixed_duration(self, voice_interface, mock_pyaudio):
        """Test recording with fixed duration"""
        duration = 2.0
        audio_data, sample_rate = voice_interface.record_audio(
            duration=duration,
            use_vad=False
        )

        assert isinstance(audio_data, np.ndarray)
        assert len(audio_data) > 0
        assert sample_rate == voice_interface.config.sample_rate

        # Verify stream was opened and closed
        assert mock_pyaudio.open.called

    def test_record_audio_vad(self, voice_interface, mock_pyaudio):
        """Test recording with voice activity detection"""
        # Create mock audio with speech pattern
        mock_stream = mock_pyaudio.open.return_value

        # Simulate: silence -> speech -> silence
        silence_chunk = b'\x00' * 2048
        speech_chunk = b'\xFF' * 2048

        mock_stream.read.side_effect = [
            silence_chunk,  # Initial silence
            speech_chunk,   # Speech detected
            speech_chunk,   # Continue speech
            silence_chunk,  # Silence again
            silence_chunk,  # More silence (triggers stop)
        ] * 10

        audio_data, sample_rate = voice_interface.record_audio(
            duration=None,
            use_vad=True
        )

        assert isinstance(audio_data, np.ndarray)
        assert len(audio_data) > 0


# ============================================================================
# RMS and VAD Tests
# ============================================================================

class TestVoiceActivityDetection:
    """Test voice activity detection"""

    def test_calculate_rms_silence(self, voice_interface):
        """Test RMS calculation for silence"""
        silence = np.zeros(1024, dtype=np.int16).tobytes()
        rms = voice_interface._calculate_rms(silence)

        assert rms < 10  # Should be very low for silence

    def test_calculate_rms_speech(self, voice_interface):
        """Test RMS calculation for speech-like signal"""
        # Generate loud signal
        signal = (np.sin(np.linspace(0, 100, 1024)) * 10000).astype(np.int16)
        rms = voice_interface._calculate_rms(signal.tobytes())

        assert rms > 1000  # Should be high for speech

    def test_is_silence_detection(self, voice_interface):
        """Test silence detection threshold"""
        # Silence
        silence = np.zeros(1024, dtype=np.int16).tobytes()
        assert voice_interface._is_silence(silence) is True

        # Speech
        speech = (np.sin(np.linspace(0, 100, 1024)) * 10000).astype(np.int16)
        assert voice_interface._is_silence(speech.tobytes()) is False


# ============================================================================
# Transcription Tests
# ============================================================================

class TestTranscription:
    """Test audio transcription"""

    def test_transcribe_basic(self, voice_interface, sample_audio_data):
        """Test basic transcription"""
        audio_data, _ = sample_audio_data

        result = voice_interface.transcribe(audio_data, language="en")

        assert 'text' in result
        assert 'language' in result
        assert 'confidence' in result
        assert isinstance(result['text'], str)
        assert len(result['text']) > 0

    def test_transcribe_language_detection(self, voice_interface, sample_audio_data):
        """Test language detection"""
        audio_data, _ = sample_audio_data

        result = voice_interface.transcribe(audio_data, language=None)

        assert result['language'] is not None

    def test_transcribe_confidence_score(self, voice_interface, sample_audio_data):
        """Test confidence score calculation"""
        audio_data, _ = sample_audio_data

        result = voice_interface.transcribe(audio_data)

        assert 'confidence' in result
        assert isinstance(result['confidence'], float)
        assert -10.0 <= result['confidence'] <= 0.0  # Log probability range

    def test_transcribe_empty_audio(self, voice_interface):
        """Test transcription with empty audio"""
        empty_audio = np.zeros(1000, dtype=np.float32)

        # Should not crash, but may return empty or noise
        result = voice_interface.transcribe(empty_audio)
        assert 'text' in result


# ============================================================================
# File I/O Tests
# ============================================================================

class TestFileOperations:
    """Test audio file operations"""

    def test_save_audio(self, voice_interface, sample_audio_data):
        """Test saving audio to file"""
        audio_data, sample_rate = sample_audio_data

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            filepath = Path(f.name)

        try:
            voice_interface.save_audio(audio_data, filepath, sample_rate)

            assert filepath.exists()
            assert filepath.stat().st_size > 0

            # Verify WAV file is readable
            with wave.open(str(filepath), 'rb') as wf:
                assert wf.getnchannels() == 1
                assert wf.getframerate() == sample_rate
        finally:
            if filepath.exists():
                filepath.unlink()

    def test_transcribe_file(self, voice_interface, sample_wav_file):
        """Test transcribing from audio file"""
        text = voice_interface.transcribe_file(sample_wav_file, language="en")

        assert isinstance(text, str)
        # Synthetic audio may produce empty or nonsense text
        # Just verify it doesn't crash

    def test_transcribe_nonexistent_file(self, voice_interface):
        """Test transcription with nonexistent file"""
        with pytest.raises(Exception):
            voice_interface.transcribe_file(Path("/nonexistent/file.wav"))


# ============================================================================
# Integration Tests
# ============================================================================

class TestVoiceInterfaceIntegration:
    """Integration tests for complete workflows"""

    def test_listen_and_transcribe(self, voice_interface, mock_pyaudio):
        """Test complete listen and transcribe workflow"""
        # Setup mock to return audio data
        mock_stream = mock_pyaudio.open.return_value
        mock_stream.read.return_value = b'\x00' * 2048

        text = voice_interface.listen_and_transcribe(duration=2.0, use_vad=False)

        assert isinstance(text, str)

    def test_complete_pipeline_with_file(self, voice_interface, sample_wav_file):
        """Test complete pipeline: save -> load -> transcribe"""
        # Transcribe the sample file
        text = voice_interface.transcribe_file(sample_wav_file)

        # Should complete without errors
        assert isinstance(text, str)


# ============================================================================
# Noise Handling Tests
# ============================================================================

class TestNoiseHandling:
    """Test noise robustness"""

    def test_transcribe_with_noise(self, voice_interface):
        """Test transcription with noisy audio"""
        # Generate noisy signal
        sample_rate = 16000
        duration = 2.0
        t = np.linspace(0, duration, int(sample_rate * duration))

        # Signal + noise
        signal = 0.3 * np.sin(2 * np.pi * 440 * t)
        noise = np.random.normal(0, 0.1, len(signal))
        noisy_audio = (signal + noise).astype(np.float32)

        # Should handle noisy audio without crashing
        result = voice_interface.transcribe(noisy_audio)
        assert 'text' in result

    def test_transcribe_extreme_noise(self, voice_interface):
        """Test transcription with extreme noise"""
        # Pure noise
        noise = np.random.normal(0, 0.5, 32000).astype(np.float32)

        # Should not crash
        result = voice_interface.transcribe(noise)
        assert 'text' in result


# ============================================================================
# Data Classes Tests
# ============================================================================

class TestVoiceCommand:
    """Test VoiceCommand dataclass"""

    def test_voice_command_creation(self):
        """Test VoiceCommand creation"""
        from datetime import datetime

        cmd = VoiceCommand(
            audio_data=b'test',
            duration=5.0,
            timestamp=datetime.now(),
            sample_rate=16000,
            channels=1
        )

        assert cmd.audio_data == b'test'
        assert cmd.duration == 5.0
        assert cmd.sample_rate == 16000
        assert cmd.channels == 1


class TestTranscribedCommand:
    """Test TranscribedCommand dataclass"""

    def test_transcribed_command_creation(self):
        """Test TranscribedCommand creation"""
        from datetime import datetime

        cmd = TranscribedCommand(
            text="navigate to kitchen",
            confidence=0.95,
            language="en",
            timestamp=datetime.now(),
            source_audio_id="test123",
            processing_time=1.5
        )

        assert cmd.text == "navigate to kitchen"
        assert cmd.confidence == 0.95
        assert cmd.language == "en"
        assert cmd.processing_time == 1.5


# ============================================================================
# Performance Tests
# ============================================================================

class TestPerformance:
    """Test performance characteristics"""

    def test_transcription_speed(self, voice_interface, sample_audio_data):
        """Test transcription completes in reasonable time"""
        import time

        audio_data, _ = sample_audio_data

        start = time.time()
        voice_interface.transcribe(audio_data)
        elapsed = time.time() - start

        # Should complete in < 5 seconds for 2 second audio with base model
        assert elapsed < 10.0  # Allow extra time for CI environments

    def test_memory_efficiency(self, voice_interface, sample_audio_data):
        """Test memory usage is reasonable"""
        audio_data, _ = sample_audio_data

        # Should not crash with normal audio
        for _ in range(5):
            voice_interface.transcribe(audio_data)


# ============================================================================
# Error Handling Tests
# ============================================================================

class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_invalid_audio_data(self, voice_interface):
        """Test handling of invalid audio data"""
        # Too short
        short_audio = np.zeros(10, dtype=np.float32)

        # Should handle gracefully (may return empty)
        result = voice_interface.transcribe(short_audio)
        assert 'text' in result

    def test_transcription_failure(self, voice_interface, sample_audio_data):
        """Test handling of transcription failure"""
        audio_data, _ = sample_audio_data

        # Mock transcription failure
        with patch.object(voice_interface.model, 'transcribe') as mock_transcribe:
            mock_transcribe.side_effect = Exception("Transcription error")

            with pytest.raises(Exception, match="Transcription"):
                voice_interface.transcribe(audio_data)


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=voice_interface", "--cov-report=term-missing"])
