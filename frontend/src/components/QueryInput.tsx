import {
  InputGroup,
  InputGroupAddon,
} from "@/components/ui/input-group"
import { Textarea } from "@/components/ui/textarea"
import { SearchIcon } from "lucide-react"
import type { Dispatch, SetStateAction, KeyboardEvent } from "react"
import type { RagConversation } from "../types/rag-conversation"

type Props = {
  value: string,
  setSearchIsTriggered: Dispatch<SetStateAction<boolean>>
  setValue: Dispatch<SetStateAction<string>>,
  setRagConversations: Dispatch<SetStateAction<RagConversation[]>>,
  className?: string
}

export default function QueryInput({ value, setSearchIsTriggered, setValue, setRagConversations, className }: Props) {

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      
      if (value.trim() === "") return

      setSearchIsTriggered(true);
      setRagConversations((prev) => [...prev, { id: crypto.randomUUID(), question: value, answer: "" }]);
      setValue("");
    }
  }

  return (
    <InputGroup className={className}>
      <Textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
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
      />
      <InputGroupAddon align="inline-end" className="absolute right-2 bottom-2">
        <SearchIcon />
      </InputGroupAddon>
    </InputGroup>
  )
}