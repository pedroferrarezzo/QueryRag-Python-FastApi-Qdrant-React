import Header from "@/components/Header";
import type { RagQuestion } from "@/types/rag";
import { useEffect, useState } from "react";
import QueryInput from "@/components/QueryInput";
import { type Document } from "@/types/rag";
import DocumentCard from "@/components/DocumentCard";
import { searchVectors } from "@/lib/api";
import { toast } from "sonner";
import SpinnerLoading from "@/components/SpinnerLoading";
import { DefaultTooltip } from "@/components/DefaultTooltip";
import { Info } from "lucide-react";

/**Página para Pesquisa de Vetores */
export default function SearchVectors() {
  const [question, setQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [ragQuestion, setRagQuestion] = useState<RagQuestion>();
  const [documents, setDocuments] = useState<Document[]>([]);

  useEffect(() => {
    if (ragQuestion) {
        const handleSearch = async () => {
          try {
              setIsLoading(true);

              const searchResult = await searchVectors({ ragQuestion });

              if (searchResult.length === 0) {
                  toast.info("Nenhum documento encontrado para a pergunta fornecida. Insira vetores antes de realizar a pesquisa!");
                  return;
              }

              setDocuments(searchResult);
          }
          catch(err: any) {
              toast.error(err.message || "Erro desconhecido durante a pesquisa de vetores");
          }
          finally {
            setIsLoading(false)
          } 
      }

      handleSearch();
    }
  }, [ragQuestion])
      
  return (
    <div className="flex flex-col items-center p-4 h-screen">
          <Header />
          
          <main className={`flex-grow flex flex-col ${documents.length > 0 ? 'justify-between' : 'justify-center'} w-full max-w-4xl overflow-hidden`}>
              <div className="mt-3 flex flex-row justify-center items-center gap-2">
                  <QueryInput value={question} setValue={setQuestion} chatInProgress={isLoading} setRagQuestion={setRagQuestion} className="shadow-lg"/>
                  {documents.length > 0 && (
                    <DefaultTooltip content="Utiliza um modelo de embeddings multimodal para recuperar documentos relevantes com base na distância de cosseno."> 
                        <Info className="w-6 h-6" />
                    </DefaultTooltip>
                  )}
              </div>

              <div className={`overflow-y-auto p-1 scrollbar-hide gap-2 flex flex-col ${documents.length > 0 ? 'flex-grow mt-4' : ''} ${isLoading ? 'flex-grow justify-center' : ''}`}>
                {isLoading 
                  ? <SpinnerLoading text="Pesquisa de vetores em andamento. Em breve você verá os resultados!" />
                  : documents.map((doc, index) => (
                  <DocumentCard key={index} doc={doc} />
                ))}
              </div>
          </main>
    </div>
  );
}