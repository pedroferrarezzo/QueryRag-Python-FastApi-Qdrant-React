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
import { FileText } from "lucide-react"

import type { Document } from "@/types/rag"

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
        <DialogHeader>
          <DialogTitle>Documentos Recuperados</DialogTitle>
        </DialogHeader>

        <ScrollArea className="max-h-[400px] pr-4">
          <div className="space-y-4">
            {props.documents.map((doc, index) => (
              <div
                key={index}
                className="border rounded-lg p-3 text-sm space-y-2"
              >
                <div className="flex justify-between">
                  <span className="font-medium">
                    {doc.metadata.source}
                  </span>
                  <span className="text-muted-foreground">
                    score: {doc.score.toFixed(4)}
                  </span>
                </div>

                {doc.rerank_score != null && (
                  <div className="text-muted-foreground text-xs">
                    rerank: {doc.rerank_score.toFixed(4)}
                  </div>
                )}

                {doc.metadata.type && (
                  <div className="text-xs">
                    tipo: {doc.metadata.type}
                  </div>
                )}

                {doc.metadata.chunk && (
                  <div className="text-xs text-muted-foreground">
                    chunk: {doc.metadata.chunk}
                  </div>
                )}
              </div>
            ))}
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  )
}