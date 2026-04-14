import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { ScrollArea } from "@/components/ui/scroll-area"
import { FileText, Info } from "lucide-react"

import type { Document } from "@/types/rag"
import { DefaultTooltip } from "./DefaultTooltip"
import DocumentCard from "./DocumentCard"

/** Props para o componente DocumentsModal */
type DocumentsModalProps = {
  documents?: Document[]
}

/** Componente para exibir os documentos recuperados em um modal */
export function DocumentsModal(props: DocumentsModalProps) {
  const [open, setOpen] = useState(false)

  if (!props.documents || props.documents.length === 0) return null

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="icon">
          <FileText className="h-4 w-4" />
        </Button>
      </DialogTrigger>

      <DialogContent className="max-w-2xl">
        <DialogHeader className="flex flex-row">
          <DialogTitle>Documentos Recuperados</DialogTitle>
          <DefaultTooltip content="Utiliza um modelo de embeddings multimodal para recuperar documentos relevantes com base na distância de cosseno."> 
              <Info className="w-4 h-4" />
          </DefaultTooltip>
        </DialogHeader>

        <ScrollArea className="max-h-[400px] pr-4">
          <div className="space-y-4">
            {props.documents.map((doc, index) => (
              <DocumentCard key={index} doc={doc} />
            ))}
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  )
}