import { createContext, useContext, useMemo, useRef, useState } from 'react';
import type { ServerConnectionStatus } from "../types/server";
import { createWebSocket } from "../lib/websocket";
import { useEffect } from 'react';
import { toast } from 'sonner';

/**Tipo do Contexto da Aplicação */
type AppContextType = {
    ragServerConnected: ServerConnectionStatus;
    setRagServerConnected: React.Dispatch<React.SetStateAction<ServerConnectionStatus>>;
    isLoading: boolean;
    setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
    ws: React.RefObject<WebSocket | null>;
}

/**Contexto da Aplicação */
const AppContext = createContext<AppContextType | undefined>(undefined);

/**Provedor de Contexto da Aplicação */
export function AppContextProvider({ children }: { children: React.ReactNode }) {
  const [ragServerConnected, setRagServerConnected] = useState<ServerConnectionStatus>("disconnected");
  const [isLoading, setIsLoading] = useState(false);
  const ws = useRef<WebSocket | null>(null);

  // Memoiza os valores do contexto para evitar re-renderizações desnecessárias nos componentes consumidores
  const values = useMemo(() => ({
        ragServerConnected,
        setRagServerConnected,
        isLoading,
        setIsLoading,
        ws
    }), [ragServerConnected, isLoading]);

  useEffect(() => {
    ws.current = createWebSocket({ 
        setRagServerConnected, 
        onOpenCallback: () => {
            toast.info("Conexão estabelecida com o servidor de RAG");
        },
        onCloseCallback: (event) => {
            const { code, wasClean } = event;

            const codeMessages: Record<number, string> = {
                1000: "Conexão encerrada com o servidor de RAG",
                1001: "Servidor de RAG indisponível ou navegação interrompida",
                1002: "Erro de protocolo durante conexão com o servidor de RAG",
                1003: "Tipo de dado não suportado pelo servidor de RAG",
                1006: "Conexão interrompida com o servidor de RAG",
                1007: "Dados inválidos recebidos do servidor de RAG",
                1008: "Violação de política do servidor de RAG",
                1009: "Mensagem muito grande recebida do servidor de RAG",
                1011: "Erro interno do servidor de RAG",
            };

            if (codeMessages[code]) {
                toast.info(codeMessages[code]);
                return;
            }

            if (!wasClean) {
                toast.info(`Conexão encerrada inesperadamente com o servidor de RAG: (${code})`);
                return;
            }

            toast.info("Conexão encerrada inesperadamente com o servidor de RAG");
        },
        errorCallback: (err) => {
            toast.error(`Erro inesperado durante estabelecimento da conexão com o servidor de RAG: ${err}`);
        }
    });

    return () => {
        ws.current?.close();
        ws.current = null;
    }

  }, [])

  return (
    <AppContext.Provider value={values}>
      {children}
    </AppContext.Provider>
  );
}

/**Hook para acessar o contexto da aplicação */
export function useAppContext(): AppContextType {
    const context = useContext(AppContext);
    if (context === undefined) {
        throw new Error('useAppContext deve ser usado dentro de um AppContextProvider');
    }

    return context;
}