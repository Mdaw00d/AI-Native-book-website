#!/usr/bin/env python3
"""
Voice Interface Module for VLA Integration
Uses OpenAI Whisper for speech-to-text conversion
"""

import whisper
import numpy as np
import pyaudio
import wave
import tempfile
import os
from typing import Optional, Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class VoiceCommand:
    """Captured audio input from user microphone"""
    audio_data: bytes
    duration: float
    timestamp: datetime
    sample_rate: int = 16000
    channels: int = 1


@dataclass
class TranscribedCommand:
    """Text output from speech-to-text conversion"""
    text: str
    confidence: float
    language: str
    timestamp: datetime
    source_audio_id: str
    processing_time: float


class VoiceInterface:
    """Handles voice command capture and transcription using Whisper"""

    def __init__(self, model_size: str = "base", sample_rate: int = 16000):
        """
        Initialize voice interface

        Args:
            model_size: Whisper model size ("tiny", "base", "small", "medium", "large")
            sample_rate: Audio sample rate in Hz (default 16000)
        """
        self.model_size = model_size
        self.sample_rate = sample_rate
        self.channels = 1  # Mono
        self.chunk_size = 1024

        print(f"Loading Whisper model: {model_size}...")
        self.model = whisper.load_model(model_size)
        print("✓ Whisper model loaded")

        self.audio = pyaudio.PyAudio()

    def record_audio(self, duration: float = 5.0) -> VoiceCommand:
        """
        Record audio from microphone

        Args:
            duration: Recording duration in seconds (default 5.0)

        Returns:
            VoiceCommand with recorded audio data
        """
        print(f"🎤 Recording for {duration} seconds...")

        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        frames = []
        num_chunks = int(self.sample_rate / self.chunk_size * duration)

        for i in range(num_chunks):
            data = stream.read(self.chunk_size, exception_on_overflow=False)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        audio_data = b''.join(frames)

        print("✓ Recording complete")

        return VoiceCommand(
            audio_data=audio_data,
            duration=duration,
            timestamp=datetime.now(),
            sample_rate=self.sample_rate,
            channels=self.channels
        )

    def transcribe_audio(
        self,
        voice_command: VoiceCommand,
        language: str = "en"
    ) -> TranscribedCommand:
        """
        Transcribe audio using Whisper

        Args:
            voice_command: VoiceCommand to transcribe
            language: Language code (default "en")

        Returns:
            TranscribedCommand with transcribed text
        """
        # Save audio to temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            with wave.open(temp_wav.name, 'wb') as wav_file:
                wav_file.setnchannels(voice_command.channels)
                wav_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wav_file.setframerate(voice_command.sample_rate)
                wav_file.writeframes(voice_command.audio_data)

            temp_path = temp_wav.name

        try:
            # Transcribe with Whisper
            print("🔄 Transcribing audio...")
            start_time = datetime.now()

            result = self.model.transcribe(
                temp_path,
                language=language,
                fp16=False  # CPU compatibility
            )

            processing_time = (datetime.now() - start_time).total_seconds()

            # Extract results
            text = result["text"].strip()
            detected_language = result.get("language", language)

            # Estimate confidence from segments (if available)
            segments = result.get("segments", [])
            if segments:
                avg_confidence = np.mean([
                    seg.get("no_speech_prob", 0.0)
                    for seg in segments
                ])
                confidence = 1.0 - avg_confidence  # Higher is better
            else:
                confidence = 0.8  # Default if no segments

            print(f"✓ Transcription: \"{text}\"")
            print(f"  Confidence: {confidence:.2f} | Time: {processing_time:.2f}s")

            return TranscribedCommand(
                text=text,
                confidence=confidence,
                language=detected_language,
                timestamp=datetime.now(),
                source_audio_id=str(voice_command.timestamp),
                processing_time=processing_time
            )

        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def listen_and_transcribe(
        self,
        duration: float = 5.0,
        language: str = "en"
    ) -> Optional[TranscribedCommand]:
        """
        Convenience method: record and transcribe in one call

        Args:
            duration: Recording duration in seconds
            language: Language code

        Returns:
            TranscribedCommand or None if failed
        """
        try:
            voice_cmd = self.record_audio(duration)
            transcribed = self.transcribe_audio(voice_cmd, language)

            # Warn if low confidence
            if transcribed.confidence < 0.5:
                print(f"⚠️  Low confidence: {transcribed.confidence:.2f}")
                print("    Consider re-recording or using text input")

            return transcribed

        except Exception as e:
            print(f"❌ Error during voice capture: {e}")
            return None

    def __del__(self):
        """Cleanup PyAudio"""
        if hasattr(self, 'audio'):
            self.audio.terminate()


def main():
    """Demo: Record and transcribe voice command"""
    import argparse

    parser = argparse.ArgumentParser(description="Voice Interface Demo")
    parser.add_argument(
        "--model",
        type=str,
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size"
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=5.0,
        help="Recording duration in seconds"
    )
    parser.add_argument(
        "--audio-file",
        type=str,
        help="Transcribe existing audio file instead of recording"
    )

    args = parser.parse_args()

    # Initialize interface
    interface = VoiceInterface(model_size=args.model)

    if args.audio_file:
        # Transcribe existing file
        print(f"📁 Transcribing file: {args.audio_file}")

        # Load audio file
        with wave.open(args.audio_file, 'rb') as wav:
            audio_data = wav.readframes(wav.getnframes())
            duration = wav.getnframes() / wav.getframerate()

            voice_cmd = VoiceCommand(
                audio_data=audio_data,
                duration=duration,
                timestamp=datetime.now(),
                sample_rate=wav.getframerate(),
                channels=wav.getnchannels()
            )

        result = interface.transcribe_audio(voice_cmd)
    else:
        # Record and transcribe
        print("\n🎙️  Voice Interface Demo")
        print("=" * 40)
        input("Press Enter to start recording...")

        result = interface.listen_and_transcribe(duration=args.duration)

    if result:
        print("\n" + "=" * 40)
        print("📝 Transcription Results")
        print("=" * 40)
        print(f"Text:       {result.text}")
        print(f"Confidence: {result.confidence:.2%}")
        print(f"Language:   {result.language}")
        print(f"Duration:   {result.processing_time:.2f}s")
        print("=" * 40)
    else:
        print("❌ Transcription failed")


if __name__ == "__main__":
    main()
