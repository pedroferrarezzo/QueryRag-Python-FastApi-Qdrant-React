import { createContext, useContext, useMemo, useState } from 'react';
import type { ServerConnectionStatus } from "../types/server";

/**Tipo do Contexto da Aplicação */
type AppContextType = {
    ragServerConnected: ServerConnectionStatus;
    setRagServerConnected: React.Dispatch<React.SetStateAction<ServerConnectionStatus>>;
    isLoading: boolean;
    setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

/**Contexto da Aplicação */
const AppContext = createContext<AppContextType | undefined>(undefined);

/**Provedor de Contexto da Aplicação */
export function AppContextProvider({ children }: { children: React.ReactNode }) {
  const [ragServerConnected, setRagServerConnected] = useState<ServerConnectionStatus>("disconnected");
  const [isLoading, setIsLoading] = useState(false);

  // Memoiza os valores do contexto para evitar re-renderizações desnecessárias nos componentes consumidores
  const values = useMemo(() => ({
        ragServerConnected,
        setRagServerConnected,
        isLoading,
        setIsLoading
    }), [ragServerConnected, isLoading]);

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