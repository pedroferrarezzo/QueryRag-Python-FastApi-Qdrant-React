import io
from pydub import AudioSegment

def convert_webm_to_wav(webm_bytes: bytes) -> bytes:
    """Converte um arquivo de áudio em formato WebM para WAV."""
    audio_stream = io.BytesIO(webm_bytes)
    
    audio = AudioSegment.from_file(audio_stream, format="webm")
    
    output_stream = io.BytesIO()
    audio.export(output_stream, format="wav")
    
    return output_stream.getvalue()