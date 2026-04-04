import { Card, CardContent } from "@/components/ui/card"
import type { RagQuestion } from "@/types/rag"
import { ConversationCardFooter } from "./ConversationCardFooter"

/** Props para o componente QuestionCard */
type QuestionCardProps = {
  ragQuestion: RagQuestion,
  className?: string
}

/** Componente para exibir a pergunta do RAG */
export default function QuestionCard(props: QuestionCardProps) {
  return (
    <div className={props.className}>
      <Card>
        <CardContent className="p-2">
          <p className="text-sm text-muted-foreground mb-2">Você</p>
          {typeof props.ragQuestion.question === "string" ? (
            <p className="text-base leading-relaxed break-words">{props.ragQuestion.question}</p>
          ) : (
            <audio controls src={URL.createObjectURL(props.ragQuestion.question)} className="w-full" />
          )}
        </CardContent>
      </Card>
      <ConversationCardFooter message={props.ragQuestion.question} timestamp={props.ragQuestion.timestamp} className="justify-end" /> 
    </div>
  )
}