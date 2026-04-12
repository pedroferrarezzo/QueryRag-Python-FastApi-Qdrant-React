import FileUpload from "@/components/FileUpload";
import Header from "@/components/Header";
import { useAppContext } from "@/contexts/AppContext";
import { Loader2 } from "lucide-react";

/** Página para Ingestão de Vetores */
export default function IngestVectors() {
  const { isLoading } = useAppContext();

  return (
    <div className="flex flex-col items-center p-4 h-screen">
      <Header />

      <main className="flex items-center justify-center w-full h-full">
        {
          isLoading ? (
            <div className="flex flex-col items-center justify-center">
              <Loader2 className="h-10 w-10 animate-spin text-muted-foreground" />

              <p className="mt-4 text-sm text-muted-foreground text-center max-w-sm">
                O arquivo está em processamento. Aguarde sem sair desta tela.
              </p>
            </div>
          )
          : (
            <FileUpload />
          )
        } 
      </main>
    </div>
  );
}