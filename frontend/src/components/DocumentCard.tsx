import { type Document } from "../types/rag";

/** Props para o componente Document */
type DocumentProps = {
    key?: number,
    doc: Document
}

/**Componente de Documento */
export default function DocumentCard({key, doc}: DocumentProps) {
    return (
        <div key={key} className="border rounded-lg p-3 text-sm space-y-2">
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
    )
}