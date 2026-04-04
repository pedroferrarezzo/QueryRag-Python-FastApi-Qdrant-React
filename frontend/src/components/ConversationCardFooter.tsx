import { Clipboard } from "./Clipboard"
import { DocumentsModal } from "./DocumentsModal"
import type { Document } from "@/types/rag"

/** Props para o componente ConversationCardFooter */
type ConversationCardFooterProps = {
  message: string | Blob,
  timestamp: Date,
  className?: string
  documents?: Document[]
}

/** Componente para exibir o rodapé da conversa, com a opção de copiar a pergunta e mostrar o timestamp */
export function ConversationCardFooter(props: ConversationCardFooterProps) {
  return (
    <div className={`flex flex-row items-center mt-2 gap-2 ${props.className}`}>
        {typeof props.message === "string" && (
          <Clipboard value={props.message} />
        )}
        
        <DocumentsModal documents={props.documents} />
        <p className="text-sm text-muted-foreground">{props.timestamp.toLocaleString()}</p>
    </div> 
  )
}