import type { ServerConnectionStatus } from "@/types/server";

/** Props para o componente RagServerStatus */
type RagServerStatusProps = {
    ragServerConnected: ServerConnectionStatus;
}

/** Componente para exibir o status de conexão com o servidor RAG */
export default function RagServerStatus(props : RagServerStatusProps){
    return (
        <div className="inline-flex items-center gap-2 text-sm font-medium">
            <span
                className={`h-2.5 w-2.5 rounded-full transition-colors ${
                props.ragServerConnected === "connected" ? "bg-green-500" : "bg-gray-400"
                }`}
            />
            <span
                className={`transition-colors ${props.ragServerConnected === "connected" ? "text-green-500" : "text-gray-400"}`}
            >
                {props.ragServerConnected === "connected" 
                    ? "RAG Server Connected" 
                    : props.ragServerConnected === "connecting" 
                    ? "RAG Server Connecting..." 
                    : "RAG Server Disconnected"
                }
            </span>
        </div>
  )
}