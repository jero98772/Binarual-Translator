#!/usr/bin/env python3
"""
Microphone Test Script
Tests your microphone by recording audio and playing it back.
"""

import pyaudio
import wave
import sys

def list_audio_devices():
    """List all available audio input devices."""
    p = pyaudio.PyAudio()
    print("\n=== Available Audio Devices ===")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            print(f"Device {i}: {info['name']}")
            print(f"  - Input Channels: {info['maxInputChannels']}")
            print(f"  - Sample Rate: {int(info['defaultSampleRate'])} Hz")
    p.terminate()
    print()

def test_microphone(duration=5, output_file="test_recording.wav"):
    """
    Record audio from the microphone and save to a file.
    
    Args:
        duration: Recording duration in seconds (default: 5)
        output_file: Output filename (default: test_recording.wav)
    """
    # Audio settings
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    
    p = pyaudio.PyAudio()
    
    print(f"\n🎤 Starting microphone test...")
    print(f"Recording for {duration} seconds...")
    print("Speak into your microphone now!\n")
    
    try:
        # Open stream
        stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)
        
        frames = []
        
        # Record audio
        for i in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
            
            # Progress indicator
            progress = (i + 1) / (RATE / CHUNK * duration) * 100
            print(f"\rRecording: {'█' * int(progress // 5)}{'-' * (20 - int(progress // 5))} {progress:.0f}%", end='')
        
        print("\n✅ Recording complete!")
        
        # Stop and close stream
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Save to file
        wf = wave.open(output_file, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"💾 Audio saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        p.terminate()
        return False

def playback_audio(filename="test_recording.wav"):
    """Play back the recorded audio file."""
    try:
        print(f"\n🔊 Playing back recording from {filename}...")
        
        wf = wave.open(filename, 'rb')
        p = pyaudio.PyAudio()
        
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                       channels=wf.getnchannels(),
                       rate=wf.getframerate(),
                       output=True)
        
        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()
        
        print("✅ Playback complete!")
        
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found!")
    except Exception as e:
        print(f"❌ Error during playback: {e}")

def main():
    """Main function to run microphone test."""
    print("\n" + "="*50)
    print("   MICROPHONE TEST UTILITY")
    print("="*50)
    
    # List available devices
    list_audio_devices()
    
    # Get recording duration from user
    try:
        duration = input("Enter recording duration in seconds (default 5): ").strip()
        duration = int(duration) if duration else 5
    except ValueError:
        duration = 5
    
    # Record audio
    if test_microphone(duration=duration):
        # Ask if user wants to play back
        playback = input("\nWould you like to hear the recording? (y/n): ").strip().lower()
        if playback == 'y':
            playback_audio()
    
    print("\n" + "="*50)
    print("Test complete!")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
