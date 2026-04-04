import type { LmmResponse } from "@/types/rag"
import { Skeleton } from "@/components/ui/skeleton"
import { ConversationCardFooter } from "./ConversationCardFooter"

/** Props para o componente AnswerCard */
type AnswerCardProps = {
  lmmResponse: LmmResponse | undefined,
  className?: string,
  chatInProgress: boolean,
  isLastAnswer: boolean
}

/** Componente para exibir a resposta do RAG, ou um esqueleto de carregamento se a resposta ainda não estiver disponível */
function AnswerSkeleton() {
    return (<div className="space-y-3">
                    <Skeleton className="h-5 w-1/3" />
                    <div className="space-y-2">
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4 w-[90%]" />
                        <Skeleton className="h-4 w-[80%]" />
                        <Skeleton className="h-4 w-[60%]" />
                    </div>
                </div>)
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
                    <AnswerSkeleton />
                )
                : null}
            </div>

            {!props.chatInProgress && props.lmmResponse ? (
                <ConversationCardFooter message={props.lmmResponse.data} documents={props.lmmResponse.documents} timestamp={props.lmmResponse.timestamp} className="justify-start" /> 
            ) : null}
        </div>
        
    )
}