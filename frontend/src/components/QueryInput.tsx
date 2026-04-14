import {
  InputGroup,
  InputGroupAddon,
} from "@/components/ui/input-group"
import { Textarea } from "@/components/ui/textarea"
import type { Dispatch, SetStateAction, KeyboardEvent } from "react"
import type { RagQuestion } from "../types/rag"
import AudioRecorder from "./AudioRecorder"
import { useAppContext } from "@/contexts/AppContext"

/** Props para o componente QueryInput */
type QueryInputProps = {
  value: string,
  setValue: Dispatch<SetStateAction<string>>,
  setRagQuestions?: Dispatch<SetStateAction<RagQuestion[]>>,
  setRagQuestion?: Dispatch<SetStateAction<RagQuestion | undefined>>,
  className?: string,
  chatInProgress: boolean
}

/** Componente para entrada de perguntas, com suporte a envio via Enter e visualização do status do servidor RAG */
export default function QueryInput(props: QueryInputProps) {

  const appContext = useAppContext();

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      
      if (props.value.trim() === "") return

      props.setRagQuestions?.((prev) => [...prev, { id: crypto.randomUUID(), question: props.value, timestamp: new Date() }]);
      props.setRagQuestion?.({ id: crypto.randomUUID(), question: props.value, timestamp: new Date() });
      props.setValue("");
    }
  }

  function handleAudioSend(blob: Blob) {
      props.setRagQuestions?.((prev) => [...prev, { id: crypto.randomUUID(), question: blob, timestamp: new Date() }]);
      props.setRagQuestion?.({ id: crypto.randomUUID(), question: blob, timestamp: new Date() });
      props.setValue("");
  }

  return (
    <InputGroup className={props.className}>
      <Textarea
        value={props.value}
        onChange={(e) => props.setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Escreva sua pergunta"
        className="
          resize-none
          min-h-[40px]
          max-h-[120px]
          overflow-y-auto
          focus-visible:ring-0 
          focus-visible:ring-offset-0 
          focus-visible:outline-none
          focus-visible:border-input
        "
        disabled={appContext.ragServerConnected !== "connected" || props.chatInProgress}
      />
      <InputGroupAddon align="inline-end" className="absolute right-2 flex items-center gap-1">
        <AudioRecorder onSend={handleAudioSend} disabled={appContext.ragServerConnected !== "connected" || props.chatInProgress} />
      </InputGroupAddon>
    </InputGroup>
  )
}