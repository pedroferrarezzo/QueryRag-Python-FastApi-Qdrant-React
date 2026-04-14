import FileUpload from "@/components/FileUpload";
import Header from "@/components/Header";
import SpinnerLoading from "@/components/SpinnerLoading";
import { useState } from "react";

/** Página para Ingestão de Vetores */
export default function IngestVectors() {
  const [isLoading, setIsLoading] = useState(false);

  return (
    <div className="flex flex-col items-center p-4 h-screen">
      <Header />

      <main className="flex items-center justify-center w-full h-full">
        {
          isLoading ? <SpinnerLoading text="Ingestão em andamento, isso pode levar alguns minutos dependendo do tamanho dos arquivos e da quantidade de dados a serem processados. Não saia da página!" />
          : (
            <FileUpload isLoading={isLoading} setIsLoading={setIsLoading} />
          )
        } 
      </main>
    </div>
  );
}