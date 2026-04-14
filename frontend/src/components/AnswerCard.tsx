import type { LmmResponse } from "@/types/rag"
import { ConversationCardFooter } from "./ConversationCardFooter"
import ResponseSkeleton from "./ResponseSkeleton"

/** Props para o componente AnswerCard */
type AnswerCardProps = {
  lmmResponse: LmmResponse | undefined,
  className?: string,
  chatInProgress: boolean,
  isLastAnswer: boolean
}

/** Componente para exibir a resposta do RAG, ou um esqueleto de carregamento se a resposta ainda não estiver disponível */
export default function AnswerCard(props: AnswerCardProps) {
    return (
        <div>
            <div className={props.className}>
                {props.lmmResponse ? (
                    <p className="break-words">{props.lmmResponse.data}</p>
                ) : props.chatInProgress && !props.lmmResponse && props.isLastAnswer
                ?  (
                    <ResponseSkeleton />
                )
                : null}
            </div>

            {!props.chatInProgress && props.lmmResponse ? (
                <ConversationCardFooter message={props.lmmResponse.data} documents={props.lmmResponse.documents} timestamp={props.lmmResponse.timestamp} className="justify-start" /> 
            ) : null}
        </div>
        
    )
}