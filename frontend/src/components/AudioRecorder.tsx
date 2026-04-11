import { useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Mic, Square, Send } from "lucide-react";
import { toast } from "sonner";

/** Props para o componente AudioRecorder */
type AudioRecorderProps = {
  onSend?: (blob: Blob) => void;
  disabled: boolean;
};

/** Componente para gravar áudio usando a API MediaRecorder e enviar o arquivo resultante */
export default function AudioRecorder(props: AudioRecorderProps) {
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);

  async function startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: "audio/wav" });
        setAudioBlob(blob);
        setAudioUrl(URL.createObjectURL(blob));
      };

      mediaRecorder.start();
      setIsRecording(true);
    }
    catch (error: any) {
      switch (error?.name) {
        case "NotAllowedError":
          toast.error("Permissão de microfone negada");
          break;

        case "NotFoundError":
          toast.error("Nenhum dispositivo de áudio encontrado");
          break;

        case "NotReadableError":
          toast.error("Microfone em uso ou erro de hardware");
          break;

        case "OverconstrainedError":
          toast.error("Configuração de áudio inválida");
          break;

        default:
          toast.error(`Erro desconhecido: ${error?.message || error?.name || error}`);
      }
    }
  }

  function stopRecording() {
    mediaRecorderRef.current?.stop();
    setIsRecording(false);

    mediaRecorderRef.current?.stream
      .getTracks()
      .forEach((track) => track.stop());
  }

  function handleSend() {
    if (!audioBlob) return;
    
    setAudioBlob(null);
    setAudioUrl(null);

    props.onSend?.(audioBlob);
  }

  useEffect(() => {
    return () => {
      if (audioUrl) URL.revokeObjectURL(audioUrl);
    };
  }, [audioUrl]);

  return (
    <div className="flex items-center">
      <div className="flex gap-2">
        {!isRecording ? (
          <Button onClick={startRecording} disabled={props.disabled}>
            <Mic className="w-4 h-4 mr-2" />
            Gravar
          </Button>
        ) : (
          <Button variant="destructive" onClick={stopRecording} disabled={props.disabled}>
            <Square className="w-4 h-4 mr-2" />
            Parar
          </Button>
        )}

        {audioBlob && (
          <Button onClick={handleSend} disabled={props.disabled}>
            <Send className="w-4 h-4 mr-2" />
            Enviar
          </Button>
        )}
      </div>
    </div>
  );
}