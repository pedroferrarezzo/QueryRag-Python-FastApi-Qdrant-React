import { createContext, useContext, useMemo, useState } from 'react';
import type { ServerConnectionStatus } from "../types/server";

/**Tipo do Contexto da Aplicação */
type AppContextType = {
    ragServerConnected: ServerConnectionStatus;
    setRagServerConnected: React.Dispatch<React.SetStateAction<ServerConnectionStatus>>;
}

/**Contexto da Aplicação */
const AppContext = createContext<AppContextType | undefined>(undefined);

/**Provedor de Contexto da Aplicação */
export function AppContextProvider({ children }: { children: React.ReactNode }) {
  const [ragServerConnected, setRagServerConnected] = useState<ServerConnectionStatus>("disconnected");

  // Memoiza os valores do contexto para evitar re-renderizações desnecessárias nos componentes consumidores
  const values = useMemo(() => ({
        ragServerConnected,
        setRagServerConnected
    }), [ragServerConnected]);

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