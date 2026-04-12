import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { Upload, X } from "lucide-react"
import { useAppContext } from "@/contexts/AppContext"
import { toast } from "sonner"
import { ingestVectors } from "@/lib/api"

/** Componente de Upload de Arquivo */
export default function FileUpload() {
  const [file, setFile] = useState<File | null>(null);
  const {isLoading, setIsLoading } = useAppContext();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0]
    if (selected) {
      setFile(selected)
    }
  }

  const handleRemove = () => {
    setFile(null)
  }

  const handleUpload = async () => {
    if (!file) return

    try {
        setIsLoading(true);

        const ingestResult = await ingestVectors({ file });

        toast.info(`Ingestão concluída. Total de Chunks armazenados: ${ingestResult.chunks_stored}`);
    }
    catch(err: any) {
        toast.error(err.message || "Erro desconhecido durante o upload do arquivo para ingestão de vetores");
    }
    finally {
      setIsLoading(false)
      setFile(null);
    }    
  }

  return (
    <Card className="w-full max-w-md">
      <CardContent className="flex flex-col gap-4 p-4" aria-description="Upload de Arquivos">
        <label className="cursor-pointer flex flex-col gap-2">
          <span className="px-4 py-2 bg-gray-200 rounded text-center">
            {file?.name ? "Arquivo Selecionado" : "Selecionar um arquivo"}
          </span>

          <Input
            type="file"
            onChange={handleFileChange}
            disabled={isLoading}
            className="hidden"
          />
        </label>

        {file && (
          <div className="flex items-center justify-between rounded-md border p-2 text-sm">
            <span className="truncate">{file.name}</span>
            <button onClick={handleRemove} disabled={isLoading}>
              <X className="h-4 w-4" />
            </button>
          </div>
        )}

        <Button
          onClick={handleUpload}
          disabled={!file || isLoading}
          className="flex items-center gap-2"
        >
          <Upload className="h-4 w-4" />
          Enviar
        </Button>
      </CardContent>
    </Card>
  )
}