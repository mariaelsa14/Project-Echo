import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import spectrogram
from pydub import AudioSegment
import matplotlib.pyplot as plt
import noisereduce as nr

# Define your paths and parameters
input_audio_path = '1710389924546_chunk_6.wav'
export_directory = 'noise reduction test'

# Ensure the export directory exists
if not os.path.exists(export_directory):
    os.makedirs(export_directory)

# Load the audio file
audioPre = AudioSegment.from_wav(input_audio_path)

# Convert the entire audio file to a numpy array
samples = np.array(audioPre.get_array_of_samples())

if audioPre.channels > 1:
    samples = samples.reshape(-1, audioPre.channels)
    samples = np.mean(samples, axis=1)  # Averaging channels for mono

# Apply noise reduction
reduced_noise_samples = nr.reduce_noise(y=samples, sr=audioPre.frame_rate)

# Function to plot and save a spectrogram as a jpg file
def plot_and_save_spectrogram(samples, sample_rate, title='Spectrogram', filename='spectrogram.jpg'):
    """
    Plots a spectrogram for the given audio samples and sample rate, then saves it as a jpg file.
    """
    f, t, Sxx = spectrogram(samples, sample_rate)
    Sxx_log = 10 * np.log10(Sxx + 1e-10)  # Convert to dB
    
    plt.figure(figsize=(20, 6))
    plt.pcolormesh(t, f, Sxx_log, shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title(title)
    plt.colorbar(format='%+2.0f dB')
    plt.ylim(0, sample_rate / 2)  # Limit frequency axis to Nyquist frequency
    tick_interval = 0.025  # Set the desired interval in seconds
    label_interval = 0.1  # Interval at which labels are placed (every 5th tick if tick_interval is 0.5)

    ticks = np.arange(0, np.max(t), tick_interval)
# Create labels, leaving every 5th label and setting the rest to empty strings
    labels = [f"{tick:.1f}" if (n % 6 == 0) else '' for n, tick in enumerate(ticks)]

    plt.xticks(ticks, labels=labels)
    # Save the plot as a jpg file
    plt.savefig(os.path.join(export_directory, filename), format='jpg')
    plt.close()  # Close the plot to free memory

# Plot and save original audio spectrogram as a jpg file
plot_and_save_spectrogram(samples, audioPre.frame_rate, title='Original Audio Spectrogram', filename='original_audio_spectrogram.jpg')

# Plot and save noise-reduced audio spectrogram as a jpg file
plot_and_save_spectrogram(reduced_noise_samples, audioPre.frame_rate, title='Noise-Reduced Audio Spectrogram', filename='noise_reduced_audio_spectrogram.jpg')