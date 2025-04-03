import os
import wave
import math

def split_wav(input_file, output_path, segment_length=5):
    """
    Split a WAV file into segments of specified length (in seconds).
    
    Args:
        input_file (str): Path to the input WAV file
        output_path (str): Directory to save the output segments
        segment_length (int): Length of each segment in seconds (default: 5)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Open the input WAV file
    with wave.open(input_file, 'rb') as wav:
        # Get WAV file parameters
        n_channels = wav.getnchannels()
        samp_width = wav.getsampwidth()
        frame_rate = wav.getframerate()
        n_frames = wav.getnframes()
        comptype = wav.getcomptype()
        compname = wav.getcompname()
        
        # Calculate total duration and number of segments
        duration = n_frames / float(frame_rate)
        n_segments = math.ceil(duration / segment_length)
        frames_per_segment = int(frame_rate * segment_length)
        
        # Get the base filename without extension
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        
        # Read all frames
        all_frames = wav.readframes(n_frames)
        
        # Split into segments
        for i in range(n_segments):
            start = i * frames_per_segment
            end = start + frames_per_segment
            segment_frames = all_frames[start*samp_width*n_channels : end*samp_width*n_channels]
            
            # Skip empty segments
            if not segment_frames:
                continue
                
            # Create output file
            output_file = os.path.join(output_path, f"{base_name}_segment_{i+1:03d}.wav")
            
            # Write segment to file
            with wave.open(output_file, 'wb') as segment:
                segment.setnchannels(n_channels)
                segment.setsampwidth(samp_width)
                segment.setframerate(frame_rate)
                segment.setcomptype(comptype, compname)
                segment.writeframes(segment_frames)
                
            print(f"Saved segment {i+1} to {output_file}")

# Example usage
if __name__ == "__main__":
    input_wav = "classical.wav"  # Replace with your input file
    output_dir = "samples"  # Replace with your desired output directory
    
    split_wav(input_wav, output_dir, segment_length=5)